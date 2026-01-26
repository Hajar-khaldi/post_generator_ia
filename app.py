import os                      
import streamlit as st         
from streamlit_tags import st_tags 
from huggingface_hub import InferenceClient 
from streamlit_option_menu import option_menu  
from streamlit_quill import st_quill 



# Permet de conserver le post généré entre les interactions Streamlit
if "post_text" not in st.session_state:
    st.session_state.post_text = ""


# ===============================
# Hugging Face API configuration
# ===============================
# Récupération du token Hugging Face depuis les variables d'environnement
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialisation du client d'inférence Hugging Face
client = InferenceClient(token=HF_TOKEN)


st.set_page_config(
    page_title="Générateur de posts IA",
    page_icon="🤖",
    layout="wide",                      # Mise en page large pour utiliser les colonnes
    initial_sidebar_state="collapsed"   # Sidebar masquée par défaut
)


st.title("🚀 Générateur de posts LinkedIn / Facebook")
st.write("Entrez des mots-clés et générez automatiquement un post optimisé.")



# Colonne gauche : formulaire
# Colonne droite : post généré
col_form, col_result = st.columns([1, 1])


# ===============================
# Prompt builder function
# ===============================
def build_prompt(keywords, platform, length_slider):
    """
    Construit dynamiquement le prompt envoyé au LLM
    en fonction des mots-clés, de la plateforme et de la longueur.
    """
    tone = "professionnel" if platform == "LinkedIn" else "amical et engageant"

    return f"""
Génère un post {platform} à partir des mots-clés :
{", ".join(keywords)}

Contraintes :
- Ton : {tone}
- Texte fluide optimisé
- Format Markdown
- Texte structuré (paragraphes, listes si utile)
- Emojis légers si pertinent
- Ajouter 3 à 5 hashtags
"""



with col_form:
    st.subheader("📝 Paramètres du post")

    # Saisie des mots-clés sous forme de tags
    keywords = st_tags(
        value=['IA', 'innovation', 'productivité'],
        label="#### Mots-clés",
        text='IA, innovation, productivité',
        suggestions=['IA', 'innovation', 'productivité'],
        maxtags=4,
        key='1'
    )

    # Sélection du type de publication
    st.markdown("#### Type de publication")
    platform = option_menu(
        menu_title="",
        options=["LinkedIn", "Facebook"],
        icons=["briefcase", "facebook"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"border": "1px solid #ccc", "background-color": "#f5f5f5"},
            "icon": {"font-size": "20px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "0px",
                "color": "#0b3d91",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "color": "white",
                "background-color": "#0b3d91",
            },
        }
    )

    # Slider pour contrôler la longueur du post (tokens)
    length_slider = st.slider("Longueur du post (tokens)", 150, 500, 350)

    # Bouton de génération
    if st.button("🚀 Générer le post"):
        if not keywords:
            st.warning("Veuillez entrer des mots-clés.")
        else:
            with st.spinner("Génération en cours..."):
                # Appel du modèle LLaMA via l'API Hugging Face
                completion = client.chat.completions.create(
                    model="meta-llama/Llama-3.1-8B-Instruct:novita",
                    messages=[
                        {
                            "role": "user",
                            "content": build_prompt(keywords, platform, length_slider)
                        }
                    ],
                    max_tokens=length_slider,
                    temperature=0.7
                )

            # Sauvegarde du texte généré dans le session_state
            st.session_state.post_text = completion.choices[0].message["content"]



with col_result:
    st.subheader("📄 Post généré")

    # Affichage du post uniquement s'il existe
    if st.session_state.post_text:
        # Aperçu du post avec mise en forme
        st.markdown(st.session_state.post_text)
        st.markdown("### ✏️ Texte du post (édition WYSIWYG)")
        st.write("Vous pouvez modifier le texte ici")

        # Éditeur WYSIWYG pour modification du contenu
        post_wysiwyg = st_quill(
            value=st.session_state.post_text,
            key="editor",
            toolbar=["bold", "italic", "underline", "color", "background", "link"]
        )

        # Bouton pour copier/télécharger le post
        st.download_button(
            label="📋 Copier le texte",
            data=st.session_state.post_text,
            file_name=f"post-{platform}.txt",
            mime="text/plain"
        )
