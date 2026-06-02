import re
from .patterns import PATTERNS
from .utils import normalize, split_phrases


# -------------------------
# HORS PERIMETRE
# -------------------------
def is_hors_perimetre(text):
    mots_exclusion = [
        "covid", "sanitaire", "masque", "distanciation",
        "lavage des mains", "desinfection", "sars", "virus"
    ]
    text = text.lower()
    return any(mot in text for mot in mots_exclusion)


# -------------------------
# MATCH PATTERNS
# -------------------------
def match_any(patterns, text):
    return any(re.search(p, text) for p in patterns)


# -------------------------
# DETECTION RESTRICTION
# -------------------------
def is_restriction(phrase):
    mots = [
        "pas", "contre", "eviter",
        "limite", "limiter", "limitation",
        "interdit", "sans",
        "reduction", "restriction"
    ]
    return any(m in phrase for m in mots)


# -------------------------
# DEBUG (TRÈS UTILE)
# -------------------------
def debug_phrase(phrase):

    phrase = normalize(phrase)

    result = {}

    for key, patterns in PATTERNS.items():

        matches = []

        for p in patterns:
            if re.search(p, phrase):
                matches.append(p)

        if matches:
            result[key] = matches

    return result


# -------------------------
# PARSER PRINCIPAL
# -------------------------
def analyser_restriction_rules(text):

    text = normalize(text)

    # EXCLUSION
    if is_hors_perimetre(text):
        return {k: 0 for k in [
            "engin_debout","engin_frontal","engin_retract","engin_tous",
            "limitation_temps_conduite","Engin",
            "charge","posture",
            "epaule","dos","cervicales","membres_inf","poignet","repetitif",
            "horaire","total"
        ]}

    phrases = split_phrases(text)

    # -------------------------
    # INIT
    # -------------------------
    res = {k: 0 for k in [
        "engin_debout","engin_frontal","engin_retract","engin_tous",
        "limitation_temps_conduite","Engin",
        "charge","posture",
        "epaule","dos","cervicales","membres_inf","poignet","repetitif",
        "horaire","total"
    ]}

    # -------------------------
    # ANALYSE PAR PHRASE
    # -------------------------
    for phrase in phrases:

        phrase = phrase.strip()

        has_neg = match_any(PATTERNS["negation"], phrase)
        has_autorisation = match_any(PATTERNS["autorisation"], phrase)
        has_restriction = is_restriction(phrase)

        is_contrainte = (has_neg or has_restriction)


        # -------------------------
        # ENGINS
        # -------------------------

        if match_any(PATTERNS["engin_frontal"], phrase):
            if has_autorisation:
                pass
            elif is_contrainte:
                res["engin_frontal"] = 1

        if match_any(PATTERNS["engin_retract"], phrase):
            if has_autorisation:
                pass
            elif is_contrainte:
                res["engin_retract"] = 1

        if match_any(PATTERNS["engin_debout"], phrase):
            if has_autorisation:
                pass
            elif is_contrainte:
                res["engin_debout"] = 1
        
        if match_any(PATTERNS["engin_tous"], phrase):
            if is_contrainte:
                res["engin_tous"] = 1

        if match_any(PATTERNS["limitation_temps_conduite"], phrase):

            if match_any(PATTERNS["engin_frontal"], phrase) or \
               match_any(PATTERNS["engin_retract"], phrase) or \
               match_any(PATTERNS["engin_debout"], phrase) or \
               match_any(PATTERNS["engin_tous"], phrase):

                if is_contrainte:
                    res["limitation_temps_conduite"] = 1

        # -------------------------
        # CHARGE
        # -------------------------
        if match_any(PATTERNS["charge"], phrase):
            if has_neg or has_restriction:
                res["charge"] = 1
            elif match_any([r"lourd\w*", r"\d+\s*kg"], phrase):
                res["charge"] = 1

        # -------------------------
        # POSTURE DETAIL
        # -------------------------
        if match_any(PATTERNS["epaule"], phrase):
            if has_neg or has_restriction:
                res["epaule"] = 1

        if match_any(PATTERNS["dos"], phrase):
            if has_neg or has_restriction:
                res["dos"] = 1

        if match_any(PATTERNS["cervicales"], phrase):
            if has_neg or has_restriction:
                res["cervicales"] = 1

        if match_any(PATTERNS["membres_inf"], phrase):
            if is_contrainte:
                res["membres_inf"] = 1
            elif "alternance" in phrase:
                 res["membres_inf"] = 1

        if match_any(PATTERNS["poignet"], phrase):
            if has_neg or has_restriction:
                res["poignet"] = 1

        if match_any(PATTERNS["repetitif"], phrase):
            if has_neg or has_restriction:
                res["repetitif"] = 1

        # -------------------------
        # HORAIRE
        # -------------------------
        if match_any(PATTERNS["horaire"], phrase):
            res["horaire"] = 1


    # -------------------------
    # AGREGATION
    # -------------------------

    if res["membres_inf"] == 1:
        res["engin_debout"] = 1

    
    # ✅ Engin global
    res["Engin"] = max(
        res["engin_debout"],
        res["engin_frontal"],
        res["engin_retract"],
        res["engin_tous"],
        res["limitation_temps_conduite"]
    )

    # ✅ Posture globale
    res["posture"] = max(
        res["epaule"],
        res["dos"],
        res["cervicales"],
        res["membres_inf"],
        res["poignet"],
        res["repetitif"]
    )

    # ✅ Score total
    res["total"] = (
        res["Engin"]
        + res["charge"]
        + res["posture"]
        + res["horaire"]
    )

    return res
