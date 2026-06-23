PATTERNS = {

    # -------------------------
    # ENGINS
    # -------------------------
    "engin_debout": [
        r"[vV]08",
        r"epl",
        r"ome",
        r"debou?t",
        r"position\s*debou?t"
    ],

    "engin_frontal": [
        r"[vV]?fronta\w*",          
        r"chariot\w*\s*[\w\s]*assis",
        r"marche\s*arr?i?[eè]r?e",
        r"en\s*marche\s*arr?i?[eè]r?e",
        r"recul\w*"
        
    ],

    "engin_retract": [
        r"[vV]?r.?tract\w*",        
        r"[vV]?lat\.?ra\w*",      
        r"chariot\w*\s*[\w\s]*assis"
    ],
 

    "engin_tous": [
        r"pas de conduite(?!.*(frontal|retract|debout))",
        r"pas de conduite de chariot automoteur port\w",
        r"sans conduite de chariot automoteur port\w",
        r"exceptionnel\w*",
        r"occasionnel\w*",
        r"ponctuel\w*",
        r"reste\s*ponctuel",
        r"doit\s*rester\s*exceptionnel",
        r"contre.?indication.*conduite"
    ],

    "limitation_temps_conduite": [
        r"\d+\s*h",
        r"\d+\s*heures?",
        r"\b\d+h\b",
        r"max\w*",
        r"maximum",
        r"semaine\s+avec",
        r"semaine\s+sans"
       
    
    ],

    # -------------------------
    # CHARGES
    # -------------------------
    "charge": [
        r"port de charges?",
        r"manutention",
        r"charges? lourdes?",
        r"\d+\s*kg",
        r"kg",
        r"lourd\w*",
        r"pas de port de charges?",
        r"eviction du port de charges?",
        r"contre.?indication.*charges?"
    ],
    

    # -------------------------
    # ÉPAULES
    # -------------------------
    "epaule": [
        r"epaule",
        r"epaules",
        r"bras en elevation",
        r"au dessus des epaules",
        r"bras au dessus",
        r"coude",
        r"bras"
    ],

    # -------------------------
    # DOS / RACHIS
    # -------------------------
    "dos": [
        r"rachis",
        r"\bdos\b",
        r"tronc",
        r"flexion",
        r"torsion",
        r"ant[eé]flexion",
        r"rotation",
        r"pench\w*\s*(en\s*avant)?"
    ],

    # -------------------------
    # CERVICALES
    # -------------------------
    "cervicales": [
        r"cervical",
        r"\bcou\b",
        r"nuque"
    ],

    # -------------------------
    # MEMBRES INF
    # -------------------------
    "membres_inf": [
        r"station\s*debou?t",
        r"marche",
        r"accroup",
        r"genou",
        r"agenouille",
        r"squat",
        r"position",
        r"alternance",
        r"assis",
        r"debou?t"
    ],

    # -------------------------
    # POIGNET
    # -------------------------
    "poignet": [
        r"poignet",
        r"pronosupination",
        r"\bmain\b"
    ],

    # -------------------------
    # REPETITIF
    # -------------------------
    "repetitif": [
        r"repet",
        r"gestes repet",
        r"mouvements repet"
    ],

    # -------------------------
    # HORAIRE
    # -------------------------
    "horaire": [
        r"mi[-\s]?temps",
        r"temps\s*partiel",
        r"demi[-\s]?journee",
        r"demi[-\s]?session\w",
        r"horaire",
        r"travail de nuit",
        r"2\*8",
        r"temps\s*de\s*travail\s*a?\s*\d+\s*%",
        r"\d+\s*%\s*du\s*temps",
        r"semaine\s+avec",
        r"semaine\s+sans",
        r"mtt"
    ],

    # -------------------------
    # NEGATION
    # -------------------------
    "negation": [
        r"\bpas\b",
        r"contre",
        r"interdit",
        r"eviter",
        r"proscrit"
    ],

    # -------------------------
    # AUTORISATION
    # -------------------------
    "autorisation": [
        r"autorise\w*",
        r"apte\w*",
        r"validation",
        r"valide",
        r"possible",
        r"peut\s+conduire",
        r"peut\s+reprendre"
    ]
}
