# Contextual B-roll

The goal is to make a spoken idea easier to understand, without changing what the speaker says or implying proof that does not exist.

## Editorial choices

1. Read a complete sentence and its preceding/following context. Identify the thing being explained, the action, and what a viewer needs to see. A mention of AI does not automatically justify a robot or typing hands.
2. Prefer real demonstrations for a named feature: screenshot, the user's screen recording, relevant code or a diagram based on supplied information. For a general concept, find illustrative internet B-roll with clear reuse terms. Use the available web search/browsing tools, not an invented provider integration.
3. `mrlabs-broll.py` proposes anchors from ID/EN keywords. It does not understand the full story or retrieve footage. Review/rewrite its query, omit weak suggestions, and insert cues manually for important concepts the keywords missed.
4. Search queries should name a concrete visible action, preferably in both Indonesian and English. Example: "mengatur trigger spreadsheet automation" / "spreadsheet automation trigger screen recording". Verify the actual page and asset, not a search-result snippet.
5. For open footage look for authoritative asset pages with stated reuse terms, e.g. Wikimedia Commons with each file's license or a stock site's actual license. Do not assume all assets on a site have the same terms. Avoid unrelated logos, unsupported graphs, invented dashboards and generated "evidence".
6. Download to the project's `assets/broll/`, record source URL, creator, license URL or permission evidence, retrieval date, local checksum and any required credit. Preview the actual media and confirm relevance. An agent marks `rights_verified: true` only after this review.
7. Bind the cue to the assembled transcript's clock. Keep the original narration; mute B-roll audio unless explicitly requested. Return to the speaker at a meaningful point. Duration follows the sentence and visible action, not an arbitrary quota.

## Approved ledger consumed by the builder

`broll-proposals.json` is separate from `broll.json`. An empty approved cue list is valid. A populated cue has:

```json
{
  "cues": [{
    "id": "broll-01",
    "start": 3.2,
    "end": 6.4,
    "anchor": "Atur trigger agar laporan diperbarui otomatis.",
    "file": "assets/broll/trigger-demo.mp4",
    "source_in": 1.0,
    "source_page": "local-user-supplied: trigger-demo.mp4",
    "license": "user-owned",
    "license_url": "local-user-permission",
    "creator": "User",
    "retrieved_at": "2026-10-28",
    "credit": "Demo milik pengguna",
    "rights_verified": true,
    "status": "approved",
    "role": "illustration",
    "mode": "pip"
  }]
}
```

Use `mode: full` for full-frame B-roll; `pip` for a bounded card. `role: evidence` requires genuine footage/data supporting that exact claim. Stock footage remains `illustration`. The v1 builder rejects unreviewed assets, missing source/rights fields, overlaps, invalid times and video durations shorter than their cue. It checks declared metadata, not legal truth or semantic relevance; those remain editorial responsibilities. Still images are supported. File paths may be absolute or project-relative.
