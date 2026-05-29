import re
from .patterns import PATTERNS
from .utils import normalize, split_phrases


def match_any(patterns, text):
    return any(re.search(p, text) for p in patterns)


def analyser_restriction_rules(text):

    text = normalize(text)
    phrases = split_phrases(text)

    res = {
        "debout": 0,
        "retract": 0,
        "frontal": 0,
        "tous": 0,
        "limitation": 0,
        "engin": 0
    }

   for phrase in phrases:
    phrase = phrase.strip()

    has_neg = match_any(PATTERNS["negation"], phrase)

    # -------------------------
    # 1. DETECTION PAR TYPES (PRIORITAIRE)
    # -------------------------
    found_type = False

    if match_any(PATTERNS["frontal"], phrase):
        if has_neg:
            res["frontal"] = 1
            res["engin"] = 1
        found_type = True

    if match_any(PATTERNS["retract"], phrase):
        if has_neg:
            res["retract"] = 1
            res["engin"] = 1
        found_type = True

    if match_any(PATTERNS["debout"], phrase):
        if has_neg:
            res["debout"] = 1
            res["engin"] = 1
        found_type = True

    # -------------------------
    # 2. BLOCAGE GLOBAL (SEULEMENT SI AUCUN TYPE)
    # -------------------------
    if not found_type and match_any(PATTERNS["tous"], phrase):
        res["tous"] = 1
        res["engin"] = 1

    # -------------------------
    # 3. LIMITATION
    # -------------------------
    if match_any(PATTERNS["limitation"], phrase):
        
  return res
