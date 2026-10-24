"""Run:  python tests/test_engine.py     (or: python -m pytest tests)"""
import os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from engine import Engine, CRISIS_ITEMS, HELPLINE

E = Engine()

# ------------------------------------------------------------------ data integrity
def test_every_item_is_complete():
    for i, it in E.items.items():
        assert it["en"].strip() and it["ar"].strip(), i
        assert not re.search(r"\[\d+\]|\(\d+\)|\s{2,}", it["en"]), (i, "formatting remnant")
        assert re.search(r"[\u0600-\u06FF]", it["ar"]), (i, "no Arabic letters")
        assert it["url"].startswith("https://"), i

def test_every_theme_has_enough_content():
    for tid, t in E.themes.items():
        kinds = [E.items[i]["type"] for i in t["items"]]
        assert kinds.count("quran") >= 3, tid
        assert kinds.count("hadith") >= 1, tid
        assert len(set(t["items"])) == len(t["items"]), (tid, "duplicate item")
        assert all(i in E.items for i in t["items"]), tid
        assert len(t["anchors"]) >= 6 and len(t["keywords"]) >= 6, tid

def test_bukhari_numbers_present_and_muslim_not_invented():
    for i, it in E.items.items():
        if it["type"] == "hadith" and it["collection"] == "Sahih al-Bukhari":
            assert isinstance(it["number"], int), i
        if it["type"] == "hadith" and it["collection"] == "Sahih Muslim":
            assert it["number"] is None, (i, "never print a Muslim number we cannot verify")

def test_excerpts_are_flagged():
    ex = [i for i, it in E.items.items() if it["excerpt"]]
    assert ex and all(i.endswith(":x") for i in ex)

# ------------------------------------------------------------------ safety
CRISIS_POS = ["I want to kill myself", "i have been feeling suicidal", "I want to end my life", "I don't want to live anymore",
              "I wish I was dead", "everyone would be better off dead without me", "i keep thinking about hurting myself",
              "I want to die", "i have no reason to live", "thinking of taking my own life", "I've been cutting myself", "I am planning on ending my life", "i keep thinking about killing myself",
              "i want to harm myself", "I might hang myself", "i think about suicide every day"]
CRISIS_NEG = ["this exam is killing me", "I'm dying to see my family again", "my phone died", "I need to kill time before my flight",
              "I'm worried about my exams", "my grandfather died last week", "I feel sad and lonely", "it is a matter of life and death for the project"]

def test_crisis_detected():
    for q in CRISIS_POS:
        r = E.respond(q)
        assert r["status"] == "crisis", q
        assert HELPLINE in r["message"], q
        assert [it["id"] for it in r["sections"][0]["items"]] == CRISIS_ITEMS

def test_crisis_not_triggered_by_everyday_language():
    for q in CRISIS_NEG:
        assert E.respond(q)["status"] != "crisis", q

def test_abuse_detected_and_no_patience_verses_shown():
    for q in ["my husband hits me", "he beats me when he is angry", "I was abused as a child", "my father is an abusive man in our home".replace("man in our home", "parent")]:
        r = E.respond(q)
        assert r["status"] == "abuse", q
        assert r["sections"] == [], q            # must never show 'be patient' verses to someone being harmed
    assert E.respond("it hit me that I should call my mom")["status"] != "abuse"
    assert E.respond("my boss abuses his power and blames me unfairly")["status"] != "abuse"

def test_rulings_are_redirected_to_scholars():
    for q in ["Is it haram to listen to music?", "what is the ruling on investing in stocks", "is it permissible to skip fasting"]:
        r = E.respond(q); assert r["status"] == "ruling" and r["sections"] == [], q

def test_soft_distress_adds_a_check_in_but_still_answers():
    r = E.respond("I can't go on like this, everything is hopeless and I see no way out")
    assert r["status"] == "soft" and HELPLINE in r["message"] and r["sections"]

# ------------------------------------------------------------------ behaviour
def test_empty_and_offtopic():
    assert E.respond("")["status"] == "empty"
    assert E.respond("   ")["status"] == "empty"
    for q in ["how do I bake bread", "what is the capital of france", "write a python function"]:
        assert E.respond(q)["status"] == "nomatch", q

def test_known_queries_land_on_the_right_theme():
    cases = {"I am so anxious about my exam results": {"anxiety", "study_work"},
             "my mother passed away and I miss her": {"bereavement"},
             "I feel so lonely and have nobody": {"loneliness"},
             "I have too much debt and cannot pay rent": {"provision"},
             "I committed a sin and want to repent": {"guilt"}}
    for q, ok in cases.items():
        r = E.respond(q); assert r["status"] in ("ok", "soft") and r["matched"][0] in ok, (q, r.get("matched"))

def test_response_shape_and_no_duplicates():
    r = E.respond("I'm afraid of my surgery and worried about everything")
    ids = [it["id"] for s in r["sections"] for it in s["items"]]
    assert len(ids) == len(set(ids)), "an item was shown twice"
    first = r["sections"][0]["items"]
    assert sum(i["type"] == "quran" for i in first) <= 3 and sum(i["type"] == "hadith" for i in first) <= 2

def test_every_theme_can_be_chosen_directly():
    for _, tid in E.theme_choices():
        r = E.respond_theme(tid); assert r["sections"][0]["items"], tid

def test_deterministic():
    q = "I feel lost and don't know my purpose"
    a, b = E.respond(q), E.respond(q)
    assert [i["id"] for s in a["sections"] for i in s["items"]] == [i["id"] for s in b["sections"] for i in s["items"]]

def test_long_input_is_truncated_not_crashing():
    assert E.respond("I am worried " * 500)["status"] in ("ok", "soft", "nomatch")

if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for f in fns:
        try: f(); print("PASS ", f.__name__)
        except AssertionError as ex: failed += 1; print("FAIL ", f.__name__, "->", ex)
    print(f"\n{len(fns) - failed}/{len(fns)} tests passed"); sys.exit(1 if failed else 0)
