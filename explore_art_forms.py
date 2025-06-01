import streamlit as st
import pandas as pd
from PIL import Image
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
    df = pd.read_sql("SELECT * FROM ARTS", conn)


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
    states = st.sidebar.multiselect("Select States", options=sorted(df['STATE'].unique()), default=None)
    types = st.sidebar.multiselect("Select Types", options=sorted(df['TYPE'].unique()), default=None)
    popularity_threshold = st.sidebar.slider("Minimum Popularity", min_value=0, max_value=int(df['POPULARITY'].max()), value=0)

    # Apply filters
    filtered_df = df.copy()

    if states:
        filtered_df = filtered_df[filtered_df['STATE'].isin(states)]
    if types:
        filtered_df = filtered_df[filtered_df['TYPE'].isin(types)]
    filtered_df = filtered_df[filtered_df['POPULARITY'] >= popularity_threshold]

    # Show count
    st.markdown(f"### Showing {len(filtered_df)} Art Form(s)")

    # Display in a nice format
    for _, row in filtered_df.iterrows():
        with st.expander(f"🎨 {row['ART_FORM']} ({row['TYPE']} - {row['STATE']})"):
            st.markdown(f"**Popularity**: {row['POPULARITY']}")
            st.markdown(f"**Description**: {row['DESCRIPTION']}")

    # Optional: sort option
    if len(filtered_df) > 1:
        sort_by = st.selectbox("Sort by", ["ART_FORM", "POPULARITY"])
        ascending = st.checkbox("Sort ascending", value=True)
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
