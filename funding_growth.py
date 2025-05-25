import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.header("💰 Funding & Growth of Indian Art & Culture")
    st.markdown("Discover how various Indian art forms have been supported through funding across regions and time.")

    # Load funding data
    funding_data = pd.read_csv("funding_data.csv")

    # Region filter
    regions = sorted(funding_data["region"].dropna().unique())
    selected_region = st.selectbox("Select Region", regions, index=regions.index("North") if "North" in regions else 0)

    # Filter by region
    region_data = funding_data[funding_data["region"] == selected_region]

    # Total funding by state
    st.subheader(f"📍 Total Funding by State – {selected_region}")
    funding_by_state = region_data.groupby("state")["funding_amount"].sum().reset_index().sort_values(by="funding_amount", ascending=False)
    fig1 = px.bar(funding_by_state, x="state", y="funding_amount",
                  labels={"funding_amount": "Funding Amount (₹)"},
                  title=f"Total Funding Distribution by State – {selected_region}",
                  color="funding_amount", color_continuous_scale="Viridis")
    st.plotly_chart(fig1, use_container_width=True)

    # Funding trend over years
    st.subheader(f"📈 Funding Trend Over Years – {selected_region}")
    yearly_trend = region_data.groupby("year")["funding_amount"].sum().reset_index()
    fig2 = px.line(yearly_trend, x="year", y="funding_amount",
                   labels={"funding_amount": "Total Funding (₹)"},
                   title=f"Funding Over the Years – {selected_region}",
                   markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Top funded art forms
    st.subheader(f"🎨 Top Funded Art Forms – {selected_region}")
    top_arts = region_data.groupby("art_form")["funding_amount"].sum().reset_index().sort_values("funding_amount", ascending=False).head(10)
    fig3 = px.bar(top_arts, x="funding_amount", y="art_form", orientation='h',
                  labels={"funding_amount": "Funding Amount (₹)", "art_form": "Art Form"},
                  title=f"Top 10 Funded Art Forms – {selected_region}",
                  color="funding_amount", color_continuous_scale="Sunset")
    st.plotly_chart(fig3, use_container_width=True)

    # Highlight
    if not funding_by_state.empty:
        top_state = funding_by_state.iloc[0]
        st.success(f"🏆 **Highest Funded State**: {top_state['state']} – ₹{top_state['funding_amount']:.2f}")

    st.markdown("---")
