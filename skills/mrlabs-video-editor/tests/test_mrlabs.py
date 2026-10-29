"""Behavioral checks of language, captions, source ranges and B-roll boundaries."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from mrlabs_core import (mrlabs_language, mrlabs_transcribe, mrlabs_caption_groups,
                         mrlabs_validate_words, mrlabs_export_srt, mrlabs_config)
from mrlabs_broll import mrlabs_broll_plan, mrlabs_validate_broll
from mrlabs_visual import (MRLABS_EFFECTS, mrlabs_theme, mrlabs_entrance, mrlabs_is_portrait,
                           mrlabs_css, mrlabs_caption_top, mrlabs_format_title_html,
                           mrlabs_normalize_effects, mrlabs_effect_specimen_html)

SPEC = importlib.util.spec_from_file_location("mrlabs_assemble", SCRIPTS / "mrlabs-assemble.py")
ASSEMBLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSEMBLE)


class LanguageBehavior(unittest.TestCase):
    def test_default_is_indonesian_and_en_is_not_translation(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(mrlabs_config(folder)["language"], "id")
        for language in ("id", "en", "auto", "mixed"):
            result = mrlabs_language(language)
            self.assertEqual(result["task"], "transcribe")
            self.assertEqual(result["language"], language if language in ("id", "en") else None)
        self.assertTrue(mrlabs_language("mixed")["multilingual"])

    def test_english_only_model_cannot_silently_accept_indonesian(self):
        for language in ("id", "mixed", "auto"):
            with self.assertRaises(ValueError):
                mrlabs_language(language, "small.en")
        self.assertEqual(mrlabs_language("en", "small.en")["model"], "small.en")

    def test_asr_receives_language_and_preserves_words(self):
        for language, text in (("id", "Belajar"), ("en", "Learning")):
            captured = {}
            class FakeWhisper:
                def __init__(self, model, **kwargs):
                    captured["model"] = model
                def transcribe(self, path, **kwargs):
                    captured.update(kwargs)
                    word = SimpleNamespace(word=text, start=.1, end=.5, probability=.9)
                    return iter([SimpleNamespace(start=.1,end=.5,text=text,words=[word])]), SimpleNamespace(language=language)
            with patch.dict(sys.modules, {"faster_whisper": SimpleNamespace(WhisperModel=FakeWhisper)}):
                result = mrlabs_transcribe("example.wav", language=language)
            self.assertEqual(captured["language"], language)
            self.assertEqual(captured["task"], "transcribe")
            self.assertEqual(result["words"][0]["text"], text)


class CaptionBehavior(unittest.TestCase):
    def test_grouping_keeps_exact_words_and_breaks_on_pause(self):
        words = [{"text":text,"start":start,"end":end} for text,start,end in
                 [("Belajar",0,.3),("AI",.3,.6),("step",1.2,1.5),("by",1.5,1.7),("step.",1.7,2)]]
        groups = mrlabs_caption_groups(words)
        self.assertEqual(len(groups), 2)
        self.assertEqual([word for group in groups for word in group["words"]], words)
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "captions.srt"
            mrlabs_export_srt(target, words)
            self.assertIn("00:00:01,200 --> 00:00:02,000", target.read_text(encoding="utf-8"))

    def test_rejects_reversed_or_outside_timestamps(self):
        for word in ({"text":"x","start":1,"end":.5}, {"text":"x","start":0,"end":8}):
            with self.assertRaises(ValueError):
                mrlabs_validate_words([word], 3)


class BrollBehavior(unittest.TestCase):
    def test_id_and_en_get_real_anchors_without_inventing_assets(self):
        for text in ("Atur workflow agar laporan otomatis.", "Show the coding workflow."):
            result = mrlabs_broll_plan({"segments":[{"text":text,"start":1,"end":5}]})
            cue = result["cues"][0]
            self.assertEqual(cue["anchor"], text)
            self.assertNotIn("file", cue)
            self.assertEqual(cue["status"], "proposed")
        self.assertEqual(mrlabs_broll_plan({"segments":[{"text":"Sampai jumpa.","start":0,"end":2}]})["cues"], [])

    def test_rights_and_timeline_required_and_valid_image_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / "demo.png"
            image.write_bytes(b"fixture image; image decoder covered in integration")
            cue = {"file":"demo.png","start":0,"end":2,"anchor":"Demo","source_page":"local-user-supplied:demo",
                   "license":"user-owned","rights_verified":True,"status":"approved","role":"illustration"}
            self.assertEqual(mrlabs_validate_broll([cue], 3, folder)[0]["kind"], "image")
            for changed in ({"rights_verified":False},{"status":"proposed"},{"end":5},{"source_page":""}):
                with self.assertRaises(ValueError):
                    mrlabs_validate_broll([{**cue,**changed}],3,folder)
            with self.assertRaises(ValueError):
                mrlabs_validate_broll([cue,{**cue,"start":1}],3,folder)


class ThemeMotion(unittest.TestCase):
    def test_short_cues_leave_time_to_read_in_every_theme(self):
        for theme_id in ('signal-clean', 'kinetic-punch', 'editorial-noir', 'warm-story', 'tech-grid',
                         'peach-doodle', 'bubble-pop', 'groovy-mint', 'sunny-picnic', 'orbit-candy',
                         'verge-glass', 'monocle-brief', 'kinfolk-linen', 'obsidian-studio', 'founder-slate'):
            theme = mrlabs_theme(theme_id)
            for role in ('caption', 'title', 'broll'):
                for duration in (.02, .2, .7, 3):
                    initial, final = mrlabs_entrance(theme, role, duration)
                    self.assertLessEqual(final['duration'], duration*.35)
                    self.assertEqual(final['opacity'], 1)
                    self.assertFalse(final['immediateRender'])

    def test_poster_tilt_survives_but_full_frame_never_shrinks_or_tilts(self):
        theme = mrlabs_theme('kinetic-punch')
        self.assertEqual(mrlabs_entrance(theme, 'title', 2)[1]['rotation'], -2)
        self.assertEqual(mrlabs_entrance(theme, 'caption', 2)[1]['rotation'], -2)
        self.assertEqual(mrlabs_entrance(theme, 'broll', 2)[1]['rotation'], 3)
        for theme_id in ('kinetic-punch', 'warm-story', 'tech-grid', 'verge-glass', 'monocle-brief', 'obsidian-studio'):
            initial, final = mrlabs_entrance(mrlabs_theme(theme_id), 'broll', .7, full=True)
            for state in (initial, final):
                self.assertEqual(state.get('rotation', 0), 0)
                self.assertEqual(state.get('scale', 1), 1)
                self.assertEqual(state.get('x', 0), 0)
                self.assertEqual(state.get('y', 0), 0)

    def test_pro_themes_use_white_or_black_bg_and_skip_bg_when_video_is_portrait(self):
        pro_ids = ('verge-glass', 'monocle-brief', 'kinfolk-linen', 'obsidian-studio', 'founder-slate')
        for theme_id in pro_ids:
            theme = mrlabs_theme(theme_id)
            self.assertIn(theme['background'], ('#FFFFFF', '#0A0A0C', '#0A0A0A'))
            self.assertEqual(theme.get('caption_position'), 'chest-float')
            self.assertTrue(theme.get('talking_head'))
            self.assertIn('--canvas-background:transparent', mrlabs_css(theme, portrait=True))
            self.assertIn(f"--canvas-background:{theme['background']}", mrlabs_css(theme, portrait=False))
        html = mrlabs_format_title_html("claude editing my videos\n14,000", mrlabs_theme('obsidian-studio'))
        self.assertIn('class="title-kicker"', html)
        self.assertIn('class="title-hero"', html)
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            (project / "sources.json").write_text(json.dumps({"c1": {"width": 1080, "height": 1920}}), encoding="utf-8")
            self.assertTrue(mrlabs_is_portrait(project))
            (project / "sources.json").write_text(json.dumps({"c1": {"width": 1920, "height": 1080}}), encoding="utf-8")
            self.assertFalse(mrlabs_is_portrait(project))
            (project / "head-samples.json").write_text(json.dumps([{"segment": "s1", "time": 0.5, "bounds": [300, 480, 780, 1800]}]), encoding="utf-8")
            self.assertEqual(mrlabs_caption_top(project), 330)

    def test_five_viral_effects_and_caption_positions(self):
        expected = {'orbit', 'ui-world', 'digital-zoom', 'headline-wall', 'pull-back-reveal'}
        self.assertEqual(set(MRLABS_EFFECTS.keys()), expected)
        normalized = mrlabs_normalize_effects({"effects": ["orbit", {"type": "headline-wall", "start": 0.5, "end": 3.0}]}, duration=5.0)
        self.assertEqual([fx["type"] for fx in normalized], ["orbit", "headline-wall"])
        self.assertEqual(normalized[0]["end"], 5.0)
        self.assertEqual(normalized[1]["start"], 0.5)
        specimen_html = mrlabs_effect_specimen_html()
        for marker in ("fx-orbit-card", "fx-ui-world", "fx-zoom-hud", "fx-headline-card", "fx-pullback"):
            self.assertIn(marker, specimen_html)
        with self.assertRaises(ValueError):
            mrlabs_normalize_effects({"effects": ["unknown-effect"]}, duration=5.0)


class SourceRanges(unittest.TestCase):
    def test_edl_range_and_duplicate_id_rejected(self):
        sources = {"c1":{"duration":4}}
        valid = {"id":"hook","clip":"c1","in":0,"out":2}
        ASSEMBLE.mrlabs_validate_edl([valid],sources)
        for edl in ([{**valid,"out":5}], [valid,valid], []):
            with self.assertRaises(ValueError):
                ASSEMBLE.mrlabs_validate_edl(edl,sources)


if __name__ == "__main__":
    unittest.main()
