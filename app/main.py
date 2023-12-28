import time
import openai
import streamlit as st
from pinecone_connection import init_pinecone
from openai_connection import search_docs



# Initialisation de Pinecone et obtention de l'index
index = init_pinecone()


# Fonction pour simuler une opération
def simuler_operation():
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)
    my_bar.empty()

def construct_prompt_for_summary(user_query:str, matches):
    # Construction du contexte à partir des matches
    context = "\n".join([match[0] for match in matches])  # Accès par indice

    # Construction du prompt final avec la requête de l'utilisateur et le contexte
    prompt = f"{user_query}\n\nContexte:\n{context}"
    return prompt



#Informations de la page
st.title("Straticia test")
st.write("Application de recherche documentaire dans le droit (Limité aux marchés public)")



# Créer un formulaire
with st.form(key="search_form"):
    # Champ de saisie de la requête
    query = st.text_input("Entrez votre requête de recherche:")
    
    # Bouton pour démarrer l'opération de recherche
    submit_button = st.form_submit_button(label="Démarrer l'Opération")


# Fonction pour effectuer la recherche et afficher les résultats
def effectuer_recherche():
    my_bar = st.progress(0)
    time.sleep(1)
    my_bar.progress(20)

    # Effectuer la recherche avec Pinecone
    matches = search_docs(query, index)  # Assurez-vous que search_docs est définie et importée
    my_bar.progress(40)

    # Construire le prompt pour le modèle GPT-3
    prompt = construct_prompt_for_summary(query, matches)
    my_bar.progress(60)
    time.sleep(1)
    my_bar.progress(80)

    # Définir les paramètres de la requête OpenAI
    max_completion_tokens = 300
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=max_completion_tokens,
        temperature=0,
    )

    my_bar.progress(100)
    time.sleep(1)
    my_bar.empty()

    st.success("Opération terminée !")
    st.write(response.choices[0].text)

# Vérifier si le formulaire a été soumis
if query:
    effectuer_recherche()
