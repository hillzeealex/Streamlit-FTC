import streamlit as st
import requests
import pandas as pd

pd.set_option('display.max_colwidth', None)

API_URL = "https://jeanmichmich-126218864119.europe-west1.run.app/predict"

st.set_page_config(
    page_title="FIT tes courses !",
    page_icon="🥗",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = 0

# Mappings pour correspondre aux attentes de l'API
prep_time_mapping = {"Rapide (<15 min)": 1, "Normal (15-30 min)": 2, "Long (>30 min)": 3}
season_mapping = {"Printemps": 1, "Été": 2, "Automne": 3, "Hiver": 4}
dish_type_mapping = {"Entrée": 1, "Plat principal": 2, "Dessert": 3, "Apéro": 4}
healthy_mapping = {"Oui": 1, "Non": 0}

# Pages
def home_page():
    # Centrer le titre et le sous-titre avec un conteneur
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>🥗 FIT tes courses !</h1>
            <p style="font-size: 18px;">Créé ta liste de courses idéale.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Espacement vertical pour séparer le bouton
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Style CSS pour le bouton "J'ai faim !"
    st.markdown(
        """
        <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
            width: 30%; /* Réduit la largeur à 40% */
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            background-color: #FF4B4B; /* Vert pour attirer l'attention */
            color: white;
            border-radius: 10px;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #FF4B4B; /* Couleur légèrement différente au survol */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Bouton pour passer à la page suivante
    if st.button("J'ai faim !"):
        st.session_state.page += 1


def ingredients_page():
    # Grand titre aligné à gauche
    st.markdown(
        """
        <h1 style="text-align: left;">🛒 Qu'y a-t-il dans ton frigo ?</h1>
        """,
        unsafe_allow_html=True,
    )

    if 'ingredients' not in st.session_state:
        st.session_state['ingredients'] = []

    # Espacement avant le champ de saisie
    st.markdown("<br>", unsafe_allow_html=True)

    # Champ de saisie et bouton alignés côte à côte
    col1, col2 = st.columns([4, 0.5])  # Ajustement pour réduire la largeur du champ et aligner le bouton
    with col1:
        new_ingredient = st.text_input(
            "Ajoutez un ingrédient :",
            placeholder="Exemple : lentil, tomato...",
            label_visibility="collapsed",  # Cache le label pour un affichage plus propre
        )
    with col2:
        if st.button("➕", key="add_button", help="Ajouter l'ingrédient"):
            if new_ingredient:
                st.session_state['ingredients'].append(new_ingredient)

    # Espacement avant la liste des ingrédients
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("### Votre liste d'ingrédients :")
    st.markdown("<br>", unsafe_allow_html=True)

    # Affichage de la liste des ingrédients
    for i, ingredient in enumerate(st.session_state['ingredients']):
        col1, col2 = st.columns([4, 0.5])
        with col1:
            st.write(ingredient)
        with col2:
            if st.button("❌", key=f"remove_{i}", help=f"Supprimer {ingredient}"):
                st.session_state['ingredients'].pop(i)

    # Espacement avant le bouton suivant
    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton pour passer à la page suivante
    if st.button("➡️ Suivant"):
        st.session_state.page += 1


# def mood_page():
#     st.title("🤤 Une envie particulière ?")

#     moods = {
#         "🏠 Réconfortant & Familier": 0,
#         "🍫 Sucré & Gourmand": 1,
#         "🍝 Salé & Polyvalent": 2,
#         "🥗 Sain & Léger": 3,
#         "🍗 Copieux & Généreux": 4,
#     }

#     # Style CSS pour uniformiser les boutons
#     st.markdown(
#         """
#         <style>
#         .stButton button {
#             width: 100%;
#             height: 50px;
#             font-size: 16px;
#             margin-bottom: 10px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     # Affichage des boutons et détection du clic
#     for mood, value in moods.items():
#         if st.button(mood, key=f"mood_{value}"):
#             st.session_state["mood"] = value
#             st.session_state.page += 1  # Passer immédiatement à la page suivante
#             break  # Stopper la boucle après la sélection d'un mood

def manual_mood_page():
    st.title("🤤 Une envie particulière ?")

    # Nouveau dictionnaire de moods
    mood_manual_mapping = {
        "🎁 Tous": None,
        "🍫 Gourmand / Savoureux": 0,
        "🏠 Confort / Réconfortant": 1,
        "🥗 Sain / Équilibré": 2,
        "👨‍👩‍👧 Familial / Convivial": 3,
        "🌶️ Épicé / Intense": 4,
        "🎉 Festif / Ludique": 5,
        "🍓 Fruité / Rafraîchissant": 6,
        "❤️ Aphrodisiaque / Envoûtant": 7,
        "🌍 Exotique / Curieux": 8,
        "⚡ Énergisant / Vitalisant": 9,
    }

    st.markdown(f"**Pour rappel, dans ton frigo il y a :** {', '.join(st.session_state['ingredients']) or 'Aucun'}")

    # Style CSS pour uniformiser les boutons
    st.markdown(
        """
        <style>
        .stButton button {
            width: 100% !important;
            height: 50px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Affichage des boutons en deux colonnes
    col1, col2 = st.columns(2)

    for i, (mood, value) in enumerate(mood_manual_mapping.items()):
        column = col1 if i % 2 == 0 else col2  # Alterne entre les colonnes
        with column:
            if st.button(mood, key=f"mood_manual{value}"):
                st.session_state["mood_manual"] = value
                st.session_state.page += 1  # Passe immédiatement à la page suivante
                break  # Arrête l'exécution après la sélection d'un mood


def other_criteria_page():
    st.title("✅ D'autres critères ?")

    # Utilisation de deux colonnes pour aérer l'interface
    col1, col2 = st.columns(2)

    with col1:
        # Critère Type de plat
        type_de_plat = st.multiselect(
            "Type de plat 🍽️:",
            ["Entrée", "Plat principal", "Dessert", "Apéro"]
        )
        st.session_state.type_de_plat = type_de_plat

        # Critère Origine culinaire
        origine = st.text_input("Origine culinaire 🌍:", placeholder="Exemple : Italien, Asiatique...")
        st.session_state.origine = origine

        # Critère Temps de préparation
        temps_preparation = st.selectbox(
            "Temps de préparation ⏱️:",
            ["Aucun", "Rapide (<15 min)", "Normal (15-30 min)", "Long (>30 min)"]
        )
        st.session_state.temps_preparation = temps_preparation

    with col2:
        # Critère Catégories alimentaires
        categories = st.multiselect(
            "Catégorie alimentaire 🌱:",
            ["Vegan", "Végétarien", "Sans gluten"]
        )
        st.session_state.categories = categories

        # Critère Saison
        saison = st.selectbox(
            "Saison 🌦️:",
            ["Aucune", "Printemps", "Été", "Automne", "Hiver"]
        )
        st.session_state.saison = saison

        # Critère Healthy (transformé en menu déroulant)
        healthy = st.selectbox(
            "Healthy 🥗:",
            ["Aucun", "Oui", "Non"]
        )
        st.session_state.healthy = healthy

    # Espacement avant le bouton
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Centrer et styliser le bouton "Trouver ma recette"
    st.markdown(
        """
        <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
            width: 50%;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            background-color: #FF4B4B; /* Vert pour attirer l'attention */
            color: white;
            border-radius: 10px;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #FF4B4B; /* Couleur légèrement différente au survol */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Trouver ma recette"):
        st.session_state.page += 1

def results_page():
    # Grand titre aligné à gauche
    st.markdown(
        """
        <h1 style="text-align: left;">🎁 Voici les recettes sélectionnées pour toi :</h1>
        """,
        unsafe_allow_html=True,
    )

    # Ajouter un espacement entre le titre et les résultats
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Appliquer les mappings
    prep_time_mapping = {"Rapide (<15 min)": 1, "Normal (15-30 min)": 2, "Long (>30 min)": 3, "Aucun": None}
    season_mapping = {"Printemps": 1, "Été": 2, "Automne": 3, "Hiver": 4, "Aucune": None}
    healthy_mapping = {"Oui": 1, "Non": 0, "Aucun": None}
    dish_type_mapping = {"Entrée": 1, "Plat principal": 2, "Dessert": 3, "Apéro": 4}

    # Préparer le payload pour l'API
    payload = {
        "user_ingredients": st.session_state.get("ingredients", []),
        "healthy": healthy_mapping.get(st.session_state.get("healthy", None)),
        "season": season_mapping.get(st.session_state.get("saison", None)),
        "dish_type": [dish_type_mapping[dt] for dt in st.session_state.get("type_de_plat", [])],
        "prep_time": prep_time_mapping.get(st.session_state.get("temps_preparation", None)),
        "origin": st.session_state.get("origine", None),
        "categories": ", ".join(st.session_state.get("categories", [])),
        "mood": st.session_state.get("mood", None),
        "mood_manual": st.session_state.get("mood_manual", None)

    }

    # Nettoyer les champs vides
    payload = {k: v for k, v in payload.items() if v not in [None, "", [], "None"]}

    # Validation avant l'appel
    if not payload.get("user_ingredients"):
        st.error("Veuillez ajouter au moins un ingrédient pour obtenir des résultats.")
        return

    try:
        # Appeler l'API
        response = requests.get(API_URL, params=payload)
        response.raise_for_status()
        data = response.json()

        # Extraire les résultats pour les modèles 1, 2 et 3
        model_results = {key: data[key] for key in ["top_5_textblob", "top_5_vader", "result_combined_df"] if key in data}

        if model_results:
            col1, col2, col3 = st.columns(3)
            columns = [col1, col2, col3]

            for i, (model, recipes) in enumerate(model_results.items()):
                if recipes:
                    best_recipe = pd.DataFrame(recipes).iloc[0]
                    with columns[i]:
                        st.markdown(
                            f"""
                            ### 🍴 {best_recipe['name']}
                            - 🌟 **Note moyenne** : {round(best_recipe['avg_rating'], 2)}
                            - ⏳ **Temps de préparation** : {best_recipe['minutes']} min
                            - ✅ **Ingrédients réutilisés** : {', '.join(best_recipe['reused_ingredients'])}
                            - 🛒 **Ingrédients manquants** : {', '.join(best_recipe['missing_ingredients'])}
                            """
                        )
        else:
            st.warning("Aucun résultat pour les modèles sélectionnés.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")

# Naviguer entre les pages
pages = [home_page, ingredients_page, manual_mood_page, other_criteria_page, results_page]
pages[st.session_state.page]()
