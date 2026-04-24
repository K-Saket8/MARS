import streamlit as st
import yfinance as yf

st.title("M&A Intelligence Platform")
st.subheader("Company Financial Overview")

ticker = st.text_input("Enter company ticker (e.g. AAPL, MSFT, GOOGL)")

if ticker:
    company = yf.Ticker(ticker)
    info = company.info

    st.write("**Company:**", info.get('longName'))
    st.write("**Sector:**", info.get('sector'))
    st.write("**Industry:**", info.get('industry'))
    st.write("**Website:**", info.get('website'))
    st.write("**Employees:**", info.get('fullTimeEmployees'))
    st.write("**Description:**", info.get('longBusinessSummary'))

    st.subheader("Key Financials (in USD Billions)")

    income_statement = company.financials
    key_metrics = income_statement.loc[['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EBITDA']]
    key_metrics_clean = key_metrics.iloc[:, :4] / 1e9
    key_metrics_clean = key_metrics_clean.round(2)

    st.dataframe(key_metrics_clean)

    st.subheader("Revenue & Net Income Trend")

    chart_data = key_metrics_clean.T
    chart_data.index = [str(col)[:4] for col in chart_data.index]

    st.line_chart(chart_data[['Total Revenue', 'Net Income']])