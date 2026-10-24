"""
Engine: turns what a person writes into a set of verified Quran verses and Sahih hadith.

Design rules
  1. RETRIEVE, never generate. Every verse / hadith shown comes from the verified knowledge base (data/kb.json).
  2. SAFETY FIRST. Crisis, abuse and "ruling" questions are handled before any matching happens.
  3. DECLINE honestly. If nothing matches well, say so and let the person pick a feeling manually.
"""
import json, os, re
import numpy as np
from matcher import Matcher

HERE = os.path.dirname(os.path.abspath(__file__))
THRESHOLD = 0.47        # minimum hybrid score to answer (chosen on DEV; see tests/evaluate.py)
SECOND_RATIO = 0.85     # a second theme is shown if its score >= 85% of the best one
MAX_CHARS = 1000

# ------------------------------------------------------------------------------------------ safety
CRISIS = [re.compile(p, re.I) for p in [
    r"\bkill(ing)? my ?self\b", r"\bsuicid", r"\bend(ing)? (my|my own) life\b", r"\bend(ing)? it all\b",
    r"\btak(e|ing) my (own )?life\b", r"\b(want|wish|going|plan(ning)?|ready|wanting) to die\b",
    r"\bdon'?t want to (live|be alive|exist)\b", r"\bbetter off dead\b", r"\bno reason to live\b",
    r"\b(hurt|harm)(ing)? my ?self\b", r"\bself[- ]?(harm|injur)", r"\bcut(ting)? my ?self\b", r"\boverdos",
    r"\bwish i (was|were) dead\b", r"\bwish i (had never|hadn'?t) been born\b", r"\bnot worth living\b",
    r"\bno point (in )?living\b", r"\bhang(ing)? my ?self\b", r"\bslit(ting)? my wrist", r"\bjump(ing)? (off|from) (a|the) (bridge|building|roof)\b",
]]
SOFT = [re.compile(p, re.I) for p in [
    r"\bcan'?t (go on|take (it|this) anymore|do this anymore)\b", r"\bgive up on life\b", r"\bno point in (life|living)\b",
    r"\blife is (meaningless|pointless)\b", r"\bwant to disappear\b",
]]
ABUSE = [re.compile(p, re.I) for p in [
    r"\b(he|she|they|my \w+|someone|he's|she's|husband|wife|father|mother|dad|mom|boyfriend|girlfriend)\s+(hits|hit|beats|beat|slaps|slapped|punch(es|ed)?|kick(s|ed)?|chok(es|ed)|strangl\w+)\s+me\b",
    r"\bbeat(s|ing)? me\b", r"\babus(es|ed|ing)? me\b", r"\bi (was|am|have been|got|were) (being )?(sexually |physically |emotionally )?abused\b",
    r"\babusive (husband|wife|father|mother|parent|parents|partner|relationship|home|boyfriend|girlfriend|boss)\b", r"\bdomestic violence\b", r"\braped?\b", r"\bmolest", r"\bsexual(ly)? (assault|abus)",
    r"\bthreatens? to (kill|hurt) me\b", r"\bafraid (of|to go home to) my (husband|wife|father|mother|partner)\b", r"\bunsafe at home\b",
]]
RULING = [re.compile(p, re.I) for p in [
    r"\bharam\b", r"\bhalal\b", r"\bpermissible\b", r"\bfatwa\b", r"\bruling (on|of|for)\b", r"\ballowed in islam\b",
    r"\bdoes islam (allow|permit|forbid)\b", r"\bis it (a )?sin to\b", r"\bis it (haram|halal|allowed|forbidden)\b",
]]

HELPLINE = "https://findahelpline.com"

MSG_CRISIS = (
    "I'm really sorry you are carrying this much pain. You deserve support from a real person right now, and you do not "
    "have to face this alone.\n\n"
    "**If you might act on these thoughts, or you are in immediate danger, please contact your local emergency number now.** "
    f"Helplines for almost every country are listed at {HELPLINE}. "
    "Reaching out to someone you trust (a family member, a friend, a doctor, a counselor, or an imam you feel safe with) "
    "is a good next step, and you can ask them to stay with you while you do.\n\n"
    "Below are a few reminders about Allah's mercy, offered gently. They are not a substitute for talking to someone."
)
MSG_SOFT = (
    "It sounds like things feel very heavy right now. If at any point you feel unsafe or think about harming yourself, "
    f"please contact your local emergency number or a helpline ({HELPLINE}), and reach out to someone you trust."
)
MSG_ABUSE = (
    "What you describe may involve abuse or violence. It is not something you are required to endure in silence, and "
    "your safety comes first.\n\n"
    f"If you are in danger now, contact your local emergency number. A helpline or local support organization can help you "
    f"plan next steps ({HELPLINE} lists services by country), and a trusted person can help too.\n\n"
    "For this reason I am not showing reminders about patience here, because they should never be used to keep someone in harm's way."
)
MSG_RULING = (
    "That sounds like a question about an Islamic ruling. The verses and hadith here are offered for reflection and "
    "comfort. They are not a way to decide what is halal or haram, and quoting texts without their context and the "
    "scholarly tradition can mislead.\n\n"
    "Please ask a qualified scholar or your local imam. If you are also carrying a feeling about this (worry, guilt, "
    "confusion), describe that feeling and I will share reflections for it."
)
MSG_NOMATCH = (
    "I couldn't match that to a feeling I understand well. Try describing what you are going through in a sentence or two "
    "(for example: *I'm anxious about my exams*, *I lost my father*, *I feel far from Allah*), or choose a feeling below."
)
MSG_EMPTY = "Write a sentence about how you are feeling or what you are going through, or choose a feeling below."

