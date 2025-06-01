import streamlit as st
import pandas as pd
import plotly.express as px
import re
import snowflake.connector

def run():
    conn = snowflake.connector.connect(
        user='Renusri',
        password='Renusri@1243potru',
        account='UPWBOZP-TB41452',   
        warehouse='COMPUTE_WH',
        database='HACKEREARTH',
        schema='PUBLIC'
    )
    heritage_data = pd.read_sql("SELECT * FROM HERITAGE_SITES", conn)

    st.header("🕌 The Living Legacy – A Story Through India's Heritage")

    st.markdown("""
    > _"In every crumbling fort, every sculpted temple, and every silent ruin, India whispers her story."_  
    From the snow-clad monasteries of the North to the ancient stepwells of the West, India's cultural heritage sites are **more than architecture** — they are **breathing chapters** of a timeless epic.
    """)

    # Age insights
    import re

# Sort by extracted numeric age to ensure correct ordering
    heritage_data['AGE_CLEANED'] = heritage_data['AGE_OF_HERITAGE'].astype(str).str.extract(r'(\d+)').astype(float)
    oldest_sites = heritage_data.sort_values(by="AGE_CLEANED", ascending=False).head(5)

    st.subheader("📜 Oldest Living Monuments")

    for _, row in oldest_sites.iterrows():
        age_raw = str(row['AGE_OF_HERITAGE'])
        match = re.search(r'\d+', age_raw)
        if match:
            age = int(match.group())
            age_str = f"{age} years old"
        else:
            age_str = "Age unknown"

        st.markdown(f"- **{row['NAME_OF_HERITAGE']}**, {row['CITY_NAME']}, {row['STATE']} – *{age_str}*")

    st.markdown("""
    These sites stand as **pillars of resilience**, surviving centuries of invasions, empires, and evolution — bearing the spiritual and cultural DNA of the land.
    """)


    # Nature of heritage
    nature_counts = heritage_data["NATURE_OF_HERITAGE"].value_counts().reset_index()
    nature_counts.columns = ["Nature", "Count"]

    st.subheader("🏛️ What Kind of Heritage Do We Preserve?")
    fig1 = px.pie(nature_counts, names="Nature", values="Count", title="Nature of Heritage Sites")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    Whether **Architectural Marvels**, **Natural Wonders**, or **Archaeological Remnants**, each heritage site is a **dialogue between time and terrain**.
    """)

    # Heritage use
    use_counts = heritage_data["HERITAGE_USE"].value_counts().reset_index()
    use_counts.columns = ["Use", "Count"]

    st.subheader("🧭 Purpose Over Time")
    fig2 = px.bar(use_counts, x="Use", y="Count", title="How Heritage Sites Are Used Today", color="Use")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    Many sites remain **religiously active**, while others evolve into **museums, learning centers, or silent ruins** — all of them continue to serve the people in their own quiet ways.
    """)

    # Zone-wise diversity
    zone_counts = heritage_data.groupby("ZONE_NAME")["NAME_OF_HERITAGE"].count().reset_index().sort_values(by="NAME_OF_HERITAGE", ascending=False)
    zone_counts.columns = ["Zone", "Count"]

    st.subheader("🗺️ Heritage Hotspots Across Zones")
    fig3 = px.bar(zone_counts, x="Zone", y="Count", title="Number of Heritage Sites by Zone", color="Zone")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Southern and Northern India** emerge as heritage havens — their temples, forts, and cultural corridors continuing to attract both pilgrims and tourists alike.
    """)

    # Story-style ending
    st.markdown("""
    ---
    ## 🌟 Why Heritage Matters

    These aren’t just places — they are **portals**. Portals into **rituals performed under starlit skies**, into **wars fought for love or honor**, into **prayers whispered for rain, peace, or prosperity**.

    Preserving and promoting them isn’t just about tourism.  
    It’s about **identity, legacy, and pride**.

    > _"To walk the paths of our ancestors is to remember who we are — and who we can become."_  

    Let India’s heritage not be buried beneath time. Let it **shine through mindful tourism**, **restoration**, and **storytelling**.

    """)

   
