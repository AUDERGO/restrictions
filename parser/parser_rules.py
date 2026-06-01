import re
from .patterns import PATTERNS
from .utils import normalize, split_phrases

def is_hors_perimetre(text):
    mots_exclusion = [
        "covid",
        "sanitaire",
        "masque",
        "distanciation",
        "lavage des mains",
        "desinfection",
        "sars",
        "virus"
    ]

    text = text.lower()

    return any(mot in text for mot in mots_exclusion)

def match_any(patterns, text):
    return any(re.search(p, text) for p in patterns)

def is_restriction(phrase):
    mots = [
        "pas",
        "contre",
        "eviter",
        "limite",
        "interdit",
        "sans",
        "reduction"
    ]
    return any(m in phrase for m in mots)

def analyser_restriction_rules(text):

    text = normalize(text)

    # 🚫 EXCLUSION
    if is_hors_perimetre(text):
        return {
            "engin_debout": 0,
            "engin_frontal": 0,
            "engin_retract": 0,
            "engin_tous": 0,
            "limitation_temps_conduite": 0,
            "Engin": 0,
            "charge": 0,
            "posture": 0,
            "epaule": 0,
            "dos": 0,
            "cervicales": 0,
            "membres_inf": 0,
            "poignet": 0,
            "repetitif": 0,
            "horaire": 0,
            "total": 0
        }


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
        "charge": 0,
        "posture": 0,

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
            if has_neg or is_restriction(phrase):
                res["engin_frontal"] = 1
            found_type = True

        if match_any(PATTERNS["engin_retract"], phrase):
            if has_neg or is_restriction(phrase):
                res["engin_retract"] = 1
            found_type = True

        if match_any(PATTERNS["engin_debout"], phrase):
            if has_neg or is_restriction(phrase):
                res["engin_debout"] = 1
            found_type = True

        # bloc global
        if not found_type and match_any(PATTERNS["engin_tous"], phrase):
            res["engin_tous"] = 1

        # limitation
        if match_any(PATTERNS["limitation_temps_conduite"], phrase):
            res["limitation_temps_conduite"] = 1

        
        # =========================
        # 2. CHARGES
        # =========================
        if match_any(PATTERNS["charge"], phrase):
            if is_restriction(phrase):
                res["charge"] = 1
                   

        # =========================
        # 3. POSTURE DETAIL
        # =========================

        if match_any(PATTERNS["epaule"], phrase):
            if is_restriction(phrase):
                res["epaule"] = 1

        if match_any(PATTERNS["dos"], phrase):
            if is_restriction(phrase):
                res["dos"] = 1

        if match_any(PATTERNS["cervicales"], phrase):
            if is_restriction(phrase):
                res["cervicales"] = 1

        if match_any(PATTERNS["membres_inf"], phrase):
            if is_restriction(phrase):
                res["membres_inf"] = 1

        if match_any(PATTERNS["poignet"], phrase):
            if is_restriction(phrase):
                res["poignet"] = 1

        if match_any(PATTERNS["repetitif"], phrase):
            if is_restriction(phrase):
                res["repetitif"] = 1

       

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
    res["posture"] = max(
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
        + res["charge"]
        + res["posture"]
        + res["horaire"]
    )

    return res
    
