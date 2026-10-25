# Final curated reference map.
#
# Only REFERENCES live here. Every word shown to a user is pulled from the verified corpora
# at build time (build_kb.py) -- nothing is typed or paraphrased by hand.
#
# Quran entries:  "s:a" | "s:a-b"  or a dict with an excerpt spec:
#     {"ref": "2:216", "from": "But perhaps you hate",           # English start phrase (optional)
#      "to": "...", "ar_from": <word index>, "ar_to": <word idx>} # Arabic word indices (0-based, inclusive)
#   Excerpts are always labelled "excerpt" in the UI.
#
# Hadith entries: (collection, hj_id, assertion_phrase[, cut_after_phrase])
#   assertion_phrase must appear in the hadith text, otherwise the build FAILS (guards against a wrong pick).

def X(ref, **kw):
    d = {"ref": ref}; d.update(kw); return d

REFS = {
    "anxiety": {
        "quran": ["13:28", "2:286", "94:5-6", X("65:2-3", frm="And whoever fears Allah", ar=(24,None)), "3:173", "9:51"],
        "hadith": [("bukhari", 6132, "worry and grief"), ("muslim", 14591, "good in every affair")],
    },
    "sadness": {
        "quran": ["93:3", "2:155-157", "3:139", "12:86", "9:40", "94:5-6"],
        "hadith": [("bukhari", 5428, "nor sorrow, nor sadness"), ("bukhari", 1261, "shedding tears")],
    },
    "bereavement": {
        "quran": ["2:155-157", "89:27-30", "2:153", "93:3", "57:22-23"],
        "hadith": [("bukhari", 5441, "It is for Allah what He takes"), ("bukhari", 1261, "shedding tears")],
    },
    "hardship": {
        "quran": ["94:5-6", "2:153", "39:10", "65:7", "2:214", "3:200"],
        "hadith": [("muslim", 14591, "good in every affair"), ("bukhari", 1260, "first stroke of a calamity")],
    },
    "hopeless": {
        "quran": ["39:53", "12:87", X("65:2-3", frm="And whoever fears Allah", ar=(24,None)), "2:214", "93:3-5"],
        "hadith": [("bukhari", 7123, "I am just as My slave thinks I am"), ("bukhari", 5771, "throw her son in the fire")],
    },
    "guilt": {
        "quran": ["39:53", "4:110", "3:135-136", "66:8", "42:25", "7:23"],
        "hadith": [("bukhari", 6072, "more pleased with the repentance"), ("muslim", 14071, "seek forgiveness from Allah")],
    },
    "loneliness": {
        "quran": ["2:186", "50:16", "20:46", "93:3", "9:40"],
        "hadith": [("bukhari", 7123, "I am with him if He remembers Me"), ("bukhari", 2346, "hand him over to an oppressor")],
    },
    "anger": {
        "quran": ["3:134", "41:34-35", "42:37", "7:199", "42:43"],
        "hadith": [("bukhari", 5882, "controls himself while in anger"), ("bukhari", 5884, "Do not become angry")],
    },
    "gratitude": {
        "quran": ["14:7", "16:18", "2:152", "93:11", "31:12"],
        "hadith": [("muslim", 14591, "he thanks (God)"), ("muslim", 14523, "Look at those who stand at a lower level", "Allah's favors.")],
    },
    "study_work": {
        "quran": [X("20:114", frm='and say, "My Lord, increase me in knowledge', ar=(13,None)), "53:39", X("65:2-3", frm="And whoever fears Allah", ar=(24,None)), X("3:159", frm="and consult them in the matter", ar=(18,None)),
                  X("13:11", frm="Indeed, Allah will not change", to="what is in themselves.", ar=(11,20)), "94:7-8", "11:88"],
        "hadith": [("bukhari", 6225, "most regular and constant"), ("muslim", 13886, "seek help from Allah")],
    },
    "failure": {
        "quran": [X("2:216", frm="But perhaps you hate", ar=(6,None)), "57:22-23", "3:139", "9:51", "12:87"],
        "hadith": [("muslim", 13886, "do not lose heart"), ("bukhari", 5431, "afflicts him with trials")],
    },
    "provision": {
        "quran": [X("65:2-3", frm="And whoever fears Allah", ar=(24,None)), "11:6", "29:60", "51:22", "65:7", "2:268"],
        "hadith": [("bukhari", 1992, "expansion in his sustenance"), ("bukhari", 1419, "Allah will make him patient")],
    },
    "illness": {
        "quran": ["26:80", "21:83-84", "10:57", "2:155-156", "94:5-6"],
        "hadith": [("bukhari", 5428, "nor sorrow, nor sadness"), ("bukhari", 5464, "also has created its treatment")],
    },
    "fear_trust": {
        "quran": ["3:173", X("65:2-3", frm="And whoever fears Allah", ar=(24,None)), X("3:159", frm="and consult them in the matter", ar=(18,None)), "9:51", "14:12", "10:62", "41:30"],
        "hadith": [("bukhari", 4357, "Best Disposer"), ("bukhari", 3497, "the third of whom is Allah")],
    },
    "weak_faith": {
        "quran": [X("57:16", to="of the truth?", ar=(0,12)), "2:186", "29:69", "4:28", "7:201", "3:8"],
        "hadith": [("bukhari", 39, "Religion is very easy"), ("bukhari", 6225, "most regular and constant")],
    },
    "family": {
        "quran": ["17:23-24", "30:21", "49:10", "42:40", "24:22"],
        "hadith": [("bukhari", 5769, "not merciful to others"), ("bukhari", 5763, "keeps good relations")],
    },
    "injustice": {
        "quran": ["42:41-43", "14:42", "3:120", "40:44", "41:34-35"],
        "hadith": [("bukhari", 4480, "gives respite to the oppressor"), ("bukhari", 2346, "hand him over to an oppressor")],
    },
    "dua": {
        "quran": ["2:186", X("40:60", to='I will respond to you."', ar=(0,4)), "7:55", "27:62", "21:87", "2:201"],
        "hadith": [("bukhari", 6103, "does not show impatience"), ("bukhari", 7209, "last third of the night")],
    },
    "overwhelmed": {
        "quran": ["2:286", "94:1-8", X("2:185", frm="Allah intends for you ease", to="hardship", ar=(27,34)), "20:25-28"],
        "hadith": [("bukhari", 1897, "Your Lord has a right on you"), ("bukhari", 6132, "worry and grief")],
    },
    "self_worth": {
        "quran": ["95:4", "17:70", "49:13", "93:5", "2:286"],
        "hadith": [("muslim", 13659, "does not look to your faces and your wealth")],
    },
    "decisions": {
        "quran": [X("3:159", frm="and consult them in the matter", ar=(18,None)), X("2:216", frm="But perhaps you hate", ar=(6,None)), "11:88", "1:5-6"],
        "hadith": [("bukhari", 1132, "Istikhara"), ("muslim", 13886, "seek help from Allah")],
    },
    "guidance": {
        "quran": ["1:5-6", "93:7", "51:56", "29:69", "13:28"],
        "hadith": [("bukhari", 71, "comprehend the religion", "comprehend the religion.")],
    },
}


