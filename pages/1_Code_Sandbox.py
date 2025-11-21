# pages/1_Code_Sandbox.py

import streamlit as st
import os
import sys
from io import StringIO
import re
from google import genai

# --- Fonctions d'exécution de code sécurisée (pour TP) ---

def execute_user_code(code_string):
    """
    Exécute un bloc de code Python et capture le stdout.
    ATTENTION: Cette méthode exécute le code localement. Non recommandée pour la production web.
    """
    if not code_string.strip():
        return None, "Erreur: Le bloc de code est vide."
    
    try:
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        
        # Utiliser un dictionnaire local pour l'exécution pour isoler l'environnement
        local_scope = {}
        exec(code_string, {}, local_scope)
        
        sys.stdout = old_stdout
        
        return redirected_output.getvalue(), None
        
    except Exception as e:
        sys.stdout = old_stdout # Rétablir la sortie standard même en cas d'erreur
        return None, f"{type(e).__name__}: {e}"

# --- Interface Streamlit pour le Sandbox ---

st.set_page_config(
    page_title="Code Sandbox",
    page_icon="🔬",
    layout="wide"
)
# Style CSS pour centrer la page
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Tenter de récupérer l'objet chat de la page principale si elle existe
chat_session = st.session_state.get("chat")

st.title("Code Sandbox : Tester votre code Python")
# st.subheader("Page 2/2 : Environnement d'Exécution")
st.markdown("---")

## Instructions pour l'Étudiant
st.info(
    """
    **Objectif de la Sandbox :** Tester les exemples de code donnés par AtlasTutor (ou votre propre code) en toute sécurité.
    
    ### Instructions d'Utilisation
    1.  Collez le code Python que vous souhaitez exécuter dans la zone de texte ci-dessous (sans les balises \`\`\`python).
    2.  Cliquez sur le bouton **"▶ Exécuter le Code"**.
    3.  Le résultat (sortie `print()`) ou l'erreur sera affiché ci-dessous.
    
    **Astuce :** Une fois le code exécuté, retournez à la page **AtlasTutor** pour lui demander d'analyser le résultat ou l'erreur !
    """
)
st.markdown("---")

# 1. Zone de saisie pour le code
code_input = st.text_area(
    "Code Python à Exécuter",
    height=300,
    key="sandbox_code_input",
    value="""# Écrivez votre code ici !
x = 10
y = 5
print(f"La somme de x et y est : {x + y}")"""
)

# 2. Bouton d'exécution
if st.button("▶ Exécuter le Code", type="primary"):
    
    # Exécution du code
    output, error = execute_user_code(code_input)

    st.markdown("### Résultat de l'Exécution")
    
    # Affichage du résultat ou de l'erreur
    if error:
        st.error(f"Erreur d'exécution : {error}")
        execution_result = f"Erreur d'exécution: {error}"
    else:
        st.success("Exécution réussie. Sortie :")
        st.code(output, language='text')
        execution_result = f"Sortie du code: {output}"