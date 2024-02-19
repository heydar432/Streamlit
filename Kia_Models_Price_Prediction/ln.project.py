import streamlit as st
import numpy as np
import pickle
import requests
import io
import warnings
warnings.filterwarnings("ignore")

# Function to load a file from a URL
def load_file_from_url(url):
  response = requests.get(url)
  response.raise_for_status() # Ensure the request was successful
  return io.BytesIO(response.content)

# Load the dictionary from the URL
lookup_dict_url = 'https://raw.githubusercontent.com/heydar432/Streamlit/main/Kia_Models_Price_Prediction/lookup_dict.pkl'

with load_file_from_url(lookup_dict_url) as file:
  lookup_dict = pickle.load(file)

# Function to load the model from the URL
def load_model():
  model_url = 'https://raw.githubusercontent.com/heydar432/Streamlit/main/Kia_Models_Price_Prediction/model_2.pkl'
  with load_file_from_url(model_url) as file:
    return pickle.load(file)

# Function to get encoded values
def get_encoded_values(lookup_dict, input_values):
  encoded_values = {}
  for key, original_value in input_values.items():
    if key in ['Model', 'Transmission','Body Type','oil_type']:
      if key in lookup_dict:
        original_value = type(list(lookup_dict[key].keys())[0])(original_value)
        if original_value in lookup_dict[key]:
          encoded_values[key] = {'Original': original_value, 'Encoded': lookup_dict[key][original_value]}
        else:
          encoded_values[key] = {'Original': original_value, 'Encoded': None}
      else:
        encoded_values[key] = {'Original': original_value, 'Encoded': None}
    else:
      # For other features, use the original value
      encoded_values[key] = {'Original': original_value, 'Encoded': original_value}
  return encoded_values

# Load your trained model
model = load_model()

# Streamlit webpage layout
st.title('Car Price Prediction App')

# Existing mappings
transmission_mapping = {
  'Avtomatik': 'Automatic',
  'Mexaniki': 'Manual',
  'Robotlaşdırılmış': 'Robotic',
  'Variator': 'CVT' # Assuming 'Variator' translates to 'Continuously Variable Transmission (CVT)'
}

# Additional mappings for 'Body Type' and 'Oil Type'
body_type_mapping = {
  'Sedan': 'Sedan',
  'Offroader / SUV': 'SUV',
  'Hetçbek': 'Hatchback',
  'Universal': 'Station Wagon',
  'Liftbek': 'Liftback'
}

oil_type_mapping = {
  'Benzin': 'Petrol',
  'Dizel': 'Diesel',
  'Hibrid': 'Hybrid',
  'Qaz': 'Gas',
  'Plug-in Hibrid': 'Plug-in Hybrid'
}

# Assuming 'lookup_dict' is defined elsewhere and contains the options for 'Transmission', 'Is New?', 'Body Type', and 'Oil Type'
transmission_options = list(lookup_dict['Transmission'].keys()) if 'Transmission' in lookup_dict else []
body_type_options = list(lookup_dict['Body Type'].keys()) if 'Body Type' in lookup_dict else []
oil_type_options = list(lookup_dict['oil_type'].keys()) if 'oil_type' in lookup_dict else []

# Apply mappings
translated_transmission_options = [transmission_mapping.get(option, option) for option in transmission_options]
translated_body_type_options = [body_type_mapping.get(option, option) for option in body_type_options]
translated_oil_type_options = [oil_type_mapping.get(option, option) for option in oil_type_options]

# Extract original values for selectbox options for 'Model'
model_options = [model for model in lookup_dict['Model'].keys() if model in ['Sorento', 'Optima', 'Rio', 'Sportage', 'Ceed', 'Cerato']] if 'Model' in lookup_dict else [] 

# Creating form for user input
with st.form(key='car_input_form'):
  # Create columns for the form
  col1, col2 = st.columns(2)

  with col1:
    model_input = st.selectbox('Model', options=model_options)
    year = st.number_input('Year', min_value=1995, max_value=2023, step=1)
    body_type = st.selectbox('Body Type', options=translated_body_type_options)
    
  with col2:
    transmission = st.selectbox('Transmission', options=translated_transmission_options)
    oil_type = st.selectbox('oil_type', options=translated_oil_type_options)
    mileage = st.number_input('Mileage (km)', min_value=1)

  submit_button = st.form_submit_button(label='Predict Price')

# On form submission
if submit_button:
  # Reverse the mapping for Transmission, Body Type, and Oil Type
  reverse_transmission = {v: k for k, v in transmission_mapping.items()}
  reverse_body_type = {v: k for k, v in body_type_mapping.items()}
  reverse_oil_type = {v: k for k, v in oil_type_mapping.items()}

  input_values = {
    'Model': model_input,
    'Year': year,
    'Body Type': reverse_body_type.get(body_type, body_type),
    'Transmission': reverse_transmission.get(transmission, transmission),
    'oil_type': reverse_oil_type.get(oil_type, oil_type),
    'Mileage (km)': mileage
  }

  # Encode the input values
  encoded_values = get_encoded_values(lookup_dict, input_values)

  # Display the original and encoded values for each input
  for key, value in encoded_values.items():
    st.text(f"{key}: Original - {value['Original']}, Encoded - {value['Encoded']}")

  # Prepare the list of encoded values for prediction
  encoded_values_list = [value['Encoded'] for value in encoded_values.values() if value['Encoded'] is not None]

  # Check if all values are encoded
  if len(encoded_values_list) == len(input_values):
    # Convert to NumPy array and reshape for prediction
    encoded_values_array = np.array(encoded_values_list).reshape(1, -1)

    # Predict the price
    predicted_price = model.predict(encoded_values_array)

    # Round the predicted price to a certain number of decimal places
    rounded_price_usd = round(predicted_price[0], 2)

    # Convert to another currency if needed
    conversion_rate = 1.7 # Example conversion rate
    rounded_price_azn = round(rounded_price_usd * conversion_rate, 2)

    # Display the prediction in both currencies
    st.success(f'Predicted Price of the Car: {rounded_price_usd} USD / {rounded_price_azn} AZN')
  else:
    # Identify which input values could not be encoded
    missing_encoded_values = [key for key, value in encoded_values.items() if value['Encoded'] is None]
    error_message = "Unable to encode the following input values: " + ", ".join(missing_encoded_values)
    st.error(error_message)
