from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
)


DATA_FILE = Path(__file__).with_name("sales_data_capstone.csv")


@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv(DATA_FILE)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Sales_Amount"] = pd.to_numeric(df["Sales_Amount"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")

    return df


if st.button("🔄 Pārlādēt datus"):
    st.cache_data.clear()
    st.rerun()

df = load_data()


st.sidebar.title("Filtri")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Reģions",
    options=regions,
    default=regions,
)

categories = sorted(df["Product_Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Produkta Kategorija",
    options=categories,
    default=categories,
)

segments = sorted(df["Customer_Segment"].dropna().unique())
selected_segments = st.sidebar.multiselect(
    "Klientu segments",
    options=segments,
    default=segments,
)


filtered_df = df.copy()

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        & (filtered_df["Date"] <= end_date)
    ]

filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
filtered_df = filtered_df[
    filtered_df["Product_Category"].isin(selected_categories)
]
filtered_df = filtered_df[
    filtered_df["Customer_Segment"].isin(selected_segments)
]


st.title("📊 Sales Performance Dashboard")
st.caption("Izmanto filtrus kreisajā pusē, lai uzzinātu detalizētaku info.")

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 26px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


total_sales = filtered_df["Sales_Amount"].sum()
total_profit = filtered_df["Profit"].sum()
average_discount = filtered_df["Discount"].mean()
average_discount_display = f"{average_discount:.2%}"
transactions = len(filtered_df)
profit_margin = total_profit / total_sales * 100 if total_sales != 0 else 0


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Kēpējie ieņēmumi", f"€{total_sales:,.2f}")
col2.metric("Kopējā Peļņa", f"€{total_profit:,.2f}")
col3.metric("Vidējā Atlaide", average_discount_display)
col4.metric("Darījumu skaits", f"{transactions:,}")
col5.metric("Peļņas Margin", f"{profit_margin:,.2f}%")

st.divider()


sales_over_time = (
    filtered_df.groupby("Date", as_index=False)["Sales_Amount"]
    .sum()
    .sort_values("Date")
)

fig = px.line(
    sales_over_time,
    x="Date",
    y="Sales_Amount",
    markers=True,
    title="Ieņēmumi konkrētā laika periodā",
)

fig.update_layout(
    template="plotly_white",
    title={"x": 0.5, "xanchor": "center"},
    xaxis_title="Datums",
    yaxis_title="Ieņēmumi(€)",
    hovermode="x unified",
)

st.plotly_chart(fig, width="stretch")


monthly_sales = filtered_df.copy()
monthly_sales["Month_Num"] = monthly_sales["Date"].dt.month
monthly_sales = monthly_sales.groupby("Month_Num", as_index=False)[
    "Sales_Amount"
].sum()

month_names_lv = {
    1: "Janvāris",
    2: "Februāris",
    3: "Marts",
    4: "Aprīlis",
    5: "Maijs",
    6: "Jūnijs",
    7: "Jūlijs",
    8: "Augusts",
    9: "Septembris",
    10: "Oktobris",
    11: "Novembris",
    12: "Decembris",
}

monthly_sales["Mēnesis"] = monthly_sales["Month_Num"].map(month_names_lv)
max_sales = monthly_sales["Sales_Amount"].max()
monthly_sales["Status"] = monthly_sales["Sales_Amount"].apply(
    lambda x: "Lielākais mēnesis" if x == max_sales else "Pārējie mēneši"
)

fig_monthly = px.bar(
    monthly_sales,
    x="Mēnesis",
    y="Sales_Amount",
    color="Status",
    color_discrete_map={
        "Lielākais mēnesis": "#E76F51",
        "Pārējie mēneši": "#A8DADC",
    },
    category_orders={
        "Mēnesis": [
            "Janvāris",
            "Februāris",
            "Marts",
            "Aprīlis",
            "Maijs",
            "Jūnijs",
            "Jūlijs",
            "Augusts",
            "Septembris",
            "Oktobris",
            "Novembris",
            "Decembris",
        ]
    },
)

fig_monthly.update_traces(texttemplate="€%{y:,.2f}", textposition="outside")
fig_monthly.update_layout(
    template="plotly_white",
    title={
        "text": "<b>Ieņēmumi pa mēnešiem</b>",
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="Mēnesis",
    yaxis_title="Ieņēmumi (€)",
    showlegend=False,
    height=500,
    margin=dict(l=60, r=30, t=80, b=70),
)

st.plotly_chart(fig_monthly, width="stretch")


left, right = st.columns(2)

profit_by_region = (
    filtered_df.groupby("Region", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig_region = px.bar(
    profit_by_region,
    x="Region",
    y="Profit",
    color="Region",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Peļņa pēc reģiona",
)

fig_region.update_traces(texttemplate="€%{y:,.2f}", textposition="outside")
fig_region.update_layout(
    template="plotly_white",
    title={"text": "<b>Peļņa pēc reģiona</b>", "x": 0.5, "xanchor": "center"},
    xaxis_title="Reģions",
    yaxis_title="Peļņa (€)",
    showlegend=False,
    height=500,
    margin=dict(l=50, r=30, t=80, b=60),
)

left.plotly_chart(fig_region, width="stretch")


sales_by_category = (
    filtered_df.groupby("Product_Category", as_index=False)["Sales_Amount"]
    .sum()
    .sort_values("Sales_Amount", ascending=False)
)

fig_category = px.bar(
    sales_by_category,
    x="Product_Category",
    y="Sales_Amount",
    title="Ieņēmumi pēc produktu kategorijas",
    color="Product_Category",
    color_continuous_scale="Teal",
)

fig_category.update_layout(
    template="plotly_white",
    title={
        "text": "<b>Ieņēmumi pēc produktu kategorijas</b>",
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="Produktu kategorija",
    yaxis_title="Ieņēmumi (€)",
    showlegend=False,
    height=500,
    margin=dict(l=50, r=30, t=80, b=60),
)

right.plotly_chart(fig_category, width="stretch")


st.subheader("Ieņēmumi vs. Peļņa")

fig_sales_profit = px.scatter(
    filtered_df,
    x="Sales_Amount",
    y="Profit",
    color="Region",
    hover_data=["Product_Category", "Customer_Segment", "Discount"],
)

fig_sales_profit.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Ieņēmum (€)",
    yaxis_title="Peļņa (€)",
)

st.plotly_chart(fig_sales_profit, width="stretch")


st.subheader("Ieņēmumi pēc reģiona un preces kategorijas")

sunburst_data = filtered_df.groupby(
    ["Region", "Product_Category"], as_index=False
)["Sales_Amount"].sum()

fig_sunburst = px.sunburst(
    sunburst_data,
    path=["Region", "Product_Category"],
    values="Sales_Amount",
    color="Sales_Amount",
    color_continuous_scale="Blues",
)

fig_sunburst.update_layout(
    template="plotly_white",
    title_x=0.5,
    coloraxis_showscale=False,
)

st.plotly_chart(fig_sunburst, width="stretch")


with st.expander("View filtered data"):
    st.dataframe(filtered_df, width="stretch")
