try:
    import streamlit as st
    from fpdf import FPDF
    import base64
except ModuleNotFoundError as e:
    st_available = False
    print(f"Erreur de module : {e}. Streamlit n'est probablement pas installé.")
    print("Veuillez exécuter 'pip install streamlit fpdf' dans votre terminal.")
else:
    st_available = True

if st_available:
    st.set_page_config(page_title="IA Scénariste Pédagogique", layout="wide")

    # --- Thème CSS personnalisé ---
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
        }

        /* Titres */
        h1, h2, h3 {
            color: #005A9C; /* Bleu institutionnel */
        }

        /* Boutons */
        .stButton>button {
            color: #FFFFFF;
            background-color: #005A9C;
            border: 2px solid #004D80;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #004D80;
            border-color: #003B66;
        }

        /* Champs de saisie */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div, .stMultiSelect>div>div {
            border-radius: 8px;
            border: 1px solid #BDBDBD;
            padding-left: 10px;
            background-color: #F9F9F9;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    st.title("🎓 IA Scénariste Pédagogique")
    st.markdown("Un assistant intelligent pour concevoir vos activités de formation pas à pas.")
    st.divider()

    st.header("📌 1. Informations générales")
    col1, col2 = st.columns(2)
    with col1:
        titre = st.text_input("🌟 Titre ou thème de la formation")
        duree = st.text_input("⏱️ Durée prévue (heures/jours)")
    with col2:
        domaine = st.text_input("📚 Domaine ou discipline concernée")
        format_formation = st.selectbox("🧽 Format", ["Présentiel", "Distanciel synchrone", "Distanciel asynchrone", "Hybride", "Autoformation guidée"])
    st.divider()


    st.header("👥 2. Public et contexte")
    col1, col2 = st.columns(2)
    with col1:
        type_public = st.text_input("👤 Type de public (étudiants, professionnels, etc.)")
        niveau = st.selectbox("📈 Niveau des participants", ["Débutants", "Intermédiaires", "Avancés", "Mixtes"])
        contexte = st.selectbox("🏫 Contexte d’apprentissage", ["Initiale", "Continue", "Certifiante", "Diplômante", "Informelle", "Interne"])
    with col2:
        effectif = st.text_input("👥 Effectif prévu")
        bases = st.text_area("📘 Compétences préalables", height=100)
    contraintes = st.text_area("⚠️ Contraintes spécifiques")
    st.divider()


    st.header("🌟 3. Objectifs pédagogiques")
    objectif_general = st.text_area("🎓 Objectif général")
    objectifs_specifiques = st.text_area("🤩 Objectifs spécifiques (utilisez des verbes d’action)")
    col1, col2 = st.columns(2)
    with col1:
        livrable = st.text_input("📦 Livrable attendu")
    with col2:
        evaluation = st.selectbox("🧪 Type d’évaluation", ["Formative", "Sommative", "Par compétences", "Auto-évaluation", "Évaluation entre pairs"])
    st.divider()


    st.header("🧠 4. Choix pédagogiques")
    col1, col2, col3 = st.columns(3)
    with col1:
        approche = st.multiselect("📚 Approche pédagogique", ["Transmissive", "Active", "Inductive", "Par projet", "Classe inversée"])
        role_apprenant = st.selectbox("🤦 Rôle de l’apprenant", ["Récepteur", "Participant", "Acteur", "Co-constructeur", "Évaluateur"])
    with col2:
        collaboratif = st.selectbox("🤝 Mode de travail", ["Individuel", "En binôme", "En groupe", "Classe entière"])
        role_formateur = st.selectbox("🧑‍🏫 Rôle du formateur", ["Guide", "Facilitateur", "Animateur", "Expert", "Observateur"])
    with col3:
        progression = st.selectbox("⏳ Progression pédagogique", ["Introduction", "Approfondissement", "Mise en pratique", "Évaluation"])
    activites = st.text_area("🌟 Activités prévues")
    st.divider()


    st.header("🛠️ 5. Moyens techniques et logistique")
    col1, col2 = st.columns(2)
    with col1:
        materiel = st.text_area("💻 Matériel disponible")
        logistique = st.text_area("🚧 Contraintes logistiques")
    with col2:
        supports = st.text_area("📌 Supports existants")
        accessibilite = st.text_area("♿ Accessibilité spécifique ?")
    st.divider()


    st.header("⏰ 6. Organisation temporelle")
    col1, col2, col3 = st.columns(3)
    with col1:
        temps_total = st.text_input("🕒 Durée totale de la séquence")
    with col2:
        decoupage = st.text_input("📁 Découpage souhaité")
    with col3:
        pauses = st.text_input("☕ Temps de pause prévu ?")
    st.divider()

    st.header("🤩 7. Perspectives et suites")
    articulation = st.text_area("🔗 Lien avec d’autres modules")
    transversales = st.text_area("🧠 Compétences transversales mobilisées")
    valorisation = st.text_area("🏁 Utilisation ou valorisation des productions ?")
    suivi = st.text_area("🔄 Suivi post-formation prévu ?")


    if 'generated_plan' not in st.session_state:
        st.session_state['generated_plan'] = ""

    if st.button("📄 Générer le plan pédagogique", type="primary"):
        plan = f"""
### 📝 Plan pédagogique synthétique

#### 1. Informations générales
- **Titre** : {titre}
- **Domaine** : {domaine}
- **Durée** : {duree}
- **Format** : {format_formation}

#### 2. Public et contexte
- **Type de public** : {type_public}
- **Effectif** : {effectif}
- **Niveau** : {niveau}
- **Compétences préalables** : {bases}
- **Contexte** : {contexte}
- **Contraintes** : {contraintes}

#### 3. Objectifs pédagogiques
- **Objectif général** : {objectif_general}
- **Objectifs spécifiques** : {objectifs_specifiques}
- **Livrable attendu** : {livrable}
- **Évaluation** : {evaluation}

#### 4. Choix pédagogiques
- **Approche** : {', '.join(approche)}
- **Rôle de l’apprenant** : {role_apprenant}
- **Travail** : {collaboratif}
- **Rôle du formateur** : {role_formateur}
- **Progression** : {progression}
- **Activités prévues** : {activites}

#### 5. Moyens et logistique
- **Matériel** : {materiel}
- **Supports existants** : {supports}
- **Contraintes logistiques** : {logistique}
- **Accessibilité** : {accessibilite}

#### 6. Organisation temporelle
- **Durée totale** : {temps_total}
- **Découpage** : {decoupage}
- **Pauses prévues** : {pauses}

#### 7. Perspectives et évolutions
- **Lien avec d’autres modules** : {articulation}
- **Compétences transversales** : {transversales}
- **Valorisation des productions** : {valorisation}
- **Suivi envisagé** : {suivi}
"""
        st.session_state['generated_plan'] = plan

    if st.session_state['generated_plan']:
        st.success("Voici votre plan structuré 👇")
        st.markdown(st.session_state['generated_plan'])

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            # FPDF gère mal l'UTF-8, on doit encoder en 'latin-1' en remplaçant les caractères inconnus
            encoded_plan = st.session_state['generated_plan'].encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 5, txt=encoded_plan)
            
            # Générer le PDF en mémoire
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📄 Télécharger le PDF",
                data=pdf_output,
                file_name="plan_pedagogique.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Une erreur est survenue lors de la génération du PDF : {e}")

else:
    print("Environnement Streamlit non détecté. Assurez-vous d'exécuter ce script avec la commande 'streamlit run nom_du_fichier.py'")
