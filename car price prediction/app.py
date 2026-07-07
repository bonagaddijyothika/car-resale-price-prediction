import streamlit as st
import pickle
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="wide"
)

# ---------------- BACKGROUND ----------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://cdn.wallpapersafari.com/81/82/hilSnu.jpg");
    background-size: cover;
    background-position: center;
}
.main {
    background-color: rgba(255,255,255,0.92);
    padding: 25px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 style='color:black'>🚗  Car Price Estimator</h1>", unsafe_allow_html=True)
st.write("Check the estimated resale value of your car")

# ---------------- LOAD MODEL ----------------
try:
    if not os.path.exists("car_price_model.pkl"):
        st.error("❌ Model file not found: car_price_model.pkl")
        st.stop()
    if not os.path.exists("model_columns.pkl"):
        st.error("❌ Column metadata file not found: model_columns.pkl")
        st.stop()
    
    model = pickle.load(open("car_price_model.pkl", "rb"))
    model_columns = pickle.load(open("model_columns.pkl", "rb"))
except Exception as e:
    st.error(f"Error loading model files: {str(e)}")
    st.stop()

# ---------------- BRAND → MODEL DATA ----------------
brand_models = {
    "Maruti Suzuki": ["Swift", "Baleno", "Dzire"],
    "Hyundai": ["i10", "i20", "Creta"],
    "Honda": ["City", "Amaze"],
    "Tata": ["Nexon", "Harrier"],
    "Toyota": ["Innova", "Fortuner"],
    "Audi": ["A4", "A6"],
    "BMW": ["X1", "X5"],
    "Mercedes": ["C-Class", "E-Class"]
}

brand_multiplier = {
    "Maruti Suzuki": 1.0,
    "Hyundai": 1.05,
    "Honda": 1.1,
    "Tata": 1.05,
    "Toyota": 1.15,
    "Audi": 1.6,
    "BMW": 1.5,
    "Mercedes": 1.7
}

model_multiplier = {
    "Swift": 1.0, "Baleno": 1.05, "Dzire": 1.02,
    "i10": 1.0, "i20": 1.08, "Creta": 1.15,
    "City": 1.12, "Amaze": 1.05,
    "Nexon": 1.1, "Harrier": 1.2,
    "Innova": 1.3, "Fortuner": 1.5,
    "A4": 1.4, "A6": 1.6,
    "X1": 1.4, "X5": 1.7,
    "C-Class": 1.5, "E-Class": 1.7
}

# ---------------- SIDEBAR (LIKE CARWALE) ----------------
st.sidebar.header("Car Details")

brand = st.sidebar.selectbox("Brand", list(brand_models.keys()))
model_name = st.sidebar.selectbox("Model", brand_models[brand])

fuel = st.sidebar.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
transmission = st.sidebar.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.sidebar.selectbox("Owner", [0, 1, 2, 3])

present_price = st.sidebar.slider("Original Price (Lakhs)", 2.0, 60.0, 8.0)
kms = st.sidebar.slider("Kilometers Driven", 0, 250000, 40000)
age = st.sidebar.slider("Car Age (Years)", 0, 20, 5)

# ---------------- INPUT DATA ----------------
input_df = pd.DataFrame({
    "Present_Price": [present_price],
    "Kms_Driven": [kms],
    "Owner": [owner],
    "Car_Age": [age]
})

for col in model_columns:
    if col not in input_df.columns:
        input_df[col] = 0

if "Fuel_Type_Diesel" in model_columns:
    input_df["Fuel_Type_Diesel"] = 1 if fuel == "Diesel" else 0
if "Fuel_Type_Petrol" in model_columns:
    input_df["Fuel_Type_Petrol"] = 1 if fuel == "Petrol" else 0
if "Transmission_Manual" in model_columns:
    input_df["Transmission_Manual"] = 1 if transmission == "Manual" else 0

input_df = input_df[model_columns]

# ---------------- PREDICTION ----------------
st.markdown("---")

if st.button("💰 Check Car Value"):
    base_price = model.predict(input_df)[0]

    final_price = (
        base_price
        * brand_multiplier[brand]
        * model_multiplier[model_name]
    )

    if final_price < 10:
        final_price = 10

    st.success(f"Estimated Resale Value: ₹ {final_price:.2f} Lakhs")

    st.markdown(f"""
    **Brand:** {brand}  
    **Model:** {model_name}  
    **Fuel:** {fuel}  
    **Transmission:** {transmission}  
    """)

    st.info("This estimate is based on market trends, car condition & brand value.")
