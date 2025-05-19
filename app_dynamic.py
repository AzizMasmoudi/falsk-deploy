# app/api/app_dynamic.py

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))

def load_model(name):
    path = os.path.join(MODEL_DIR, f"{name}.pkl")
    return joblib.load(path)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json()
        model_name = payload.pop("model_name")
        model = load_model(model_name)

        # 1. DataFrame brut
        df = pd.DataFrame([payload])

        # 2. One-hot encoding automatique
        df_encoded = pd.get_dummies(df)

        # 3. Récupérer les colonnes attendues par le modèle
        if hasattr(model, "feature_names_in_"):
            expected_cols = list(model.feature_names_in_)
        else:
            expected_cols = model.get_booster().feature_names

        # 4. Ajouter les colonnes manquantes à 0
        for col in expected_cols:
            if col not in df_encoded.columns:
                df_encoded[col] = 0

        # 5. Réordonner les colonnes
        df_encoded = df_encoded[expected_cols]

        # 6. Prédiction
        pred = model.predict(df_encoded)[0]
        return jsonify({"prediction": int(pred)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
