import sys
import os
import streamlit as st
import pandas as pd

# Ajoute le dossier racine du projet au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =============================
# CONFIG APP
# =============================
st.set_page_config(page_title="Parser Restrictions", layout="wide")

st.title("Analyse des restrictions médicales")

# =============================
# IMPORT DES MODULES
# =============================
try:
    from parser.parser_hybrid import analyser_restriction
    from parser.parser_rules import debug_phrase
except Exception as e:
    st.error(f"Erreur import modules : {e}")
    st.stop()

# =============================
# SECTION : UPLOAD EXCEL
# =============================
st.header("📂 Traitement fichier Excel")

uploaded_file = st.file_uploader(
    "Charge ton fichier Excel",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Fichier chargé")

    st.write("Colonnes détectées :")
    st.write(df.columns.tolist())

    # Sélection colonne
    text_col = st.selectbox(
        "Choisir la colonne contenant le texte",
        df.columns
    )

    if st.button("🚀 Lancer l'extraction"):
        with st.spinner("Traitement en cours..."):

            df_result = df[text_col].apply(analyser_restriction).apply(pd.Series)
            df_final = pd.concat([df, df_result], axis=1)

            st.success("✅ Extraction terminée")

            st.dataframe(df_final.head())

            # Export
            output_file = "resultat_parser.xlsx"
            df_final.to_excel(output_file, index=False)

            with open(output_file, "rb") as f:
                st.download_button(
                    "📥 Télécharger le fichier résultat",
                    f,
                    file_name=output_file
                )

# =============================
# SECTION DEBUG (IMPORTANT)
# =============================
st.header("🧪 Mode DEBUG")

df_result = pd.DataFrame([result])
st.dataframe(df_result, use_container_width=True)


debug_input = st.text_area(
    "Saisir un texte à analyser",
    height=200
)

if st.button("🔎 Lancer DEBUG"):
    if debug_input.strip() == "":
        st.warning("⚠️ Merci de saisir un texte avant de lancer le debug")
    else:
        try:
            result = analyser_restriction(debug_input)

            if isinstance(result, dict):
                df_result = pd.DataFrame([result]).T.reset_index()
                df_result.columns = ["Variable", "Valeur"]

                st.dataframe(df_result, use_container_width=True)
            else:
                st.write(result)

        except Exception as e:
            st.error(f"Erreur : {e}")

