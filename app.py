
import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# TRAFFICLENS | ROAD SAFETY INTELLIGENCE
# =========================================================

st.set_page_config(
    page_title="TrafficLens | Road Safety Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent
DATA = BASE  # CSV files are stored beside app.py in the repository root.

SOURCE_URL = "https://www.data.gov.in/catalog/road-accidents-india-2019"

annual = pd.DataFrame({
    "Year": [2016, 2017, 2018, 2019],
    "Road Accidents": [480652, 464910, 467044, 449002],
    "Persons Killed": [150785, 147913, 151417, 151113],
    "Persons Injured": [494624, 470975, 469418, 451361],
})

EXPECTED_FILES = [
    "RA2019_A25.csv",
    "RA2019_A29d.csv",
    "RA2019_A45.csv",
    "RA2019_A49.csv",
    "RA2019_A47.csv",
    "RA2019_A4.csv",
    "RA2019_A3.csv",
    "RA2019_A2.csv",
]


# =========================================================
# PREMIUM THEME
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --purple: #7453e8;
    --purple-dark: #5035b5;
    --lavender: #eee9ff;
    --teal: #0f9f9a;
    --navy: #202342;
    --muted: #696b84;
    --surface: #ffffff;
    --border: #e8e5f4;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, rgba(128, 94, 240, 0.11), transparent 34%),
        radial-gradient(ellipse at 95% 8%, rgba(28, 184, 176, 0.08), transparent 28%),
        #f7f7fc;
    color: var(--navy);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(247, 247, 252, 0.82);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f0edff 0%, #ffffff 62%, #f3fbfa 100%);
    border-right: 1px solid #e3def5;
}

[data-testid="stSidebar"] * {
    color: #29264b;
}

h1, h2, h3, h4 {
    color: #242344 !important;
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.4px;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: #555875;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff 0%, #f4f0ff 100%);
    border: 1px solid #e5defa;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 6px 22px rgba(62, 46, 120, 0.055);
    animation: fadeUp 0.55s ease both;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(91, 65, 173, 0.12);
}

[data-testid="stMetricLabel"] {
    color: #696786 !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #6548d7 !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    font-weight: 600;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 11px;
    border: 1px solid #d8d0fa;
    background: linear-gradient(110deg, #7453e8, #8b70f0);
    color: white;
    font-weight: 700;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    color: white;
    border-color: #6e4fe0;
    box-shadow: 0 7px 18px rgba(101, 72, 215, 0.22);
    transform: translateY(-2px);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 10px;
    border-color: #ded9f0;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e8e5f4;
    border-radius: 12px;
    overflow: hidden;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.78);
    border: 1px solid #e8e5f4;
    border-radius: 13px;
}

