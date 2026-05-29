PATTERNS = {

    "debout": [
        r"v?0?8",
        r"debou?t",
        r"epl",
        r"ome"
    ],

    "retract": [
        r"retrac\w*",         # ✅ couvre retract, retractable, retrac...
    ],

    "frontal": [
        r"fronta\w*",         # ✅ couvre frontal, frontale
    ],

    "tous": [
        r"pas de conduite(?!.*(frontal|retract|debout))",
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
