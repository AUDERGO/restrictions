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
        r"exceptionnel\w*",
        r"\ r"occasionnel\w*",    r"\d+\s*%",
        r"reste\s*ponctuel",
        r"doit\s*rester\s*exceptionnel",
        r"contre.?indication.*conduite"
    ],

    "limitation": [
        r"\d+\s*h",
        r"\d+\s*%",
        r"\d+\s*heures?",
        r"semaine\s+avec",
        r"semaine\s+sans"
        r"\b\d+h\b",
        r"max\w*",
        r"maximum",
        r"limite\w*",
        
    ]
    
    "negation": [
        r"\bpas\b",
        r"contre",
        r"interdit",
        r"eviter"

    ],

    "autorisation": [
        r"autorise\w*",
        r"apte\w*",
        r"validation",
        r"valide",
        r"peut\s+reprendre",
        r"possible"
 ]
 
}
