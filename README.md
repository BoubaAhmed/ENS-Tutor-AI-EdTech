# 🎓 ENS-Tutor-AI-EdTech

## 🤖 Assistant Pédagogique en Science Informatique (Niveau Lycée)

Ce projet est une solution de **Technologie Éducative (EdTech)** visant à démontrer l'efficacité des agents conversationnels basés sur l'Intelligence Artificielle (Google Gemini LLM) pour le **tutorat personnalisé**.

**ENS Tutor** couvre l'intégralité du programme d'Informatique du lycée, incluant :
* **Algorithmique et Structures de données**
* **Programmation** (Python, HTML, CSS, JavaScript de base)
* **Réseaux et Internet** (Protocoles, routage)
* **Architecture Matérielle** (Binaire, logique)
* **Bureautique**

### 🎯 Contexte Académique

Ce dépôt a été développé par **Bouba Ahmed** et **Lkhalidi Mohamed** dans le cadre du Master **Technologie Éducative** à l'**ENS de Meknès**.

---

### 🧱 Architecture du Dépôt et Versions de l'Agent

Afin d'explorer différentes approches d'IA conversationnelle pour l'éducation, ce projet intègre **trois architectures de chatbot distinctes**.

| Fichier/Dossier | Description de la Version | Technologie Clé | Objectif Pédagogique |
| :--- | :--- | :--- | :--- |
| `pytutor_app.py` & `pages/` | **Version 1 (Chatbot Principal)** | Google Gemini (Cloud) | Fournit l'expérience de tutorat conversationnel en Informatique, utilisant un **System Prompt** optimisé. |
| `pages/1_Code_Sandbox.py` | **Version 2 (Chatbot + Sandbox)** | Streamlit `st.text_area` + `exec()` local | Intègre un environnement d'exécution sécurisé pour les tests de code Python, permettant une **analyse pédagogique** du résultat par l'IA. |
| `llama_local_chatbot.py` | **Version 3 (Expérimentale / LLM Local)** | Modèle Llama (Local) | Démontre la faisabilité du tutorat en utilisant un **modèle de langage exécuté localement** (par opposition au Cloud), essentiel pour les contraintes de confidentialité ou de faible connectivité. |