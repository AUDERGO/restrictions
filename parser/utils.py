import re

def normalize(text):
    text = str(text).lower()

    replacements = {
        "é": "e", "è": "e", "ê": "e",
        "à": "a", "ù": "u", "ô": "o"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def split_phrases(text):
    return re.split(r"[.\n]", text)
