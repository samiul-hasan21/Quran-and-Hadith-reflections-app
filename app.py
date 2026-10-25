"""
Reflections from the Quran & Sunnah
Describe how you feel; get verified verses (Quran) and authentic hadith (Sahih al-Bukhari / Sahih Muslim).

Nothing is generated: every verse and hadith is retrieved verbatim from a verified text collection.
Run locally:  python app.py   ->  http://localhost:7860
"""
import os
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")      # no telemetry

import html, re
import gradio as gr
from engine import Engine

E = Engine()

# ----------------------------------------------------------------------------------------- rendering
URL_RE = re.compile(r"(https?://[^\s<)]*[^\s<).,;:!?])")


def esc(s):
    return html.escape(s, quote=True)


def md_lite(text):
    """Tiny, safe markdown: **bold**, *italic*, bare links, paragraphs. Everything is escaped first."""
    out = []
    for para in text.split("\n\n"):
        p = esc(para)
        p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"\*(.+?)\*", r"<i>\1</i>", p)
        p = URL_RE.sub(r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>', p)
        out.append(f"<p>{p}</p>")
    return "".join(out)


def quran_card(it):
    dots_s = "\u2026 " if it.get("cut_start") else ""
    dots_e = " \u2026" if it.get("cut_end") and not it["en"].endswith("\u2026") else ""
    badge = '<span class="badge" title="Part of the verse(s) is shown; the cut is marked with an ellipsis">excerpt</span>' if it["excerpt"] else ""
    return (
        '<div class="card q">'
        f'<div class="ref"><b>Surah {esc(it["surah_name"])}</b> <span>({esc(it["surah_meaning"])})</span>'
        f' <span class="num">{esc(it["ref"])}</span>{badge}</div>'
        f'<div class="ar" dir="rtl" lang="ar">{dots_s}{esc(it["ar"])}{dots_e}</div>'
        f'<div class="en">{dots_s}{esc(it["en"])}</div>'
        f'<a class="src" href="{esc(it["url"])}" target="_blank" rel="noopener noreferrer">Read in context on Quran.com \u2197</a>'
        "</div>"
    )


def hadith_card(it):
    num = f' <span class="num">#{it["number"]}</span>' if it.get("number") else ""
    badge = '<span class="badge" title="Only the relevant part of this narration is shown">excerpt</span>' if it["excerpt"] else ""
    en = it["en"]
    if len(en) > 600:
        preview = en[:380].rsplit(" ", 1)[0] + " \u2026"
        body = (f'<div class="en">{esc(preview)}</div>'
                f'<details class="more"><summary>Read the full hadith</summary><div class="en">{esc(en)}</div></details>')
    else:
        body = f'<div class="en">{esc(en)}</div>'
    link_text = "Open on Sunnah.com \u2197" if it.get("number") else "Find on Sunnah.com \u2197"
    return (
        '<div class="card h">'
        f'<div class="ref"><b>{esc(it["collection"])}</b>{num} <span>\u00b7 {esc(it["book"])}</span>{badge}</div>'
        f'<div class="narr">{esc(it["narrator"])}</div>'
        f"{body}"
        f'<details class="arb"><summary>Arabic text (includes the chain of narrators)</summary>'
        f'<div class="ar sm" dir="rtl" lang="ar">{esc(it["ar"])}</div></details>'
        f'<a class="src" href="{esc(it["url"])}" target="_blank" rel="noopener noreferrer">{link_text}</a>'
        "</div>"
    )


def render(resp):
    parts = ['<div class="qh">']
    if resp.get("message"):
        care = resp["status"] in ("crisis", "abuse", "soft")
        parts.append(f'<div class="notice{" care" if care else ""}">{md_lite(resp["message"])}</div>')
    for sec in resp["sections"]:
        parts.append(f'<div class="sec"><h3>{esc(sec["title"])}</h3>')
        if sec["intro"]:
            parts.append(f'<p class="intro">{esc(sec["intro"])}</p>')
        parts.extend(quran_card(i) if i["type"] == "quran" else hadith_card(i) for i in sec["items"])
        parts.append("</div>")
    if resp["sections"]:
        if resp.get("matched") and resp["status"] in ("ok", "soft"):
            names = " and ".join(f"<b>{esc(s['title'])}</b>" for s in resp["sections"])
            parts.append(f'<p class="fine">Matched to {names}. If this does not fit, choose a different feeling from the list.</p>')
        parts.append(
            '<p class="fine">Shown word-for-word from the sources listed below; excerpts are marked. '
            "These are reflections for comfort, not rulings or medical advice.</p>")
    parts.append("</div>")
    return "".join(parts)


WELCOME = (
    '<div class="qh"><div class="notice"><p>Tell me how you are feeling or what you are going through, '
    "and I will bring you verses of the Quran and authentic hadith that speak to it.</p>"
    "<p>You can also pick a feeling from the list.</p></div></div>"
)


def search(text):
    resp = E.respond(text)
    sugg = resp.get("suggestions") or []
    choices = [(s["title"], f"theme:{s['id']}") for s in sugg]
    return render(resp), gr.update(choices=choices, value=None, visible=bool(sugg))


def choose(value):
    """Dropdown / suggestion picked by the user (category or single feeling)."""
    if not value:
        return WELCOME, gr.update(visible=False)
    return render(E.respond_pick(value)), gr.update(visible=False)


# ----------------------------------------------------------------------------------------- interface
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Naskh+Arabic&display=swap');
.qh{max-width:860px;margin:0 auto}
.qh h3{margin:18px 0 2px;font-size:1.25rem}
.qh .intro{margin:0 0 6px;color:var(--body-text-color-subdued)}
.qh .card{border:1px solid var(--border-color-primary);border-radius:14px;padding:16px 18px;margin:12px 0;background:var(--background-fill-secondary)}
.qh .card.q{border-left:4px solid #1f8f5f}
.qh .card.h{border-left:4px solid #b8860b}
.qh .ref{font-size:.88rem;color:var(--body-text-color-subdued);display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px}
.qh .ref b{color:var(--body-text-color)}
.qh .num{font-variant-numeric:tabular-nums;border-radius:6px;padding:0 6px;background:var(--background-fill-primary)}
.qh .badge{font-size:.7rem;border:1px solid var(--border-color-primary);border-radius:20px;padding:1px 8px}
.qh .ar{font-family:'Amiri','Noto Naskh Arabic','Scheherazade New','Traditional Arabic',serif;font-size:1.7rem;line-height:2.4;text-align:right;direction:rtl;margin:6px 0 10px;color:var(--body-text-color)}
.qh .ar.sm{font-size:1.25rem;line-height:2.1}
.qh .en{font-size:1.02rem;line-height:1.7;color:var(--body-text-color)}
.qh .narr{font-size:.92rem;font-style:italic;color:var(--body-text-color-subdued);margin-bottom:4px}
.qh details{margin:8px 0}
.qh summary{cursor:pointer;font-size:.9rem;color:var(--body-text-color-subdued)}
.qh a.src{display:inline-block;margin-top:8px;font-size:.85rem}
.qh .notice{border:1px solid var(--border-color-primary);border-radius:14px;padding:6px 16px;margin:8px 0;background:var(--background-fill-secondary)}
.qh .notice.care{border-left:5px solid #c0392b}
.qh .fine{font-size:.82rem;color:var(--body-text-color-subdued);margin-top:14px}
footer{visibility:hidden}
"""

HEADER = """
<div style="text-align:center;margin:6px 0 2px">
  <div style="font-size:2rem">\U0001F54C</div>
  <h1 style="margin:2px 0;font-size:1.7rem">Reflections from the Quran &amp; Sunnah</h1>
  <p style="margin:2px 0;color:var(--body-text-color-subdued)">Verified verses and authentic hadith for how you feel today.</p>
</div>
"""

ABOUT = f"""
**How it works.** Your words are compared with example statements for {len(E.themes)} common feelings and life situations
(anxiety, grief, hardship, guilt, loneliness, study, provision and more). The best-matching feeling selects verses of the
Quran and hadith from Sahih al-Bukhari and Sahih Muslim. **Nothing is generated by an AI model**, so nothing can be invented
or misquoted: each text is copied from a verified source, and the full-context link is shown with it.

**Accuracy, measured honestly.** On 36 sentences that were kept out of the app's training examples, the right feeling
appeared in the answer for 26 (72%). Another 3 were declined but the right feeling was offered as a one-tap suggestion, so
29 of 36 (81%) reached the right feeling within one tap. 5 were matched to a different feeling and 2 were missed. On an
earlier set of 66 messages the right feeling came first 89% of the time (97% within the top three), and all 16 off-topic
messages were declined. Short, abstract sentences are the hardest. If the result does not fit you, choose a feeling yourself.

**Limits.** Understands English only. Cannot give rulings (halal/haram), which belong to qualified scholars. Not a substitute
for professional mental-health care. If you are in crisis, please contact local emergency services or a helpline
(https://findahelpline.com). This app does not save what you write.

**Sources.** Quran Arabic: Tanzil (Uthmani). Quran English: Saheeh International (via QuranEnc.com). Hadith: Sahih al-Bukhari
(tr. Muhsin Khan) and Sahih Muslim (tr. Abdul Hamid Siddiqui), text via sunnah.com. Hadith numbers are shown only for Bukhari,
where they were verified against a second dataset; Muslim hadith are cited by book. Word vectors: GloVe (Stanford, PDDL).
"""

EXAMPLES = [
    "I'm overthinking everything lately",
    "I regret hurting someone I love",
    "Someone I trusted lied to me",
    "I'm tired of pretending to be happy",
    "I'm afraid Allah won't forgive me",
    "I'm struggling to control my anger",
    "I feel like my efforts are going to waste",
    "I'm in love with someone I can't marry",
    "My parents don't understand me",
    "I'm wondering why Allah is testing me so much",
    "I lost my job and I'm worried about paying rent",
    "I'm feeling grateful for what I have",
]

with gr.Blocks(title="Reflections from the Quran & Sunnah", css=CSS,
               theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="stone")) as demo:
    gr.HTML(HEADER)
    with gr.Row():
        with gr.Column(scale=5):
            box = gr.Textbox(label="What is on your heart?", lines=4, max_length=1000,
                             placeholder="For example: I'm anxious about my exams and can't sleep\u2026")
            with gr.Row():
                go = gr.Button("Find reflections", variant="primary")
                clear = gr.Button("Clear")
            gr.Examples(EXAMPLES, inputs=box, label="Try one of these", examples_per_page=len(EXAMPLES))
            pick = gr.Dropdown(choices=E.picker_choices(), value=None, label="Or choose a feeling", interactive=True)
            suggest = gr.Radio(choices=[], value=None, visible=False, interactive=True,
                               label="Not sure I understood. Is it one of these?")
        with gr.Column(scale=7):
            out = gr.HTML(WELCOME)
    with gr.Accordion("About, accuracy and sources", open=False):
        gr.Markdown(ABOUT)

    go.click(search, box, [out, suggest], scroll_to_output=True)
    box.submit(search, box, [out, suggest], scroll_to_output=True)
    pick.input(choose, pick, [out, suggest], scroll_to_output=True)        # .input = only when the person picks
    suggest.input(choose, suggest, [out, suggest], scroll_to_output=True)
    clear.click(lambda: ("", None, WELCOME, gr.update(choices=[], value=None, visible=False)), None, [box, pick, out, suggest])


if __name__ == "__main__":
    # pwa=True lets phones "install" the page to the home screen (needs HTTPS, which Render provides)
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)),
                pwa=True, favicon_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"))
