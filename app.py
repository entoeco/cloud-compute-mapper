import streamlit as st
import pandas as pd
import pydeck as pdk  # NEW: Streamlit's advanced 3D mapping library

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

    st.write("### Data Center Locations")
    st.markdown("Hover over a node to see cloud infrastructure details.")

    if 'lat' in df.columns and 'lon' in df.columns:
        map_data = df[(df['lat'] != 0.0) & (df['lon'] != 0.0)]

        # --- THE PYDECK UPGRADE ---
        # 1. Define how the data looks (The Layer)
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_color="[0, 255, 0, 200]", # Cyber Green
            #get_radius=2000,  # Base radius in meters
            radius_scale=10,  # Scale radius with zoom level
            radius_min_pixels=2, # Minimum radius in pixels
            pickable=True, # THIS IS THE MAGIC WORD THAT ENABLES HOVERING!
        )

        # 2. Define where the camera starts (The View)
        view_state = pdk.ViewState(
            latitude=map_data['lat'].mean(), # Center camera on the data
            longitude=map_data['lon'].mean(),
            zoom=3,
            pitch=45, # Try changing this to 45 later for a cool 3D angled view!
        )

        # 3. Render the map with a custom HTML tooltip
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>Domain:</b> {target_domain} <br/>"
                        "<b>Provider:</b> {provider} <br/>"
                        "<b>Location:</b> {data_center_location}",
                "style": {
                    "backgroundColor": "#222222",
                    "color": "white",
                    "font-family": "sans-serif"
                }
            }
        ))
    else:
        st.warning("⚠️ Waiting for coordinate data.")

    st.divider()

    st.write("### Provider Market Share")
    provider_counts = df['provider'].value_counts()
    st.bar_chart(provider_counts)

    with st.expander("🔍 View Raw Intelligence Data"):
        st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ Dataset not found.")
