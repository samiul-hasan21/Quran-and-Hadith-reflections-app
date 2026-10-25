# The 12 feeling categories supplied by the project owner, verbatim (10 sentences each).
#
# SPLIT (fixed BEFORE any matching was run):
#   sentences at index 2, 5, 8 of every category are HELD OUT as a test set (36 sentences);
#   the other 7 per category (84) become example phrases ("anchors") for the matcher.
#
# LABELS for held-out sentences were also written before running: the first id is the primary theme,
# the rest are other reasonable matches (a feeling often fits more than one theme).

CATEGORIES = {
 "Overthinking": [
  "I'm overthinking everything lately.",
  "I'm overthinking about my future.",
  "I'm overthinking every little thing I said.",
  "I'm scared that something bad will happen.",
  "I can't stop thinking about the past.",
  "I'm afraid of losing someone I love.",
  "My mind won't let me rest.",
  "I'm always imagining the worst possible outcome.",
  "I keep questioning my own decisions.",
  "I'm overthinking whether I'm good enough.",
 ],
 "Feeling guilty": [
  "I'm feeling guilty about something I did.",
  "I regret hurting someone I love.",
  "I can't forgive myself for my mistakes.",
  "I feel like I've disappointed my family.",
  "I'm ashamed of my past.",
  "I did something wrong, and it's haunting me.",
  "I feel guilty even when I try to move on.",
  "I wish I could undo my mistakes.",
  "I'm struggling to forgive myself.",
  "I feel like I don't deserve happiness anymore.",
 ],
 "Betrayal and heartbreak": [
  "Someone I love betrayed me.",
  "I trusted someone, and they broke my trust.",
  "The person I love hurt me deeply.",
  "I feel betrayed by my closest friend.",
  "Someone I trusted lied to me.",
  "I gave someone my everything, but they left.",
  "I can't believe someone I love could do this to me.",
  "I'm struggling to trust people again.",
  "I feel replaceable.",
  "Why do the people I love hurt me the most?",
 ],
 "Sadness and loneliness": [
  "I'm feeling lonely even when I'm surrounded by people.",
  "I feel like nobody understands me.",
  "I'm tired of pretending to be happy.",
  "I feel empty inside.",
  "I have nobody to talk to.",
  "I'm missing someone I can't get back.",
  "I feel forgotten by everyone.",
  "I'm smiling outside but hurting inside.",
  "I don't feel like myself anymore.",
  "I wish someone would ask me if I'm okay.",
 ],
 "Anxiety and fear": [
  "I'm scared of what tomorrow will bring.",
  "I'm feeling anxious about my future.",
  "I'm afraid of failing.",
  "I feel like I'm losing control of my life.",
  "I'm worried about my family's future.",
  "I'm scared that I'll never be successful.",
  "I can't calm my thoughts.",
  "I'm afraid of disappointing everyone.",
  "I feel nervous about making the wrong decision.",
  "I'm constantly worried about things I can't control.",
 ],
 "Regret and repentance": [
  "I keep repeating the same mistakes.",
  "I've done things I wish I hadn't done.",
  "I'm afraid Allah won't forgive me.",
  "I've been distant from Allah lately.",
  "I want to become a better Muslim.",
  "I feel ashamed of my sins.",
  "I've made promises to Allah that I couldn't keep.",
  "I want to repent, but I don't know where to start.",
  "I keep falling back into my old habits.",
  "I feel like I've lost my way spiritually.",
 ],
 "Anger and resentment": [
  "I'm angry at someone who hurt me.",
  "I can't let go of what they did to me.",
  "I want revenge on the person who betrayed me.",
  "I'm tired of being treated unfairly.",
  "I feel like nobody respects me.",
  "I get angry over the smallest things.",
  "I hate how people take advantage of my kindness.",
  "I can't stop replaying that argument in my head.",
  "I want to forgive, but I'm still hurting.",
  "I'm struggling to control my anger.",
 ],
 "Hopelessness and loss of motivation": [
  "I'm losing hope in everything.",
  "I feel like nothing is working out for me.",
  "I'm tired of trying so hard.",
  "I feel like I'm falling behind in life.",
  "I'm afraid I'll never achieve my dreams.",
  "I don't know what I'm doing with my life.",
  "I'm struggling to find a reason to keep trying.",
  "Everything feels too difficult right now.",
  "I feel like my efforts are going to waste.",
  "I need a reminder that things can get better.",
 ],
 "Gratitude and happiness": [
  "I'm feeling grateful for what I have.",
  "Allah has blessed me in ways I didn't expect.",
  "I'm finally finding peace in my life.",
  "I'm happy with how far I've come.",
  "I want to thank Allah for everything.",
  "I'm feeling hopeful about my future.",
  "I'm grateful that I got another chance.",
  "I'm happy that my duas were answered.",
  "I want to become more grateful every day.",
  "I'm experiencing a peace I can't explain.",
 ],
 "Relationship struggles": [
  "I'm in love with someone I can't marry.",
  "I'm scared of losing my relationship.",
  "I feel like I'm the only one trying.",
  "Someone I love is slowly becoming distant.",
  "I'm struggling to move on from my ex.",
  "I love someone who doesn't love me back.",
  "I'm confused about whether I should stay or leave.",
  "I'm afraid my relationship is taking me away from Allah.",
  "I keep making dua for someone I love.",
  "I'm struggling to accept that someone is not meant for me.",
 ],
 "Family problems": [
  "I'm feeling pressured by my family.",
  "My parents don't understand me.",
  "I'm hurt by the way my family treats me.",
  "I feel like I'm never good enough for my parents.",
  "I'm struggling to forgive a family member.",
  "I feel responsible for everyone's happiness.",
  "I'm tired of hiding my problems from my family.",
  "I want to make my parents proud.",
  "I'm feeling neglected by the people closest to me.",
  "I don't know how to deal with family conflicts.",
 ],
 "Faith and spiritual struggles": [
  "I'm feeling distant from Allah.",
  "I'm struggling to pray regularly.",
  "My iman feels weak lately.",
  "I'm wondering why Allah is testing me so much.",
  "I'm making dua, but I'm losing patience.",
  "I feel spiritually lost.",
  "I'm struggling to understand why bad things happen to good people.",
  "I want to get closer to Allah again.",
  "I'm finding it difficult to trust Allah's plan.",
  "I need a reminder that Allah has not abandoned me.",
 ],
}

