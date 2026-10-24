"""Reproduce the matcher evaluation:  python tests/evaluate.py
DEV  = used to tune settings.   TEST = written before the matcher existed, never tuned on."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, HERE)
from matcher import Matcher
from engine import THRESHOLD
from evalsets import DEV, TEST

D = os.path.join(HERE, "..", "data")
themes = json.load(open(os.path.join(D, "kb.json"), encoding="utf8"))["themes"]
VEC, VOC = os.path.join(D, "glove50k.npz"), os.path.join(D, "glove50k_vocab.json")

def run(m, data, thr):
    on = [(q, a) for q, a in data if a != ["none"]]; off = [(q, a) for q, a in data if a == ["none"]]
    t1 = t3 = 0
    for q, acc in on:
        r = m.rank(q); top, s = r[0]
        t1 += (s["score"] >= thr and top in acc); t3 += any(t in acc for t, _ in r[:3])
    rej = sum(m.rank(q)[0][1]["score"] < thr for q, _ in off)
    return t1 / len(on), t3 / len(on), rej / len(off), len(on), len(off)

cfgs = [("Hybrid (meaning + keywords)", dict(emb_w=1.0, kw_w=0.3, remove_pc=1, top_pair=2), THRESHOLD),
        ("Keywords only",              dict(emb_w=0.0, kw_w=0.3, remove_pc=0, top_pair=1), None),
        ("Word-vector meaning only",   dict(emb_w=1.0, kw_w=0.0, remove_pc=1, top_pair=2), None)]
print(f"{'Setup':30}{'thr':>6} | {'DEV top1':>8}{'top3':>6} | {'TEST top1':>9}{'top3':>6}{'offRej':>8}")
for name, cfg, thr in cfgs:
    m = Matcher(VEC, VOC, themes, **cfg)
    if thr is None:                       # baselines: highest off-topic DEV score + small margin
        thr = max(m.rank(q)[0][1]["score"] for q, a in DEV if a == ["none"]) + 0.02
    d, t = run(m, DEV, thr), run(m, TEST, thr)
    print(f"{name:30}{thr:6.2f} | {d[0]:8.2f}{d[1]:6.2f} | {t[0]:9.2f}{t[1]:6.2f}{t[2]:8.2f}")
print(f"\nTEST: {t[3]} on-topic + {t[4]} off-topic queries. top1 counts abstentions as misses.")
