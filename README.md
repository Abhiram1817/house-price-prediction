# 🏡 House Price Predictor

A machine learning web application that predicts residential property sale prices based on key features of a house.

## 📌 Overview

This project uses the **Ames Housing Dataset** from Kaggle, which contains 79 features describing various aspects of residential homes in Ames, Iowa. A Random Forest Regression model was trained on this data, achieving **~90% accuracy (R² = 0.90)**.

## 🛠️ Tech Stack
- **Python** — Core language
- **Pandas & NumPy** — Data preprocessing and feature engineering
- **Scikit-learn** — Model training (Random Forest Regressor)
- **Streamlit** — Interactive web application

## ⚙️ How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/Abhiram1817/house-price-prediction.git
cd house-price-prediction
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Download dataset from [Kaggle](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data) and place `train.csv` inside a `data/` folder

4. Train the model
```bash
python app.py
```

5. Run the app
```bash
streamlit run streamlit_app.py
```

## 📊 Model Performance

| Model | R² Score |
|---|---|
| Linear Regression | ~0.78 |
| Random Forest | **~0.90** |

## 📃 Dataset
Ames Housing Dataset — [Kaggle Competition](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)
