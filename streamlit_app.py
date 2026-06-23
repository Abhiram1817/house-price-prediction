import streamlit as st
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('features.pkl', 'rb') as f:
    feature_names = pickle.load(f)

st.set_page_config(page_title="House Price Estimator", page_icon="🏡", layout="wide")

st.markdown("## 🏡 House Price Estimator")
st.markdown("Fill in the property details below to get an estimated sale price.")
st.divider()

# ── SECTION 1: Location & Lot ──────────────────────────────
st.markdown("#### 📍 Location & Lot")
col1, col2 = st.columns(2)

with col1:
    lot_area = st.number_input("Lot Area (sq ft)", min_value=1000, max_value=50000, value=8000, step=500)

with col2:
    lot_shape = st.selectbox("Lot Shape", ["Regular", "Slightly Irregular", "Moderately Irregular", "Irregular"])
    lot_shape_map = {"Regular": "Reg", "Slightly Irregular": "IR1", "Moderately Irregular": "IR2", "Irregular": "IR3"}

st.divider()

# ── SECTION 2: House Style & Structure ─────────────────────
st.markdown("#### 🏠 House Style & Structure")
col4, col5, col6 = st.columns(3)

with col4:
    house_style = st.selectbox("House Style", [
        "1 Story", "2 Story", "1.5 Story Finished",
        "Split Level", "Split Foyer", "1.5 Story Unfinished"
    ])
    style_map = {
        "1 Story": "1Story", "2 Story": "2Story",
        "1.5 Story Finished": "1.5Fin", "Split Level": "SLvl",
        "Split Foyer": "SFoyer", "1.5 Story Unfinished": "1.5Unf"
    }

with col5:
    overall_qual = st.select_slider("Overall Condition",
        options=["Very Poor", "Poor", "Fair", "Below Average", "Average",
                 "Above Average", "Good", "Very Good", "Excellent", "Outstanding"],
        value="Average"
    )
    quality_map = {
        "Very Poor": 1, "Poor": 2, "Fair": 3, "Below Average": 4,
        "Average": 5, "Above Average": 6, "Good": 7,
        "Very Good": 8, "Excellent": 9, "Outstanding": 10
    }

with col6:
    year_built = st.number_input("Year Built", min_value=1900, max_value=2010, value=1995)
    year_remod = st.number_input("Year Remodelled", min_value=1900, max_value=2010, value=year_built)

st.divider()

# ── SECTION 3: Size & Space ─────────────────────────────────
st.markdown("#### 📐 Size & Space")
col7, col8, col9 = st.columns(3)

with col7:
    gr_liv_area = st.number_input("Living Area (sq ft)", min_value=400, max_value=6000, value=1500, step=100)
    total_bsmt_sf = st.number_input("Basement Area (sq ft)", min_value=0, max_value=3000, value=800, step=50)

with col8:
    totrms_abvgrd = st.selectbox("Total Rooms Above Ground", list(range(2, 15)), index=4)
    bedroom_abvgr = st.selectbox("Bedrooms Above Ground", list(range(0, 9)), index=3)

with col9:
    fireplaces = st.selectbox("Fireplaces", [0, 1, 2, 3])
    wood_deck_sf = st.number_input("Wood Deck Area (sq ft)", min_value=0, max_value=1000, value=0, step=10)

st.divider()

# ── SECTION 4: Kitchen & Bathrooms ──────────────────────────
st.markdown("#### 🍳 Kitchen & Bathrooms")
col10, col11, col12 = st.columns(3)

with col10:
    kitchen_qual = st.selectbox("Kitchen Quality", ["Excellent", "Good", "Average", "Fair", "Poor"])
    kitchen_map = {"Excellent": "Ex", "Good": "Gd", "Average": "TA", "Fair": "Fa", "Poor": "Po"}
    kitchen_abvgr = st.selectbox("Number of Kitchens", [1, 2, 3])

with col11:
    full_bath = st.selectbox("Full Bathrooms", [0, 1, 2, 3, 4])
    half_bath = st.selectbox("Half Bathrooms", [0, 1, 2])

with col12:
    bsmt_full_bath = st.selectbox("Basement Full Bathrooms", [0, 1, 2])
    bsmt_half_bath = st.selectbox("Basement Half Bathrooms", [0, 1, 2])

st.divider()

# ── SECTION 5: Garage ───────────────────────────────────────
st.markdown("#### 🚗 Garage")
col13, col14 = st.columns(2)

with col13:
    garage_cars = st.selectbox("Garage Capacity (cars)", [0, 1, 2, 3, 4])

with col14:
    garage_area = st.number_input("Garage Area (sq ft)", min_value=0, max_value=1500, value=garage_cars * 250, step=50)

st.divider()

# ── SECTION 6: Utilities ────────────────────────────────────
st.markdown("#### ⚡ Utilities")
col15, col16, col17 = st.columns(3)

