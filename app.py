import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Diagnostic OPCVM")

uploaded_file = st.file_uploader(
    "Importer le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    xls = pd.ExcelFile(uploaded_file)

    st.write("Feuilles trouvées :")
    st.write(xls.sheet_names)

    df = pd.read_excel(
        uploaded_file,
        sheet_name="Data_Analysis",
        header=None
    )

    st.write("Dimensions :", df.shape)

    st.subheader("20 premières lignes")

    st.dataframe(
        df.head(20).astype(str),
        width="stretch"
    )