.insight-card {
    background: linear-gradient(120deg, #ffffff, #f1edff);
    border: 1px solid #ded6fa;
    border-left: 5px solid #7453e8;
    border-radius: 15px;
    padding: 18px 20px;
    margin: 10px 0 16px 0;
    color: #454361;
    box-shadow: 0 5px 18px rgba(67, 49, 126, 0.045);
    animation: fadeUp 0.5s ease both;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.insight-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 24px rgba(67, 49, 126, 0.10);
}

.insight-card strong {
    color: #6244cf;
}

.teal-card {
    background: linear-gradient(120deg, #ffffff, #e9fbf8);
    border: 1px solid #c9eeea;
    border-left: 5px solid #0f9f9a;
    border-radius: 15px;
    padding: 17px 20px;
    margin: 10px 0 16px 0;
    animation: fadeUp 0.55s ease both;
}

.teal-card strong {
    color: #087e79;
}

.hero {
    background: linear-gradient(115deg, #5b3bc6 0%, #7957e8 54%, #19a7a1 130%);
    color: white;
    padding: 30px 32px;
    border-radius: 22px;
    margin: 4px 0 22px 0;
    box-shadow: 0 13px 34px rgba(94, 66, 190, 0.18);
    animation: fadeUp 0.55s ease both;
}

.hero h1, .hero h2, .hero p, .hero span {
    color: white !important;
}

.hero h1 {
    font-size: clamp(27px, 3.5vw, 42px);
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    font-size: 16px;
    opacity: 0.94;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 800;
    opacity: 0.86;
    margin-bottom: 10px;
}

.section-label {
    color: #7354db;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 5px;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(9px); }
    to { opacity: 1; transform: translateY(0); }
}

hr {
    border-color: #e8e5f4 !important;
}

a {
    color: #684bd5 !important;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA LOADING AND HELPERS
# =========================================================

@st.cache_data(show_spinner=False)
def load_csv(filename):
    path = BASE / filename

    if not path.exists():
        return pd.DataFrame(), f"File not found: {filename}"

    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        df.columns = [str(col).strip() for col in df.columns]
        return df, None
    except Exception as exc:
        return pd.DataFrame(), f"Could not read CSV: {exc}"


def format_number(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError, OverflowError):
        return str(value)


def page_heading(title, subtitle):
    st.markdown('<div class="section-label">TRAFFICLENS ANALYTICS</div>',
                unsafe_allow_html=True)
    st.title(title)
    st.caption(subtitle)
    st.divider()


def hero(title, subtitle, eyebrow="ROAD SAFETY INTELLIGENCE"):
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    safe_eyebrow = html.escape(eyebrow)
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{safe_eyebrow}</div>
            <h1>{safe_title}</h1>
            <p>{safe_subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(title, body, teal=False):
    css_class = "teal-card" if teal else "insight-card"
    st.markdown(
        f'<div class="{css_class}"><strong>{html.escape(title)}</strong>'
        f'<br>{html.escape(body)}</div>',
        unsafe_allow_html=True,
    )


def show_chart(fig, height=450):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="DM Sans, sans-serif", color="#454361"),
        title_font=dict(family="Manrope, sans-serif", size=18, color="#292747"),
        height=height,
        margin=dict(l=15, r=30, t=65, b=25),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#ded6fa",
            font=dict(color="#292747"),
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0,
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#eeebf6",
        zerolinecolor="#e5e0f1",
    )
    fig.update_yaxes(
        showgrid=False,
        zerolinecolor="#e5e0f1",
    )
    st.plotly_chart(fig, use_container_width=True)


def make_category_summary(filename, keyword, exclude_total_columns=False):
    df, error = load_csv(filename)

    if error:
        return pd.DataFrame(), error

    if df.empty or len(df.columns) == 0:
        return pd.DataFrame(), "The dataset is empty."

    # Remove aggregate rows before adding category values.
    first_col = df.columns[0]
    labels = df[first_col].astype(str).str.strip().str.casefold()
    df = df.loc[labels.ne("total")].copy()

    # Match the requested measure in the real CSV headers.
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
        result.sort_values("Reported count", ascending=False).reset_index(drop=True),
        None,
    )


def category_page(title, subtitle, filename, keyword, chart_title,
                  interpretation, exclude_total_columns=False):
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
                st.write(f"Rows: {len(df)} · Columns: {len(df.columns)}")
                st.write("CSV column names:")
                st.code("\n".join(map(str, df.columns)))
                st.dataframe(df.head(), use_container_width=True)
        return

    if result.empty:
        st.warning("No chartable categories were found.")
        return

    top = result.iloc[0]

    a, b, c = st.columns(3)
    a.metric("Categories analysed", len(result))
    b.metric("Largest category", str(top["Category"]))
    c.metric("Reported count", format_number(top["Reported count"]))

    insight_card(
        "Key finding",
        f'{top["Category"]} has the largest summed reported count in this table: '
        f'{format_number(top["Reported count"])}.',
    )

    fig = px.bar(
        result.sort_values("Reported count", ascending=True),
        x="Reported count",
        y="Category",
        orientation="h",
        title=chart_title,
        text="Reported count",
        color="Reported count",
        color_continuous_scale=["#c9bafa", "#7553e8", "#18aaa2"],
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        margin=dict(l=15, r=65, t=65, b=20),
        height=max(420, 42 * len(result)),
    )
    show_chart(fig, max(420, 42 * len(result)))

    st.markdown("### Interpretation")
    st.write(interpretation)

    st.info(
        "Important limitation: reported counts are not exposure-adjusted accident rates. "
        "Counts alone do not prove causation or show which condition has the highest risk."
    )

    with st.expander("View summary table"):
        st.dataframe(result, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download category summary",
        result.to_csv(index=False).encode("utf-8"),
        file_name=f"trafficlens_{filename.replace('.csv', '')}_summary.csv",
        mime="text/csv",
    )


def percentage_change(start, end):
    if not start:
        return 0.0
    return (end - start) / start * 100


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown("# 🚦 TrafficLens")
st.sidebar.caption("ROAD SAFETY INTELLIGENCE")
st.sidebar.markdown("---")

pages = [
    "Overview",
    "Road Safety Insights",
    "Annual Trends",
    "Weather Analysis",
    "Traffic Violations",
    "Junction Analysis",
    "Data Explorer",
    "Methodology & About",
]

page = st.sidebar.radio("EXPLORE DASHBOARD", pages)

st.sidebar.markdown("---")
st.sidebar.markdown(f"[Official Government data ↗]({SOURCE_URL})")
st.sidebar.caption("Exploratory analysis · Aggregate reported data")
st.sidebar.caption("Python · Pandas · Streamlit · Plotly")


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":
    hero(
        "Road Safety Intelligence",
        "Explore reported accident patterns, understand annual trends, "
        "and discover where further road-safety investigation may help.",
    )

    st.markdown("#### 🇮🇳 India · Reported totals in 2019")

    a, b, c = st.columns(3)
    a.metric("Road accidents", format_number(449002))
    b.metric("Persons killed", format_number(151113))
    c.metric("Persons injured", format_number(451361))

    st.markdown("#### At a glance")
    st.caption("Change in reported counts between 2016 and 2019")

    metric_info = [
        ("Road Accidents", "Reported accidents"),
        ("Persons Killed", "Persons killed"),
        ("Persons Injured", "Persons injured"),
    ]

    cols = st.columns(3)
    for col, (metric, label) in zip(cols, metric_info):
        start = int(annual.iloc[0][metric])
        end = int(annual.iloc[-1][metric])
        change = percentage_change(start, end)
        with col:
            col.metric(
                label,
                format_number(end),
                f"{change:+.1f}% since 2016",
                delta_color="inverse" if metric != "Persons Killed" else "normal",
            )

    st.markdown("#### Explore annual totals")
    selected = st.multiselect(
        "Select measures to compare",
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
            color_discrete_sequence=["#7453e8", "#0f9f9a", "#e69a36"],
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=9))
        show_chart(fig)
    else:
        st.info("Select at least one measure to display the chart.")

    st.markdown("#### Areas worth investigating")
    left, right = st.columns(2)

    with left:
        insight_card(
            "Speed management",
            "Review the reported traffic-violation categories and investigate "
            "where speed-management measures may be useful.",
        )
        insight_card(
            "Safer junctions",
            "Study junction design alongside traffic flow, road geometry, "
            "and the number of junctions of each type.",
        )

    with right:
        insight_card(
            "Weather preparedness",
            "Combine weather-related counts with traffic exposure and local "
            "weather conditions before drawing risk conclusions.",
            teal=True,
        )
        insight_card(
            "Evidence-led decisions",
            "Add time, location, road-design, traffic-volume, and reporting "
            "details to support stronger future analysis.",
            teal=True,
        )

    st.warning(
        "These are aggregate reported counts, not individual accident records. "
        "Trends describe what changed; they do not by themselves explain why."
    )


# =========================================================
# ROAD SAFETY INSIGHTS
# =========================================================

elif page == "Road Safety Insights":
    hero(
        "Road Safety Insights",
        "Turn the supplied aggregate tables into clear findings, "
        "responsible interpretations, and practical next steps.",
        "FINDINGS · INTERPRETATION · ACTION",
    )

    st.markdown("### 01 · Annual pattern")

    accidents_change = percentage_change(
        annual.iloc[0]["Road Accidents"],
        annual.iloc[-1]["Road Accidents"],
    )
    deaths_change = percentage_change(
        annual.iloc[0]["Persons Killed"],
        annual.iloc[-1]["Persons Killed"],
    )
    injuries_change = percentage_change(
        annual.iloc[0]["Persons Injured"],
        annual.iloc[-1]["Persons Injured"],
    )

    a, b, c = st.columns(3)
    a.metric("Road accidents", f"{accidents_change:+.1f}%", "2016 to 2019")
    b.metric("Persons killed", f"{deaths_change:+.1f}%", "2016 to 2019")
    c.metric("Persons injured", f"{injuries_change:+.1f}%", "2016 to 2019")

    insight_card(
        "Finding",
        "Reported accidents and injuries were lower in 2019 than in 2016. "
        "Reported deaths were also slightly lower over that period, although "
        "the annual death count peaked in 2018.",
    )

    trend_long = annual.melt(
        id_vars="Year",
        value_vars=["Road Accidents", "Persons Killed", "Persons Injured"],
        var_name="Measure",
        value_name="Reported count",
    )
    trend_fig = px.line(
        trend_long,
        x="Year",
        y="Reported count",
        color="Measure",
        markers=True,
        title="Reported annual totals",
        color_discrete_sequence=["#7453e8", "#0f9f9a", "#e69a36"],
    )
    trend_fig.update_traces(line=dict(width=3), marker=dict(size=8))
    show_chart(trend_fig)

    st.markdown("### 02 · Traffic-violation pattern")
    violations, violation_error = make_category_summary(
        "RA2019_A47.csv", "number of accidents"
    )

    if violation_error:
        st.warning(f"Traffic-violation summary unavailable: {violation_error}")
    else:
        top_v = violations.iloc[0]
        st.metric("Largest reported category", top_v["Category"],
                  format_number(top_v["Reported count"]))

        insight_card(
            "Finding",
            f'{top_v["Category"]} is the largest category in the available '
            f'traffic-violation table, with {format_number(top_v["Reported count"])} '
            "summed reported counts.",
        )

        vfig = px.bar(
            violations.head(8).sort_values("Reported count"),
            x="Reported count",
            y="Category",
            orientation="h",
            title="Largest reported violation categories",
            text="Reported count",
            color="Reported count",
            color_continuous_scale=["#c9bafa", "#7553e8", "#18aaa2"],
        )
        vfig.update_traces(texttemplate="%{text:,}", textposition="outside",
                           cliponaxis=False)
        vfig.update_layout(coloraxis_showscale=False, margin=dict(r=60))
        show_chart(vfig, max(400, 42 * min(8, len(violations))))

    st.markdown("### 03 · Weather pattern")
    weather, weather_error = make_category_summary(
        "RA2019_A25.csv", "total accidents"
    )

    if weather_error:
        st.warning(f"Weather summary unavailable: {weather_error}")
    else:
        top_w = weather.iloc[0]
        st.metric("Largest reported weather category", top_w["Category"],
                  format_number(top_w["Reported count"]))

        insight_card(
            "How to interpret this",
            "The category with the most reported accidents is not necessarily "
            "the most dangerous. A risk comparison would need traffic exposure, "
            "time spent travelling in each condition, and reporting context.",
            teal=True,
        )

    st.markdown("### 04 · Junction pattern")
    junctions, junction_error = make_category_summary(
        "RA2019_A49.csv",
        "total number of accidents",
        exclude_total_columns=True,
    )

    if junction_error:
        st.warning(f"Junction summary unavailable: {junction_error}")
    else:
        top_j = junctions.iloc[0]
        st.metric("Largest reported junction category", top_j["Category"],
                  format_number(top_j["Reported count"]))

        insight_card(
            "Investigation priority",
            "Compare junction categories with the number of junctions, traffic "
            "volume, road layout, and severity before prioritising locations.",
        )

    st.markdown("### 05 · Recommended next steps")
    st.markdown("""
    1. **Prioritise investigation, not blame.** Use the largest reported categories
       as starting points for further examination.
    2. **Collect exposure data.** Include traffic volume, vehicle-kilometres,
       junction counts, and time spent travelling in each condition.
    3. **Add time and location detail.** Hour, day, road segment, weather severity,
       and road-design fields would support more useful comparisons.
    4. **Separate frequency from severity.** Analyse fatal, injury, and property-only
       outcomes separately wherever the source data supports it.
    5. **Validate before acting.** Check reporting completeness, definitions, missing
       values, and geographic coverage with the relevant authority.
    """)

    st.info(
        "Scope note: these findings describe the supplied aggregate tables. "
        "They are not causal conclusions, a validated prediction model, or "
        "a ranking of the safest and most dangerous roads."
    )

    # One-click downloadable summary of annual totals.
    st.download_button(
        "⬇️ Download annual findings data",
        annual.to_csv(index=False).encode("utf-8"),
        file_name="trafficlens_annual_findings.csv",
        mime="text/csv",
    )


# =========================================================
# ANNUAL TRENDS
# =========================================================

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
    change = percentage_change(start, end)

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
        color_discrete_sequence=["#7453e8"],
    )
    fig.update_traces(line=dict(width=4), marker=dict(size=10))
    show_chart(fig)

    difference = end - start
    if difference < 0:
        st.write(
            f"The reported count decreased by {format_number(abs(difference))} "
            f"between 2016 and 2019 ({abs(change):.1f}%). "
            "This describes the trend but does not establish its cause."
        )
    elif difference > 0:
        st.write(
            f"The reported count increased by {format_number(difference)} "
            f"between 2016 and 2019 ({change:.1f}%). "
            "This describes the trend but does not establish its cause."
        )
    else:
        st.write("The reported count was unchanged over this period.")

    st.dataframe(annual, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download annual totals CSV",
        annual.to_csv(index=False).encode("utf-8"),
        file_name="trafficlens_annual_trends.csv",
        mime="text/csv",
    )


