import streamlit as st
import yfinance as yf

st.title("M&A Intelligence Platform")
st.subheader("Company Financial Overview")

search_query = st.text_input("Search company by name (e.g. Apple, Microsoft, Tesla)")

if search_query:
    results = yf.Search(search_query).quotes
    us_results = [r for r in results if r.get('exchDisp') in ['NASDAQ', 'NYSE']]

    if not us_results:
        st.warning("No US listed companies found. Try a different name.")
    else:
        options = {f"{r.get('longname')} ({r.get('symbol')}) — {r.get('exchDisp')}": r.get('symbol') for r in us_results}
        selected = st.selectbox("Select a company", list(options.keys()))
        ticker = options[selected]

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
        wanted = ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EBITDA']
        available = [m for m in wanted if m in income_statement.index]
        key_metrics = income_statement.loc[available]
        key_metrics_clean = key_metrics.iloc[:, :4] / 1e9
        key_metrics_clean = key_metrics_clean.round(2)

        st.dataframe(key_metrics_clean)

        st.subheader("Revenue & Net Income Trend")

        chart_data = key_metrics_clean.T
        chart_data.index = [str(col)[:4] for col in chart_data.index]

        st.line_chart(chart_data[['Total Revenue', 'Net Income']])