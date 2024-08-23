import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv(r'C:\Users\Heydar\Desktop\Data Science\My_projects\Make a project for forecast stock prices using time series. Use streamlit library\streamlit/all_stock_prices.csv')  # Replace with the path to your dataset

# Custom CSS to make the app more colorful
st.markdown(
    """
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #2E86C1;
        color: white;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1 {
        color: #FFFFFF;
    }

    /* Number inputs */
    input[type="number"] {
        background-color: #5DADE2;
        color: white;
        border: 2px solid #FFFFFF;
        border-radius: 5px;
    }

    /* Checkbox */
    [data-testid="stCheckbox"] {
        color: white;
    }

    /* Header color */
    .stHeader {
        color: #2980B9;
    }

    /* DataFrame table */
    [data-testid="stDataFrameContainer"] {
        background-color: #EBF5FB;
        border: 2px solid #2E86C1;
        border-radius: 10px;
    }

    /* General text */
    .css-10trblm {
        color: #2980B9;
    }

    /* Body background color */
    body {
        background-color: #F2F3F4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title('Stock Data Analysis')

# Create a sidebar for filters on the far left
with st.sidebar:
    st.header('🎛️ Filters')
    min_change_1_month = st.number_input('Min 1-Month Change (%)', value=None)
    min_change_6_month = st.number_input('Min 6-Month Change (%)', value=None)
    min_change_1_year = st.number_input('Min 1-Year Change (%)', value=None)
    min_change_5_year = st.number_input('Min 5-Year Change (%)', value=None)
    min_price = st.number_input('Min Current Close Price', value=None)
    max_price = st.number_input('Max Current Close Price', value=None)

# Initialize filtered_df with the original dataframe
filtered_df = df.copy()

# Apply filters to the dataframe if values are provided
if min_change_1_month is not None:
    filtered_df = filtered_df[filtered_df['1-Month Change (%)'] >= min_change_1_month]

if min_change_6_month is not None:
    filtered_df = filtered_df[filtered_df['6-Month Change (%)'] >= min_change_6_month]

if min_change_1_year is not None:
    filtered_df = filtered_df[filtered_df['1-Year Change (%)'] >= min_change_1_year]

if min_change_5_year is not None:
    filtered_df = filtered_df[filtered_df['5-Year Change (%)'] >= min_change_5_year]

if min_price is not None:
    filtered_df = filtered_df[filtered_df['Current Close Price'] >= min_price]

if max_price is not None:
    filtered_df = filtered_df[filtered_df['Current Close Price'] <= max_price]

# Checkbox to hide or show the "Security Name" column
show_security_name = st.checkbox('Show Security Name Column', value=True)

# Hide the "Security Name" column if checkbox is unchecked
if not show_security_name:
    filtered_df = filtered_df.drop(columns=['Security Name'])

# Display the filtered data with a wide table
st.header('📋 Filtered Data')
st.dataframe(filtered_df, use_container_width=True)
