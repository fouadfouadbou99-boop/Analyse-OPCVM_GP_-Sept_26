import streamlit as st
import pandas as pd

st.title("Analyse OPCVM")

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    xls = pd.ExcelFile(uploaded_file)

    st.success(
        f"{len(xls.sheet_names)} feuilles détectées"
    )

    for sheet in xls.sheet_names:

        st.subheader(sheet)

        df = pd.read_excel(
            uploaded_file,
            sheet_name=sheet
        )

        st.dataframe(df)