# =========================================================
# WEATHER ANALYSIS
# =========================================================

elif page == "Weather Analysis":
    category_page(
        "Weather Analysis",
        "Explore reported accidents by weather category.",
        "RA2019_A25.csv",
        "total accidents",
        "Reported accidents by weather category",
        "The bars compare reported accident counts summed across the available "
        "state/UT rows. A large count does not automatically mean a weather "
        "condition has higher accident risk: traffic volume and time spent "
        "travelling in each condition are not measured here.",
    )


# =========================================================
# TRAFFIC VIOLATIONS
# =========================================================

elif page == "Traffic Violations":
    category_page(
        "Traffic Violation Analysis",
        "Compare reported accident counts across violation categories.",
        "RA2019_A47.csv",
        "number of accidents",
        "Reported accidents by traffic-violation category",
        "The largest bar identifies the category with the largest summed "
        "reported count in this table. It is a starting point for investigation, "
        "not proof that this factor caused every accident or has the highest "
        "individual risk.",
    )


# =========================================================
# JUNCTION ANALYSIS
# =========================================================

elif page == "Junction Analysis":
    category_page(
        "Junction Analysis",
        "Explore reported accident counts by junction type.",
        "RA2019_A49.csv",
        "total number of accidents",
        "Reported accidents by junction type",
        "This chart compares junction categories in the available city summary "
        "table. A risk ranking would also require the number of junctions of "
        "each type, traffic volume, road layout, and reporting coverage.",
        exclude_total_columns=True,
    )


