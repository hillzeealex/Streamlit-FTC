import streamlit as st
import requests
import pandas as pd
pd.set_option('display.max_colwidth', None)  # Supprime la limitation de la largeur des colonnes


# URL de votre API FastAPI
API_URL = "http://127.0.0.1:8000/predict"

# Configurer la page Streamlit
st.set_page_config(
    page_title="FIT tes courses !",
    page_icon="🥗",
    layout="wide"
)

# Interface principale
def main():
    st.title("🥗 FIT tes courses !")
    st.markdown("**L'app qui te permet de créer ta liste de courses idéale !**")
    st.divider()

    # Créer deux colonnes pour les sections Ingrédients et Mood
    col1, col2 = st.columns(2)

    # Colonne 1 : Section Ingrédients
    with col1:
        st.subheader("🛒 Vos Ingrédients")
        if 'ingredients' not in st.session_state:
            st.session_state['ingredients'] = []

        # Ajouter un nouvel ingrédient
        new_ingredient = st.text_input(
            "Ajoutez un ingrédient (appuyez sur Ajouter l'ingrédient pour valider) :",
            placeholder="Exemple : lentil, tomato..."
        )
        if st.button("➕ Ajouter l'ingrédient"):
            if new_ingredient:
                st.session_state['ingredients'].append(new_ingredient)
            else:
                st.warning("Veuillez entrer un ingrédient valide.")


        # Supprimer un ingrédient
        st.write("Liste actuelle des ingrédients :")
        if st.session_state['ingredients']:
            for ingredient in st.session_state['ingredients']:
                sub_col1, sub_col2 = st.columns([8, 2])
                with sub_col1:
                    st.write(ingredient)
                with sub_col2:
                    if st.button(f"❌", key=ingredient):
                        st.session_state['ingredients'].remove(ingredient)
                        st.experimental_rerun()
        else:
            st.write("Aucun ingrédient ajouté.")

    # Colonne 2 : Section Mood
    with col2:
        st.subheader("🎭 Ton Mood")

        # Mapping des moods avec icônes
        mood_icons = {
            "Tous": "🎯 Tous",
            "Réconfortant & Familier": "🏠 Réconfortant & Familier",
            "Sucré & Gourmand": "🍫 Sucré & Gourmand",
            "Salé & Polyvalent": "🥗 Salé & Polyvalent",
            "Sain & Léger": "🍎 Sain & Léger",
            "Copieux & Généreux": "🍖 Copieux & Généreux",
        }

        # Ajout de boutons pour chaque mood
        selected_mood = st.radio(
            "",
            options=list(mood_icons.keys()),
            format_func=lambda mood: mood_icons[mood]
        )

        # Mapping des moods sélectionnés à des valeurs numériques
        mood_mapping = {
            "Tous" : None,
            "Réconfortant & Familier" : 1,
            "Sucré & Gourmand": 2,
            "Salé & Polyvalent": 3,
            "Sain & Léger": 4,
            "Copieux & Généreux": 5
        }
        mood = mood_mapping[selected_mood]

    # Ajouter une ligne de séparation
    st.divider()

    # Ajouter un saut de ligne avant la section suivante
    st.markdown("<br>", unsafe_allow_html=True)

    # Section Filtres
    st.subheader("⚙️ Tes critères")

    with st.expander("⚙️ clic pour afficher plus de critères ", expanded=False):
        col1, col2 = st.columns(2)

        # Colonne 1 : Option Healthy, Saison et Origine
        with col1:
            st.markdown("**Healthy**")
            healthy = st.selectbox(
                "5 fruits et légumes par jours",
                ["Aucun", "Oui", "Non"]
            )
            healthy_mapping = {"Aucun": None, "Oui": 1, "Non": 0}
            healthy = healthy_mapping[healthy]

            st.markdown("**Saison**")
            saison = st.selectbox(
                "Choisis ta saison : été, hiver, automne, printemps",
                ["Aucune", "Printemps", "Été", "Automne", "Hiver"]
            )
            saison_mapping = {"Aucune": None, "Printemps": 1, "Été": 2, "Automne": 3, "Hiver": 4}
            saison = saison_mapping[saison]

            st.markdown("**Origine**")
            origine = st.text_input("Cette semaine tu te sens : italien, américain, français...")

        # Colonne 2 : Type de plat, Temps de préparation et Catégories
        with col2:
            st.markdown("**Type de plat**")
            type_de_plat = st.multiselect(
                "Tu es plus entrée, plat, dessert ou apéro",
                ["Aucun", "Entrée", "Plat principal", "Dessert", "Apéro"]
            )
            type_de_plat_mapping = {"Aucun": None, "Entrée": 1, "Plat principal": 2, "Dessert": 3, "Apéro": 4}
            # Convertir les sélections en leurs valeurs correspondantes
            type_de_plat = [type_de_plat_mapping[plat] for plat in type_de_plat]

            st.markdown("**Temps de préparation**")
            temps_preparation = st.selectbox(
                "On voudrait tous avoir plus de 24h dans une journée",
                ["Aucun", "Rapide (<15 min)", "Normal (15-30 min)", "Long (>30 min)"]
            )
            temps_preparation_mapping = {"Aucun": None, "Rapide (<15 min)": 0, "Normal (15-30 min)": 1, "Long (>30 min)": 2}
            temps_preparation = temps_preparation_mapping[temps_preparation]

            st.markdown("**Catégories alimentaires**")
            categories = st.multiselect(
                "Si tu es Vegan, Végétarien ou autre, on est avec toi",
                ["Vegan", "Végétarien", "Sans gluten"]
            )

    st.divider()

    # Recherche de recettes
    if st.button("🔍 Rechercher des recettes"):
        if not st.session_state['ingredients']:
            st.warning("Veuillez ajouter au moins un ingrédient avant de lancer la recherche.")
        else:
            # Préparer les paramètres pour l'API
            payload = {
                "user_ingredients": st.session_state['ingredients'],
                "healthy": healthy,
                "season": saison,
                "dish_type": type_de_plat,
                "prep_time": temps_preparation,
                "origin": origine,
                "categories": ", ".join(categories),
                "mood" : mood
            }
            # Appeler l'API FastAPI
            try:
                response = requests.get(API_URL, params=payload)
                response.raise_for_status()
                data = response.json()
                # Afficher les résultats
                st.header("📋 A vos courses !")
                st.markdown(f"**Ingrédients déjà présents :** {', '.join(st.session_state['ingredients']) or 'Aucun'}")

                if response.status_code == 200:

                    # Combiner les DataFrames
                                        # Modèle 1
                    if "result_combined_df" in data and data["result_combined_df"]:
                        combined_df = pd.DataFrame(data["result_combined_df"])

                    else:
                        st.warning("Les résultats des Modèles sont vides.")

                    st.subheader("📊 Résultats")
                    total_recipes = len(combined_df)
                    total_reviews = combined_df["num_reviews"].sum()
                    avg_rating = combined_df["avg_rating"].mean()
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Recettes selectionnées", total_recipes)
                    with col2:
                        st.metric("Nombre total d'avis", total_reviews)
                    with col3:
                        st.metric("Note moyenne", round(avg_rating, 2))

                    st.subheader("	✅ Listes recettes sélectionnées")
                    st.dataframe(combined_df)

                    # Vérifiez si les données pour Transformers, VADER et les votes sont disponibles
                    if (
                        "top_5_textblob" in data and data["top_5_textblob"] and
                        "top_5_vader" in data and data["top_5_vader"] and
                        "result_combined_df" in data and data["result_combined_df"]
                    ):
                        # Convertir les données en DataFrames
                        top_5_textblob_df = pd.DataFrame(data["top_5_textblob"])
                        top_5_vader_df = pd.DataFrame(data["top_5_vader"])
                        combined_df = pd.DataFrame(data["result_combined_df"])

                        # Identifier la meilleure recette selon Transformers
                        best_textblob_recipe = top_5_textblob_df.iloc[0]

                        # Identifier la meilleure recette selon VADER
                        best_vader_recipe = top_5_vader_df.iloc[0]

                        # Identifier la recette avec le plus de votes
                        most_voted_recipe = combined_df.sort_values(by="num_reviews", ascending=False).iloc[0]

                        # Créer trois colonnes pour afficher les meilleures recettes
                        col1, col2, col3 = st.columns(3)

                        # Afficher la meilleure recette selon textblob
                        with col1:
                            st.subheader("🥇 Meilleure recette (textblob)")
                            st.markdown(f"### **{best_textblob_recipe['name']}**")
                            st.write(f"🌟 Note moyenne : {round(best_textblob_recipe['avg_rating'], 2)}")
                            st.write(f"👥 Nombre d'avis : {best_textblob_recipe['num_reviews']}")
                            st.write(f"🏆 Calories : {best_textblob_recipe['calories']} kcal")
                            st.write(f"⏳ Temps de préparation : {best_textblob_recipe['minutes']} min")
                            st.markdown("**🛒 Ingrédients nécessaires :**")
                            st.write(", ".join(best_textblob_recipe['missing_ingredients']))
                            st.markdown("**🌱 Ingrédients à réutiliser :**")
                            st.write(", ".join(best_textblob_recipe['reused_ingredients']))


                        # Téléchargement des résultats
                        st.download_button(
                            label="Télécharger (CSV)",
                            data=combined_df.to_csv(index=False),
                            file_name="recettes.csv",
                            mime="text/csv",
                        )

                        # Afficher la meilleure recette selon VADER
                        with col2:
                            st.subheader("🎖️ Meilleure recette (VADER)")
                            st.markdown(f"### **{best_vader_recipe['name']}**")
                            st.write(f"🌟 Note moyenne : {round(best_vader_recipe['avg_rating'], 2)}")
                            st.write(f"👥 Nombre d'avis : {best_vader_recipe['num_reviews']}")
                            st.write(f"🏆 Calories : {best_vader_recipe['calories']} kcal")
                            st.write(f"⏳ Temps de préparation : {best_vader_recipe['minutes']} min")
                            st.markdown("**🛒 Ingrédients nécessaires :**")
                            st.write(", ".join(best_vader_recipe['missing_ingredients']))
                            st.markdown("**🌱 Ingrédients à réutiliser :**")
                            st.write(", ".join(best_vader_recipe['reused_ingredients']))

                        # Afficher la recette avec le plus de votes
                        with col3:
                            st.subheader("✨ Recette avec le plus de votes")
                            st.markdown(f"### **{most_voted_recipe['name']}**")
                            st.write(f"🌟 Note moyenne : {round(most_voted_recipe['avg_rating'], 2)}")
                            st.write(f"👥 Nombre d'avis : {most_voted_recipe['num_reviews']}")
                            st.write(f"🏆 Calories : {most_voted_recipe['calories']} kcal")
                            st.write(f"⏳ Temps de préparation : {most_voted_recipe['minutes']} min")
                            st.markdown("**🛒 Ingrédients nécessaires :**")
                            st.write(", ".join(most_voted_recipe['missing_ingredients']))
                            st.markdown("**🌱 Ingrédients à réutiliser :**")
                            st.write(", ".join(most_voted_recipe['reused_ingredients']))

                    with st.expander("⚙️ clic pour afficher la reco de chaque modèle ", expanded=False):
                        if (
                            "top_5_transformer" in data and data["top_5_transformer"] and
                            "top_5_vader" in data and data["top_5_vader"] and
                            "result_combined_df" in data and data["result_combined_df"]
                        ):
                            # Convertir les données en DataFrames
                            st.subheader("Top 5 avis (transformers)")
                            st.dataframe(top_5_transformer_df)

                            # Convertir les données en DataFrames
                            st.subheader("Top 5 avis (VADER)")
                            st.dataframe(top_5_vader_df)

                        # Modèle 1
                        if "result1" in data and data["result1"]:
                            st.subheader("Reco par reconnaissance d'ingrédients")
                            df1 = pd.DataFrame(data["result1"])
                            st.dataframe(df1)
                        else:
                            st.warning("Les résultats du Modèle 1 sont vides.")

                        # Modèle 2
                        if "result2" in data and data["result2"]:
                            st.subheader("Reco par similiratié cosinus sur la concaténation des ingrédients")
                            df2 = pd.DataFrame(data["result2"])
                            st.dataframe(df2)
                        else:
                            st.warning("Les résultats du Modèle 2 sont vides.")
                        #Modèle 3
                        if "result3" in data and data["result3"]:
                            st.subheader("Reco par similiratié cosinus sur la concaténation des ingrédients séparer d'une virgule")
                            df3 = pd.DataFrame(data["result3"])
                            st.dataframe(df3)
                        else:
                            st.warning("Les résultats du Modèle 3 sont vides.")

                        # Modèle 4
                        if "result4" in data and data["result4"]:
                            st.subheader("Reco par recherche des voisins KNN")
                            df4 = pd.DataFrame(data["result4"])
                            st.dataframe(df4)
                        else:
                            st.warning("Les résultats du Modèle 4 sont vides.")
            except requests.exceptions.RequestException as e:
                st.error(f"Pas de résultat, veuillez modifier vos filtres")

    st.image("courses_ideal.png", caption="Fit des courses comme nos modèles de Machine Learning")

# Exécuter l'application
if __name__ == "__main__":
    main()



                    # # Barre de recherche
                    # st.subheader("Toutes les recettes combinées (sans doublons)")
                    # search_term = st.text_input(
                    #     "Recherchez une recette ou un ingrédient",
                    #     placeholder="Entrez un mot-clé pour filtrer (ex. lentil, tomato)...",
                    #     key="search_input"
                    # )

                    # # Filtrer localement le DataFrame combiné
                    # if search_term:
                    #     filtered_df = combined_df[
                    #         combined_df.apply(lambda row: search_term.lower() in str(row.values).lower(), axis=1)
                    #     ]
                    # else:
                    #     filtered_df = combined_df

                    # # Afficher les données filtrées
                    # st.dataframe(filtered_df, use_container_width=True)
