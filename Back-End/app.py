from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS

# Load the trained model, label encoders, and dataset
model = joblib.load("modified_yield_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
data = pd.read_csv("yield_df.csv").drop(columns=["SN"])

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Endpoint to get unique areas and items
@app.route('/dropdown-options', methods=['GET'])
def get_dropdown_options():
    areas = data["Area"].unique().tolist()
    items = data["Item"].unique().tolist()
    return jsonify({"areas": areas, "items": items}), 200

# Endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from request
        input_data = request.json
        area = input_data.get('Area')
        item = input_data.get('Item')
        year = input_data.get('Year')
        rainfall = input_data.get('average_rain_fall_mm_per_year')
        pesticides = input_data.get('pesticides_tonnes')
        temp = input_data.get('avg_temp')

        # Validate input
        if None in [area, item, year, rainfall, pesticides, temp]:
            return jsonify({'error': 'All fields are required.'}), 400

        # Encode categorical inputs
        area_encoded = label_encoders["Area"].transform([area])[0]
        item_encoded = label_encoders["Item"].transform([item])[0]

        # Prepare input features for prediction
        input_features = np.array([[area_encoded, item_encoded, year, rainfall, pesticides, temp]])
        predicted_yield = model.predict(input_features)[0]

        # Calculate the maximum yield for the selected area and item
        max_yield = data[(data["Area"] == area) & (data["Item"] == item)]["hg/ha_yield"].max()

        if max_yield:
            percentage_yield = (predicted_yield / max_yield) * 100
        else:
            percentage_yield = 0

        # Return the predicted percentage
        return jsonify({'predicted_percentage': percentage_yield}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
