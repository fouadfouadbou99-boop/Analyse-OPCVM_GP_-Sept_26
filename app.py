import streamlit as st
import pandas as pd
from io import BytesIO

# ======================================================
# CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="OPCVM Analytics",
    page_icon="📈",
    layout="wide"
)

# ======================================================
# TITRE
# ======================================================

st.title("📈 OPCVM Analytics")

st.markdown("""
### Tableau de bord OPCVM Actions

- Performance YTD
- Performance annualisée
- Sharpe
- Treynor
- Information Ratio
- Classement
""")

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:
    st.header("Paramètres")
    st.metric("Taux sans risque", "2.25 %")

# ======================================================
# IMPORT
# ======================================================

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

# ======================================================
# ANALYSE
# ======================================================

if uploaded_file:

    try:

        metrics = pd.read_excel(
            uploaded_file,
            sheet_name="Metrics",
            header=None
        )

        nb_cols = metrics.shape[1]

        funds = metrics.iloc[1, 1:nb_cols].tolist()

        perf_ytd = pd.to_numeric(
            metrics.iloc[2, 1:nb_cols],
            errors="coerce"
        )

        perf_ann = pd.to_numeric(
            metrics.iloc[3, 1:nb_cols],
            errors="coerce"
        )

        vol = pd.to_numeric(
            metrics.iloc[4, 1:nb_cols],
            errors="coerce"
        )

        te = pd.to_numeric(
            metrics.iloc[6, 1:nb_cols],
            errors="coerce"
        )

        sharpe = pd.to_numeric(
            metrics.iloc[7, 1:nb_cols],
            errors="coerce"
        )

        beta = pd.to_numeric(
            metrics.iloc[8, 1:nb_cols],
            errors="coerce"
        )

        treynor = pd.to_numeric(
            metrics.iloc[9, 1:nb_cols],
            errors="coerce"
        )

        ir = pd.to_numeric(
            metrics.iloc[10, 1:nb_cols],
            errors="coerce"
        )

        var95 = pd.to_numeric(
            metrics.iloc[11, 1:nb_cols],
            errors="coerce"
        )

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

        ranking = ranking.dropna(subset=["Fonds"])

        ranking = ranking.sort_values(
            by="Perf YTD",
            ascending=False
        )

        ranking["Rang"] = range(
            1,
            len(ranking) + 1
        )

        # ==================================================
        # KPI
        # ==================================================

        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🏆 Meilleur OPCVM",
            str(ranking.iloc[0]["Fonds"])
        )

        c2.metric(
            "📈 Performance Max",
            f"{ranking['Perf YTD'].max():.2%}"
        )

        c3.metric(
            "📊 Sharpe Max",
            f"{ranking['Sharpe'].max():.2f}"
        )

        c4.metric(
            "🎯 IR Max",
            f"{ranking['IR'].max():.2f}"
        )

        # ==================================================
        # TOP 3
        # ==================================================

        st.markdown("---")

        st.subheader("🥇 Top 3 OPCVM")

        top3 = ranking.head(3)

        cols = st.columns(3)

        for col, (_, row) in zip(cols, top3.iterrows()):
            col.metric(
                f"#{int(row['Rang'])} {row['Fonds']}",
                f"{row['Perf YTD']:.2%}"
            )

        # ==================================================
        # CLASSEMENT
        # ==================================================

        st.markdown("---")

        st.subheader("🏆 Classement")

        display_df = ranking.copy()

        display_df["Perf YTD"] = display_df["Perf YTD"].map(lambda x: f"{x:.2%}")
        display_df["Perf Annualisée"] = display_df["Perf Annualisée"].map(lambda x: f"{x:.2%}")
        display_df["Volatilité"] = display_df["Volatilité"].map(lambda x: f"{x:.2%}")
        display_df["Tracking Error"] = display_df["Tracking Error"].map(lambda x: f"{x:.2%}")
        display_df["Treynor"] = display_df["Treynor"].map(lambda x: f"{x:.2%}")
        display_df["VaR95"] = display_df["VaR95"].map(lambda x: f"{x:.2%}")
        display_df["Sharpe"] = display_df["Sharpe"].map(lambda x: f"{x:.2f}")
        display_df["IR"] = display_df["IR"].map(lambda x: f"{x:.2f}")
        display_df["Beta"] = display_df["Beta"].map(lambda x: f"{x:.2f}")

        st.dataframe(
            display_df,
            use_container_width=True
        )

        # ==================================================
        # EXPORT EXCEL
        # ==================================================

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="xlsxwriter"
        ) as writer:

            ranking.to_excel(
                writer,
                sheet_name="Classement",
                index=False
            )

        st.download_button(
            label="📥 Télécharger Excel",
            data=output.getvalue(),
            file_name="Classement_OPCVM.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Analyse terminée.")

    except Exception as e:
        st.error(f"Erreur : {e}")
