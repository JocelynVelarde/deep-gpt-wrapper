import joblib
import pandas as pd
import numpy as np

# Load saved models
clf_pipeline = joblib.load("classification_pipeline.pkl")
category_models = joblib.load("all_regressors.pkl")

# Define features (same order as training)
numeric_features = [
    'MTS2VENTAS_NUM', 'PUERTASREFRIG_NUM', 'CAJONESESTACIONAMIENTO_NUM',
    'LATITUD_NUM', 'LONGITUD_NUM', 'num_locales_cercanos',
    'reportes_cercanos', 'num_escuelas', 'densidad', 'CENTRO_CERCANO'
]
categorical_features = [
    'PLAZA_CVE', 'NIVELSOCIOECONOMICO_DES', 'ENTORNO_DES',
    'SEGMENTO_MAESTRO_DESC', 'LID_UBICACION_TIENDA'
]

# Load some stats from training to fill missing values
# (You should export and load these from training too, but here's a placeholder)
training_stats = {
    'numeric_medians': {
        'MTS2VENTAS_NUM': 100, 'PUERTASREFRIG_NUM': 2, 'CAJONESESTACIONAMIENTO_NUM': 10,
        'LATITUD_NUM': 25.7, 'LONGITUD_NUM': -100.2, 'num_locales_cercanos': 5,
        'reportes_cercanos': 3, 'num_escuelas': 2, 'densidad': 5000, 'CENTRO_CERCANO': 0
    },
    'categorical_modes': {
        'PLAZA_CVE': 'P1', 'NIVELSOCIOECONOMICO_DES': 'Medio',
        'ENTORNO_DES': 'Urbano', 'SEGMENTO_MAESTRO_DESC': 'Tipo A',
        'LID_UBICACION_TIENDA': 'Ubicacion 1'
    }
}

def safe_predict(latitude, longitude):
    input_data = {
        'LATITUD_NUM': latitude,
        'LONGITUD_NUM': longitude,
    }

    # Fill in other numeric features with median
    for col in numeric_features:
        if col not in input_data:
            input_data[col] = training_stats['numeric_medians'].get(col, 0)

    # Fill in categorical features with mode
    for col in categorical_features:
        input_data[col] = training_stats['categorical_modes'].get(col, 'Unknown')

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])[numeric_features + categorical_features]

    # Predict category
    category = clf_pipeline.predict(input_df)[0]
    category_proba = clf_pipeline.predict_proba(input_df)[0]

    # Predict regression
    if category in category_models:
        input_transformed = clf_pipeline.named_steps['preprocessor'].transform(input_df)
        prediction = category_models[category].predict(input_transformed)[0]
    else:
        prediction = 0
        print(f"No model for category {category}, using default prediction.")

    return category, prediction, category_proba


# Example inference
if __name__ == "__main__":
    lat, lon = 25.70486, -100.15613
    category, sales, proba = safe_predict(lat, lon)
    print(f"Lat: {lat}, Lon: {lon}")
    print(f"Predicted Category: {category}")
    print(f"Predicted Sales: ${sales:,.2f}")
    print(f"Category Probabilities: {proba}")
