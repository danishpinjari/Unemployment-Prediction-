import pickle
import numpy as np

# Load the Gradient Boosting model
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Check if the model has a predict method
if hasattr(model, 'predict'):
    # Sample input
    cpi_value = 9.739993139  # Example CPI
    gdp_value = 0.525527439 # Example GDP
    input_data = np.array([[cpi_value, gdp_value]])
    
    # Make a prediction
    prediction = model.predict(input_data)
    print(f"Predicted Unemployment Rate: {prediction[0]}")
else:
    print("The loaded model does not have a predict method.")
