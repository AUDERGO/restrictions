import re
from .patterns import PATTERNS
from .utils import normalize, split_phrases

def is_hors_perimetre(text):
    mots_exclusion = [
        "covid", "sanitaire", "masque", "distanciation",
        "lavage des mains", "desinfection", "sars", "virus"
    ]
    text = text.lower()
    return any(mot in text for mot in mots_exclusion)

def match_any(patterns, text):
    return any(re.search(p, text) for p in patterns)

def is_restriction(phrase):
    mots = [
       "pas", "contre", "eviter", "limite",
        "interdit", "sans", "reduction"
    ]
    return any(m in phrase for m in mots)

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


def analyser_restriction_rules(text):
    text = normalize(text)

    # -------------------------
    # 1. HORS PERIMETRE
    # -------------------------
    if is_hors_perimetre(text):
        return {k: 0 for k in [
            "engin_debout","engin_frontal","engin_retract","engin_tous",
            "limitation_temps_conduite","Engin","charge","posture",
            "epaule","dos","cervicales","membres_inf","poignet","repetitif",
            "horaire","total"
        ]}

    phrases = split_phrases(text)

    res = {k: 0 for k in [
         "engin_debout","engin_frontal","engin_retract","engin_tous",
        "limitation_temps_conduite","Engin","charge","posture",
        "epaule","dos","cervicales","membres_inf","poignet","repetitif",
        "horaire","total"
    ]}


    # -------------------------
    # 2. ANALYSE PAR PHRASE
    # -------------------------
    for phrase in phrases:

        phrase = phrase.strip()

        has_neg = match_any(PATTERNS["negation"], phrase)
        has_autorisation = match_any(PATTERNS["autorisation"], phrase)
        has_restriction = is_restriction(phrase)

        # REGLE CLE
        is_contrainte = (has_neg or has_restriction) and not has_autorisation


        # -------------------------
        # 3. ENGINS
        # -------------------------
        autorisation_engin_debout = False
        autorisation_engin_frontal = False
        autorisation_engin_retract = False

        engin_present = (
            match_any(PATTERNS["engin_frontal"], phrase) or
            match_any(PATTERNS["engin_retract"], phrase) or
            match_any(PATTERNS["engin_debout"], phrase) or
            match_any(PATTERNS["engin_tous"], phrase)
        )

        if match_any(PATTERNS["engin_frontal"], phrase):
            if has_autorisation:
                autorisation_engin_frontal = True
            elif is_contrainte and not autorisation_engin_frontal:
                res["engin_frontal"] = 1
              

        if match_any(PATTERNS["engin_retract"], phrase):
            if has_autorisation:
                autorisation_engin_retract = True
            elif is_contrainte and not autorisation_engin_retract:
                res["engin_retract"] = 1

        if match_any(PATTERNS["engin_debout"], phrase):
            if has_autorisation:
                autorisation_engin_debout = True
            elif is_contrainte and not autorisation_engin_debout:
                res["engin_debout"] = 1


        if match_any(PATTERNS["engin_tous"], phrase):
            if is_contrainte:
                res["engin_tous"] = 1

        # limitation seulement si engin ET contrainte
        if engin_present and match_any(PATTERNS["limitation_temps_conduite"], phrase):
            if is_contrainte:
                res["limitation_temps_conduite"] = 1



        # -------------------------
        # 4. CHARGE
        # -------------------------

        if match_any(PATTERNS["charge"], phrase):
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["charge"] = 1
                
        # -------------------------
        # 5. POSTURE DETAIL
        # -------------------------
                
        if match_any(PATTERNS["epaule"], phrase):
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["epaule"] = 1

        if match_any(PATTERNS["dos"], phrase):
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["dos"] = 1

        if match_any(PATTERNS["cervicales"], phrase):
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["cervicales"] = 1

        if match_any(PATTERNS["membres_inf"], phrase): 
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["membres_inf"] = 1

        if match_any(PATTERNS["poignet"], phrase):
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["poignet"] = 1

        if match_any(PATTERNS["repetitif"], phrase):
            if (has_neg or is_restriction(phrase)) and not has_autorisation:
                res["repetitif"] = 1

        
        # -------------------------
        # 6. HORAIRE
        # -------------------------
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

    # Posture globale
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
    