with col15:
    central_air = st.selectbox("Central Air Conditioning", ["Yes", "No"])
    ac_map = {"Yes": "Y", "No": "N"}

with col16:
    heating_qc = st.selectbox("Heating Quality", ["Excellent", "Good", "Average", "Fair", "Poor"])
    heat_map = {"Excellent": "Ex", "Good": "Gd", "Average": "TA", "Fair": "Fa", "Poor": "Po"}

with col17:
    paved_drive = st.selectbox("Paved Driveway", ["Paved", "Partial", "Dirt/Gravel"])
    drive_map = {"Paved": "Y", "Partial": "P", "Dirt/Gravel": "N"}

st.divider()

# ── SECTION 7: Sale Info ────────────────────────────────────
st.markdown("#### 🏷️ Sale Info")
col18, col19 = st.columns(2)

with col18:
    sale_type = st.selectbox("Sale Type", [
        "Warranty Deed (Conventional)", "Warranty Deed (Cash)",
        "New Home", "Court Officer Deed", "Contract"
    ])
    sale_type_map = {
        "Warranty Deed (Conventional)": "WD",
        "Warranty Deed (Cash)": "CWD",
        "New Home": "New",
        "Court Officer Deed": "COD",
        "Contract": "Con"
    }

with col19:
    sale_condition = st.selectbox("Sale Condition", [
        "Normal", "Abnormal", "Adjacent Land Purchase",
        "Allocation", "Family Sale", "Partial"
    ])
    condition_map = {
        "Normal": "Normal", "Abnormal": "Abnormal",
        "Adjacent Land Purchase": "AdjLand",
        "Allocation": "Alloca",
        "Family Sale": "Family",
        "Partial": "Partial"
    }

st.divider()

# ── PREDICT ─────────────────────────────────────────────────
if st.button("Estimate Price →", use_container_width=True):
    with st.spinner("Calculating your estimate..."):
        df = pd.read_csv('data/train.csv')
        df = df.drop(columns=['Alley', 'PoolQC', 'Fence', 'MiscFeature', 'FireplaceQu'], errors='ignore')

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna(df[col].median())

        le = LabelEncoder()
        encoders = {}
        for col in df.select_dtypes(include='object').columns:
            encoders[col] = LabelEncoder()
            df[col] = encoders[col].fit_transform(df[col])

        input_data = df[feature_names].median().to_frame().T

        def encode_cat(col, val, default_val):
            if col in encoders and val in encoders[col].classes_:
                return encoders[col].transform([val])[0]
            return default_val

        user_inputs = {
            'OverallQual': quality_map[overall_qual],
            'GrLivArea': gr_liv_area,
            'GarageCars': garage_cars,
            'GarageArea': garage_area,
            'TotalBsmtSF': total_bsmt_sf,
            'YearBuilt': year_built,
            'YearRemodAdd': year_remod,
            'FullBath': full_bath,
            'HalfBath': half_bath,
            'BsmtFullBath': bsmt_full_bath,
            'BsmtHalfBath': bsmt_half_bath,
            'TotRmsAbvGrd': totrms_abvgrd,
            'BedroomAbvGr': bedroom_abvgr,
            'Fireplaces': fireplaces,
            'KitchenAbvGr': kitchen_abvgr,
            'WoodDeckSF': wood_deck_sf,
            'LotArea': lot_area,
            'HouseStyle': encode_cat('HouseStyle', style_map[house_style], 0),
            'KitchenQual': encode_cat('KitchenQual', kitchen_map[kitchen_qual], 0),
            'CentralAir': encode_cat('CentralAir', ac_map[central_air], 0),
            'HeatingQC': encode_cat('HeatingQC', heat_map[heating_qc], 0),
            'PavedDrive': encode_cat('PavedDrive', drive_map[paved_drive], 0),
            'SaleType': encode_cat('SaleType', sale_type_map[sale_type], 0),
            'SaleCondition': encode_cat('SaleCondition', condition_map[sale_condition], 0),
            '1stFlrSF': gr_liv_area * 0.55,
        }

        for col, val in user_inputs.items():
            if col in input_data.columns:
                input_data[col] = val

        prediction = model.predict(input_data)[0]

    # Result
    st.success(f"### 🏷️ Estimated Sale Price: ${prediction:,.0f}")
    st.markdown("---")

    st.markdown("**Summary of your property:**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Living Area", f"{gr_liv_area} sq ft")
    c2.metric("Condition", overall_qual)
    c3.metric("Year Built", year_built)

    if prediction < 100000:
        st.caption("This looks like a modest, older property — good entry-level option.")
    elif prediction < 175000:
        st.caption("A solid mid-range home with decent features and space.")
    elif prediction < 275000:
        st.caption("Above average property — good quality with modern features.")
    else:
        st.caption("High-value property — excellent condition, great location, or both.")

    st.balloons()

st.markdown(" ")
st.caption("Built using the Ames Housing dataset · Random Forest · ~90% accuracy")