"""Optional real-media smoke test. Writes only synthetic fixtures to ignored output/."""
import argparse
from pathlib import Path
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from mrlabs_core import (MRLABS_DEFAULTS, mrlabs_run, mrlabs_tool, mrlabs_write,
                         mrlabs_hash, mrlabs_read, mrlabs_transcribe)
from mrlabs_visual import mrlabs_build


def mrlabs_script(name, *args):
    return mrlabs_run([sys.executable, SKILL / "scripts" / f"mrlabs-{name}.py", *args])


def mrlabs_main():
    from PIL import Image, ImageDraw
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--asr", action="store_true", help="Requires output/verification/indonesian.wav and english.wav")
    args = parser.parse_args()
    work = REPO / "output/verification"
    work.mkdir(parents=True, exist_ok=True)
    source = work / "synthetic-source.mp4"
    mrlabs_run([mrlabs_tool("ffmpeg"), "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000", "-t", "4", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-c:a", "aac", source])
    original_hash = mrlabs_hash(source)
    project = work / "synthetic-project"
    if not (project / "sources.json").exists():
        print(mrlabs_script("ingest", project, source, "--skip-transcription"), flush=True)
    mrlabs_write(project / "edl.json", [{"id":"hook","clip":"c1","in":0,"out":1.5},
                                      {"id":"demo","clip":"c1","in":2,"out":3.5}])
    print(mrlabs_script("assemble", project), flush=True)
    words = [{"text":text,"start":start,"end":end} for text,start,end in
             [("Belajar",.1,.45),("AI",.45,.7),("step",1.6,1.9),("by",1.9,2.1),("step.",2.1,2.55)]]
    mrlabs_write(project / "words.json", words)
    mrlabs_write(project / "transcript.json", {"segments":[{"start":.1,"end":2.55,"text":"Belajar AI step by step."}],"words":words})
    print(mrlabs_script("broll", project), flush=True)
    image = Image.new("RGB", (810,456), "#192c3a")
    draw = ImageDraw.Draw(image)
    draw.rectangle((70,100,240,310), fill="#7ef4c2")
    draw.rectangle((330,100,500,310), fill="#8ac7ff")
    draw.rectangle((590,100,740,310), fill="#ffd34d")
    demo = work / "synthetic-diagram.png"
    image.save(demo)
    mrlabs_write(project / "broll.json", {"cues":[{"id":"test-image","file":str(demo),"start":.7,"end":1.4,
                 "anchor":"Belajar AI", "source_page":"local-synthetic-test:diagram","license":"test-fixture",
                 "rights_verified":True,"status":"approved","role":"illustration","mode":"pip"},
                {"id":"test-video","file":str(source),"start":1.6,"end":2.4,"source_in":0,
                 "anchor":"step by step", "source_page":"local-synthetic-test:ffmpeg-testsrc2","license":"test-fixture",
                 "rights_verified":True,"status":"approved","role":"illustration","mode":"full"}]})
    mrlabs_write(project / "visual.json", {"titles":[{"text":"Contoh sintetis / Synthetic demo","start":.15,"end":1.4}],
                                          "sfx":[{"id":"click_001","time":.7,"gain":.1}]})
    for theme in mrlabs_read(SKILL / "assets/themes.json")["themes"]:
        config = {**MRLABS_DEFAULTS,"theme":theme["id"]}
        mrlabs_write(project / "project.json", config)
        mrlabs_build(project)
        target = work / f"{theme['id']}.html"
        target.write_text((project / "index.html").read_text(encoding="utf-8"),encoding="utf-8")
        print(f"BUILT {theme['id']}", flush=True)
    mrlabs_write(project / "project.json", MRLABS_DEFAULTS)
    mrlabs_build(project)
    result = {"synthetic_source_unchanged":mrlabs_hash(source)==original_hash,"theme_count":5,
              "broll_modes_tested":["image-pip","video-full"],"assembly_segments":2}
    if args.asr:
        result["asr"] = {}
        for language, name in (("id","indonesian.wav"),("en","english.wav")):
            transcript = mrlabs_transcribe(work/name,language=language,model="small",keywords=["MR Labs","AI"])
            if not transcript["words"] or transcript["detected_language"] != language:
                raise AssertionError(f"ASR failed: {language}")
            mrlabs_write(work/f"asr-{language}.json",transcript)
            result["asr"][language] = {"model":"small","words":len(transcript["words"]),"language":transcript["detected_language"]}
            print(f"ASR {language}: {len(transcript['words'])} words",flush=True)
    if args.render:
        output = project / "renders/smoke.mp4"
        version = 2
        while output.exists():
            output = project / f"renders/smoke-v{version}.mp4"
            version += 1
        print(mrlabs_script("render",project,output,"--quality","draft"),flush=True)
        print(mrlabs_script("check-cuts",project,output),flush=True)
        result["render"] = mrlabs_read(project / "work/final-qa/report.json")
    mrlabs_write(work/"smoke-report.json",result)
    print(result)


if __name__ == "__main__":
    mrlabs_main()