CRISIS_ITEMS = ["q:39:53", "q:93:3-5", "q:2:186", "h:bukhari:5771"]


class Engine:
    def __init__(self, data_dir=None):
        d = data_dir or os.path.join(HERE, "data")
        self.kb = json.load(open(os.path.join(d, "kb.json"), encoding="utf8"))
        self.items = self.kb["items"]
        self.themes = self.kb["themes"]
        self.m = Matcher(os.path.join(d, "glove50k.npz"), os.path.join(d, "glove50k_vocab.json"), self.themes)
        self.ivec = {i: self.m.embed(it["en"][:500]) for i, it in self.items.items()}

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _any(patterns, text):
        return any(p.search(text) for p in patterns)

    def theme_choices(self):
        return [(t["title"], tid) for tid, t in self.themes.items()]

    def _pick(self, tid, qvec, n_quran=3, n_hadith=2, exclude=()):
        ids = [i for i in self.themes[tid]["items"] if i not in exclude]
        def ranked(kind, n):
            lst = [i for i in ids if self.items[i]["type"] == kind]
            scored = []
            for pos, i in enumerate(lst):
                prior = 1.0 - pos / max(1, len(lst))                # editorial order carries most weight
                v = self.ivec.get(i)
                sim = float(v @ qvec) if (qvec is not None and v is not None) else 0.0
                scored.append((0.7 * prior + 0.3 * sim, pos, i))
            scored.sort(key=lambda x: (-x[0], x[1]))
            return [i for _, _, i in scored[:n]]
        return ranked("quran", n_quran) + ranked("hadith", n_hadith)

    def _section(self, tid, ids):
        t = self.themes[tid]
        return {"id": tid, "title": t["title"], "intro": t["intro"], "items": [self.items[i] for i in ids]}

    # ---------------------------------------------------------------- public API
    def respond(self, text):
        text = (text or "").strip()
        if not text:
            return {"status": "empty", "message": MSG_EMPTY, "sections": []}
        text = text[:MAX_CHARS]

        if self._any(CRISIS, text):
            return {"status": "crisis", "message": MSG_CRISIS, "sections": [
                {"id": "crisis", "title": "Reminders of Allah's mercy", "intro": "", "items": [self.items[i] for i in CRISIS_ITEMS]}]}
        if self._any(ABUSE, text):
            return {"status": "abuse", "message": MSG_ABUSE, "sections": []}
        if self._any(RULING, text):
            return {"status": "ruling", "message": MSG_RULING, "sections": []}

        soft = self._any(SOFT, text)
        ranked = self.m.rank(text)
        (t1, s1), (t2, s2) = ranked[0], ranked[1]
        if s1["score"] < THRESHOLD:
            if soft:
                return {"status": "soft", "message": MSG_SOFT, "sections": [
                    self._section("hopeless", self._pick("hopeless", None))]}
            return {"status": "nomatch", "message": MSG_NOMATCH, "sections": []}

        qv = self.m.embed(text)
        sections = [self._section(t1, self._pick(t1, qv))]
        shown = {i["id"] for i in sections[0]["items"]}
        if s2["score"] >= THRESHOLD and s2["score"] >= SECOND_RATIO * s1["score"]:
            ids = self._pick(t2, qv, n_quran=1, n_hadith=1, exclude=shown)
            if ids:
                sections.append(self._section(t2, ids))
        return {"status": "soft" if soft else "ok", "message": MSG_SOFT if soft else "", "sections": sections,
                "matched": [t1] + ([t2] if len(sections) > 1 else [])}

    def respond_theme(self, tid):
        if tid not in self.themes:
            return {"status": "empty", "message": MSG_EMPTY, "sections": []}
        return {"status": "ok", "message": "", "sections": [self._section(tid, self._pick(tid, None))], "matched": [tid]}
