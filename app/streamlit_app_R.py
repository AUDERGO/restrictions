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

            # Initialisation à 0 pour tout le monde
            df_result = pd.DataFrame(0, index=df.index, columns=["résultat"])
 
            # Appliquer le script seulement si ≠ APTE
            mask = df["Aptitude"] != "APTE"
            df_result.loc[mask] = df.loc[mask, text_col].apply(analyser_restriction).apply(pd.Series)
            df_final = pd.concat([df, df_result], axis=1)

            # =============================
            # NETTOYAGE DES COLONNES
            # =============================

            # Colonnes à garder
            colonnes_base = ["Manager", "Matricule", "Nom", "Date de visite", "Aptitude", "Précision"]

            # Colonnes ajoutées par le parser
            colonnes_parser = df_result.columns.tolist()

            # Liste finale
            colonnes_finales = colonnes_base + colonnes_parser

            # Garde uniquement ces colonnes
            df_final = df_final[colonnes_finales]

            # Supprimer l'heure si datetime
            df_final["Date de visite"] = pd.to_datetime(df_final["Date de visite"], errors="coerce").dt.date

            st.success("✅ Extraction terminée")

            st.dataframe(df_final, use_container_width=True)

            # =============================
            # Création du fichier à télécharger
            # =============================
        
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Nom du fichier avec date + heure
            output_file = f"resultat_parser_{timestamp}.xlsx"

            # Export
            df_final.to_excel(output_file, index=False)

            # Bouton téléchargement
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

debug_input = st.text_area(
    "Saisir un texte à analyser",
    height=200
)

if st.button("🔎 Lancer DEBUG"):
    if debug_input.strip() == "":
        st.warning("⚠️ Merci de saisir un texte avant de lancer le debug")
    else:
        try:
            # ===== 1. DEBUG PATTERNS =====
            st.subheader("🔎 Patterns détectés")

            debug_output = debug_phrase(debug_input)

            # affichage lisible
            if isinstance(debug_output, dict):
                df_debug = pd.DataFrame(
                    [(k, ", ".join(v)) for k, v in debug_output.items()],
                    columns=["Catégorie", "Termes détectés"]
                )

                st.dataframe(df_debug, use_container_width=True)

            else:
                st.write(debug_output)

            # ===== 2. RESULTAT PARSER =====
            st.subheader("📊 Résultat parser")

            result = analyser_restriction(debug_input)

            if isinstance(result, dict):
                df_result = pd.DataFrame([result]).T.reset_index()
                df_result.columns = ["Variable", "Valeur"]

                st.dataframe(df_result, use_container_width=True)
            else:
                st.write(result)

        except Exception as e:
            st.error(f"Erreur : {e}")
