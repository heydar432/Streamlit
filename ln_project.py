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
    response.raise_for_status()  # Ensure the request was successful
    return io.BytesIO(response.content)

# Load the dictionary from the URL
lookup_dict_url = 'https://raw.githubusercontent.com/heydar432/Streamlit/main/lookup_dict.pkl'
with load_file_from_url(lookup_dict_url) as file:
    lookup_dict = pickle.load(file)

# Function to load the model from the URL
def load_model():
    model_url = 'https://raw.githubusercontent.com/heydar432/Streamlit/main/model_2.pkl'
    with load_file_from_url(model_url) as file:
        return pickle.load(file)

# Function to get encoded values
def get_encoded_values(lookup_dict, input_values):
    encoded_values = {}
    for key, original_value in input_values.items():
        if key in ['Model', 'Transmission', 'İs_New?']:
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
st.title('Car Price Prediction App (Azerbaijan Market)'

# Mapping dictionaries
transmission_mapping = {
    'Avtomatik': 'Automatic',
    'Mexaniki': 'Manual',
    'Robotlaşdırılmış': 'Robotic'
}

is_new_mapping = {
    'Bəli': 'Yes',
    'Xeyr': 'No'
}

# Apply mapping to the options
transmission_options = list(lookup_dict['Transmission'].keys()) if 'Transmission' in lookup_dict else []
is_new_options = list(lookup_dict['İs_New?'].keys()) if 'İs_New?' in lookup_dict else []

# Translated options for Transmission and Is New?
translated_transmission_options = [transmission_mapping.get(option, option) for option in transmission_options]
translated_is_new_options = [is_new_mapping.get(option, option) for option in is_new_options]

# Extract original values for selectbox options
model_options = [model for model in lookup_dict['Model'].keys() if model in ['Sorento', 'Optima', 'Rio', 'Sportage', 'Ceed', 'Cerato']] if 'Model' in lookup_dict else [] 

# Creating form for user input
with st.form(key='car_input_form'):
    # Create columns for the form
    col1, col2 = st.columns(2)

    with col1:
        model_input = st.selectbox('Model', options=model_options)
        year = st.number_input('Year', min_value=1990, max_value=2023, step=1)
        transmission = st.selectbox('Transmission', options=translated_transmission_options)
    
    with col2:
        is_new = st.selectbox('Is New?', options=translated_is_new_options)
        mileage = st.number_input('Mileage (km)', min_value=0)
        hp = st.number_input('Horsepower (HP)', min_value=0)

    submit_button = st.form_submit_button(label='Predict Price')

# On form submission
if submit_button:
    # Reverse the mapping for Transmission and Is New?
    reverse_transmission = {v: k for k, v in transmission_mapping.items()}
    reverse_is_new = {v: k for k, v in is_new_mapping.items()}

    input_values = {
        'Model': model_input,
        'Year': year,
        'Transmission': reverse_transmission.get(transmission, transmission),
        'İs_New?': reverse_is_new.get(is_new, is_new),
        'Mileage (km)': mileage,
        'HP': hp
    }

    # Encode the input values
    encoded_values = get_encoded_values(lookup_dict, input_values)
    encoded_values_list = [value['Encoded'] for value in encoded_values.values() if value['Encoded'] is not None]

    # Check if all values are encoded
    if len(encoded_values_list) == len(input_values):
        # Convert to NumPy array and reshape
        encoded_values_array = np.array(encoded_values_list).reshape(1, -1)

        # Predict the price
        predicted_price = model.predict(encoded_values_array)

        # Round the predicted price to three decimal places
        rounded_price_usd = round(predicted_price[0], 1)

        # Convert to AZN
        conversion_rate = 1.7
        rounded_price_azn = round(rounded_price_usd * conversion_rate, 1)

        # Display the prediction in both USD and AZN
        st.success(f' Predicted Price of the Car: {rounded_price_usd} USD  / {rounded_price_azn} AZN ')
    else:
        # Identify which input values could not be encoded
        missing_encoded_values = [key for key, value in encoded_values.items() if value['Encoded'] is None]
        error_message = "Unable to encode the following input values: " + ", ".join(missing_encoded_values)
        st.error(error_message)

