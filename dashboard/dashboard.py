import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(layout="wide")

# CUSTOM CSS DARK GLASS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
}

[data-testid="stVerticalBlock"] > div {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# LOAD DATA
df = pd.read_csv("https://raw.githubusercontent.com/Rahmatbaaka/Analisis-Data-Boston-Marathon-2015-2017/main/dashboard/df_marathon.csv")

# SIDEBAR FILTER
st.sidebar.title("📊 Filter Data")

years = st.sidebar.multiselect(
    "Pilih Tahun",
    df["year"].unique(),
    default=df["year"].unique()
)

gender = st.sidebar.multiselect(
    "Pilih Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered = df[(df["year"].isin(years)) & (df["Gender"].isin(gender))]

# HEADER
st.title("🏃‍♂️ Marathon Performance Dashboard")
st.markdown("### Analisis Data Pelari Marathon")

# KPI METRICS
col1, col2, col3 = st.columns(3)

col1.metric("Total Pelari", len(filtered))
col2.metric("Rata-rata Umur", round(filtered["Age"].mean(), 1))
col3.metric("Rata-rata Pace", round(filtered["Pace"].mean(), 2))

st.divider()

# AGE DISTRIBUTION
st.subheader("📊 Distribusi Umur")

fig = px.histogram(
    filtered,
    x="Age",
    nbins=50,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# AGE VS PACE
st.subheader("📈 Hubungan Umur vs Pace")

fig = px.scatter(
    filtered,
    x="Age",
    y="Pace",
    color="Gender",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# TREND PACE
st.subheader("📉 Trend Pace per Tahun")

trend = filtered.groupby("year")["Pace"].mean().reset_index()

fig = px.line(
    trend,
    x="year",
    y="Pace",
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# GENDER PERFORMANCE
st.subheader("🚻 Performa Berdasarkan Gender")

gender_perf = filtered.groupby("Gender")["Pace"].mean().reset_index()

fig = px.bar(
    gender_perf,
    x="Gender",
    y="Pace",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# COUNTRY DOMINANCE
st.subheader("🌍 Negara Dominan")

top_country = filtered["Country"].value_counts().head(10).reset_index()
top_country.columns = ["Country", "Count"]

fig = px.bar(
    top_country,
    x="Country",
    y="Count",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# BEST PERFORMANCE COUNTRY
st.subheader("🏆 Negara Performa Terbaik")

best_country = filtered.groupby("Country")["Pace"].mean().sort_values().head(10).reset_index()

fig = px.bar(
    best_country,
    x="Country",
    y="Pace",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
---
<div style="text-align:center; color:gray; font-size:14px;">
© 2026 Rahmat Hidayat — Marathon Dashboard | Built with Streamlit
</div>
""", unsafe_allow_html=True)
