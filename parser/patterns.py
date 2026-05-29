PATTERNS = {

    "debout": [
               
        r"[vV]?08",                 # v08, 08
        r"[vV]?epl",                # epl, vpl
        r"[vV]?ome",                # ome
        r"debou?t"
    ],

    "retract": [
        r"[vV]?r.?tract\w*",        # retract, rtract, r.tract…
        r"[vV]?lat\.?ra\w*",        # lat.ra / latra
        r"chariot\w*\s*[\w\s]*assis"
        
    ],

    "frontal": [
        r"[vV]?fronta\w*",          # frontal / frontale
        r"chariot\w*\s*[\w\s]*assis",
        r"marche\s*arr?i?[eè]r?e",
        r"en\s*marche\s*arr?i?[eè]r?e",
        r"recul\w*"

    ],

    "tous": [
        r"pas de conduite(?!.*(frontal|retract|debout))",
        r"sans conduite",
        r"pas de conduite de chariot automoteur port\w",
        r"ponctuel\w*",
        r"exceptionnel\w*",
        r"contre.?indication.*conduite"
    ],

    "limitation": [
        r"\d+\s*h",
        r"\d+\s*%",
        r"limite\w*",
        r"max\w*",
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
