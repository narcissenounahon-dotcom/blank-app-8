import streamlit as st
import pandas as pd
import random
import numpy as np

# Configuration de la page
st.set_page_config(page_title="Simulation Under and Over 7", layout="wide")

# Initialisation des variables de session pour l'historique
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Lancer #", "Dé 1", "Dé 2", "Total", "Résultat"])

# --- FONCTIONS UTILES ---
def lancer_dés(n_lancers=1):
    lancers = []
    for _ in range(n_lancers):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        total = d1 + d2
        if total < 7:
            res = "Moins de 7"
        elif total == 7:
            res = "Égal à 7"
        else:
            res = "Plus de 7"
        lancers.append([d1, d2, total, res])
    return lancers

def ajouter_lancers(n_lancers):
    nouveaux = lancer_dés(n_lancers)
    for l in nouveaux:
        idx = len(st.session_state.history) + 1
        # Utilisation de pd.concat pour ajouter la ligne de manière propre
        nouvelle_ligne = pd.DataFrame([[idx, l[0], l[1], l[2], l[3]]], 
                                     columns=["Lancer #", "Dé 1", "Dé 2", "Total", "Résultat"])
        st.session_state.history = pd.concat([st.session_state.history, nouvelle_ligne], ignore_index=True)

# --- TITRE DE L'APPLICATION ---
st.title("🎲 Application de Simulation - Under and Over 7")
st.markdown("---")

# --- BARRE LATÉRALE : PARAMÈTRES ET SIMULATIONS DE MASSE ---
with st.sidebar:
    st.header("⚙️ Paramètres de Simulation")
    
    if st.button("🔄 Réinitialiser l'historique"):
        st.session_state.history = pd.DataFrame(columns=["Lancer #", "Dé 1", "Dé 2", "Total", "Résultat"])
        st.rerun()
        
    st.markdown("---")
    st.subheader("⚡ Simulation Intensive")
    st.write("Tester la précision des estimations expérimentales sur des lancers de masse :")
    
    taille_test = st.radio("Sélectionner le nombre de lancers pour le test :", [100, 500, 1000])
    
    if st.button(f"Lancer le test de {taille_test} simulations"):
        ajouter_lancers(taille_test)
        st.success(f"{taille_test} lancers ajoutés avec succès !")

# --- SECTION PRINCIPALE : LANCER DE DÉS MANUEL ---
col_action1, col_action2 = st.columns([1, 2])

with col_action1:
    st.subheader("🎲 Jouer un coup")
    if st.button("🎯 Générer un Nouveau Lancer", use_container_width=True):
        ajouter_lancers(1)

# --- CALCUL DES STATISTIQUES ---
df = st.session_state.history
total_lancers = len(df)

if total_lancers > 0:
    counts = df["Résultat"].value_counts()
    freq_moins = counts.get("Moins de 7", 0) / total_lancers
    freq_egal = counts.get("Égal à 7", 0) / total_lancers
    freq_plus = counts.get("Plus de 7", 0) / total_lancers
    
    # Trouver l'estimation expérimentale (la catégorie la plus fréquente)
    categories = {"Moins de 7": freq_moins, "Égal à 7": freq_egal, "Plus de 7": freq_plus}
    estimation_prochain = max(categories, key=categories.get)
    
    # Affichage du dernier lancer de dés
    dernier_lancer = df.iloc[-1]
    with col_action2:
        st.metric(
            label=f"Dernier Lancer (Total : {dernier_lancer['Total']})", 
            value=f"🎲 {dernier_lancer['Dé 1']}  +  🎲 {dernier_lancer['Dé 2']}  =  {dernier_lancer['Résultat']}"
        )
else:
    freq_moins = freq_egal = freq_plus = 0.0
    estimation_prochain = "Données insuffisantes"

# --- TABLEAU DE BORD STATISTIQUES ---
st.markdown("### 📊 Tableau de Bord Statistiques")
c1, c2, c3 = st.columns(3)
c1.metric("Fréquence Moins de 7", f"{freq_moins:.1%}")
c2.metric("Fréquence Égal à 7", f"{freq_egal:.1%}")
c3.metric("Fréquence Plus de 7", f"{freq_plus:.1%}")

# --- ESTIMATION EXPÉRIMENTALE & ATTENTION LÉGALE ---
st.markdown("### 🔮 Estimation pour le Prochain Lancer")
st.info(f"Sur la base de vos données actuelles ({total_lancers} lancers), la catégorie statistiquement la plus fréquente est : **{estimation_prochain}**")

# Message de prévention obligatoire
st.warning(
    "⚠️ **AVERTISSEMENT LÉGAL :** Cette estimation est basée uniquement sur des données historiques expérimentales. "
    "Elle n'est en aucun cas une prédiction fiable pour de futurs résultats réels. "
    "Le hasard n'a pas de mémoire (chaque lancer est indépendant). Ce simulateur **NE DOIT PAS** être utilisé "
    "pour parier de l'argent réel. Jouez de manière responsable."
)

# --- HISTORIQUE DES RÉSULTATS ---
st.markdown("### 🕒 Historique des Résultats Précédents")
if total_lancers > 0:
    # Affiche les lancers du plus récent au plus ancien
    st.dataframe(df.sort_index(ascending=False), use_container_width=True, height=250)
else:
    st.write("Aucun lancer enregistré pour le moment. Cliquez sur le bouton ci-dessus ou utilisez la simulation intensive.")
    
