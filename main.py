from parser.parser_hybrid import analyser_restriction

tests = [
    "pas de conduite de chariot frontal ni retractable",
    "conduite autorisee 2h par jour",
    "apte a la conduite"
]

for t in tests:
    print("\n---")
    print(t)
    print(analyser_restriction(t))
