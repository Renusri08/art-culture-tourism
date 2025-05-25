import streamlit as st
import pandas as pd
from PIL import Image


def run():
    
    
    # your art form filtering code here
    @st.cache_data
    def load_art_forms():
        df = pd.read_csv("art_forms_data.csv")
        return df

    df = load_art_forms()

    # Page title
    st.title("🎭 Explore Traditional Art Forms")
    st.markdown("Discover diverse traditional art forms from across India. Use the filters to explore art by state, type, and popularity.")
    # Art Gallery Section
    st.markdown("---")
    st.subheader("🖼️ Art Gallery")

    gallery_data = [
        {"name": "Kathakali", "state": "Kerala", "file": "images/kathakkali.png"},
        {"name": "Madhubani Painting", "state": "Bihar", "file": "images/madhubani.png"},
        {"name": "Pattachitra", "state": "Odisha", "file": "images/pattachithra.png"},
    ]

    img_cols = st.columns(3)

    for i, item in enumerate(gallery_data):
        with img_cols[i]:
            img = Image.open(item["file"])
            img = img.resize((250, 250))  # Resize to uniform dimensions
            st.image(img, caption=f"{item['name']} – {item['state']}")
    # Sidebar filters
    st.sidebar.header("Filter Art Forms")
    states = st.sidebar.multiselect("Select States", options=sorted(df['state'].unique()), default=None)
    types = st.sidebar.multiselect("Select Types", options=sorted(df['type'].unique()), default=None)
    popularity_threshold = st.sidebar.slider("Minimum Popularity", min_value=0, max_value=int(df['popularity'].max()), value=0)

    # Apply filters
    filtered_df = df.copy()

    if states:
        filtered_df = filtered_df[filtered_df['state'].isin(states)]
    if types:
        filtered_df = filtered_df[filtered_df['type'].isin(types)]
    filtered_df = filtered_df[filtered_df['popularity'] >= popularity_threshold]

    # Show count
    st.markdown(f"### Showing {len(filtered_df)} Art Form(s)")

    # Display in a nice format
    for _, row in filtered_df.iterrows():
        with st.expander(f"🎨 {row['art_form']} ({row['type']} - {row['state']})"):
            st.markdown(f"**Popularity**: {row['popularity']}")
            st.markdown(f"**Description**: {row['description']}")

    # Optional: sort option
    if len(filtered_df) > 1:
        sort_by = st.selectbox("Sort by", ["art_form", "popularity"])
        ascending = st.checkbox("Sort ascending", value=True)
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
