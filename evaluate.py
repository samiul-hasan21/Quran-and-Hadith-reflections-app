"""Reproduce the matcher evaluation:  python tests/evaluate.py

TEST2 = 36 sentences held out from the owner's 12 categories (never used as example phrases)  <- headline number
TEST  = earlier held-out set (written before the first matcher existed)                       <- regression check
DEV   = used for tuning only
Strict = exact labels.  Adjusted = a prediction in a theme that was later split off from the labelled one also counts
(EQUIV in evalsets.py, declared before the older sets were re-run).
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, HERE)
from matcher import Matcher
from engine import THRESHOLD, MATCHER_KW, EXTRA_STOP
from evalsets import DEV, TEST, TEST2, EQUIV

D = os.path.join(HERE, "..", "data")
themes = json.load(open(os.path.join(D, "kb.json"), encoding="utf8"))["themes"]
VEC, VOC = os.path.join(D, "glove50k.npz"), os.path.join(D, "glove50k_vocab.json")


def accepted(labels, adjusted):
    s = set(labels)
    if adjusted:
        for l in labels:
            s |= EQUIV.get(l, set())
    return s


def run(m, data, thr, adjusted=False, verbose=False):
    on = [(q, a) for q, a in data if a != ["none"]]
    t1 = t3 = 0
    for q, labels in on:
        acc = accepted(labels, adjusted)
        r = m.rank(q); top, s = r[0]
        hit1 = s["score"] >= thr and top in acc
        hit3 = any(t in acc for t, _ in r[:3])
        t1 += hit1; t3 += hit3
        if verbose and not hit1:
            why = "declined" if s["score"] < thr else f"-> {top}"
            print(f"     miss: {q[:60]:60} {why:20} want {labels[0]:16} top3={[t for t,_ in r[:3]]}")
    return t1 / len(on), t3 / len(on)


cfgs = [("Hybrid (meaning + keywords)", dict(MATCHER_KW), THRESHOLD),
        ("Keywords only",              dict(emb_w=0.0, kw_w=0.6, remove_pc=0, top_pair=1, extra_stop=EXTRA_STOP), None),
        ("Word-vector meaning only",   dict(emb_w=1.0, kw_w=0.0, remove_pc=1, top_pair=2, extra_stop=EXTRA_STOP), None)]

print(f"{'Setup':29}{'thr':>5} | {'TEST2 top1':>10}{'top3':>6} | {'old TEST: strict':>16}{'adjusted':>9}{'top3':>6} | off-topic declined")
hybrid = None
for name, cfg, thr in cfgs:
    m = Matcher(VEC, VOC, themes, **cfg)
    if thr is None:                       # baselines: highest off-topic DEV score + small margin
        thr = max(m.rank(q)[0][1]["score"] for q, a in DEV if a == ["none"]) + 0.02
    a = run(m, TEST2, thr); b = run(m, TEST, thr); c = run(m, TEST, thr, adjusted=True)
    offs = [q for q, x in DEV + TEST if x == ["none"]]
    rej = sum(m.rank(q)[0][1]["score"] < thr for q in offs)
    print(f"{name:29}{thr:5.2f} | {a[0]:10.2f}{a[1]:6.2f} | {b[0]:16.2f}{c[0]:9.2f}{c[1]:6.2f} | {rej}/{len(offs)}")
    if name.startswith("Hybrid"):
        hybrid = (m, thr)

m, thr = hybrid
print(f"\nTEST2 = {len(TEST2)} sentences from the owner's categories. Misses for the hybrid matcher:")
run(m, TEST2, thr, verbose=True)
# ---- what the user actually sees (end to end, using the real engine) ---------------------------------------
from engine import Engine
E = Engine()
shown = rescued = lost = wrong = 0
for q, labels in TEST2:
    resp = E.respond(q); acc = set(labels)
    ids = {s["id"] for s in resp["sections"]}
    if resp["status"] in ("ok", "soft") and ids:
        if ids & acc: shown += 1
        else: wrong += 1
    else:
        sug = {s["id"] for s in resp.get("suggestions", [])}
        if sug & acc: rescued += 1
        else: lost += 1
n = len(TEST2)
print(f"\nWhat the user sees for the {n} held-out sentences (a labelled feeling appears in the answer):")
print(f"  right feeling shown in the answer            : {shown:2d}/{n}")
print(f"  declined, right feeling offered as a guess   : {rescued:2d}/{n}")
print(f"  declined, right feeling not offered          : {lost:2d}/{n}")
print(f"  answered with a different feeling            : {wrong:2d}/{n}")
print("\n'top1' counts a declined on-topic message as a miss.")
