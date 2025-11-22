import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Flight Data Analysis Dashboard",
    layout="wide",
)

# =========================
# 1. CHARGEMENT DES DONNÉES
# =========================
data = pd.read_csv("airlines_flights_data.csv")
data.drop(columns="index", inplace=True)

st.title("Flight Data Analysis Dashboard")

# ---- KPIs ----
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric("Nombre total de vols", f"{len(data):,}".replace(",", " "))
with col_kpi2:
    st.metric("Compagnies aériennes", data["airline"].nunique())
with col_kpi3:
    st.metric("Villes (source / destination)",
              f"{data['source_city'].nunique()} / {data['destination_city'].nunique()}")

# ---- Sidebar ----
st.sidebar.title("À propos du projet")
st.sidebar.write(
    """
Dashboard interactif d’analyse des vols :

- Python (pandas, seaborn, matplotlib)
- Streamlit
- Dataset : réservations de vols (Inde)
"""
)
st.sidebar.write("Lien public de l'application :")
st.sidebar.code("https://flight-analysis-kenza-yqiudzr7dd7rkkqe3ygr9b.streamlit.app")

# ---- Aperçu dataset ----
st.markdown("### Aperçu du dataset")

with st.expander("Afficher les informations détaillées"):
    col_info, col_desc = st.columns(2)

    with col_info:
        st.markdown("**Info**")
        buf = io.StringIO()
        data.info(buf=buf)
        st.text(buf.getvalue())

    with col_desc:
        st.markdown("**Statistiques descriptives**")
        st.write(data[["duration", "days_left", "price"]].describe())

st.markdown("**Aperçu des premières lignes**")
st.dataframe(data.head())

st.markdown("---")

# =========================
# 2. DISTRIBUTION DES VOLS
# =========================
st.header("1. Distribution des vols")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fréquences des horaires de départ")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    dep_counts = data["departure_time"].value_counts()
    ax1.bar(dep_counts.index, dep_counts.values,
            color=["#4c72b0", "#55a868", "#4c72b0", "#c44e52", "#8172b3", "#ccb974"])
    plt.xticks(rotation=20)
    st.pyplot(fig1)

with col2:
    st.subheader("Fréquences des horaires d'arrivée")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    arr_counts = data["arrival_time"].value_counts()
    ax2.bar(arr_counts.index, arr_counts.values,
            color=["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b3", "#937860"])
    plt.xticks(rotation=20)
    st.pyplot(fig2)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Villes de départ – fréquences")
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    src_counts = data["source_city"].value_counts()
    ax3.bar(src_counts.index, src_counts.values,
            color=["#4c72b0", "#55a868", "#4c72b0", "#c44e52", "#8172b3", "#ccb974"])
    plt.xticks(rotation=20)
    st.pyplot(fig3)

with col4:
    st.subheader("Villes d’arrivée – fréquences")
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    dst_counts = data["destination_city"].value_counts()
    ax4.bar(dst_counts.index, dst_counts.values,
            color=["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b3", "#937860"])
    plt.xticks(rotation=20)
    st.pyplot(fig4)

st.markdown("---")

# =========================
# 3. ANALYSE DES PRIX
# =========================
st.header("2. Analyse des prix")

col5, col6 = st.columns(2)

with col5:
    st.subheader("Prix moyen par compagnie")
    mean_price_airline = data.groupby("airline")["price"].mean().round(2)
    st.dataframe(mean_price_airline.reset_index())

with col6:
    st.subheader("Prix par compagnie et classe")
    g1 = sns.catplot(
        x="airline",
        y="price",
        kind="bar",
        palette="rocket",
        data=data,
        hue="class",
        height=4,
        aspect=1.5,
    )
    plt.xticks(rotation=20)
    st.pyplot(g1.fig)

col7, col8 = st.columns(2)

with col7:
    st.subheader("Prix par horaire de départ")
    g2 = sns.catplot(
        x="departure_time",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.3,
    )
    plt.xticks(rotation=20)
    st.pyplot(g2.fig)

with col8:
    st.subheader("Prix par horaire d'arrivée")
    g3 = sns.catplot(
        x="arrival_time",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.3,
    )
    plt.xticks(rotation=20)
    st.pyplot(g3.fig)

st.subheader("Prix vs horaire d’arrivée selon le créneau de départ")
g4 = sns.relplot(
    x="arrival_time",
    y="price",
    data=data,
    col="departure_time",
    kind="line",
    height=3,
    aspect=1,
)
st.pyplot(g4.fig)

st.markdown("---")

# =========================
# 4. PRIX PAR VILLES & JOURS RESTANTS
# =========================
st.header("3. Prix par villes et par nombre de jours restants")

col9, col10 = st.columns(2)

with col9:
    st.subheader("Prix moyen par ville de départ")
    g5 = sns.catplot(
        x="source_city",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.3,
    )
    plt.xticks(rotation=20)
    st.pyplot(g5.fig)

with col10:
    st.subheader("Prix moyen par ville d’arrivée")
    g6 = sns.catplot(
        x="destination_city",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.3,
    )
    plt.xticks(rotation=20)
    st.pyplot(g6.fig)

st.subheader("Prix en fonction du nombre de jours restants avant départ")
fig_days, ax_days = plt.subplots(figsize=(8, 4))
sns.lineplot(x="days_left", y="price", data=data, ax=ax_days)
st.pyplot(fig_days)

st.markdown("---")

# =========================
# 5. ECONOMY VS BUSINESS
# =========================
st.header("4. Comparaison Economy vs Business et cas Vistara")

col11, col12 = st.columns(2)

with col11:
    st.subheader("Prix moyen par classe")
    eco = data[data["class"] == "Economy"]
    bus = data[data["class"] == "Business"]

    st.metric("Economy", f"{eco['price'].mean():,.0f}".replace(",", " "))
    st.metric("Business", f"{bus['price'].mean():,.0f}".replace(",", " "))

with col12:
    st.subheader("Cas spécifique : Vistara, Delhi → Hyderabad (Business)")
    new_data = data[
        (data["airline"] == "Vistara")
        & (data["source_city"] == "Delhi")
        & (data["destination_city"] == "Hyderabad")
        & (data["class"] == "Business")
    ]
    st.write(new_data)

    if not new_data.empty:
        st.metric("Prix moyen", f"{new_data['price'].mean():,.0f}".replace(",", " "))
    else:
        st.info("Aucun vol trouvé pour ce filtre.")
