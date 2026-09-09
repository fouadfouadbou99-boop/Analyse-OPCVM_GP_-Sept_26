import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="OPCVM Analytics",
    page_icon="📈",
    layout="wide"
)

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

with st.sidebar:
    st.header("Paramètres")
    st.metric("Taux sans risque", "2.25 %")

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        metrics = pd.read_excel(
            uploaded_file,
            sheet_name="Metrics"
        )

        funds = metrics.columns[1:].tolist()

        perf_ytd = pd.to_numeric(
            metrics.iloc[0, 1:],
            errors="coerce"
        )

        perf_ann = pd.to_numeric(
            metrics.iloc[1, 1:],
            errors="coerce"
        )

        vol = pd.to_numeric(
            metrics.iloc[2, 1:],
            errors="coerce"
        )

        te = pd.to_numeric(
            metrics.iloc[4, 1:],
            errors="coerce"
        )

        sharpe = pd.to_numeric(
            metrics.iloc[5, 1:],
            errors="coerce"
        )

        beta = pd.to_numeric(
            metrics.iloc[6, 1:],
            errors="coerce"
        )

        treynor = pd.to_numeric(
            metrics.iloc[7, 1:],
            errors="coerce"
        )

        ir = pd.to_numeric(
            metrics.iloc[8, 1:],
            errors="coerce"
        )

        var95 = pd.to_numeric(
            metrics.iloc[9, 1:],
            errors="coerce"
        )

        ranking = pd.DataFrame({
            "Fonds": funds,
            "Perf YTD": perf_ytd.values,
            "Perf Annualisée": perf_ann.values,
            "Volatilité": vol.values,
            "Tracking Error": te.values,
            "Sharpe": sharpe.values,
            "Beta": beta.values,
            "Treynor": treynor.values,
            "IR": ir.values,
            "VaR95": var95.values
        })

        ranking = ranking.sort_values(
            by="Perf YTD",
            ascending=False
        ).reset_index(drop=True)

        ranking["Rang"] = ranking.index + 1

        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🏆 Meilleur OPCVM",
            ranking.iloc[0]["Fonds"]
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

        st.markdown("---")
        st.subheader("🥇 Top 3 OPCVM")

        top3 = ranking.head(3)

        cols = st.columns(3)

        for col, (_, row) in zip(cols, top3.iterrows()):
            col.metric(
                f"#{row['Rang']} {row['Fonds']}",
                f"{row['Perf YTD']:.2%}"
            )

        st.markdown("---")
        st.subheader("🏆 Classement")

        display_df = ranking.copy()

        for col in [
            "Perf YTD",
            "Perf Annualisée",
            "Volatilité",
            "Tracking Error",
            "Treynor",
            "VaR95"
        ]:
            display_df[col] = display_df[col].apply(
                lambda x: f"{x:.2%}"
            )

        for col in [
            "Sharpe",
            "IR",
            "Beta"
        ]:
            display_df[col] = display_df[col].apply(
                lambda x: f"{x:.2f}"
            )

        st.dataframe(
            display_df,
            width="stretch"
        )

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
            "📥 Télécharger Excel",
            data=output.getvalue(),
            file_name="Classement_OPCVM.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Analyse terminée.")

    except Exception as e:
        st.error(f"Erreur : {e}")
