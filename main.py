import pandas as pd
from parser.parser_hybrid import analyser_restriction

# -------------------------
# 1. LECTURE EXCEL
# -------------------------
df = pd.read_excel("data/CRITERES ENGIN A TROUVER.xlsx")

# 👉 IMPORTANT : vérifier nom colonne texte
print(df.columns)

TEXT_COL = df.columns[0]  # ajuste si besoin

# -------------------------
# 2. APPLICATION PARSER
# -------------------------
df_result = df[TEXT_COL].apply(analyser_restriction).apply(pd.Series)

df_final = pd.concat([df, df_result], axis=1)

# -------------------------
# 3. EXPORT
# -------------------------
df_final.to_excel("resultat_parser.xlsx", index=False)

print("✅ Fichier généré : resultat_parser.xlsx")
