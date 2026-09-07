import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

model = joblib.load("model.pkl")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    if "features" not in data:
        return jsonify({"error": "لازم تبعت 'features' في الـ JSON body"}), 400

    features = data["features"]

    X = np.array(features)
    if X.ndim == 1:
        X = X.reshape(1, -1)

    expected = getattr(model, "n_features_in_", None)
    if expected is not None and X.shape[1] != expected:
        return jsonify({
            "error": f"عدد الفيتشرز غلط. متوقع {expected} لكن جالك {X.shape[1]}"
        }), 400

    preds = model.predict(X)
    return jsonify({"predictions": preds.tolist()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
