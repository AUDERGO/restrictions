import re
from .patterns import PATTERNS
from .utils import normalize, split_phrases


def match_any(patterns, text):
    return any(re.search(p, text) for p in patterns)


def analyser_restriction_rules(text):

    text = normalize(text)
    phrases = split_phrases(text)

    res = {

        # ENGINS
        "engin_debout": 0,
        "engin_frontal": 0,
        "engin_retract": 0,
        "engin_tous": 0,
        "limitation_temps_conduite": 0,
        "Engin": 0,

        # AUTRES
        "Charge": 0,
        "Posture": 0,

        "epaule": 0,
        "dos": 0,
        "cervicales": 0,
        "membres_inf": 0,
        "poignet": 0,
        "repetitif": 0,

        "horaire": 0,

        "total": 0
    }

    # -------------------------
    # ANALYSE PAR PHRASE
    # -------------------------
    for phrase in phrases:
        phrase = phrase.strip()

        has_neg = match_any(PATTERNS["negation"], phrase)

        # =========================
        # 1. ENGINS
        # =========================

        found_type = False

        if match_any(PATTERNS["engin_frontal"], phrase):
            if has_neg:
                res["engin_frontal"] = 1
            found_type = True

        if match_any(PATTERNS["engin_retract"], phrase):
            if has_neg:
                res["engin_retract"] = 1
            found_type = True

        if match_any(PATTERNS["engin_debout"], phrase):
            if has_neg:
                res["engin_debout"] = 1
            found_type = True

        # bloc global
        if not found_type and match_any(PATTERNS["engin_tous"], phrase):
            res["engin_tous"] = 1

        # limitation
        if match_any(PATTERNS["limitation_temps_conduite"], phrase):
            res["limitation_temps_conduite"] = 1

        # condition conduite
        if match_any(PATTERNS["condition_conduite"], phrase):
            res["Engin"] = 1

        # =========================
        # 2. CHARGES
        # =========================
        if match_any(PATTERNS["charge"], phrase):
            res["Charge"] = 1

        # =========================
        # 3. POSTURE DETAIL
        # =========================

        if match_any(PATTERNS["epaule"], phrase):
            res["epaule"] = 1

        if match_any(PATTERNS["dos"], phrase):
            res["dos"] = 1

        if match_any(PATTERNS["cervicales"], phrase):
            res["cervicales"] = 1

        if match_any(PATTERNS["membres_inf"], phrase):
            res["membres_inf"] = 1

        if match_any(PATTERNS["poignet"], phrase):
            res["poignet"] = 1

        if match_any(PATTERNS["repetitif"], phrase):
            res["repetitif"] = 1

        # =========================
        # 4. POSTURE GLOBAL
        # =========================
        if match_any(PATTERNS["posture"], phrase):
            res["Posture"] = 1

        # =========================
        # 5. HORAIRE
        # =========================
        if match_any(PATTERNS["horaire"], phrase):
            res["horaire"] = 1

    # -------------------------
    # AGREGATION
    # -------------------------

    # Engin global
    res["Engin"] = max(
        res["engin_debout"],
        res["engin_frontal"],
        res["engin_retract"],
        res["engin_tous"],
        res["limitation_temps_conduite"]
    )

    # Posture global
    res["Posture"] = max(
        res["Posture"],
        res["epaule"],
        res["dos"],
        res["cervicales"],
        res["membres_inf"],
        res["poignet"],
        res["repetitif"]
    )

    # Total score
    res["total"] = (
        res["Engin"]
        + res["Charge"]
        + res["Posture"]
        + res["horaire"]
    )

    return res
    
