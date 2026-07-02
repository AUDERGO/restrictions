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
        "pas de", "eviter", "contre indication",
        "limite", "limiter", "limitation",
        "interdit", "sans", "contre-indication",
        "reduction", "restriction",
        "eviction", "exclusion", "proscrit"
    ]
    
    return any(m in phrase for m in mots)

# -------------------------
# RESTRICTION FORTE ENGIN
# -------------------------
def is_restriction_engin(phrase):

    mots = [
        "pas de",
        "sans",
        "interdit",
        "contre indication",
        "contre-indication",
        "eviction",
        "exclusion",
        "exceptionnel",
        "occasionnel",
        "ponctuel",
        "doit rester exceptionnelle",
        "doit rester exceptionnel"
    ]

    phrase = phrase.lower()

    return any(mot in phrase for mot in mots)


# -------------------------
# DEBUG
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
def analyser_restriction_rules(text, aptitude=None):

    text = normalize(text)

    # ✅ FILTRE APTE
    if aptitude and aptitude.strip().lower() == "apte":
        return {
            "engin_debout": 0,
            "engin_frontal": 0,
            "engin_retract": 0,
            "engin_tous": 0,
            "limitation_temps_conduite": 0,
            "Engin": 0,
            "charge": 0,
            "poids": None,
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

    # ✅ EXCLUSION
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
    colonnes = [
        "engin_debout","engin_frontal","engin_retract","engin_tous",
        "limitation_temps_conduite","Engin",
        "charge","poids","posture",
        "epaule","dos","cervicales","membres_inf","poignet","repetitif",
        "horaire","total"
    ]

    res = {col: (None if col == "poids" else 0) for col in colonnes}

    # -------------------------
    # ANALYSE
    # -------------------------
    for phrase in phrases:

        phrase = phrase.strip()

        # découpe fine
        sous_phrases = re.split(r"[.\n,;:]|(?<=\s)-\s", phrase)

        for sp in sous_phrases:

            sp = sp.strip()
            
            # ETAPE 1 : filtrer faux positifs
            if "pas de contre indication" in sp or "pas de contre-indication" in sp:
                continue

            has_neg_sp = match_any(PATTERNS["negation"], sp)
            has_autorisation_sp = match_any(PATTERNS["autorisation"], sp)
            has_restriction_sp = is_restriction(sp)

            # ETAPE 2 : calcul vraie contrainte
            is_contrainte_sp = has_restriction_sp or has_neg_sp

            is_restriction_engin_sp = is_restriction_engin(sp)

            is_limitation_temps = match_any(
                PATTERNS["limitation_temps_conduite"],
                sp
            )


            # -------------------------
            # ENGINS SPECIFIQUES
            # -------------------------
            engin_map = {
                "engin_frontal": PATTERNS["engin_frontal"],
                "engin_retract": PATTERNS["engin_retract"],
                "engin_debout": PATTERNS["engin_debout"],
            }

            for nom_engin, patterns_engin in engin_map.items():
                if match_any(patterns_engin, sp):
                    if is_limitation_temps:
                        continue
                    if is_restriction_engin_sp:
                        res[nom_engin] = 1   
                        
            """
            for nom_engin, patterns_engin in engin_map.items():
                if match_any(patterns_engin, sp):
                    if is_limitation_temps:
                        continue
                    if is_contrainte_sp:
                        res[nom_engin] = 1
            """

            
            # -------------------------
            # ENGINS GLOBAL
            # -------------------------
            if match_any(PATTERNS["engin_tous"], sp):
                if not is_limitation_temps and is_restriction_engin_sp:
                    res["engin_tous"] = 1
                    res["Engin"] = 1

            """
            if match_any(PATTERNS["engin_tous"], sp):
                if is_interdiction_engin_sp:
                    res["engin_tous"] = 1
                    res["Engin"] = 1      
    

            if match_any(PATTERNS["engin_tous"], sp):
                if not is_limitation_temps and is_contrainte_sp:
                    res["engin_tous"] = 1
                    res["Engin"] = 1
            """


            # -------------------------
            # LIMITATION TEMPS ENGINS
            # -------------------------
            if match_any(PATTERNS["limitation_temps_conduite"], sp):
                res["limitation_temps_conduite"] = 1
                res["Engin"] = 1   # une limitation implique Engin


            # -------------------------
            # CHARGE + POIDS
            # -------------------------

            # EXTRACTION POIDS (prioritaire et indépendante)
            match_poids = re.search(r"(\d+)\s*(kg|kilo\w*|kilogramm\w*)", sp)

            if match_poids:
                poids_valeur = int(match_poids.group(1))

                #  toujours prendre la valeur la plus restrictive (minimum)
                res["poids"] = poids_valeur if res["poids"] is None else min(res["poids"], poids_valeur)

                # poids implique automatiquement une contrainte
                res["charge"] = max(res["charge"], 1)

            # DETECTION CHARGE (sans poids)
            if match_any(PATTERNS["charge"], sp):

                # cas restriction explicite
                if is_contrainte_sp:
                    res["charge"] = max(res["charge"], 1)

                # cas implicite (charges lourdes sans "pas")
                elif re.search(r"charge\w*\s*lourd", sp):
                    res["charge"] = max(res["charge"], 1)

            """
            # -------------------------
            # CHARGE
            # -------------------------

            if match_any(PATTERNS["charge"], sp):
                if is_contrainte_sp:
                    res["charge"] = 1
                elif re.search(r"\d+\s*kg", sp):
                    res["charge"] = 1

            # -------------------------
            # POIDS
            # -------------------------
            match_poids = re.search(r"(\d+)\s*(kg|kilo\w*)", sp)
            if match_poids:
                poids_valeur = int(match_poids.group(1))
                res["poids"] = poids_valeur if res["poids"] is None else min(res["poids"], poids_valeur)
            """

            # -------------------------
            # POSTURE
            # -------------------------
            if match_any(PATTERNS["epaule"], sp) and is_contrainte_sp:
                res["epaule"] = 1

            if match_any(PATTERNS["dos"], sp) and is_contrainte_sp:
                res["dos"] = 1

            if match_any(PATTERNS["cervicales"], sp) and is_contrainte_sp:
                res["cervicales"] = 1

            if match_any(PATTERNS["membres_inf"], sp):
                if is_contrainte_sp or re.search(r"altern\w*", sp):
                    res["membres_inf"] = 1

            if match_any(PATTERNS["poignet"], sp) and is_contrainte_sp:
                res["poignet"] = 1

            if match_any(PATTERNS["repetitif"], sp) and is_contrainte_sp:
                res["repetitif"] = 1

            # -------------------------
            # HORAIRE
            # -------------------------
            if match_any(PATTERNS["horaire"], sp):
                res["horaire"] = max(res["horaire"], 1)

    # -------------------------
    # AGREGATION
    # -------------------------
    if res["membres_inf"] == 1:
        res["engin_debout"] = 1

    res["Engin"] = max(
        res["engin_debout"],
        res["engin_frontal"],
        res["engin_retract"],
        res["engin_tous"],
        res["limitation_temps_conduite"]
    )

    res["posture"] = max(
        res["epaule"],
        res["dos"],
        res["cervicales"],
        res["membres_inf"],
        res["poignet"],
        res["repetitif"]
    )

    res["total"] = res["Engin"] + res["charge"] + res["posture"] + res["horaire"]

    return res
