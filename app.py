import streamlit as st

st.set_page_config(
    page_title="OPCVM Analytics",
    layout="wide"
)

st.title("OPCVM Analytics")

st.markdown("""
Application d'analyse des OPCVM actions :

- Performance YTD
- Performance annualisée
- Volatilité annualisée
- Tracking Error
- Sharpe
- Treynor
- Information Ratio
- VaR 95%
- Max Drawdown
""")