# =========================================================
# DATA EXPLORER
# =========================================================

elif page == "Data Explorer":
    page_heading(
        "Data Explorer",
        "Inspect the actual CSV files bundled with this application.",
    )

    files = sorted(BASE.glob("*.csv"))

    if not files:
        st.error("No CSV files were found beside app.py.")
        st.write("Expected repository structure:")
        st.code(
            "TrafficLens-Road-Safety-Analytics/\n"
            "  app.py\n"
            "  requirements.txt\n"
            "  RA2019_A25.csv\n"
            "  RA2019_A47.csv\n"
            "  RA2019_A49.csv\n"
        )
    else:
        selected_file = st.selectbox(
            "Choose a dataset",
            [file.name for file in files],
        )
        df, error = load_csv(selected_file)

        if error:
            st.error(error)
        else:
            a, b, c = st.columns(3)
            a.metric("Rows", format_number(len(df)))
            b.metric("Columns", format_number(len(df.columns)))
            c.metric("Missing cells", format_number(int(df.isna().sum().sum())))

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
                "⬇️ Download displayed data",
                view.to_csv(index=False).encode("utf-8"),
                file_name=f"trafficlens_{selected_file}",
                mime="text/csv",
            )

            with st.expander("Data quality report"):
                quality = pd.DataFrame({
                    "Column": df.columns,
                    "Data type": [str(dtype) for dtype in df.dtypes],
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
                st.write(
                    f"Exact duplicate rows: {format_number(int(df.duplicated().sum()))}"
                )

                missing_cols = int(df.isna().any().sum())
                st.write(f"Columns containing missing values: {missing_cols}")

                if missing_cols:
                    st.caption(
                        "Missing cells are reported for transparency. "
                        "This dashboard does not silently fill missing values."
                    )


# =========================================================
# METHODOLOGY & ABOUT
# =========================================================

elif page == "Methodology & About":
    page_heading(
        "Methodology & About",
        "Project purpose, data handling, source, and limitations.",
    )

    hero(
        "About TrafficLens",
        "Traffic Accident Pattern Analysis and Road Safety Insights Using Python",
        "PROJECT OVERVIEW",
    )

    st.markdown("### Objective")
    st.write(
        "To explore reported road-accident totals and selected aggregate patterns, "
        "and translate the findings into understandable road-safety questions "
        "for further investigation."
    )

    st.markdown("### Analysis workflow")
    st.markdown("""
    1. Load the supplied CSV files using Pandas.
    2. Inspect dimensions, missing cells, data types, and column names.
    3. Exclude the aggregate row labelled `Total` before summing categories.
    4. Convert category values to numeric form and summarize reported counts.
    5. Visualize annual and category patterns with Plotly.
    6. Interpret findings with explicit limitations and practical next steps.
    """)

    st.markdown("### Dataset inventory")

    inventory = []
    for filename in EXPECTED_FILES:
        df, error = load_csv(filename)
        inventory.append({
            "File": filename,
            "Status": "Loaded" if error is None else "Missing / unreadable",
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing cells": int(df.isna().sum().sum()) if error is None else None,
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
    - Tables with different geographic coverage must not be combined as if they represented the same population.
    - Reported counts are not exposure-adjusted rates.
    - Counts alone cannot prove causation.
    - This application does not claim to predict individual accidents.
    - Stronger risk analysis would require more detailed location, traffic-volume,
      road-design, time-of-day, and exposure data.
    """)

    st.markdown("### Technology stack")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Language", "Python")
    t2.metric("Data", "Pandas")
    t3.metric("Dashboard", "Streamlit")
    t4.metric("Charts", "Plotly")

    st.caption(
        "TrafficLens is an educational analytics project. Interpret results "
        "within the scope and definitions of the underlying source tables."
    )
