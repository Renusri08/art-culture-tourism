from PIL import Image
import streamlit as st
import pandas as pd
import random
import os


def run():
    # Load datasets
    heritage_data = pd.read_csv("heritage_sites_data.csv")
    tourism_data = pd.read_csv("tourism_data.csv")
    art_data = pd.read_csv("art_forms_data.csv")

    
    st.markdown("<h1 style='text-align: center;'>🇮🇳 Welcome to the Cultural Gateway of Incredible India</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Explore timeless traditions, historical marvels, and travel responsibly.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])  # adjust ratio as needed

    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.write("Current working directory:", os.getcwd())
        st.write("Files in this directory:", os.listdir())
        img=Image.open("main.png")
        st.image(img, width=500)  # or your preferred size

    with col2:
        st.markdown("""
        ### ✨ Discover India's Cultural Soul  
        Journey through centuries of tradition, breathtaking heritage sites, and vibrant art forms.  
        This platform invites you to:
        
        - 🎨 Explore regional art and craftsmanship  
        - 🏛️ Witness ancient architecture and spiritual sites  
        - 🌍 Travel mindfully with responsible tourism tips  

        **Uncover the heartbeat of India — one culture at a time.**
        """)

    st.markdown("---")

    # Thematic Cards
    st.subheader("🧭 What would you like to explore?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎭 Traditional Art Forms")
        st.markdown("Dive into India’s rich artscape of dance, crafts, and performance.")
        st.button("Explore Art", key="btn1", on_click=lambda: st.session_state.update({"main_nav_radio": "Explore Art Forms"}))

    with col2:
        st.markdown("### 🏛️ Cultural Heritage Map")
        st.markdown("Discover India's heritage through geo-visual experiences.")
        st.button("View Map", key="btn2", on_click=lambda: st.session_state.update({"main_nav_radio": "Cultural Heritage Map"}))

    with col3:
        st.markdown("### 🌿 Responsible Tourism")
        st.markdown("Learn trends and support sustainable journeys across regions.")
        st.button("Tourism Insights", key="btn3", on_click=lambda: st.session_state.update({"main_nav_radio": "Tourism Analytics"}))

    st.markdown("---")

    # KPIs
    st.subheader("📊 Cultural Snapshot")
    col1, col2, col3 = st.columns(3)
    col1.metric("🗺️ Heritage Sites", len(heritage_data))
    col2.metric("🎨 Art Forms", art_data['art_form'].nunique())
    col3.metric("📍 Regions Covered", tourism_data['region'].nunique())

    st.markdown("---")

    # 🔎 Search for an Art Form
    st.subheader("🔍 Search an Art Form")
    search_term = st.text_input("Enter art form name or state:")
    if search_term:
        results = art_data[art_data['art_form'].str.contains(search_term, case=False) | art_data['state'].str.contains(search_term, case=False)]
        if not results.empty:
            for _, row in results.iterrows():
                st.markdown(f"🎨 **{row['art_form']}** ({row['type']} – {row['state']})  \n_{row['description']}_")
        else:
            st.warning("No matching art forms found.")

    st.markdown("---")

    # 🗺️ Cultural Image Gallery
    st.subheader("🖼️ Cultural Glimpses")
    art_samples = art_data.sample(n=3)
    img_cols = st.columns(3)
    for i, (_, row) in enumerate(art_samples.iterrows()):
        with img_cols[i]:
            st.markdown(f"**{row['art_form']}** – {row['state']}")
            st.image("https://source.unsplash.com/400x300/?india,culture", use_column_width=True)

    st.markdown("---")

        # PLAN MY TRIP SECTION
    st.markdown("---")
    st.subheader("🧳 Plan My Cultural Trip")

    st.markdown("Customize your preferences and discover the best places to experience India's cultural richness:")

    # User inputs
    trip_col1, trip_col2 = st.columns(2)

    with trip_col1:
        interests = st.multiselect(
            "Select your interests",
            ["Art & Handicrafts", "Historical Heritage", "Cultural Festivals", "Spiritual Places", "Nature & Scenic Spots"],
            default=["Art & Handicrafts"]
        )
        selected_regions = st.multiselect(
            "Preferred Regions",
            sorted(heritage_data["ZONE_NAME"].dropna().unique()),
            default=["North"]
        )

    with trip_col2:
        travel_months = st.multiselect(
            "Preferred Travel Months",
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            default=["Dec", "Jan"]
        )

    # Generate suggestions
    if st.button("🔍 Show Recommendations"):
        st.markdown("### ✨ Recommended Destinations & Experiences")

        # Filter heritage data
        matched_sites = heritage_data[heritage_data["ZONE_NAME"].isin(selected_regions)]

        if "Historical Heritage" in interests:
            st.markdown("**🏛️ Heritage Sites to Explore:**")
            for _, row in matched_sites.sample(min(3, len(matched_sites))).iterrows():
                st.markdown(f"- {row['NAME_OF_HERITAGE']} ({row['CITY_NAME']}, {row['STATE']}) – *{row['NATURE_OF_HERITAGE']}*")

        if "Art & Handicrafts" in interests:
            matched_arts = art_data[art_data["state"].isin(matched_sites["STATE"].unique())]
            st.markdown("**🎨 Local Art Forms You Shouldn't Miss:**")
            for _, row in matched_arts.sample(min(3, len(matched_arts))).iterrows():
                st.markdown(f"- {row['art_form']} ({row['state']}) – *{row['type']}*")

        if "Cultural Festivals" in interests:
            st.markdown("**🎉 Suggested Festival Seasons:**")
            if any(month in ["Oct", "Nov"] for month in travel_months):
                st.markdown("- Diwali and Navaratri are widely celebrated during these months in Western and Northern India.")
            if any(month in ["Jan", "Feb"] for month in travel_months):
                st.markdown("- Pongal and Republic Day parades are highlights in South and North.")
            if any(month in ["Jul", "Aug", "Sep"] for month in travel_months):
                st.markdown("- Monsoon and harvest festivals across East and North-East.")

        if "Spiritual Places" in interests:
            st.markdown("**🕉️ Spiritual & Pilgrimage Spots:**")
            for site in matched_sites[matched_sites["HERITAGE_USE"].str.contains("religious", case=False, na=False)].sample(min(2, 5)).itertuples():
                st.markdown(f"- {site.NAME_OF_HERITAGE} ({site.STATE})")

        if "Nature & Scenic Spots" in interests:
            st.markdown("**🏞️ Nature-Centric Heritage Sites:**")
            for site in matched_sites[matched_sites["NATURE_OF_HERITAGE"].str.contains("Natural", case=False, na=False)].sample(min(2, 5)).itertuples():
                st.markdown(f"- {site.NAME_OF_HERITAGE} ({site.STATE})")

        st.success("Travel mindfully! Consider visiting off-season or less-crowded destinations for a more sustainable experience.")


    # 💎 Hidden Gem
    st.subheader("💎 Hidden Cultural Gem")
    sample_art = art_data.sample(1).iloc[0]
    st.markdown(f"**{sample_art['art_form']}** from **{sample_art['state']}** – {sample_art['description']}")

    st.info("Navigate using the sidebar to begin your immersive journey through India's cultural and tourism landscape.")
