import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sky-Graph Dashboard", page_icon="☁️", layout="wide")
st.title("☁️ Project Sky-Graph: Global Cloud Map")

@st.cache_data
def load_data():
    return pd.read_csv("skygraph_dataset.csv")

try:
    df = load_data()
    
    col1, col2 = st.columns(2)
    col1.metric("Domains Scanned", len(df))
    col2.metric("Unique Providers Found", df['provider'].nunique())
    
    st.divider()

    # --- THIS IS THE NEW MAP SECTION ---
    st.write("### Data Center Locations")
    st.markdown("Physical infrastructure routing the target domains.")
    
    if 'lat' in df.columns and 'lon' in df.columns:
        # Filter out bad data
        map_data = df[(df['lat'] != 0.0) & (df['lon'] != 0.0)]
        # Draw the map!
        st.map(map_data, size=5000, color="#00ff00") 
    else:
        st.warning("⚠️ Waiting for coordinate data.")

    st.divider()

    # --- We keep the Bar Chart down here ---
    st.write("### Provider Market Share")
    provider_counts = df['provider'].value_counts()
    st.bar_chart(provider_counts)

    with st.expander("🔍 View Raw Intelligence Data"):
        st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ Dataset not found.")
