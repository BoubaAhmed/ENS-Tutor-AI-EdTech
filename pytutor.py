import streamlit as st
import os
from google import genai
from google.genai import types

# Configuration de la page Streamlit
st.set_page_config(
    page_title="PyTutor - Votre Tuteur Python",
    page_icon="🚀",
    layout="centered"
)

# --- 1. CONFIGURATION ET CLÉ API ---
@st.cache_resource
def init_client():
    """Initialise le client Gemini une seule fois"""
    try:
        client = genai.Client()
        return client
    except Exception as e:
        st.error(f"ERREUR: Impossible d'initialiser le client Gemini. Détail: {e}")
        return None

# --- 2. LE SYSTEM PROMPT (Le Cerveau du Tuteur) ---
SYSTEM_PROMPT_PYTUTOR = """
Tu es **PyTutor**, un tuteur virtuel hautement qualifié, patient et **dynamique**, spécialisé dans l'enseignement des concepts de base de la programmation en Python.

**NIVEAU CIBLE :** Tes explications doivent être parfaitement adaptées aux **élèves du lycée**. Cela signifie :
* Utiliser un langage **clair, simple et concret**.
* Privilégier les **analogies** basées sur des situations quotidiennes, les jeux vidéo, ou la logique simple.
* Être **motivateur** et dédramatiser les erreurs de code.

**CONCEPTEUR ET CONTEXTE ACADÉMIQUE :**
Ce chatbot a été construit par **Bouba Ahmed** dans le cadre du module **Technologie Éducative à l'ENS de Meknès (Master)**. Ton objectif est de démontrer comment les chatbots basés sur l'IA peuvent servir d'outils puissants pour le tutorat au lycée.

#### RÈGLES DE CONDUITE ####
1.  **Rôle Principal :** Agir comme un mentor pour adolescents : **accessible et fun**.
2.  **Style de Réponse :** Ton **enthousiaste, clair, concis**, et toujours encourageant. Ne sois ni trop formel ni trop familier.
3.  **Formatage :** Chaque fois que tu expliques un concept de code, tu dois fournir un **exemple de code Python** dans un bloc de code (` ```python...``` `), et tu dois le commenter pour l'expliquer ligne par ligne.
4.  **Vérification de la Compréhension :** Après chaque explication majeure, pose une petite question (un mini-quiz) pour t'assurer que l'utilisateur a compris.
5.  **Focus :** Limite strictement les sujets à Python et ses librairies standard. Décline poliment toute question non pertinente.

Commence la conversation par une salutation chaleureuse et mentionne brièvement que tu as été créé par Bouba Ahmed à l'ENS de Meknès pour aider les lycéens avec Python. Ensuite, demande à l'utilisateur quel concept il souhaite apprendre aujourd'hui.
"""

# --- INITIALISATION DE L'APPLICATION ---
def init_chat_session():
    """Initialise la session de chat"""
    if "chat" not in st.session_state:
        client = init_client()
        if client:
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT_PYTUTOR,
            )
            st.session_state.chat = client.chats.create(
                model="gemini-2.5-flash",
                config=config
            )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Ajouter le message de bienvenue initial
        if st.session_state.chat:
            try:
                response = st.session_state.chat.send_message("")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.text
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "Bonjour ! Je suis PyTutor, votre tuteur Python. Comment puis-je vous aider aujourd'hui ?"
                })

# --- INTERFACE STREAMLIT ---
def main():
    # En-tête de l'application
    st.title("🚀 PyTutor - Votre Tuteur Python")
    st.markdown("---")
    
    # Initialiser la session de chat
    init_chat_session()
    
    # Afficher l'historique des messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Zone de saisie utilisateur
    if st.session_state.chat:
        if prompt := st.chat_input("Posez votre question sur Python..."):
            # Ajouter le message de l'utilisateur
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Générer la réponse
            with st.chat_message("assistant"):
                with st.spinner("PyTutor réfléchit..."):
                    try:
                        response = st.session_state.chat.send_message(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response.text
                        })
                    except Exception as e:
                        error_msg = f"❌ Une erreur est survenue : {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
    else:
        st.error("❌ Le client Gemini n'a pas pu être initialisé. Vérifiez votre clé API.")
        
    # Sidebar avec informations
    with st.sidebar:
        st.header("ℹ️ À propos de PyTutor")
        st.markdown("""
        **PyTutor** est votre assistant personnel pour apprendre Python !
        
        ✨ **Fonctionnalités :**
        - Explications claires et détaillées
        - Exemples de code commentés
        - Quiz interactifs
        - Support des débutants
        
        💡 **Conseils :**
        - Posez des questions spécifiques
        - Demandez des exemples pratiques
        - N'hésitez pas à demander des clarifications
        
        🎯 **Sujets couverts :**
        - Bases de Python
        - Structures de données
        - Fonctions et classes
        - Modules standards
        - Bonnes pratiques
        """)
        
        st.markdown("---")
        if st.button("🔄 Nouvelle Conversation"):
            st.session_state.messages = []
            st.session_state.pop("chat", None)
            init_chat_session()
            st.rerun()

if __name__ == "__main__":
    main()