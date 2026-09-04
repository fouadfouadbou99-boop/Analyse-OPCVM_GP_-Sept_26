import streamlit as st
import pandas as pd

st.title("Diagnostic Data_Analysis")

file = st.file_uploader("Excel", type=["xlsx"])

if file:

    df = pd.read_excel(
        file,
        sheet_name="Data_Analysis",
        header=None
    )

    st.write("Dimensions :", df.shape)

    st.dataframe(df.head(20))
