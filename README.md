# ENS-Tutor-AI-EdTech

## Assistant Pédagogique en Science Informatique (Niveau Lycée)

Ce projet est une solution de **Technologie Éducative (EdTech)** visant à démontrer l'efficacité des agents conversationnels basés sur l'Intelligence Artificielle (Google Gemini LLM) pour le **tutorat personnalisé**.

**ENS Tutor** couvre l'intégralité du programme d'Informatique du lycée, incluant :
* **Algorithmique et Structures de données**
* **Programmation** (Python, HTML, CSS, JavaScript de base)
* **Réseaux et Internet** (Protocoles, routage)
* **Architecture Matérielle** (Binaire, logique)
* **Bureautique**

### Contexte Académique

Ce dépôt a été développé par **Bouba Ahmed** et **Lkhalidi Mohamed** dans le cadre du Master **Technologie Éducative** à l'**ENS de Meknès**.

---

### Architecture du Dépôt et Versions de l'Agent

Afin d'explorer différentes approches d'IA conversationnelle pour l'éducation, ce projet intègre **trois architectures de chatbot distinctes**.

| Fichier/Dossier | Nom de la Version | Technologie Clé | Objectif Pédagogique et Portée |
| :--- | :--- | :--- | :--- |
| `pytutor.py` | **Version 1 (Tuteur Python)** | Google Gemini API (Cloud) | Fournit une expérience de tutorat exclusivement centrée sur le langage **Python** (prototype initial). |
| `ChatBot_with_Sandbox.py` & `pages/` | **Version 2 (ENS Tutor Complet)** | Gemini API (Cloud) + Streamlit `exec()` | **L'agent final, multidisciplinaire.** Couvre toute la **Science Informatique**. Intègre le **Code Sandbox** (`pages/1_Code_Sandbox.py`) pour l'exécution et l'analyse pédagogique des résultats du code. |
| `Ollama_Bot.py` | **Version 3 (Expérimentale/LLM Local)** | Modèle Llama via Ollama (Local) | Démontre la faisabilité du tutorat en utilisant un **modèle de langage exécuté localement**. Répond aux enjeux de **confidentialité** et d'**accessibilité** dans des environnements scolaires avec des contraintes de connectivité. |

### Technologies et Dépendances

Les composants clés du projet incluent :

* **Langage :** Python 3.x
* **Modèles LLM :** Google Gemini (`gemini-2.5-flash`) pour la production et Llama (via Ollama) pour l'expérimentation locale.
* **Interface :** Streamlit pour un déploiement web rapide et convivial.
* **Gestion de l'IA Locale :** Ollama (pour la version `Ollama_Bot.py` uniquement).

Vous devriez également inclure un fichier `requirements.txt` listant au minimum :
```bash
google-genai
streamlit
```

### Démarrage Rapide

Cloner le dépôt :

```Bash
git clone [https://github.com/BoubaAhmed/ENS-Tutor-AI-EdTech.git](https://github.com/BoubaAhmed/ENS-Tutor-AI-EdTech.git)
cd ENS-Tutor-AI-EdTech
```
Installer les dépendances :

```Bash
pip install -r requirements.txt
```
Configurer la Clé Gemini :

```Bash
export GEMINI_API_KEY='VOTRE_CLÉ_API'
```
Lancer l'Application Principale (ENS Tutor Complet) :

```Bash
streamlit run ChatBot_with_Sandbox.py
```