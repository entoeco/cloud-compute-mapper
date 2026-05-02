import streamlit as st
import pandas as pd
import pydeck as pdk  # Streamlit's advanced 3D mapping library

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

    st.write("### Data Center & University Campus Locations")
    st.markdown("Hover over a point to see details. Green points are data centers, blue points are university campuses, and red lines connect campuses to their data centers.")
    st.markdown("**Legend:** 🟢 Data Centers | 🔵 University Campuses | 🔴 Campus to Data Center Connection")

    # Filter out rows with missing lat/lon for both data centers and campuses
    map_data_dc = df[(df['lat'].notna()) & (df['lon'].notna()) & (df['lat'] != 0.0) & (df['lon'] != 0.0)]
    map_data_campus = df[(df['campus_lat'].notna()) & (df['campus_lon'].notna())]
    # Filter data for lines: ensure both campus and data center coordinates are available
    map_data_lines = df[
        (df['lat'].notna()) & (df['lon'].notna()) & (df['lat'] != 0.0) & (df['lon'] != 0.0) &
        (df['campus_lat'].notna()) & (df['campus_lon'].notna())
    ]

    if not map_data_dc.empty or not map_data_campus.empty or not map_data_lines.empty:

        # Data Center Layer (Green)
        data_center_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data_dc,
            get_position="[lon, lat]",
            get_color="[0, 255, 0, 200]", # Cyber Green
            radius_scale=10,
            radius_min_pixels=2,
            pickable=True,
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
        )

        # University Campus Layer (Blue)
        campus_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data_campus,
            get_position="[campus_lon, campus_lat]",
            get_color="[0, 150, 255, 200]", # Blue
            radius_scale=10,
            radius_min_pixels=2,
            pickable=True,
            tooltip={
                "html": "<b>University:</b> {university_name} <br/>"
                        "<b>Campus Location (Approx):</b> {campus_lat}, {campus_lon}",
                "style": {
                    "backgroundColor": "#222222",
                    "color": "white",
                    "font-family": "sans-serif"
                }
            }
        )

        # Line Layer (Red) connecting campus to data center
        line_layer = pdk.Layer(
            "LineLayer",
            data=map_data_lines,
            get_source_position="[campus_lon, campus_lat]",
            get_target_position="[lon, lat]",
            get_color="[255, 0, 0, 160]", # Red lines
            get_width=3,
            pickable=True,
            tooltip={
                "html": "<b>University:</b> {university_name} <br/>"
                        "<b>Data Center Provider:</b> {provider}",
                "style": {
                    "backgroundColor": "#222222",
                    "color": "white",
                    "font-family": "sans-serif"
                }
            }
        )

        # Combine layers
        layers = [data_center_layer, campus_layer, line_layer]

        # Define where the camera starts (The View)
        # Use mean of all relevant coordinates for initial view
        all_latitudes = pd.concat([map_data_dc['lat'], map_data_campus['campus_lat']]).dropna()
        all_longitudes = pd.concat([map_data_dc['lon'], map_data_campus['campus_lon']]).dropna()

        if not all_latitudes.empty and not all_longitudes.empty:
            view_state = pdk.ViewState(
                latitude=all_latitudes.mean(),
                longitude=all_longitudes.mean(),
                zoom=3,
                pitch=45, # Angled view
            )

            # Render the map
            st.pydeck_chart(pdk.Deck(
                layers=layers,
                initial_view_state=view_state,
                tooltip=True
            ))
        else:
            st.warning("⚠️ No valid coordinates found to display map.")
    else:
        st.warning("⚠️ Waiting for coordinate data or no valid data to display.")

    st.divider()

    st.write("### Provider Market Share")
    provider_counts = df['provider'].value_counts()
    st.bar_chart(provider_counts)

    with st.expander("🔍 View Raw Intelligence Data"):
        # Changed use_container_width=True to width='stretch'
        st.dataframe(df, width='stretch')

except FileNotFoundError:
    st.error("⚠️ Dataset not found.")
