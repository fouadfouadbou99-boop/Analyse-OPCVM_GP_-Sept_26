import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ----------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="OPCVM Analytics",
    page_icon="📈",
    layout="wide"
)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("📈 OPCVM Analytics")

st.markdown("""
Tableau de bord de suivi des OPCVM Actions

• Performance  
• Risque  
• Sharpe  
• Treynor  
• Information Ratio  
• Export Excel  
• Export PDF
""")

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.header("Paramètres")

    st.metric(
        "Taux sans risque",
        "2.25 %"
    )

# ----------------------------------------------------
# IMPORT EXCEL
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

# ----------------------------------------------------
# TRAITEMENT
# ----------------------------------------------------

if uploaded_file:

    metrics = pd.read_excel(
        uploaded_file,
        sheet_name="Metrics",
        header=None
    )

    # --------------------------------------------
    # LECTURE DES METRIQUES
    # --------------------------------------------

    funds = metrics.iloc[1, 1:16].tolist()

    perf_ytd = metrics.iloc[2, 1:16].astype(float)

    perf_ann = metrics.iloc[3, 1:16].astype(float)

    vol = metrics.iloc[4, 1:16].astype(float)

    rf = metrics.iloc[5, 1:16].astype(float)

    te = metrics.iloc[6, 1:16].astype(float)

    sharpe = metrics.iloc[7, 1:16].astype(float)

    beta = metrics.iloc[8, 1:16].astype(float)

    treynor = metrics.iloc[9, 1:16].astype(float)

    ir = metrics.iloc[10, 1:16].astype(float)

    var95 = metrics.iloc[11, 1:16].astype(float)

    # --------------------------------------------
    # TABLEAU
    # --------------------------------------------

    ranking = pd.DataFrame({

        "Fonds": funds,
        "Perf YTD": perf_ytd,
        "Perf Annualisée": perf_ann,
        "Volatilité": vol,
        "Tracking Error": te,
        "Sharpe": sharpe,
        "Beta": beta,
        "Treynor": treynor,
        "IR": ir,
        "VaR95": var95

    })

    # --------------------------------------------
    # SCORE GLOBAL
    # --------------------------------------------

    ranking["Score"] = (

        ranking["Perf YTD"].rank(pct=True) * 0.50 +

        ranking["Sharpe"].rank(pct=True) * 0.30 +

        ranking["IR"].rank(pct=True) * 0.20

    )

    ranking = ranking.sort_values(
        "Score",
        ascending=False
    )

    ranking["Rang"] = range(
        1,
        len(ranking) + 1
    )

    # --------------------------------------------
    # KPI
    # --------------------------------------------

    best_fund = ranking.iloc[0]["Fonds"]

    best_perf = ranking["Perf YTD"].max()

    best_sharpe = ranking["Sharpe"].max()

    best_ir = ranking["IR"].max()

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🏆 Meilleur OPCVM",
        best_fund
    )

    c2.metric(
        "📈 Performance Max",
        f"{best_perf:.2%}"
    )

    c3.metric(
        "📊 Sharpe Max",
        f"{best_sharpe:.2f}"
    )

    c4.metric(
        "🎯 IR Max",
        f"{best_ir:.2f}"
    )

    # --------------------------------------------
    # TOP 3
    # --------------------------------------------

    st.markdown("---")

    st.subheader("🥇 Top 3 OPCVM")

    top3 = ranking.head(3)

    col1, col2, col3 = st.columns(3)

    for col, (_, row) in zip(
        [col1, col2, col3],
        top3.iterrows()
    ):

        col.metric(
            label=f"#{row['Rang']} {row['Fonds']}",
            value=f"{row['Perf YTD']:.2%}"
        )

    # --------------------------------------------
    # TABLEAU FORMATÉ
    # --------------------------------------------

    ranking_display = ranking.copy()

    for col in [
        "Perf YTD",
        "Perf Annualisée",
        "Volatilité",
        "Tracking Error",
        "Treynor",
        "VaR95"
    ]:

        ranking_display[col] = ranking_display[col].map(
            lambda x: f"{x:.2%}"
        )

    for col in [
        "Sharpe",
        "IR",
        "Beta",
        "Score"
    ]:

        ranking_display[col] = ranking_display[col].map(
            lambda x: f"{x:.2f}"
        )

    st.markdown("---")

    st.subheader("🏆 Classement")

    st.dataframe(
        ranking_display,
        width="stretch"
    )

    # ------