HELD_OUT = (2, 5, 8)

# Which theme each TRAINING sentence teaches. Default per category, with per-index exceptions.
DEFAULT_THEME = {
 "Overthinking": "overthinking", "Feeling guilty": "self_forgiveness", "Betrayal and heartbreak": "betrayal",
 "Sadness and loneliness": "loneliness", "Anxiety and fear": "anxiety", "Regret and repentance": "guilt",
 "Anger and resentment": "anger", "Hopelessness and loss of motivation": "motivation",
 "Gratitude and happiness": "gratitude", "Relationship struggles": "love_relationship",
 "Family problems": "family", "Faith and spiritual struggles": "weak_faith",
}
EXCEPTIONS = {
 ("Overthinking", 3): "fear_trust",
 ("Sadness and loneliness", 3): "sadness", ("Sadness and loneliness", 7): "sadness",
 ("Anxiety and fear", 0): "fear_trust", ("Anxiety and fear", 3): "fear_trust", ("Anxiety and fear", 4): "fear_trust",
 ("Regret and repentance", 3): "weak_faith", ("Regret and repentance", 4): "weak_faith", ("Regret and repentance", 9): "weak_faith",
 ("Anger and resentment", 3): "injustice", ("Anger and resentment", 4): "injustice", ("Anger and resentment", 6): "injustice",
 ("Hopelessness and loss of motivation", 0): "hopeless", ("Hopelessness and loss of motivation", 1): "hopeless",
 ("Hopelessness and loss of motivation", 7): "hardship", ("Hopelessness and loss of motivation", 9): "hopeless",
 ("Faith and spiritual struggles", 3): "why_trials", ("Faith and spiritual struggles", 4): "dua",
 ("Faith and spiritual struggles", 6): "why_trials",
}

