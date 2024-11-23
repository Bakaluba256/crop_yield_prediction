# Importing Dependencies
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder 
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
data = pd.read_csv("yield_df.csv")

# Drop unnecessary columns
data = data.drop(columns=["SN"])

# Encode categorical features
label_encoders = {}
for column in ["Area", "Item"]:
    encoder = LabelEncoder()
    data[column] = encoder.fit_transform(data[column])  # Transform categorical values to numerical
    label_encoders[column] = encoder  # Store encoders for later use

# Separate features and target variable
X = data.drop(columns=["hg/ha_yield"])  # Features
y = data["hg/ha_yield"]  # Target

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestRegressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate model performance metrics
mae = mean_absolute_error(y_test, y_pred)  # Mean Absolute Error
mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error
r2 = r2_score(y_test, y_pred)  # R-squared
accuracy_percentage = model.score(X_test, y_test) * 100  # Convert R² to percentage

# Print metrics
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R²): {r2}")
print(f"Model Accuracy: {accuracy_percentage:.2f}%")  # Accuracy as a percentage

# Save the trained model and label encoders
joblib.dump(model, "yield_model.pkl")  # Save the model
joblib.dump(label_encoders, "label_encoders.pkl")  # Save encoders
print("The model has been saved as 'yield_model.pkl'")
print("The Encoder has been saved as 'label_encoders.pkl'")
