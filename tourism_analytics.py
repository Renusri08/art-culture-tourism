import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("📊 Tourism Analytics Dashboard")
    st.markdown("Gain insights into how tourism is evolving across Indian states and regions, month-by-month and year-by-year.")

    # Load data
    @st.cache_data
    def load_data():
        tourism_df = pd.read_csv("tourism_data.csv")
        monthly_df = pd.read_csv("monthly_tourism_data.csv")
        return tourism_df, monthly_df

    tourism_df, monthly_df = load_data()

    # Sidebar filters
    st.sidebar.header("Filter Options")
    years = sorted(tourism_df['year'].unique())
    regions = sorted(tourism_df['region'].dropna().unique())

    selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
    selected_regions = st.sidebar.multiselect("Select Region(s)", regions, default=["North"])
    # Filtered DataFrames
    tourism_filtered = tourism_df[(tourism_df['year'] == selected_year) & (tourism_df['region'].isin(selected_regions))]
    monthly_filtered = monthly_df[(monthly_df['year'] == selected_year) & (monthly_df['region'].isin(selected_regions))]
    region_label = ", ".join(selected_regions)
    # KPIs
    st.markdown(f"### National Overview – {selected_year} in {region_label}")
    col1, col2= st.columns(2)
    col1.metric("Total Visitors in", f"{int(tourism_filtered['visitors'].sum()):,}")
    col2.metric("Avg. Growth Rate (%)", f"{tourism_filtered['growth_rate'].mean():.2f}")
    selected_region = tourism_filtered.groupby("region")["visitors"].sum().idxmax()
    
      
    st.markdown("---")

    # Top 10 states by visitors (always overall, no filter)
    st.subheader("🏆 All-Time Top 10 States by Visitor Count")
    top_states = tourism_df.groupby("state")["visitors"].sum().nlargest(10).reset_index()
    fig_top_states = px.bar(
        top_states,
        x="state",
        y="visitors",
        color="state",
        title="Top 10 Tourist States (Overall)",
        labels={"visitors": "Number of Visitors"},
    )
    st.plotly_chart(fig_top_states, use_container_width=True)

    # Growth rate trend (filtered)
    region_label = ", ".join(selected_regions)
    st.subheader(f"📈 Growth Rate Trend – {region_label}")
    growth_trend = tourism_df[tourism_df['region'].isin(selected_regions)].groupby(["year", "region"])["growth_rate"].mean().reset_index()
    fig_growth = px.line(
        growth_trend,
        x="year",
        y="growth_rate",
        color="region",
        markers=True,
        title=f"Growth Rate Over Time for {region_label}",
        labels={"growth_rate": "Growth Rate (%)"},
    )
    st.plotly_chart(fig_growth, use_container_width=True)

    # Monthly trends
    st.subheader(f"📅 Monthly Visitor Trends – {selected_year} – {region_label}")
    monthly_sorted = monthly_filtered.sort_values(by="month_num")
    fig_monthly = px.line(
        monthly_sorted,
        x="month_num",
        y="visitors",
        color="state",
        markers=True,
        labels={"month_num": "Month", "visitors": "Visitors"},
        title=f"Monthly Tourism Trend in {region_label} – {selected_year}"
    )
    fig_monthly.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=[
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]))
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Sustainable tourism tip
    st.info("🌱 **Sustainable Tourism Tip**: Encourage exploration of lesser-known cultural destinations in peak months to reduce pressure on top tourist spots.")

    # Expandable raw data
    with st.expander("📄 View Raw Data"):
        st.markdown("#### Yearly Summary (Filtered)")
        st.dataframe(tourism_filtered.reset_index(drop=True))
        st.markdown("#### Monthly Trends (Filtered)")
        st.dataframe(monthly_filtered.reset_index(drop=True))