# =====================================================================================================
# EXTENSION v2 -- added for the owner's 12 feeling categories (see userfeelings.py)
# Same rules as above: references only; every hadith has an assertion phrase; excerpts cut at explicit
# boundaries (English phrase + Arabic word indices, both checked at build time).
# =====================================================================================================

# --- more content for themes that already existed -------------------------------------------------
REFS["anxiety"]["quran"] += ["64:11"]
REFS["fear_trust"]["quran"] += [X("12:64", frm="But Allah is the best guardian", ar=(11, 16)), "64:11"]
REFS["weak_faith"]["quran"] += ["93:3"]
REFS["gratitude"]["quran"] += ["10:58"]
REFS["gratitude"]["hadith"] += [("bukhari", 1097, "thankful slave")]
REFS["anger"]["quran"] += [X("15:85", frm="so forgive with gracious forgiveness.", ar=(11, 13)), "12:92"]
REFS["anger"]["hadith"].insert(0, ("bukhari", 3147, "I know a word"))        # the Prophet's practical remedy first
REFS["guilt"]["quran"] += [X("2:222", frm="Indeed, Allah loves those who are constantly repentant", ar=(21, 26)), "5:39"]
REFS["guilt"]["hadith"] += [("bukhari", 6069, "most superior way of asking for forgiveness")]

# --- new themes ------------------------------------------------------------------------------------
REFS.update({
    "overthinking": {
        "quran": ["13:28", "57:22-23", "64:11", "9:51", "2:286", "94:5-6", X("2:216", frm="But perhaps you hate", ar=(6, None))],
        "hadith": [("bukhari", 5060, "evil thoughts", 'uttered."'), ("bukhari", 6132, "worry and grief"),
                   ("muslim", 13886, "do not lose heart")],
    },
    "self_forgiveness": {
        "quran": ["28:16", "39:53", "12:92", X("11:114", frm="Indeed, good deeds do away with misdeeds", to="do away with misdeeds.", ar=(7, 10)),
                  "7:23", "3:135-136"],
        "hadith": [("bukhari", 6072, "more pleased with the repentance"), ("muslim", 14071, "seek forgiveness from Allah")],
    },
    "betrayal": {
        "quran": ["12:18", X("39:36", to="(ﷺ)]?", ar=(0, 3)), "16:127", "12:86", "93:3", "40:44",
                  X("2:216", frm="But perhaps you hate", ar=(6, None))],
        "hadith": [("bukhari", 5901, "stung twice"), ("bukhari", 5431, "afflicts him with trials"),
                   ("bukhari", 7123, "I am just as My slave thinks I am")],
    },
    "love_relationship": {
        "quran": [X("2:216", frm="But perhaps you hate", ar=(6, None)), "30:21", "25:74", "94:5-6", "57:22-23", "2:186",
                  X("2:165", frm="But those who believe are stronger in love for Allah.", to="stronger in love for Allah.", ar=(11, 15))],
        "hadith": [("muslim", 13886, "do not lose heart"), ("bukhari", 1132, "Istikhara"), ("bukhari", 1837, "can afford to marry")],
    },
    "motivation": {
        "quran": ["18:30", "11:115", X("3:195", frm="Never will I allow", to="you are of one another.", ar=(3, 15)),
                  "94:7-8", "29:69", "94:5-6", "2:286"],
        "hadith": [("bukhari", 6225, "most regular and constant"), ("bukhari", 39, "Religion is very easy"),
                   ("muslim", 13886, "seek help from Allah")],
    },
    "why_trials": {
        "quran": ["29:2-3", "2:155-157", "2:214", "67:2", X("21:35", frm="And We test you with evil and with good as trial", ar=(4, 9)),
                  "64:11", "57:22-23"],
        "hadith": [("bukhari", 5431, "afflicts him with trials"), ("bukhari", 5428, "nor sorrow, nor sadness"),
                   ("muslim", 14591, "good in every affair")],
    },
})
