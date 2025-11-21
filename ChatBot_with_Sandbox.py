# pytutor_app.py

import streamlit as st
import os
import re # Nécessaire pour l'exécution du code si on le faisait dans le chat
from google import genai
from google.genai import types

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="ENS Tutor - Votre Tuteur Informatique",
    page_icon="🚀",
    layout="wide"
)

# --- 1. CONFIGURATION ET CLÉ API ---
@st.cache_resource
def init_client():
    """Initialise le client Gemini une seule fois"""
    try:
        client = genai.Client()
        return client
    except Exception as e:
        # Stocke l'erreur dans st.session_state
        st.session_state.client_error = f"ERREUR: Impossible d'initialiser le client Gemini. Détail: {e}"
        return None

# --- 2. LE SYSTEM PROMPT (Le Cerveau du Tuteur) ---
SYSTEM_PROMPT_ENSTUTOR = """
Tu es **ENS Tutor**, un tuteur virtuel hautement qualifié, patient et **dynamique**, spécialisé dans l'enseignement des concepts de la **Science Informatique** pour les élèves du lycée.

**DOMAINE DE MAÎTRISE :** Tu couvres tous les grands domaines de l'informatique :
* **Fondamentaux :** Bureautique, Algorithmique, Structures de données.
* **Architecture :** Architecture Matérielle (binaire, logique, etc.).
* **Réseaux :** Principes des réseaux (Internet, protocoles).
* **Programmation :** Python, ainsi que les bases de CSS, HTML et JavaScript.

**NIVEAU CIBLE :** Tes explications doivent être parfaitement adaptées aux **élèves du lycée**. Cela signifie :
* Utiliser un langage **clair, simple et concret**.
* Privilégier les **analogies** basées sur des situations quotidiennes, les jeux vidéo, ou la logique simple.
* Être **motivateur** et dédramatiser les erreurs.

**CONCEPTEUR ET CONTEXTE ACADÉMIQUE :**
Ce chatbot a été construit par **Bouba Ahmed et Lkhalidi Mohamed** dans le cadre du module **Technologie Éducative à l'ENS de Meknès (Master)**. Ton objectif est de démontrer comment les chatbots basés sur l'IA peuvent servir d'outils puissants pour le tutorat au lycée.

#### RÈGLES DE CONDUITE ####
1.  **Rôle Principal :** Agir comme un mentor pour adolescents : **accessible et fun**.
2.  **Style de Réponse :** Ton **enthousiaste, clair, concis**, et toujours encourageant. Ne sois ni trop formel ni trop familier.
3.  **Formatage & Code :**
    * Commence toujours par une explication **conceptuelle** simple.
    * Fournis des exemples de code (` ```python...``` `, ` ```html...``` `, etc.) **uniquement si le sujet le nécessite** (programmation). Commente l'exemple ligne par ligne.
4.  **Vérification de la Compréhension :** Après chaque explication majeure, pose une petite question (un mini-quiz) pour t'assurer que l'utilisateur a compris.
5.  **Gestion du Contexte :** Si la question de l'utilisateur est **ambiguë** (ex: "C'est quoi un bit?"), demande poliment une clarification pour déterminer s'il parle d'architecture matérielle, de codage, ou d'une autre notion avant de répondre.

Commence la conversation par une salutation chaleureuse, présente-toi comme **InfoTutor** et mentionne brièvement que tu as été créé par Bouba Ahmed et Lkhalidi Mohamed à l'ENS de Meknès pour aider les lycéens avec toute l'Informatique. Ensuite, demande à l'utilisateur quel concept il souhaite apprendre aujourd'hui.
"""

# Style CSS pour centrer la page
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE L'APPLICATION ---
def init_chat_session():
    """Initialise la session de chat"""
    client = init_client()

    if "chat" not in st.session_state and client:
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT_ENSTUTOR,
        )
        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash",
            config=config
        )
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Tenter d'ajouter le message de bienvenue initial (déclenché par le System Prompt)
        if "chat" in st.session_state and st.session_state.chat:
            try:
                # Envoyer un prompt vide pour forcer la salutation du System Prompt
                response = st.session_state.chat.send_message("Initialisation")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text
                })
            except Exception:
                # Message de secours si l'API échoue au premier appel
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Bonjour ! Je suis ENS Tutor, votre tuteur Informatique. Comment puis-je vous aider aujourd'hui ?"
                })


# --- INTERFACE STREAMLIT (Page 1) ---
def main():
    # En-tête de l'application
    st.title("🤖 ENS Tutor : Tuteur Conversationnel Informatique")
    st.subheader("Page 1/2 : Apprentissage et Discussion")
    
    # ⚠️ Vérification du client avant l'initialisation de session
    client = init_client()
    if not client:
        st.error(st.session_state.get('client_error', "Le client Gemini n'a pas pu être initialisé. Vérifiez votre clé API."))
        return # Arrête l'exécution si le client n'est pas prêt

    # Initialiser la session de chat
    init_chat_session()
    
    # Afficher l'historique des messages
    chat_container = st.container()
    with chat_container:

        # --- Écran d’accueil et message de bienvenue ---
        if len(st.session_state.messages) <= 1 and any("Bienvenue" in msg['content'] for msg in st.session_state.messages):
            # Afficher le message de bienvenue du bot en premier
            if st.session_state.messages:
                 with st.chat_message(st.session_state.messages[0]["role"]):
                    st.markdown(st.session_state.messages[0]["content"])

            # Ensuite afficher la boîte d'information
            st.info(
                """
                💡 **Mode d'emploi ENS Tutor :**
                
                1.  **Posez votre question** sur l'Informatique (Algorithmique, Réseaux, Programmation, etc.).
                2.  Je vous donnerai une explication claire, des **analogies concrètes** et des exemples (code, schémas, etc.).
                3.  Pour **tester votre code** (Python uniquement), utilisez la page **"Code Sandbox"** dans la barre latérale !
                """, icon="🚀"
            )

        # --- Sinon afficher la conversation complète ---
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    
    # Zone de saisie utilisateur
    if "chat" in st.session_state:
        if prompt := st.chat_input("Posez votre question sur Python..."):
            # 1. Ajouter le message de l'utilisateur
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 2. Générer la réponse
            with st.chat_message("assistant"):
                with st.spinner("ENS Tutor réfléchit..."):
                    try:
                        # Utiliser la méthode non-streaming
                        response = st.session_state.chat.send_message(prompt)
                        st.markdown(response.text)
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response.text
                        })
                    except Exception as e:
                        error_msg = f"Une erreur est survenue lors de la réponse : {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
    
    # Sidebar avec informations
    with st.sidebar:
        st.header("À propos de ENS Tutor")
        st.markdown("""
        **ENS Tutor** est un assistant pédagogique spécialisé pour les élèves de **lycée** !
        
        **Développeurs :**
        - Bouba Ahmed
        - Lkhalidi Mohamed
        
        **Contexte académique :**
        Projet développé dans le cadre du module **Technologie Éducative** à l'ENS de Meknès (Master).
        """)
        
        st.markdown("---")
        if st.button("Nouvelle Conversation 🔄"):
            # Réinitialisation propre de la session
            for key in list(st.session_state.keys()):
                if key != 'client_error': # Garder l'erreur client si elle existe
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()