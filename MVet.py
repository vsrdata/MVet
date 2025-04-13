import streamlit as st
import pandas as pd
import requests

# Page config
st.set_page_config(page_title="MVet - Pet Clinic Locator", layout="centered")

# --- Styling with gradient title and visible subtitle box ---
st.markdown("""
    <style>
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #1e90ff, #32cd32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .small-box {
        max-width: 600px;
        margin: auto;
        padding: 16px;
        border-radius: 12px;
        background-color: #ffffff;
        color: #333333;
        font-size: 18px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Title and Subtitle ---
st.markdown('<div class="gradient-text">MVet</div>', unsafe_allow_html=True)
st.markdown(
    "<div class='small-box'>One stop for all things you need for your <b>furry friends & fam</b> health! 🐾</div>",
    unsafe_allow_html=True)

# --- Input ---
pincode_input = st.text_input("Enter your location pincode")

# --- Load your clinic data (update the path if needed) ---
url = "https://raw.githubusercontent.com/vsrdata/MVet/refs/heads/main/Veterinary%20Clinic%20Data.csv"
pincode_data = pd.read_csv(url)

# --- Function to geocode using OpenStreetMap Nominatim ---
def get_lat_lon_from_pincode(pincode):
    url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&country=India&format=json"
    response = requests.get(url, headers={'User-Agent': 'MVetApp/1.0'})
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
    return None, None


# --- Main logic for handling input and displaying results ---
if pincode_input and pincode_input.isdigit():
    pincode_input = int(pincode_input)

    if pincode_input in pincode_data["Pincode"].values:
        result_df = pincode_data[pincode_data["Pincode"] == pincode_input][["Hospital Name", "Location"]]

        st.markdown("### Clinics Found:")
        st.dataframe(result_df)

        lat, lon = get_lat_lon_from_pincode(pincode_input)
        if lat and lon:
            st.markdown("### Location Map:")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        else:
            st.warning("Could not fetch coordinates for this pincode.")
    else:
        st.error("No clinics found for this pincode or invalid input.")
        st.info("Try again entering a valid pincode.")

