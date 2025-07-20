import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def train_model(df):
    # Drop unnecessary columns
    df_model = df.copy()
    df_model = df_model.drop(['Date', 'Month_Name'], axis=1)

    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df_model, drop_first=True)

    # Features & Target
    X = df_encoded.drop('EV_Sales_Quantity', axis=1)
    y = df_encoded['EV_Sales_Quantity']

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train Model
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluation
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f"✅ Model Trained - RMSE: {rmse:.2f}")

    return model, X_test, y_test, y_pred
