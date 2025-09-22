# app.py
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

@st.cache_data(ttl=3600)
def fetch_countries():
    """Fetch country-level current COVID data from disease.sh"""
    url = "https://disease.sh/v3/covid-19/countries"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data)
    # pick and prepare useful columns
    cols = ['country','countryInfo','continent','cases','todayCases','deaths','todayDeaths',
            'recovered','active','population','tests','updated']
    df = df[[c for c in cols if c in df.columns]]
    df['updated'] = pd.to_datetime(df['updated'], unit='ms')
    df['iso2'] = df['countryInfo'].apply(lambda x: x.get('iso2') if isinstance(x, dict) else None)
    return df

@st.cache_data(ttl=3600)
def fetch_historical(country, lastdays=180):
    """Fetch historical data for a country (cases/deaths/recovered)."""
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays={lastdays}"
    resp = requests.get(url, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    timeline = data.get('timeline') or {}
    cases = timeline.get('cases', {})
    deaths = timeline.get('deaths', {})
    recovered = timeline.get('recovered', {})
    df = pd.DataFrame({
        'date': pd.to_datetime(list(cases.keys())),
        'cases': list(cases.values()),
        'deaths': list(deaths.values()),
        'recovered': list(recovered.values())
    }).sort_values('date')
    df.set_index('date', inplace=True)
    return df

def main():
    st.title("COVID-19 Data Visualization Dashboard")
    st.markdown("**Data source:** disease.sh (free public API)")

    df = fetch_countries()

    st.sidebar.header("Controls")
    continents = ['All'] + sorted(df['continent'].dropna().unique().tolist())
    sel_cont = st.sidebar.selectbox("Continent", continents)
    metric = st.sidebar.selectbox("Metric", ['cases','deaths','recovered','active'])
    top_n = st.sidebar.slider("Top N countries", 5, 20, 10)

    if sel_cont != 'All':
        dff = df[df['continent'] == sel_cont].copy()
    else:
        dff = df.copy()

    dff_sorted = dff.sort_values(metric, ascending=False).head(top_n)

    # Bar chart (top countries)
    fig = px.bar(dff_sorted, x='country', y=metric, title=f"Top {top_n} countries by {metric}")
    st.plotly_chart(fig, use_container_width=True)

    # Show table
    st.subheader("Top countries (table)")
    st.dataframe(dff_sorted[['country','iso2','continent','population',metric,'todayCases','todayDeaths']])

    # Download CSV
    csv = dff_sorted.to_csv(index=False)
    st.download_button("Download CSV (top countries)", csv, file_name="covid_top_countries.csv", mime="text/csv")

    st.markdown("---")
    st.header("Country historical trend")
    country = st.selectbox("Select a country for historical trend", options=sorted(df['country'].tolist()))
    if country:
        try:
            hist = fetch_historical(country)
            fig2 = px.line(hist, y='cases', title=f"Confirmed cases in {country} (last {hist.shape[0]} days)")
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Could not fetch historical data for {country}. Error: {e}")

if __name__ == "__main__":
    main()
