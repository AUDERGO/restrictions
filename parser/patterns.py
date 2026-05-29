PATTERNS = {

    # -------------------------
    # ENGINS
    # -------------------------
    "engin_debout": [
        r"v?0?8",
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
        r"sans conduite",
        r"pas de conduite de chariot automoteur port\w",
        r"exceptionnel\w*",
        r"\ r"occasionnel\w*",
        r"ponctuel\w*",
        r"\d+\s*%",
        r"reste\s*ponctuel",
        r"doit\s*rester\s*exceptionnel",
        r"contre.?indication.*conduite"
    ],

    "limitation_temps_conduite": [
        r"\d+\s*h",
        r"\d+\s*heures?",
        r"\d+\s*%",
        r"\b\d+h\b",
        r"max\w*",
        r"maximum",
        r"limite\w*",
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
        r"kg"
        r"pas de port de charges?",
        r"eviction du port de charges?",
        r"contre.?indication.*charges?"
    ],

    # -------------------------
    # POSTURE GLOBALE
    # -------------------------
    "posture": [
        r"posture",
        
    ],

    # -------------------------
    # ÉPAULES
    # -------------------------
    "epaule": [
        r"epaule",
        r"epaules",
        r"bras en elevation",
        r"au dessus des epaules",
        r"bras au dessus"
    ],

    # -------------------------
    # DOS / RACHIS
    # -------------------------
    "dos": [
        r"rachis",
        r"dos",
        r"tronc",
        r"flexion",
        r"torsion",
        r"ant[eé]flexion",
        r"rotation"
    ],

    # -------------------------
    # CERVICALES
    # -------------------------
    "cervicales": [
        r"cervical",
        r"cou",
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
    # POIGNET / MAIN
    # -------------------------
    "poignet": [
        r"poignet",
        r"main",
        r"pronosupination",
        r"poignee"
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
    # HORAIRE / ORGANISATION
    # -------------------------
    "horaire": [
        r"mi[-\s]?temps",
        r"temps\s*partiel",
        r"demi[-\s]?journee",
        r"horaire",
        r"travail de nuit",
        r"2\*8",
        r"alternance",
        r"semaine\s+avec",
        r"semaine\s+sans"
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
