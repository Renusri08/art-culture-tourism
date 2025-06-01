import streamlit as st
st.set_page_config(page_title="Incredible India", layout="wide")
# App title in sidebar
# Sidebar navigation
st.sidebar.title("🧭 Navigation")
# Section selector
page = st.sidebar.radio(
    "Go to",
    ["Home", "Explore Art Forms", "Cultural Heritage sites", "Tourism Analytics", "Funding & Growth", "Recommendations"],
    key="main_nav_radio"  # <--- add a unique key
)

# Navigation logic
if page == "Home":
    import home
    home.run()

elif page == "Explore Art Forms":
    import explore_art_forms
    explore_art_forms.run()

elif page == "Cultural Heritage sites":
    import cultural_heritage
    cultural_heritage.run()

elif page == "Tourism Analytics":
    import tourism_analytics
    tourism_analytics.run()

elif page == "Funding & Growth":
    import funding_growth
    funding_growth.run()

elif page == "Recommendations":
    import recommendations
    recommendations.run()
