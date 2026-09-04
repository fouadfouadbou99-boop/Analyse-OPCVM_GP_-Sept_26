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

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="OPCVM Analytics",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📈 OPCVM Analytics")

    st.markdown("---")

    st.subheader("Paramètres")

    st.metric(
        "Taux sans risque",
        "2.25 %"
    )

# =====================================================
# HEADER
# =====================================================

st.title("📈 OPCVM Analytics")

st.markdown("""
### Tableau de bord OPCVM Actions

- Performance
- Risque
- Sharpe
- Treynor
- Information Ratio
- Export Excel
- Export PDF
""")

# =====================================================
# UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

# =====================================================
# PROCESS
# =====================================================

if uploaded_file:

    metrics = pd.read_excel(
        uploaded_file,
        sheet_name="Metrics",
        header=None
    )

    # =================================================
    # EXTRACTION METRICS
    # =================================================

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

    # =================================================
    # SCORE GLOBAL
    # =================================================

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
        len(ranking)+1
    )

    # =================================================
    # KPI
    # =================================================

    st.markdown("---")

    best_fund = ranking.iloc[0]["Fonds"]

    best_perf = ranking["Perf YTD"].max()

    best_sharpe = ranking["Sharpe"].max()

    best_ir = ranking["IR"].max()

    c1,c2,c3,c4 = st.columns(4)

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

    # =================================================
    # TOP 3
    # =================================================

    st.markdown("---")

    st.subheader("🥇 Top 3 OPCVM")

    top3 = ranking.head(3)

    cols = st.columns(3)

    for col, (_, row) in zip(
        cols,
        top3.iterrows()
    ):

        col.metric(
            f"#{row['Rang']} {row['Fonds']}",
            f"{row['Perf YTD']:.2%}"
        )

   ranking_display = ranking.copy()

ranking_display = ranking_display[
    [
        "Rang",
        "Fonds",
        "Perf YTD",
        "Perf Annualisée",
        "Volatilité",
        "Sharpe",
        "Treynor",
        "IR"
    ]
]

ranking_display["Perf YTD"] = ranking_display["Perf YTD"].apply(
    lambda x: "{:.2%}".format(x)
)

ranking_display["Perf Annualisée"] = ranking_display["Perf Annualisée"].apply(
    lambda x: "{:.2%}".format(x)
)

ranking_display["Volatilité"] = ranking_display["Volatilité"].apply(
    lambda x: "{:.2%}".format(x)
)

ranking_display["Treynor"] = ranking_display["Treynor"].apply(
    lambda x: "{:.2%}".format(x)
)

ranking_display["Sharpe"] = ranking_display["Sharpe"].apply(
    lambda x: "{:.2f}".format(x)
)

ranking_display["IR"] = ranking_display["IR"].apply(
    lambda x: "{:.2f}".format(x)
)

st.dataframe(
    ranking_display,
    width="stretch"
)
