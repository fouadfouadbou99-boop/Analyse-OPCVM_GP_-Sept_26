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

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="OPCVM Analytics",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📈 OPCVM Analytics")

st.markdown(
"""
Tableau de bord de suivi des OPCVM Actions

- Performance
- Risque
- Sharpe
- Treynor
- Information Ratio
- Export Excel
- Export PDF
"""
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Paramètres")

    st.metric(
        "Taux sans risque",
        "2.25 %"
    )

# --------------------------------------------------
# UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type="xlsx"
)

# --------------------------------------------------
# PROCESS
# --------------------------------------------------

if uploaded_file:

    metrics = pd.read_excel(
        uploaded_file,
        sheet_name="Metrics",
        header=None
    )

    funds = metrics.iloc[1,1:16].tolist()

    perf_ytd = metrics.iloc[2,1:16].astype(float)

    perf_ann = metrics.iloc[3,1:16].astype(float)

    vol = metrics.iloc[4,1:16].astype(float)

    te = metrics.iloc[5,1:16].astype(float)

    sharpe = metrics.iloc[6,1:16].astype(float)

    beta = metrics.iloc[7,1:16].astype(float)

    treynor = metrics.iloc[8,1:16].astype(float)

    ir = metrics.iloc[9,1:16].astype(float)

    var95 = metrics.iloc[10,1:16].astype(float)

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

    ranking["Rang"] = ranking["Perf YTD"].rank(
        ascending=False,
        method="dense"
    )

    ranking = ranking.sort_values(
        "Rang"
    )

    # ------------------------------------------
    # KPI
    # ------------------------------------------

    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "🏆 Meilleur Fonds",
        ranking.iloc[0]["Fonds"]
    )

    c2.metric(
        "Performance Max",
        f"{ranking['Perf YTD'].max():.2%}"
    )

    c3.metric(
        "Sharpe Max",
        f"{ranking['Sharpe'].max():.2f}"
    )

    c4.metric(
        "Nombre OPCVM",
        len(ranking)
    )

    # ------------------------------------------
    # TOP 3
    # ------------------------------------------

    st.markdown("---")

    st.subheader("🏅 Top 3 OPCVM")

    top3 = ranking.head(3)

    cols = st.columns(3)

    for idx,row in top3.iterrows():

        cols[int(row["Rang"])-1].metric(
            row["Fonds"],
            f"{row['Perf YTD']:.2%}"
        )

    # ------------------------------------------
    # CLASSEMENT
    # ------------------------------------------

    st.markdown("---")

    st.subheader("🏆 Classement")

    st.dataframe(
        ranking,
        width="stretch"
    )

    # ------------------------------------------
    # PERFORMANCE
    # ------------------------------------------

    st.subheader("📈 Performance YTD")

    fig_perf = px.bar(
        ranking,
        x="Fonds",
        y="Perf YTD",
        color="Perf YTD",
        text_auto=".2%"
    )

    st.plotly_chart(
        fig_perf,
        width="stretch"
    )

    # ------------------------------------------
    # SHARPE
    # ------------------------------------------

    st.subheader("📊 Ratio
