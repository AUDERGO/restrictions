PATTERNS = {

    "debout": [
        r"[v]?0?8",
        r"[v]?e?p[l1]",
        r"[o0]?m[e3]",
        r"debou?t",
        r"chariot\w*\s*\w*debou?t"
    ],

    "retract": [
        r"r[ée]?trac?t\w*",
        r"chariot\w*\s*\w*retract"
    ],

    "frontal": [
        r"frontal\w*",
        r"chariot\w*\s*\w*assis"
    ],

    "tous": [
        r"pas de conduite",
        r"sans conduite",
        r"contre.?indication.*conduite"
    ],

    "limitation": [
        r"\d+\s*h",
        r"\d+\s*%",
        r"limite\w*",
        r"max\w*",
        r"ponctuel\w*",
        r"exceptionnel\w*"
    ],

    "negation": [
        r"pas",
        r"contre",
        r"eviter",
        r"interdit"
    ],

    "autorisation": [
        r"autorise\w*",
        r"apte\w*",
        r"possible",
        r"peut\s+conduire"
    ]
}
