"""
Feeling -> theme matcher. Pure numpy (no ML framework), ~10 MB of data, runs comfortably on a free host.

Pipeline
  text -> normalise -> tokens -> SIF-weighted average of GloVe vectors -> remove common component
       -> cosine similarity to each theme's example phrases        (meaning evidence)
       +  weighted keyword / phrase cues                            (lexical evidence)
       -> hybrid score per theme -> ranked themes, with abstention when the best score is too low.
"""
import json, re, math
import numpy as np

STOP = set("""a an the of to in on at for from by with and or but if then so is are was were be been being am do does did
doing have has had having i me my mine myself we our ours you your yours he she it its they them their his her this that
these those there here as about into over under again just very really too also can could would should will shall may
might must than up out off all any some more most such own same only s t don didn doesn isn aren wasn weren won wouldn
couldn shouldn ve ll re d m what when where which who whom why how because while during before after through above below
between both each few other nor not no yes ok please help""".split())


def norm_text(s):
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


class Matcher:
    def __init__(self, vec_npz, vocab_json, themes, emb_w=1.0, kw_w=0.25, kw_cap=2.0, top_pair=2,
                 remove_pc=1, sif_a=1e-3):
        z = np.load(vec_npz)
        self.V = z["vecs"].astype(np.float32)
        words = json.load(open(vocab_json))
        self.w2i = {w: i for i, w in enumerate(words)}
        n = len(words)
        H = math.log(n) + 0.5772
        p = 1.0 / ((np.arange(n) + 1) * H)               # Zipf estimate of unigram probability from frequency rank
        self.sif = (sif_a / (sif_a + p)).astype(np.float32)
        self.themes = themes
        self.emb_w, self.kw_w, self.kw_cap, self.top_pair, self.remove_pc = emb_w, kw_w, kw_cap, top_pair, remove_pc

        # raw anchor embeddings -> common component -> normalised anchors
        raw = {t: [self._raw(a) for a in d["anchors"]] for t, d in themes.items()}
        allv = np.vstack([v for vs in raw.values() for v in vs if v is not None])
        self.pcs = None
        if remove_pc:
            _, _, vt = np.linalg.svd(allv - 0, full_matrices=False)
            self.pcs = vt[:remove_pc]
        self.anchor = {}
        for t, vs in raw.items():
            m = np.vstack([self._finish(v) for v in vs if v is not None])
            self.anchor[t] = m

        # keyword cues, normalised the same way as user text
        self.kws = {}
        for t, d in themes.items():
            lst = []
            for k in d["keywords"]:
                w = 1.0
                if isinstance(k, (tuple, list)):
                    k, w = k
                lst.append((norm_text(k), w))
            self.kws[t] = lst

    # ---- embedding
    def tokens(self, text):
        s = text.lower().replace("\u2019", "'").replace("\u2018", "'")
        for pat, rep in ((r"can't", "cannot"), (r"won't", "will not"), (r"n't", " not"), (r"'m", " am"), (r"'re", " are"),
                         (r"'ve", " have"), (r"'ll", " will"), (r"'d", " would"), (r"'s", "")):
            s = re.sub(pat, rep, s)
        return [t for t in re.findall(r"[a-z]+", s) if t not in STOP]

    def _lookup(self, t):
        if t in self.w2i:
            return self.w2i[t]
        for suf in ("ing", "ed", "es", "s", "ly"):
            if t.endswith(suf) and t[: -len(suf)] in self.w2i:
                return self.w2i[t[: -len(suf)]]
        return None

    def _raw(self, text):
        idx = [i for i in (self._lookup(t) for t in self.tokens(text)) if i is not None]
        if not idx:
            return None
        w = self.sif[idx]
        return (self.V[idx] * w[:, None]).sum(0) / w.sum()

    def _finish(self, v):
        if self.pcs is not None:
            for pc in self.pcs:
                v = v - (v @ pc) * pc
        n = np.linalg.norm(v)
        return v / n if n > 0 else v

    def embed(self, text):
        v = self._raw(text)
        return None if v is None else self._finish(v)

    # ---- keyword evidence
    def kw_score(self, theme, text):
        nt = norm_text(text)
        toks = nt.split()
        padded = f" {nt} "
        total, hits = 0.0, []
        for kw, w in self.kws[theme]:
            if not kw:
                continue
            ok = False
            if " " in kw:
                ok = f" {kw} " in padded or (kw in nt)
            elif len(kw) <= 3:
                ok = kw in toks
            else:
                ok = any(t.startswith(kw) for t in toks)
            if ok:
                total += w
                hits.append(kw)
        return min(total, self.kw_cap), hits

    # ---- scoring
    def score(self, text):
        q = self.embed(text)
        out = {}
        for t in self.themes:
            if q is not None:
                sims = np.sort(self.anchor[t] @ q)[::-1]
                e = float(sims[: self.top_pair].mean())
            else:
                e = 0.0
            k, hits = self.kw_score(t, text)
            out[t] = dict(emb=e, kw=k, hits=hits, score=self.emb_w * e + self.kw_w * k)
        return out

    def rank(self, text):
        sc = self.score(text)
        return sorted(sc.items(), key=lambda kv: -kv[1]["score"])
