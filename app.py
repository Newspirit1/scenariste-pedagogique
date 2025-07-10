import streamlit as st
from fpdf import FPDF
import base64
import openai  # NOUVEAU : Bibliothèque pour parler à l'IA
import json    # NOUVEAU : Pour interpréter la réponse de l'IA

# --- Configuration de la page ---
st.set_page_config(page_title="IA Scénariste Pédagogique", layout="wide")

# --- NOUVEAU : Logique de l'IA ---

# Fonction pour appeler l'IA et générer le contenu
def generer_plan_par_ia(idee_initiale, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Le "prompt" : C'est l'instruction que nous donnons à l'IA. C'est la partie la plus importante !
        prompt_systeme = """
        Tu es un ingénieur pédagogique expert, spécialisé dans la conception de formations innovantes.
        Ta mission est de prendre une idée brute de formation et de la transformer en un scénario pédagogique structuré.
        Réponds UNIQUEMENT en format JSON valide, sans aucun texte avant ou après.
        Le JSON doit contenir les clés suivantes, que tu rempliras de manière créative et pertinente :
        "titre", "domaine", "duree", "format_formation", "type_public", "effectif", "niveau", "bases", "contexte", "objectif_general", "objectifs_specifiques", "livrable", "approche", "role_apprenant", "collaboratif", "role_formateur", "activites"
        Pour "objectifs_specifiques", liste au moins 3 objectifs avec des verbes d'action.
        Pour "activites", propose une séquence logique d'activités.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Ou "gpt-4-turbo" pour de meilleurs résultats
            messages=[
                {"role": "system", "content": prompt_systeme},
                {"role": "user", "content": f"Voici mon idée de formation : {idee_initiale}"}
            ],
            response_format={"type": "json_object"} # NOUVEAU : On force une réponse JSON
        )
        
        contenu_genere = response.choices[0].message.content
        return json.loads(contenu_genere)
    
    except Exception as e:
        st.error(f"Une erreur est survenue avec l'API OpenAI : {e}")
        return None

# --- Interface utilisateur ---

st.title("🎓 IA Scénariste Pédagogique")
st.markdown("Décrivez votre idée et laissez l'IA construire une première version de votre plan de formation.")
st.divider()

# --- NOUVEAU : Section de génération par IA ---
st.header("✨ 1. Lancez l'IA")

# Demander la clé API (de manière sécurisée)
api_key_input = st.text_input("🔑 Entrez votre clé API OpenAI", type="password", help="Votre clé est utilisée pour cette session et n'est pas stockée.")

idee = st.text_area("✏️ Décrivez votre idée de formation en une phrase", "Une formation de 2 jours pour une équipe marketing sur les bases de l'analyse de données avec Google Analytics.")

if st.button("🚀 Générer le scénario avec l'IA"):
    if not api_key_input:
        st.warning("Veuillez entrer votre clé API OpenAI pour continuer.")
    else:
        with st.spinner("L'IA réfléchit à votre scénario... Veuillez patienter."):
            plan_genere = generer_plan_par_ia(idee, api_key_input)
            if plan_genere:
                # On stocke les suggestions de l'IA dans l'état de la session
                st.session_state.update(plan_genere)
                st.success("Scénario généré ! Vous pouvez maintenant l'affiner ci-dessous.")

# --- Formulaire pré-rempli par l'IA ---

st.header("📌 2. Affinez votre plan de formation")

# Utilise les valeurs de st.session_state ou une chaîne vide par défaut
def get_value(key):
    return st.session_state.get(key, "")

col1, col2 = st.columns(2)
with col1:
    titre = st.text_input("🌟 Titre", get_value("titre"))
    duree = st.text_input("⏱️ Durée", get_value("duree"))
with col2:
    domaine = st.text_input("📚 Domaine", get_value("domaine"))
    format_formation = st.selectbox("🧽 Format", ["Hybride", "Présentiel", "Distanciel synchrone", "Distanciel asynchrone", "Autoformation guidée"], index=0 if not get_value("format_formation") else ["Hybride", "Présentiel", "Distanciel synchrone", "Distanciel asynchrone", "Autoformation guidée"].index(get_value("format_formation")))

# ... (le reste du formulaire est identique, mais utilise get_value() pour chaque champ)
st.header("👥 Public et contexte")
type_public = st.text_input("👤 Type de public", get_value("type_public"))
# ... et ainsi de suite pour tous les autres champs.
# Pour faire court, je ne vais pas répéter tous les champs ici, mais le principe est le même :
# remplacez st.text_input("Label") par st.text_input("Label", get_value("nom_de_la_cle"))

# Exemple pour les objectifs :
st.header("🌟 Objectifs pédagogiques")
objectif_general = st.text_area("🎓 Objectif général", get_value("objectif_general"))
objectifs_specifiques = st.text_area("🤩 Objectifs spécifiques", get_value("objectifs_specifiques"))
livrable = st.text_input("📦 Livrable attendu", get_value("livrable"))

# Exemple pour les activités
st.header("🧠 Choix pédagogiques")
activites = st.text_area("🌟 Activités prévues", get_value("activites"), height=200)

# etc.

# ... Le reste du code pour générer le Markdown et le PDF reste le même
# Assurez-vous simplement que les variables (titre, domaine, etc.) sont bien assignées 
# à partir des widgets comme dans votre code original.

st.divider()
if st.button("📄 Générer le plan final (PDF)"):
    # Recréer le plan avec les valeurs potentiellement modifiées du formulaire
    final_plan = f"""
### 📝 Plan pédagogique synthétique
- **Titre**: {titre}
- **Domaine**: {domaine}
# ... etc, comme dans votre code original
"""
    st.markdown(final_plan)
    # Le code de génération PDF reste identique
