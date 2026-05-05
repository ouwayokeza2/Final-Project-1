"""
Streamlit dashboard for U.S. labor market indicators with a healthcare focus.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path("data/bls_labor_data.csv")


st.set_page_config(
    page_title="U.S. Labor Market Dashboard",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the dashboard data."""
    if not DATA_PATH.exists():
        st.info("Data file not found. Fetching BLS data now...")
        from fetch_bls_data import update_dataset
        update_dataset()

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.sort_values(["indicator", "date"])
    return df    


df = load_data()

st.title("U.S. Labor Market Dashboard with Healthcare Focus")
st.write(
    "This dashboard uses Bureau of Labor Statistics data to show national labor "
    "market trends and connect them to healthcare workforce conditions."
)

latest_date = df["date"].max()
st.caption(f"Most recent observation in dataset: {latest_date.strftime('%B %Y')}")

st.sidebar.header("Dashboard Filters")

indicators = sorted(df["indicator"].unique())
selected_indicators = st.sidebar.multiselect(
    "Choose indicators",
    indicators,
    default=indicators,
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Choose date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["indicator"].isin(selected_indicators))
    & (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
].copy()

st.subheader("Latest Labor Market Snapshot")

latest_rows = (
    filtered.sort_values("date")
    .groupby("indicator", as_index=False)
    .tail(1)
    .sort_values("indicator")
)

cols = st.columns(3)
for idx, row in enumerate(latest_rows.itertuples(index=False)):
    with cols[idx % 3]:
        st.metric(
            label=row.indicator,
            value=f"{row.value:,.2f}",
            delta=None
            if pd.isna(row.month_to_month_change)
            else f"{row.month_to_month_change:,.2f} from previous month",
        )

st.divider()

st.subheader("Labor Market Trends Over Time")

if filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    fig = px.line(
        filtered,
        x="date",
        y="value",
        color="indicator",
        markers=True,
        title="Selected Labor Market Indicators",
        labels={
            "date": "Date",
            "value": "Value",
            "indicator": "Indicator",
        },
    )
    fig.update_layout(legend_title_text="Indicator")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Healthcare Employment Compared with Total Nonfarm Employment")

comparison = df[
    df["indicator"].isin(["Healthcare Employment", "Total Nonfarm Employment"])
].copy()

comparison = comparison[
    (comparison["date"].dt.date >= start_date)
    & (comparison["date"].dt.date <= end_date)
]

if not comparison.empty:
    fig2 = px.line(
        comparison,
        x="date",
        y="value",
        color="indicator",
        markers=True,
        title="Healthcare Employment and Total Nonfarm Employment",
        labels={
            "date": "Date",
            "value": "Employment Level",
            "indicator": "Indicator",
        },
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Month-to-Month Changes")

change_data = filtered.dropna(subset=["month_to_month_change"])

if not change_data.empty:
    fig3 = px.bar(
        change_data,
        x="date",
        y="month_to_month_change",
        color="indicator",
        barmode="group",
        title="Monthly Change by Indicator",
        labels={
            "date": "Date",
            "month_to_month_change": "Month-to-Month Change",
            "indicator": "Indicator",
        },
    )
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Cleaned Dataset")

st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="filtered_bls_labor_data.csv",
    mime="text/csv",
)

st.markdown(
    """
    ### Interpretation

    The dashboard helps show how national employment, unemployment, wages,
    labor force participation, and healthcare employment move over time. This is
    useful for understanding workforce availability, wage pressure, and staffing
    challenges in healthcare and operations-focused industries.
    """
)
