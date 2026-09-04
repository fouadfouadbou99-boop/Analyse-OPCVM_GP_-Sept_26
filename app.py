import streamlit as st
import pandas as pd
from io import BytesIO

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
Tableau de bord OPCVM Actions

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

    st.metric(
        "Taux sans risque",
        "2.25 %"
    )

# ======================================================
# IMPORT
# ======================================================

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

# ======================================================
# LECTURE
# ======================================================

if uploaded_file:

    metrics = pd.read_excel(
        uploaded_file,
        sheet_name="Metrics",
        header=None
    )

    funds = metrics.iloc[1, 1:16].tolist()

    perf_ytd = metrics.iloc[2, 1:16].astype(float)

    perf_ann = metrics.iloc[3, 1:16].astype(float)

    vol = metrics.iloc[4, 1:16].astype(float)

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

    ranking = ranking.sort_values(
        "Perf YTD",
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
        ranking.iloc[0]["Fonds"]
    )

    c2.metric(
        "📈 Performance Max",
        "{:.2%}".format(
            ranking["Perf YTD"].max()
        )
    )

    c3.metric(
        "📊 Sharpe Max",
        "{:.2f}".format(
            ranking["Sharpe"].max()
        )
    )

    c4.metric(
        "🎯 IR Max",
        "{:.2f}".format(
            ranking["IR"].max()
        )
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

            "#{} {}".format(
                int(row["Rang"]),
                row["Fonds"]
            ),

            "{:.2%}".format(
                row["Perf YTD"]
            )
        )

    # ==================================================
    # CLASSEMENT
    # ==================================================

    st.markdown("---")

    st.subheader("🏆 Classement")

    display_df = ranking.copy()

    display_df["Perf YTD"] = display_df["Perf YTD"].apply(
        lambda x: "{:.2%}".format(x)
    )

    display_df["Perf Annualisée"] = display_df["Perf Annualisée"].apply(
        lambda x: "{:.2%}".format(x)
    )

    display_df["Volatilité"] = display_df["Volatilité"].apply(
        lambda x: "{:.2%}".format(x)
    )

    display_df["Tracking Error"] = display_df["Tracking Error"].apply(
        lambda x: "{:.2%}".format(x)
    )

    display_df["Treynor"] = display_df["Treynor"].apply(
        lambda x: "{:.2%}".format(x)
    )

    display_df["VaR95"] = display_df["VaR95"].apply(
        lambda x: "{:.2%}".format(x)
    )

    display_df["Sharpe"] = display_df["Sharpe"].apply(
        lambda x: "{:.2f}".format(x)
    )

    display_df["IR"] = display_df["IR"].apply(
        lambda x: "{:.2f}".format(x)
    )

    display_df["Beta"] = display_df["Beta"].apply(
        lambda x: "{:.2f}".format(x)
    )

    st.dataframe(
        display_df,
        width="stretch"
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
