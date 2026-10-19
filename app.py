import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="TrafficLens | Road Safety Analytics",
    page_icon="🚦",
    layout="wide"
)

BASE = Path(__file__).parent
DATA = BASE / "data"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #081322 0%, #101e33 100%);
    color: #edf4ff;
}
[data-testid="stSidebar"] {
    background: #0b1728;
    border-right: 1px solid #26364d;
}
h1, h2, h3 { color: #edf4ff !important; }
p, label, .stMarkdown { color: #c6d4e8; }
div[data-testid="stMetric"] {
    background: #14243a;
    border: 1px solid #2a405c;
    padding: 18px;
    border-radius: 14px;
}
div[data-testid="stMetricValue"] { color: #5eead4; }
div[data-testid="stMetricLabel"] { color: #b7c8dd; }
</style>
""", unsafe_allow_html=True)

def load_csv(filename):
    path = DATA / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

st.sidebar.markdown("# 🚦 TrafficLens")
st.sidebar.caption("ROAD SAFETY ANALYTICS")
page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Annual Trends", "Weather Analysis",
     "Traffic Violations", "Junction Analysis", "Data Explorer", "About"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Source: Government of India road-accident tables, 2019 catalog")

annual = pd.DataFrame({
    "Year": [2016, 2017, 2018, 2019],
    "Road Accidents": [480652, 464910, 467044, 449002],
    "Persons Killed": [150785, 147913, 151417, 151113],
    "Persons Injured": [494624, 470975, 469418, 451361]
})

def heading(title, subtitle):
    st.title(title)
    st.caption(subtitle)

def category_chart(filename, keyword, title, exclude_total=False):
    df = load_csv(filename)
    if df.empty:
        st.warning(f"Dataset not found: {filename}")
        return

    cols = [
        c for c in df.columns
        if keyword.lower() in str(c).lower()
        and "rank" not in str(c).lower()
    ]

    if exclude_total:
        cols = [
            c for c in cols
            if not str(c).strip().lower().startswith("total -")
        ]

    # Keep category columns with numeric data; exclude summary totals
    if not cols:
        st.info("No matching category columns were found.")
        return

    totals = {}
    for col in cols:
        vals = pd.to_numeric(df[col], errors="coerce")
        totals[str(col)] = vals.sum()

    result = pd.DataFrame({
        "Category": list(totals.keys()),
        "Reported count": list(totals.values())
    })
    result = result.sort_values("Reported count", ascending=False)

    fig = px.bar(
        result, x="Reported count", y="Category",
        orientation="h", title=title,
        template="plotly_dark", color="Reported count",
        color_continuous_scale=["#1d4ed8", "#5eead4"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max(400, 45 * len(result)),
        yaxis={"categoryorder": "total ascending"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True, hide_index=True)

if page == "Overview":
    heading("Road Safety Intelligence", "TrafficLens · Explore reported road-safety patterns")
    st.markdown("### India · Annual reported totals")
    c1, c2, c3 = st.columns(3)
    c1.metric("Road accidents · 2019", f"{449002:,}")
    c2.metric("Persons killed · 2019", f"{151113:,}")
    c3.metric("Persons injured · 2019", f"{451361:,}")

    st.markdown("### Annual trends")
    selected = st.multiselect(
        "Choose metrics",
        ["Road Accidents", "Persons Killed", "Persons Injured"],
        default=["Road Accidents", "Persons Killed"]
    )
    long_df = annual.melt(
        id_vars="Year", value_vars=selected,
        var_name="Metric", value_name="Reported count"
    )
    fig = px.line(
        long_df, x="Year", y="Reported count",
        color="Metric", markers=True,
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "These are aggregate reported counts, not individual accident "
        "records. Category tables may cover different populations or scopes."
    )

elif page == "Annual Trends":
    heading("Annual Trends", "Reported totals across 2016–2019")
    st.dataframe(annual, use_container_width=True, hide_index=True)
    metric = st.selectbox(
        "Select metric",
        ["Road Accidents", "Persons Killed", "Persons Injured"]
    )
    fig = px.line(
        annual, x="Year", y=metric, markers=True,
        title=metric, template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.download_button(
        "Download annual trends CSV",
        annual.to_csv(index=False),
        file_name="trafficlens_annual_trends.csv",
        mime="text/csv"
    )

elif page == "Weather Analysis":
    heading("Weather Analysis", "Accident counts by reported weather category")
    category_chart(
        "RA2019_A25.csv", "total accidents",
        "Reported accidents by weather"
    )

elif page == "Traffic Violations":
    heading("Traffic Violations", "Reported accidents by violation category")
    category_chart(
        "RA2019_A47.csv", "number of accidents",
        "Reported accidents by traffic violation"
    )

elif page == "Junction Analysis":
    heading("Junction Analysis", "Reported accidents across junction categories")
    category_chart(
        "RA2019_A49.csv", "total number of accidents",
        "Reported accidents by junction type",
        exclude_total=True
    )

elif page == "Data Explorer":
    heading("Data Explorer", "Inspect the available aggregate datasets")
    files = sorted(p.name for p in DATA.glob("*.csv"))
    if not files:
        st.warning("No CSV files were found in the data folder.")
    else:
        selected_file = st.selectbox("Choose dataset", files)
        df = load_csv(selected_file)
        st.caption(f"{len(df):,} rows · {len(df.columns):,} columns")
        search = st.text_input("Filter rows by text")
        if search:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False)
            ).any(axis=1)
            df = df[mask]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download selected dataset",
            df.to_csv(index=False),
            file_name=selected_file,
            mime="text/csv"
        )

elif page == "About":
    heading("About TrafficLens", "Project methodology and data transparency")
    st.markdown("""
    **Project:** Traffic Accident Pattern Analysis and Road Safety Insights Using Python

    **Purpose:** Explore annual reported totals and aggregate patterns by
    weather, traffic violations and junction type.

    **Tools:** Python, Pandas, Streamlit and Plotly.

    **Data source:** Government of India Open Government Data (OGD) portal,
    Ministry of Road Transport and Highways.

    **Important limitations**
    - The supplied tables are aggregate state/city summaries.
    - They are not a dataset of individual GPS-tagged accident incidents.
    - Different tables may have different geographic coverage and definitions.
    - Counts alone do not establish the probability or cause of an accident.
    - No predictive model is claimed by this version of the application.
    """)
    st.markdown(
        "[Official OGD catalog](https://www.data.gov.in/catalog/road-accidents-india-2019)"
    )
