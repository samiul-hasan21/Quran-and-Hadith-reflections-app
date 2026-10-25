"""Assemble data/kb.json = verified items + theme definitions + item lists + attributions."""
import json, sys
import os
HERE_ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE_)
from build_items import build
from themes import THEMES, CATEGORIES
from userfeelings import train_anchors

items, theme_items = build()
themes = {}
TRAIN = train_anchors()
assert set(TRAIN) <= set(THEMES), set(TRAIN) - set(THEMES)
for tid, spec in THEMES.items():
    anchors = list(dict.fromkeys(spec["anchors"] + TRAIN.get(tid, [])))   # own phrases + the owner's training sentences
    themes[tid] = dict(title=spec["title"], intro=spec["intro"], anchors=anchors,
                       keywords=[list(k) if isinstance(k, tuple) else k for k in spec["keywords"]],
                       items=theme_items[tid])
assert set(themes) == set(theme_items), set(themes) ^ set(theme_items)

kb = {
  "meta": {
    "quran_arabic": "Tanzil Quran text (Uthmani), tanzil.net",
    "quran_english": "Saheeh International translation, via QuranEnc.com (Noor International Center)",
    "hadith": "Sahih al-Bukhari (tr. M. Muhsin Khan) and Sahih Muslim (tr. Abdul Hamid Siddiqui), text via sunnah.com",
    "word_vectors": "GloVe 6B 100d (Pennington, Socher & Manning, Stanford), Public Domain Dedication and License, pruned to 50k words",
    "version": 1,
  },
  "themes": themes,
  "categories": [{"id": f"cat{n}", "title": name, "themes": ts} for n, (name, ts) in enumerate(CATEGORIES)],
  "other_themes": [t for t in themes if t not in {x for _, ts in CATEGORIES for x in ts}],
  "items": items,
}
OUT = os.path.join(HERE_, "..", "data")
os.makedirs(OUT, exist_ok=True)
json.dump(kb, open(os.path.join(OUT, "kb.json"), "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
print("themes:", len(themes), "| items:", len(items), "| size KB:", round(os.path.getsize(os.path.join(OUT, "kb.json"))/1024))
