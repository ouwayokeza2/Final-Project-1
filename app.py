import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
import subprocess
import sys

st.set_page_config(
    page_title="U.S. Labor Market Dashboard",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = Path("data/bls_labor_data.csv")

SERIES_LABELS = {
    "Unemployment Rate": "Measures the percentage of people in the labor force who are unemployed.",
    "Total Nonfarm Employment": "Shows the total number of payroll jobs in the U.S. economy, excluding farm workers.",
    "Healthcare Employment": "Tracks employment in healthcare, which connects directly to workforce planning and healthcare operations.",
    "Labor Force Participation Rate": "Shows the percentage of the population that is working or actively looking for work.",
    "Average Hourly Earnings": "Tracks worker pay trends across the private sector.",
    "Average Weekly Hours": "Shows changes in average hours worked, which can signal labor demand and scheduling pressure."
}

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        subprocess.run([sys.executable, "fetch_bls_data.py"], check=True)

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    return df.sort_values(["indicator", "date"])

df = load_data()

st.title("📊 U.S. Labor Market Dashboard with Healthcare Focus")
st.markdown(
    """
    This interactive dashboard explores key U.S. labor market indicators using official
    Bureau of Labor Statistics data. The project connects labor market trends to real-world
    workforce issues in **healthcare, operations, and supply chain management**.
    """
)

latest_date = df["date"].max()
st.success(f"Latest available data in this dashboard: **{latest_date.strftime('%B %Y')}**")

with st.sidebar:
    st.header("Dashboard Controls")

    indicator_options = sorted(df["indicator"].unique())
    selected_indicators = st.multiselect(
        "Select indicators",
        indicator_options,
        default=indicator_options
    )

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_range = st.slider(
        "Select date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    st.markdown("---")
    st.caption("Data source: U.S. Bureau of Labor Statistics public API")

filtered = df[
    (df["indicator"].isin(selected_indicators)) &
    (df["date"].dt.date >= selected_range[0]) &
    (df["date"].dt.date <= selected_range[1])
].copy()

st.subheader("1. Key Labor Market Snapshot")

latest_rows = filtered.sort_values("date").groupby("indicator").tail(1)
metric_cols = st.columns(3)

for i, row in enumerate(latest_rows.itertuples()):
    with metric_cols[i % 3]:
        st.metric(
            label=row.indicator,
            value=f"{row.value:,.2f} {row.unit}"
        )

st.markdown("---")

st.subheader("2. Indicator Explanations")
for indicator in selected_indicators:
    st.markdown(f"**{indicator}:** {SERIES_LABELS.get(indicator, 'Labor market indicator.')}")

st.markdown("---")

st.subheader("3. Labor Market Trends Over Time")
st.markdown(
    """
    The indicators are separated by unit so the charts remain readable. This avoids comparing
    percentages, dollars, hours, and employment levels on the same scale.
    """
)

for unit in filtered["unit"].unique():
    unit_data = filtered[filtered["unit"] == unit]
    fig = px.line(
        unit_data,
        x="date",
        y="value",
        color="indicator",
        markers=True,
        title=f"Labor Market Indicators Measured in {unit}",
        labels={
            "date": "Date",
            "value": f"Value ({unit})",
            "indicator": "Indicator"
        }
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("4. Healthcare Employment vs. Total Nonfarm Employment")
comparison = df[df["indicator"].isin(["Healthcare Employment", "Total Nonfarm Employment"])].copy()

comparison["indexed_value"] = comparison.groupby("indicator")["value"].transform(
    lambda x: (x / x.iloc[0]) * 100
)

fig = px.line(
    comparison,
    x="date",
    y="indexed_value",
    color="indicator",
    markers=True,
    title="Indexed Employment Growth: Healthcare vs. Total Nonfarm Employment",
    labels={
        "date": "Date",
        "indexed_value": "Index Value (First Month = 100)",
        "indicator": "Indicator"
    }
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.info(
    """
    Indexing both employment series to 100 allows a fair comparison of growth trends.
    This is important because total nonfarm employment is much larger than healthcare employment.
    """
)

st.markdown("---")

st.subheader("5. Project Insight")
st.markdown(
    """
    The dashboard shows that labor market data can help organizations understand workforce
    pressure, wage trends, and staffing needs. For healthcare organizations, tracking employment,
    wages, and labor force participation can support better decisions about hiring, scheduling,
    budgeting, and long-term operations planning.
    """
)

st.subheader("6. Download Cleaned Data")
st.download_button(
    label="Download Cleaned BLS Dataset",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="bls_labor_data.csv",
    mime="text/csv"
)
