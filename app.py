
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="TrafficLens | Road Safety Intelligence",
    page_icon="🚦",
    layout="wide",
)

BASE = Path(__file__).parent
DATA = BASE / "data"

# -------------------- DESIGN --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #07111f, #10243a);
    color: #edf4ff;
}
[data-testid="stSidebar"] {
    background: #081525;
    border-right: 1px solid #29445e;
}
h1, h2, h3 { color: #f3f7ff !important; }
p, label, .stMarkdown { color: #c8d6e8; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #12263c, #142c42);
    border: 1px solid #29455f;
    padding: 18px;
    border-radius: 15px;
}
[data-testid="stMetricValue"] { color: #5eead4 !important; }
[data-testid="stMetricLabel"] { color: #b9cce0 !important; }
.insight {
    background: #12283d;
    border: 1px solid #29455f;
    padding: 17px;
    border-radius: 14px;
    margin-bottom: 10px;
}
.insight strong { color: #5eead4; }
</style>
""", unsafe_allow_html=True)

SOURCE_URL = (
    "https://www.data.gov.in/catalog/road-accidents-india-2019"
)

# Verified aggregate figures from the supplied state/UT tables.
annual = pd.DataFrame({
    "Year": [2016, 2017, 2018, 2019],
    "Road Accidents": [480652, 464910, 467044, 449002],
    "Persons Killed": [150785, 147913, 151417, 151113],
    "Persons Injured": [494624, 470975, 469418, 451361],
})

# -------------------- DATA LOADING --------------------
@st.cache_data(show_spinner=False)
def load_csv(filename):
    path = DATA / filename

    if not path.exists():
        return pd.DataFrame(), f"File not found: data/{filename}"

    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        df.columns = [str(c).strip() for c in df.columns]
        return df, None
    except Exception as exc:
        return pd.DataFrame(), f"Could not read CSV: {exc}"


def format_number(number):
    return f"{int(number):,}"


def page_heading(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.divider()


def show_chart(fig, height=450):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=15, r=30, t=65, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def make_category_summary(filename, keyword, exclude_total_columns=False):
    df, error = load_csv(filename)

    if error:
        return pd.DataFrame(), error

    if df.empty or len(df.columns) == 0:
        return pd.DataFrame(), "The dataset is empty."

    # Remove the aggregate row before summing individual categories.
    first_col = df.columns[0]
    labels = df[first_col].astype(str).str.strip().str.casefold()
    df = df.loc[labels.ne("total")].copy()

    # Find metric columns using the actual CSV column names.
    cols = [
        col for col in df.columns
        if keyword.casefold() in str(col).casefold()
        and "rank" not in str(col).casefold()
    ]

    if exclude_total_columns:
        cols = [
            col for col in cols
            if not str(col).strip().casefold().startswith("total -")
        ]

    if not cols:
        return pd.DataFrame(), (
            f"No columns matched '{keyword}'. "
            "Open Data Explorer to inspect the CSV headers."
        )

    rows = []

    for col in cols:
        values = pd.to_numeric(df[col], errors="coerce").dropna()

        if values.empty:
            continue

        # Preserve a readable category label.
        label = str(col)
        position = label.casefold().find(keyword.casefold())

        if position >= 0:
            label = label[:position].strip(" -_:")
        label = label or str(col)

        rows.append({
            "Category": label,
            "Reported count": int(values.sum()),
        })

    result = pd.DataFrame(rows)

    if result.empty:
        return result, "Matching columns were found, but no numeric values were available."

    return (
        result.sort_values(
            "Reported count", ascending=False
        ).reset_index(drop=True),
        None,
    )


def category_page(title, subtitle, filename, keyword, chart_title, interpretation,
                  exclude_total_columns=False):
    page_heading(title, subtitle)

    result, error = make_category_summary(
        filename, keyword, exclude_total_columns
    )

    if error:
        st.error(error)

        with st.expander("Diagnose this dataset"):
            df, load_error = load_csv(filename)

            if load_error:
                st.code(load_error)
            else:
                st.write(f"Rows: {len(df)} | Columns: {len(df.columns)}")
                st.write("CSV column names:")
                st.code("\n".join(map(str, df.columns)))
                st.dataframe(df.head(), use_container_width=True)

        return

    if result.empty:
        st.warning("No chartable categories were found.")
        return

    top = result.iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Categories analysed", len(result))
    c2.metric("Largest reported category", top["Category"])
    c3.metric("Reported count", format_number(top["Reported count"]))

    st.markdown("### Key finding")
    st.markdown(
        f'<div class="insight"><strong>{top["Category"]}</strong><br>'
        f'has the largest summed reported count in this table: '
        f'<strong>{format_number(top["Reported count"])}</strong>.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Visual analysis")
    fig = px.bar(
        result.sort_values("Reported count", ascending=True),
        x="Reported count",
        y="Category",
        orientation="h",
        title=chart_title,
        text="Reported count",
        color="Reported count",
        color_continuous_scale=["#2455a6", "#5eead4"],
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        margin=dict(l=15, r=50, t=65, b=20),
        height=max(420, 48 * len(result)),
    )
    show_chart(fig, max(420, 48 * len(result)))

    st.markdown("### What does this mean?")
    st.write(interpretation)

    st.info(
        "Important limitation: reported counts are not accident rates. "
        "These figures alone do not prove causation or establish which "
        "condition is most dangerous."
    )

    with st.expander("View the summary table"):
        st.dataframe(result, use_container_width=True, hide_index=True)

    st.download_button(
        "Download category summary",
        result.to_csv(index=False),
        file_name=f"trafficlens_{filename.replace('.csv', '')}_summary.csv",
        mime="text/csv",
    )


# -------------------- NAVIGATION --------------------
st.sidebar.markdown("# 🚦 TrafficLens")
st.sidebar.caption("ROAD SAFETY INTELLIGENCE")
page = st.sidebar.radio(
    "EXPLORE DASHBOARD",
    [
        "Overview",
        "Annual Trends",
        "Weather Analysis",
        "Traffic Violations",
        "Junction Analysis",
        "Data Explorer",
        "Methodology & About",
    ],
)
st.sidebar.divider()
st.sidebar.markdown(f"[Official Government data ↗]({SOURCE_URL})")
st.sidebar.caption("Exploratory analysis · Aggregate reported data")


# -------------------- OVERVIEW --------------------
if page == "Overview":
    st.markdown("## 🚦 TRAFFICLENS")
    st.title("Road Safety Intelligence")
    st.markdown(
        "### Understand reported accident patterns. Identify areas for further investigation."
    )
    st.write(
        "This project explores government road-accident tables to understand "
        "annual trends and selected patterns by weather, traffic violations "
        "and junction type."
    )

    st.markdown("### India · Reported totals in 2019")
    a, b, c = st.columns(3)
    a.metric("Road accidents", format_number(449002))
    b.metric("Persons killed", format_number(151113))
    c.metric("Persons injured", format_number(451361))

    st.markdown("### What changed between 2016 and 2019?")

    metrics = [
        ("Road Accidents", "Reported accidents"),
        ("Persons Killed", "Persons killed"),
        ("Persons Injured", "Persons injured"),
    ]

    cols = st.columns(3)

    for col, (metric, label) in zip(cols, metrics):
        start = int(annual.iloc[0][metric])
        end = int(annual.iloc[-1][metric])
        change = (end - start) / start * 100

        with col:
            st.metric(
                label,
                format_number(end),
                f"{change:+.1f}% since 2016",
                delta_color="inverse" if metric != "Persons Killed" else "normal",
            )

    st.markdown("### Annual trend explorer")

    selected = st.multiselect(
        "Select measures",
        ["Road Accidents", "Persons Killed", "Persons Injured"],
        default=["Road Accidents", "Persons Killed"],
    )

    if selected:
        long_data = annual.melt(
            id_vars="Year",
            value_vars=selected,
            var_name="Measure",
            value_name="Reported count",
        )

        fig = px.line(
            long_data,
            x="Year",
            y="Reported count",
            color="Measure",
            markers=True,
            title="Annual reported totals · 2016–2019",
        )
        show_chart(fig)
    else:
        st.info("Select at least one measure to display the chart.")

    st.markdown("### Road-safety priorities to investigate")
    st.markdown("""
    - **Speed management:** review the reported traffic-violation categories.
    - **Safer junctions:** investigate junction design alongside traffic volume.
    - **Weather preparedness:** combine weather counts with exposure and local conditions.
    - **Evidence-led decisions:** collect location, time, traffic-flow and road-design data.
    """)

    st.warning(
        "These are aggregate reported counts, not individual accident records. "
        "The observed trends do not by themselves prove why counts changed."
    )


# -------------------- ANNUAL TRENDS --------------------
elif page == "Annual Trends":
    page_heading(
        "Annual Trends",
        "Compare reported totals across 2016–2019.",
    )

    metric = st.selectbox(
        "Choose a measure",
        ["Road Accidents", "Persons Killed", "Persons Injured"],
    )

    start = int(annual.iloc[0][metric])
    end = int(annual.iloc[-1][metric])
    change = (end - start) / start * 100

    a, b, c = st.columns(3)
    a.metric("2016", format_number(start))
    b.metric("2019", format_number(end))
    c.metric("Overall change", f"{change:+.1f}%")

    fig = px.line(
        annual,
        x="Year",
        y=metric,
        markers=True,
        title=f"{metric} · Reported annual totals",
    )
    show_chart(fig)

    if change < 0:
        st.write(
            f"The reported count decreased by {format_number(start - end)} "
            f"between 2016 and 2019 ({abs(change):.1f}%). "
            "This describes the trend, but does not establish its cause."
        )
    elif change > 0:
        st.write(
            f"The reported count increased by {format_number(end - start)} "
            f"between 2016 and 2019 ({change:.1f}%). "
            "This describes the trend, but does not establish its cause."
        )
    else:
        st.write("The reported count was unchanged over this period.")

    st.dataframe(annual, use_container_width=True, hide_index=True)

    st.download_button(
        "Download annual totals CSV",
        annual.to_csv(index=False),
        file_name="trafficlens_annual_trends.csv",
        mime="text/csv",
    )


# -------------------- WEATHER --------------------
elif page == "Weather Analysis":
    category_page(
        "Weather Analysis",
        "Explore reported accidents by weather category.",
        "RA2019_A25.csv",
        "total accidents",
        "Reported accidents by weather category",
        "The bars compare the reported accident counts summed across the "
        "available state/UT rows. A large count does not automatically mean "
        "that weather condition has a higher accident risk: traffic volume "
        "and time spent travelling in each condition are not measured here.",
    )


# -------------------- TRAFFIC VIOLATIONS --------------------
elif page == "Traffic Violations":
    category_page(
        "Traffic Violation Analysis",
        "Compare reported accident counts across violation categories.",
        "RA2019_A47.csv",
        "number of accidents",
        "Reported accidents by traffic-violation category",
        "The largest bar identifies the category with the largest summed "
        "reported count in this table. It is a useful starting point for "
        "further investigation, not proof that this factor caused every "
        "accident or has the highest individual risk.",
    )


# -------------------- JUNCTIONS --------------------
elif page == "Junction Analysis":
    category_page(
        "Junction Analysis",
        "Explore reported accident counts by junction type.",
        "RA2019_A49.csv",
        "total number of accidents",
        "Reported accidents by junction type",
        "This chart compares the junction categories in the selected city "
        "summary table. A risk ranking would also require the number of "
        "junctions of each type, traffic volume and reporting coverage.",
        exclude_total_columns=True,
    )


# -------------------- DATA EXPLORER --------------------
elif page == "Data Explorer":
    page_heading(
        "Data Explorer",
        "Inspect the actual CSV files bundled with this application.",
    )

    files = sorted(DATA.glob("*.csv"))

    if not files:
        st.error("No CSV files were found inside the data folder.")
        st.write("Expected structure:")
        st.code("TrafficLens-Road-Safety-Analytics/\n  app.py\n  requirements.txt\n  data/\n    RA2019_A25.csv\n    RA2019_A47.csv\n    RA2019_A49.csv")
    else:
        selected_file = st.selectbox(
            "Choose a dataset",
            [f.name for f in files],
        )
        df, error = load_csv(selected_file)

        if error:
            st.error(error)
        else:
            a, b, c = st.columns(3)
            a.metric("Rows", f"{len(df):,}")
            b.metric("Columns", f"{len(df.columns):,}")
            c.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

            query = st.text_input(
                "Search rows",
                placeholder="Enter a city, state, category or value",
            )

            view = df.copy()

            if query:
                mask = view.astype(str).apply(
                    lambda col: col.str.contains(
                        query, case=False, na=False, regex=False
                    )
                ).any(axis=1)
                view = view[mask]

            st.caption(f"Displaying {len(view):,} of {len(df):,} rows.")
            st.dataframe(view, use_container_width=True, hide_index=True)

            st.download_button(
                "Download displayed data",
                view.to_csv(index=False),
                file_name=f"trafficlens_{selected_file}",
                mime="text/csv",
            )

            with st.expander("Data quality report"):
                quality = pd.DataFrame({
                    "Column": df.columns,
                    "Data type": [str(t) for t in df.dtypes],
                    "Missing values": [
                        int(df[col].isna().sum()) for col in df.columns
                    ],
                    "Unique values": [
                        int(df[col].nunique(dropna=True)) for col in df.columns
                    ],
                })

                st.dataframe(
                    quality,
                    use_container_width=True,
                    hide_index=True,
                )
                st.write(f"Exact duplicate rows: {int(df.duplicated().sum()):,}")


# -------------------- METHODOLOGY --------------------
elif page == "Methodology & About":
    page_heading(
        "Methodology & About",
        "Project purpose, data handling and limitations.",
    )

    st.markdown("### Project title")
    st.write(
        "**Traffic Accident Pattern Analysis and Road Safety Insights Using Python**"
    )

    st.markdown("### Objective")
    st.write(
        "To explore reported road-accident totals and selected aggregate "
        "patterns, and translate the findings into understandable road-safety "
        "questions for further investigation."
    )

    st.markdown("### Analysis workflow")
    st.markdown("""
    1. Load the supplied CSV files using Pandas.
    2. Inspect dimensions, missing cells and column names.
    3. Exclude the aggregate row labelled `Total` before summing category counts.
    4. Convert category values to numeric form and summarize reported counts.
    5. Visualize annual and category patterns with Plotly.
    6. Interpret findings with clear limitations and practical next steps.
    """)

    st.markdown("### Dataset inventory")
    expected = [
        "RA2019_A25.csv",
        "RA2019_A29d.csv",
        "RA2019_A45.csv",
        "RA2019_A49.csv",
        "RA2019_A47.csv",
        "RA2019_A4.csv",
        "RA2019_A3.csv",
        "RA2019_A2.csv",
    ]

    inventory = []

    for filename in expected:
        df, error = load_csv(filename)
        inventory.append({
            "File": filename,
            "Status": "Loaded" if error is None else "Missing / unreadable",
            "Rows": len(df),
            "Columns": len(df.columns),
        })

    st.dataframe(
        pd.DataFrame(inventory),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Official data source")
    st.markdown(f"[Government of India OGD catalog ↗]({SOURCE_URL})")

    st.markdown("### Limitations")
    st.markdown("""
    - The included tables are aggregate state/UT or city summaries, not individual incident records.
    - Some tables describe annual totals across 2016–2019; others contain category summaries from the 2019 catalog.
    - Tables with different geographic coverage must not be combined as if they were the same population.
    - Reported counts are not exposure-adjusted rates.
    - Counts alone cannot prove causation.
    - This application does not claim to predict individual accidents.
    - More detailed location, traffic-volume, road-design and time-of-day data would be needed for stronger risk analysis.
    """)

    st.markdown("### Technology")
    st.write("Python · Pandas · Streamlit · Plotly")
