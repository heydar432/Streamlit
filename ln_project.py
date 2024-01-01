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
lookup_dict_url = 'https://github.com/heydar432/Streamlit/blob/main/lookup_dict.pkl'
with load_file_from_url(lookup_dict_url) as file:
    lookup_dict = pickle.load(file)

# Function to load the model from the URL
def load_model():
    model_url = 'https://github.com/heydar432/Streamlit/blob/main/model_1.pkl'
    with load_file_from_url(model_url) as file:
        return pickle.load(file)

# Function to get encoded values
def get_encoded_values(lookup_dict, input_values):
    encoded_values = {}
    for key, original_value in input_values.items():
        if key in lookup_dict:
            original_value = type(list(lookup_dict[key].keys())[0])(original_value)
            if original_value in lookup_dict[key]:
                encoded_values[key] = {'Original': original_value, 'Encoded': lookup_dict[key][original_value]}
            else:
                encoded_values[key] = {'Original': original_value, 'Encoded': None}
        else:
            encoded_values[key] = {'Original': original_value, 'Encoded': None}
    return encoded_values

# Load your trained model
model = load_model()

# Streamlit webpage layout
st.title('Car Price Prediction App')

# Extract original values for selectbox options
model_options = [model for model in lookup_dict['Model'].keys() if model in ['Sorento', 'Optima', 'Rio', 'Sportage', 'Ceed', 'Cerato']] if 'Model' in lookup_dict else [] # because they are more numerous
origin_options = list(lookup_dict['Origin'].keys()) if 'Origin' in lookup_dict else []
transmission_options = list(lookup_dict['Transmission'].keys()) if 'Transmission' in lookup_dict else []
drive_type_options = list(lookup_dict['Drive Type'].keys()) if 'Drive Type' in lookup_dict else []
is_new_options = list(lookup_dict['İs_New?'].keys()) if 'İs_New?' in lookup_dict else []
oil_type_options = list(lookup_dict['oil_type'].keys()) if 'oil_type' in lookup_dict else []
# saler_name_options = list(lookup_dict['Saler_name'].keys()) if 'Saler_name' in lookup_dict else []

# Creating form for user input
with st.form(key='car_input_form'):
    # Create columns for the form
    col1, col2, col3 = st.columns(3)

    with col1:
        model_input = st.selectbox('Model', options=model_options)
        year = st.number_input('Year', min_value=1990, max_value=2023, step=1)
        transmission = st.selectbox('Transmission', options=transmission_options)
    
    with col2:
        drive_type = st.selectbox('Drive Type', options=drive_type_options)
        is_new = st.selectbox('Is New?', options=is_new_options)
        seat_count = st.number_input('Seat Count', min_value=1, max_value=10, step=1)

    with col3:
        origin = st.selectbox('Origin', options=origin_options)
        # saler_name = st.selectbox('Saler_name', options=saler_name_options)
        oil_type = st.selectbox('Oil Type', options=oil_type_options)

    mileage = st.number_input('Mileage (km)', min_value=0)
    hp = st.number_input('Horsepower (HP)', min_value=0)

    submit_button = st.form_submit_button(label='Predict Price')

# On form submission
if submit_button:
    input_values = {
        'Model': model_input,
        'Year': year,
        'Transmission': transmission,
        'Drive Type': drive_type,
        'İs_New?': is_new,
        'Seat Count': seat_count,
        'Origin': origin,
        #'Saler_name': saler_name,
        'oil_type': oil_type,
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
        rounded_price = round(predicted_price[0], 3)

        # Display the prediction
        st.success(f'Predicted Price of the Car: ${rounded_price}')
    else:
        st.error('Some input values could not be encoded. Please check your inputs.')

# Note: Ensure that 'lookup_dict' is defined or loaded in this script.
