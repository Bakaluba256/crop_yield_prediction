import pickle
import joblib

# Load the model using pickle
with open('yield_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Save the model using joblib with compression
joblib.dump(model, 'modified_yield_model.pkl', compress=('zlib', 3))
