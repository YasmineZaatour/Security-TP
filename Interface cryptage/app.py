import streamlit as st
from cryptage_cypher import cryptageCypher, decryptageCypher 

def cypher_app():
    # Titre de l'application
    st.title("Chiffrement de César : Cryptage et Décryptage")

    # Champs pour l'entrée utilisateur
    input_text = st.text_area("Entrez le texte à chiffrer ou déchiffrer", "")
    key = st.number_input("Sélectionnez la clé (décalage)", min_value=1, max_value=25, value=5)

    # Boutons pour choisir entre le chiffrement et le déchiffrement
    action = st.radio("Action", ("Chiffrer", "Déchiffrer"))

    # Bouton pour exécuter l'action
    if st.button("Exécuter"):
        if input_text:
            if action == "Chiffrer":
                output_text = cryptageCypher(input_text, key)
                st.success(f"Texte crypté : {output_text}")
            elif action == "Déchiffrer":
                output_text = decryptageCypher(input_text, key)
                st.success(f"Texte décrypté : {output_text}")
        else:
            st.error("Veuillez entrer un texte à chiffrer ou déchiffrer.")