# Held-out labels, fixed before running: (category, index) -> acceptable themes (first = primary)
HELD_OUT_LABELS = {
 ("Overthinking", 2): ["overthinking", "anxiety"],
 ("Overthinking", 5): ["fear_trust", "anxiety", "overthinking"],
 ("Overthinking", 8): ["overthinking", "decisions", "anxiety"],
 ("Feeling guilty", 2): ["self_forgiveness", "guilt"],
 ("Feeling guilty", 5): ["self_forgiveness", "guilt"],
 ("Feeling guilty", 8): ["self_forgiveness", "guilt"],
 ("Betrayal and heartbreak", 2): ["betrayal"],
 ("Betrayal and heartbreak", 5): ["betrayal", "sadness", "loneliness"],
 ("Betrayal and heartbreak", 8): ["betrayal", "self_worth"],
 ("Sadness and loneliness", 2): ["sadness", "loneliness"],
 ("Sadness and loneliness", 5): ["sadness", "bereavement", "love_relationship"],
 ("Sadness and loneliness", 8): ["sadness", "self_worth", "guidance"],
 ("Anxiety and fear", 2): ["anxiety", "fear_trust", "failure"],
 ("Anxiety and fear", 5): ["anxiety", "fear_trust", "failure", "motivation"],
 ("Anxiety and fear", 8): ["decisions", "anxiety", "overthinking"],
 ("Regret and repentance", 2): ["guilt", "self_forgiveness"],
 ("Regret and repentance", 5): ["guilt", "self_forgiveness"],
 ("Regret and repentance", 8): ["guilt", "weak_faith"],
 ("Anger and resentment", 2): ["anger", "betrayal", "injustice"],
 ("Anger and resentment", 5): ["anger"],
 ("Anger and resentment", 8): ["anger", "betrayal", "family"],
 ("Hopelessness and loss of motivation", 2): ["motivation", "overwhelmed", "hopeless", "hardship"],
 ("Hopelessness and loss of motivation", 5): ["guidance", "motivation"],
 ("Hopelessness and loss of motivation", 8): ["motivation", "failure", "hopeless"],
 ("Gratitude and happiness", 2): ["gratitude"],
 ("Gratitude and happiness", 5): ["gratitude"],
 ("Gratitude and happiness", 8): ["gratitude"],
 ("Relationship struggles", 2): ["love_relationship", "family"],
 ("Relationship struggles", 5): ["love_relationship", "betrayal"],
 ("Relationship struggles", 8): ["love_relationship", "dua"],
 ("Family problems", 2): ["family", "injustice"],
 ("Family problems", 5): ["family", "overwhelmed"],
 ("Family problems", 8): ["family", "loneliness", "injustice"],
 ("Faith and spiritual struggles", 2): ["weak_faith"],
 ("Faith and spiritual struggles", 5): ["weak_faith", "guidance"],
 ("Faith and spiritual struggles", 8): ["fear_trust", "weak_faith", "why_trials"],
}

def train_anchors():
    """theme -> list of lower-cased training sentences."""
    out = {}
    for cat, sents in CATEGORIES.items():
        for i, s in enumerate(sents):
            if i in HELD_OUT:
                continue
            t = EXCEPTIONS.get((cat, i), DEFAULT_THEME[cat])
            out.setdefault(t, []).append(s.lower().rstrip("."))
    return out

def held_out_set():
    return [(CATEGORIES[c][i], labels) for (c, i), labels in HELD_OUT_LABELS.items()]

if __name__ == "__main__":
    n_train = sum(len(v) for v in train_anchors().values())
    print("categories:", len(CATEGORIES), "| sentences:", sum(len(v) for v in CATEGORIES.values()),
          "| train anchors:", n_train, "| held out:", len(held_out_set()))
    for t, v in sorted(train_anchors().items()): print(f"  {t:18} +{len(v)} anchors")
