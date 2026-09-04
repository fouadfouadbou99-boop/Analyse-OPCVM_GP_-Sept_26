import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors

st.set_page_config(
    page_title="OPCVM Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Tableau de Bord OPCVM")

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    xls = pd.ExcelFile(uploaded_file)

    st.success(
        f"{len(xls.sheet_names)} feuilles détectées"
    )

    metrics = pd.read_excel(
        uploaded_file,
        sheet_name="Metrics",
        header=None
    )

    funds = metrics.iloc[1,1:16].tolist()

    perf_ytd = metrics.iloc[2,1:16].astype(float).tolist()

    perf_ann = metrics.iloc[3,1:16].astype(float).tolist()

    vol = metrics.iloc[4,1:16].astype(float).tolist()

    te = metrics.iloc[6,1:16].astype(float).tolist()

    sharpe = metrics.iloc[7,1:16].astype(float).tolist()

    beta = metrics.iloc[8,1:16].astype(float).tolist()

    treynor = metrics.iloc[9,1:16].astype(float).tolist()

    ir = metrics.iloc[10,1:16].astype(float).tolist()

    var95 = metrics.iloc[11,1:16].astype(float).tolist()

    ranking = pd.DataFrame(
        {
            "Fonds": funds,
            "Perf YTD": perf_ytd,
            "Perf Annualisée": perf_ann,
            "Volatilité": vol,
            "Tracking Error": te,
            "Sharpe": sharpe,
            "Beta": beta,
            "Treynor": treynor,
            "IR": ir,
            "VaR 95%": var95
        }
    )

    ranking["Rang"] = (
        ranking["Perf YTD"]
        .rank(
            ascending=False,
            method="dense"
        )
    )

    ranking = ranking.sort_values(
        "Rang"
    )

    meilleur_fonds = ranking.iloc[0]["Fonds"]

    perf_max = ranking["Perf YTD"].max()

    sharpe_max = ranking["Sharpe"].max()

    nb_fonds = len(ranking)

    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "🏆 Meilleur Fonds",
        meilleur_fonds
    )

    c2.metric(
        "Performance Max",
        f"{perf_max:.2%}"
    )

    c3.metric(
        "Sharpe Max",
        f"{sharpe_max:.2f}"
    )

    c4.metric(
        "Nombre de Fonds",
        nb_fonds
    )

    st.markdown("---")

    st.subheader("🏆 Classement OPCVM")

    st.dataframe(
        ranking,
        use_container_width=True
    )

    st.subheader(
        "📊 Classement par Performance"
    )

    fig1 = px.bar(
        ranking,
        x="Fonds",
        y="Perf YTD",
        color="Perf YTD"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader(
        "📊 Ratio de Sharpe"
    )

    fig2 = px.bar(
        ranking,
        x="Fonds",
        y="Sharpe",
        color="Sharpe"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader(
        "📊 Risk / Return"
    )

    fig3 = px.scatter
