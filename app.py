import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="Flight Data Analysis", layout="wide")

# =========================
# 1. LOAD DATA
# =========================
data = pd.read_csv("airlines_flights_data.csv")

data.drop(columns="index", inplace=True)

st.title("Flight Data Analysis Dashboard")

# --- Aperçu général ---
st.markdown("### Aperçu du dataset")

col_info, col_desc = st.columns(2)

with col_info:
    st.markdown("**Info**")
    buf = io.StringIO()
    data.info(buf=buf)
    st.text(buf.getvalue())

with col_desc:
    st.markdown("**Statistiques descriptives**")
    st.write(data.describe())

st.markdown("**Aperçu des premières lignes**")
st.dataframe(data.head())

st.markdown("---")

# =========================
# 2. DISTRIBUTIONS SIMPLES
# =========================
st.header("1. Distribution des vols")

# Departure time + Arrival time
col1, col2 = st.columns(2)

with col1:
    st.subheader("Departure time frequencies")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    ax1.bar(
        data["departure_time"].value_counts().index,
        data["departure_time"].value_counts().values,
        color=["lightblue", "lightgreen"],
    )
    ax1.set_xlabel("Departure time")
    ax1.set_ylabel("Freq")
    st.pyplot(fig1)

with col2:
    st.subheader("Arrival time frequencies")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.bar(
        data["arrival_time"].value_counts().index,
        data["arrival_time"].value_counts().values,
        color=["g", "y"],
    )
    ax2.set_xlabel("Arrival time")
    ax2.set_ylabel("Freq")
    st.pyplot(fig2)

# Source city + Destination city
col3, col4 = st.columns(2)

with col3:
    st.subheader("Source city frequencies")
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    ax3.bar(
        data["source_city"].value_counts().index,
        data["source_city"].value_counts().values,
        color=["lightblue", "lightgreen"],
    )
    ax3.set_xlabel("Source city")
    ax3.set_ylabel("Freq")
    st.pyplot(fig3)

with col4:
    st.subheader("Destination city frequencies")
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    ax4.bar(
        data["destination_city"].value_counts().index,
        data["destination_city"].value_counts().values,
        color=["g", "y"],
    )
    ax4.set_xlabel("Destination city")
    ax4.set_ylabel("Freq")
    st.pyplot(fig4)

st.markdown("---")


# =========================
# 3. PRICE ANALYSIS
# =========================
st.header("2. Analyse des prix")

# Prix moyen par airline + boxplot airline/class
col5, col6 = st.columns(2)

with col5:
    st.subheader("Average price by airline")
    mean_price_airline = data.groupby("airline")["price"].mean()
    st.write(mean_price_airline)

with col6:
    st.subheader("Price vs airline (Economy / Business)")
    g1 = sns.catplot(
        x="airline",
        y="price",
        kind="bar",
        palette="rocket",
        data=data,
        hue="class",
        height=4,
        aspect=1.2,
    )
    st.pyplot(g1.fig)

# Prix vs departure / arrival time
col7, col8 = st.columns(2)

with col7:
    st.subheader("Price vs departure time")
    g2 = sns.catplot(
        x="departure_time",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.2,
    )
    st.pyplot(g2.fig)

with col8:
    st.subheader("Price vs arrival time")
    g3 = sns.catplot(
        x="arrival_time",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.2,
    )
    st.pyplot(g3.fig)

# Small multiples arrival vs price by departure
st.subheader("Price vs arrival time by departure time")


g4 = sns.relplot(
    x="arrival_time",
    y="price",
    data=data,
    col="departure_time",
    kind="line",
    height=3,
    aspect=1.0,
)

st.pyplot(g4.fig)



# 3. Prix par villes et par jours restants
# =========================
st.header("3. Prix par villes et par nombre de jours restants")

col9, col10 = st.columns(2)

with col9:
    st.subheader("Prix par ville de départ")
    g5 = sns.catplot(
        x="source_city",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.2,
    )
    g5.set_xlabels("Source city")
    g5.set_ylabels("Average price")
    st.pyplot(g5.fig)

with col10:
    st.subheader("Prix par ville d’arrivée")
    g6 = sns.catplot(
        x="destination_city",
        y="price",
        kind="bar",
        palette="deep",
        data=data,
        height=4,
        aspect=1.2,
    )
    g6.set_xlabels("Destination city")
    g6.set_ylabels("Average price")
    st.pyplot(g6.fig)

st.subheader("Prix en fonction du nombre de jours restants avant le départ")

fig_days, ax_days = plt.subplots(figsize=(6, 4))
sns.lineplot(x="days_left", y="price", data=data, ax=ax_days)
ax_days.set_xlabel("Jours restants avant le départ")
ax_days.set_ylabel("Prix du billet")
st.pyplot(fig_days)
