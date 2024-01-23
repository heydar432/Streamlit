pip install openpyxl

import pandas as pd
import numpy as np
import streamlit as st

df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Trendyol_MCDM_project/products_data.xlsx')

# Function to extract the part of the link up to the second '&'
def extract_link_part(link):
    parts = link.split('&', 2)
    return '&'.join(parts[:2]) if len(parts) > 1 else link

# Apply the function to each link
df['Link_Part'] = df['product_link'].apply(extract_link_part)

# Check for duplicates based on the Link_Part
duplicated_partial = df[df['Link_Part'].duplicated(keep=False)]

# If no partial duplicates, check for complete duplicates
if duplicated_partial.empty:
    duplicated_full = df[df['product_link'].duplicated(keep=False)]
else:
    duplicated_full = pd.DataFrame()

# Result
result = duplicated_partial if not duplicated_partial.empty else duplicated_full
# If partial duplicates exist, drop duplicates based on 'Link_Part'
if not duplicated_partial.empty:
    df = df.drop_duplicates(subset='Link_Part', keep='first')
# Otherwise, drop complete duplicates
else:
    df = df.drop_duplicates(subset='product_link', keep='first')

# Displaying the DataFrame after dropping duplicates

del df['Link_Part']

count_original = len(df)
df = df.drop_duplicates(subset='product_link', keep='first')
new_count = len(df)

count_deleted = count_original-new_count
print('Count of deleted duplicated records:',count_deleted)

# Original count of rows where 'Model' is 'Kulaküstü'
original_kulakustu_count = (df['Model'] == 'Kulaküstü').sum()

search_terms = [
    '520bt',
    'bt760',
    'p47',
    'b39',
    'c-932-tf',
    'c-927',
    'p7236',
    'b-s16',
    'kulakustu',
    'gamer-kulaklik',
    'kafaustu',
    'kulak-ustu',
    'kafa-ustu',
    'headphone'
]

# Creating a regex pattern to match any of the search terms
regex_pattern = '|'.join(search_terms)

# Original count of rows where 'Model' is 'Kulaküstü'
original_kulakustu_count = (df['Model'] == 'Kulaküstü').sum()

# Update 'Model' to 'Kulaküstü' where 'product_link' contains any of the search terms
df.loc[df['product_link'].str.contains(regex_pattern, case=False, na=False), 'Model'] = 'Kulaküstü'

# New count of rows where 'Model' is 'Kulaküstü'
new_kulakustu_count = (df['Model'] == 'Kulaküstü').sum()

# Count of updated rows
updated_headphones_count = new_kulakustu_count - original_kulakustu_count

# The updated DataFrame and count of updated rows
print('Count of filled by headphones model feature :',updated_headphones_count)
# Original count of rows where 'Model' is 'Kulaküstü'
original_kulakici_count = (df['Model'] == 'Kulak İçi').sum()

search_terms_2 = [
    'kulakici',
    'kulak-ici',
    'earphone',
    'alcatel-a3',
    'earpods'
]

# Creating a regex pattern to match any of the search terms
regex_pattern = '|'.join(search_terms_2)

# Original count of rows where 'Model' is 'Kulaküstü'
original_kulakici_count = (df['Model'] == 'Kulak İçi').sum()

# Update 'Model' to 'Kulaküstü' where 'product_link' contains any of the search terms
df.loc[df['product_link'].str.contains(regex_pattern, case=False, na=False), 'Model'] = 'Kulak İçi'

# New count of rows where 'Model' is 'Kulaküstü'
new_kulakici_count = (df['Model'] == 'Kulak İçi').sum()

# Count of updated rows
updated_count = new_kulakici_count - original_kulakici_count

# The updated DataFrame and count of updated rows
print('Count of filled by earphones model feature :', updated_count)
# filtering headphones
df = df[df['Model']=='Kulaküstü']

# Search terms for 'product_link'
search_terms_3 = ['kablosuz', 'wireless', 'bluetooth']

# Creating a regex pattern to match any of the search terms
regex_pattern = '|'.join(search_terms_3)

# Filtering DataFrame where 'Bluetooth Versiyon' is NaN (null) and 'product_link' contains any of the search terms
filtered_bl_wr_df = df[df['Bluetooth Versiyon'].isnull() &
                 df['product_link'].str.contains(regex_pattern, case=False, na=False)]

# filtering notnull records using Bluetooth Versiyon column
filtered_df_non_null_bluetooth = df[df['Bluetooth Versiyon'].notnull()]
df = pd.concat([filtered_bl_wr_df,filtered_df_non_null_bluetooth])
df = df[df['rating-line-count']!='Not found']

# Converting 'total-review-count' to numeric for comparison
df['total-review-count'] = pd.to_numeric(df['total-review-count'])
df['Bluetooth Versiyon'] = pd.to_numeric(df['Bluetooth Versiyon'])

# Applying the filter
filtered_df = df[(df['rating-line-count'] != 'Not found') & (df['total-review-count'] > 30)&(df['Bluetooth Versiyon']>4.9)&(df['Mikrofon']=='Var')]

filtered_df['rating-line-count'] = pd.to_numeric(filtered_df['rating-line-count'])

filtered_df.drop(['seller-name-text','Model','Mikrofon','Çift Telefon Desteği'],axis=1,inplace=True)
df = filtered_df
# Translating the column names to English
column_translations = {
    'product_link': 'Product Link',
    'prc-dsc': 'Product Price',
    'rating-line-count': 'Rating Score',
    'total-review-count': 'Total Review Count',
    'favorite-count': 'Favorite Count',
    'campaign-name': 'Campaign Name',
    'dd-txt-vl': 'Delivery Duration Text Value',
    'sl-pn': 'Seller Rating',
    'Garanti Tipi': 'Warranty Type',
    'Renk': 'Color',
    'Aktif Gürültü Önleme (ANC)': 'Active Noise Cancellation (ANC)',
    'Suya/Tere Dayanıklılık': 'Water/Sweat Resistance',
    'Bluetooth Versiyon': 'Bluetooth Version',
    'Dokunmatik Kontrol': 'Touch Control',
    'Garanti Süresi': 'Warranty Period'
}

df.rename(columns=column_translations, inplace=True)

# Displaying the DataFrame with translated column names
df.head(3)
# Extracting the numeric part and converting it to a float
df['Product Price(TL)'] = df['Product Price'].str.extract(r'(\d+(?:,\d+)?)').replace(',', '.', regex=True).astype(float)

del df['Product Price']

df = df[~df['Product Price(TL)'].isin([1, 2])]

# Add 30 (shipping cost) to 'Product Price(TL)' if it's less than 150
df.loc[df['Product Price(TL)'] < 150, 'Product Price(TL)'] += 30

# Add 30 (shipping cost) to 'Product Price(TL)' if it's equal or greater than 150 and Campaign Name is not '150 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)'
df.loc[(df['Product Price(TL)'] >= 150) & (df['Campaign Name'] != '150 TL ve Üzeri Kargo Bedava (Satıcı Karşılar)'), 'Product Price(TL)'] += 30

df.rename(columns={'Product Price(TL)': 'Total Price (TL)'}, inplace=True)

del df['Campaign Name']

# translate Turkish to English

# Create mapping dictionaries for each column
delivery_duration_mapping = {
    'Not found': 'Not found',
    '2 gün içinde': 'Within 2 days',
    '5 gün içinde': 'Within 5 days',
    '1 gün içinde kargoda': 'Ships within 1 day',
    '3 gün içinde': 'Within 3 days'
}

warranty_type_mapping = {
    'İthalatçı Garantili': 'Importer Guaranteed',
    'Resmi Distribütör Garantili': 'Official Distributor Guaranteed',
    np.nan: 'Not Available'
}

color_mapping = {
    'Siyah': 'Black', 'Mavi': 'Blue', 'Pembe': 'Pink', 'Mor': 'Purple', 
    'Beyaz': 'White', 'Kırmızı': 'Red', 'Yeşil': 'Green', 'Metalik': 'Metallic',
    'Altın': 'Gold', 'Turkuaz': 'Turquoise', 'Bej': 'Beige', 'Gümüş': 'Silver',
    'Gri': 'Gray', 'Turuncu': 'Orange', 'Lacivert': 'Navy', 
    np.nan: 'Not Available'
}

anc_mapping = {
    'Var': 'Available', 'Yok': 'Not Available', np.nan: 'Not Available'
}

water_resistance_mapping = {
    'Var': 'Available', 'Yok': 'Not Available', np.nan: 'Not Available'
}

touch_control_mapping = {
    'Var': 'Available', 'Yok': 'Not Available', np.nan: 'Not Available'
}

warranty_period_mapping = {
    '2 Yıl': '2 Years', '1 Yıl': '1 Year', np.nan: 'Not Available'
}

# Apply the mappings to the DataFrame
df['Delivery Duration Text Value'] = df['Delivery Duration Text Value'].map(delivery_duration_mapping)
df['Warranty Type'] = df['Warranty Type'].map(warranty_type_mapping)
df['Color'] = df['Color'].map(color_mapping)
df['Active Noise Cancellation (ANC)'] = df['Active Noise Cancellation (ANC)'].map(anc_mapping)
df['Water/Sweat Resistance'] = df['Water/Sweat Resistance'].map(water_resistance_mapping)
df['Touch Control'] = df['Touch Control'].map(touch_control_mapping)
df['Warranty Period'] = df['Warranty Period'].map(warranty_period_mapping)

df_cop_1 = df.copy()

# translate Turkish to English

# Create mapping dictionaries for each column
delivery_duration_mapping = {
    'Not found': 'Not found',
    '2 gün içinde': 'Within 2 days',
    '5 gün içinde': 'Within 5 days',
    '1 gün içinde kargoda': 'Ships within 1 day',
    '3 gün içinde': 'Within 3 days'
}

warranty_type_mapping = {
    'İthalatçı Garantili': 'Importer Guaranteed',
    'Resmi Distribütör Garantili': 'Official Distributor Guaranteed',
    np.nan: 'Not Available'
}

color_mapping = {
    'Siyah': 'Black', 'Mavi': 'Blue', 'Pembe': 'Pink', 'Mor': 'Purple', 
    'Beyaz': 'White', 'Kırmızı': 'Red', 'Yeşil': 'Green', 'Metalik': 'Metallic',
    'Altın': 'Gold', 'Turkuaz': 'Turquoise', 'Bej': 'Beige', 'Gümüş': 'Silver',
    'Gri': 'Gray', 'Turuncu': 'Orange', 'Lacivert': 'Navy', 
    np.nan: 'Not Available'
}

anc_mapping = {
    'Var': 'Available', 'Yok': 'Not Available', np.nan: 'Not Available'
}

water_resistance_mapping = {
    'Var': 'Available', 'Yok': 'Not Available', np.nan: 'Not Available'
}

touch_control_mapping = {
    'Var': 'Available', 'Yok': 'Not Available', np.nan: 'Not Available'
}

warranty_period_mapping = {
    '2 Yıl': '2 Years', '1 Yıl': '1 Year', np.nan: 'Not Available'
}

# Apply the mappings to the DataFrame
df['Delivery Duration Text Value'] = df['Delivery Duration Text Value'].map(delivery_duration_mapping)
df['Warranty Type'] = df['Warranty Type'].map(warranty_type_mapping)
df['Color'] = df['Color'].map(color_mapping)
df['Active Noise Cancellation (ANC)'] = df['Active Noise Cancellation (ANC)'].map(anc_mapping)
df['Water/Sweat Resistance'] = df['Water/Sweat Resistance'].map(water_resistance_mapping)
df['Touch Control'] = df['Touch Control'].map(touch_control_mapping)
df['Warranty Period'] = df['Warranty Period'].map(warranty_period_mapping)


mapping_deliv_dict = {'Not found':0,
                '1 gün içinde kargoda':3,
                '2 gün içinde':2,
                '3 gün içinde':1}

mapping_warr_dict = {'İthalatçı Garantili':1,
                     'Resmi Distribütör Garantili':2}
df['Delivery Duration Text Value'] = df['Delivery Duration Text Value'].map(mapping_deliv_dict)

df['Warranty Type'] = df['Warranty Type'].map(mapping_warr_dict)
df['Warranty Type'].fillna(0,inplace=True)

df['Active Noise Cancellation (ANC)']=df['Active Noise Cancellation (ANC)'].map({'Var':1, 'Yok':0})
df['Active Noise Cancellation (ANC)'].fillna(0,inplace=True)

df['Water/Sweat Resistance']=df['Water/Sweat Resistance'].map({'Var':1, 'Yok':0})
df['Water/Sweat Resistance'].fillna(0,inplace=True)

df['Touch Control']=df['Touch Control'].map({'Var':1, 'Yok':0})
df['Touch Control'].fillna(0,inplace=True)

df['Warranty Period']=df['Warranty Period'].map({'3 Yıl':3,'2 Yıl':2, '1 Yıl':1})
df['Warranty Period'].fillna(0,inplace=True)

df['Favorite Count'] = pd.to_numeric(df['Favorite Count'])

df['Seller Rating'] = pd.to_numeric(df['Seller Rating'])

df = df[['Rating Score', 'Total Review Count', 'Favorite Count',
       'Delivery Duration Text Value', 'Seller Rating', 'Warranty Type',
       'Active Noise Cancellation (ANC)', 'Water/Sweat Resistance',
       'Bluetooth Version', 'Touch Control', 'Warranty Period',
       'Total Price (TL)']]

group_fixed_features = ['Active Noise Cancellation (ANC)', 'Water/Sweat Resistance', 'Bluetooth Version', 'Touch Control',]
group_prod_rating = ['Rating Score','Total Review Count', 'Favorite Count']
group_sel_features = ['Seller Rating', 'Delivery Duration Text Value']
group_warranty = ['Warranty Period','Warranty Type']
group_price = ['Total Price (TL)']

# Creating a dictionary to hold these groups
feature_groups = {
    "Fixed Features": group_fixed_features,
    "Product Rating": group_prod_rating,
    "Seller Features": group_sel_features,
    "Warranty": group_warranty,
    "Price": group_price
}

portion_for_groups =1/len(feature_groups)

# Count the number of keys, excluding 'Fixed Features'
group_fixed_features_weights = {feature: portion_for_groups/len(group_fixed_features) for feature in group_fixed_features}
group_prod_rating_weights = {feature: portion_for_groups/len(group_prod_rating) for feature in group_prod_rating}
group_sel_features_weights = {feature: portion_for_groups/len(group_sel_features) for feature in group_sel_features}
group_warranty_weights = {feature: portion_for_groups/len(group_warranty) for feature in group_warranty}
group_price_weights = {feature: portion_for_groups/len(group_price) for feature in group_price}

# Combining all weight dictionaries
all_weights = {**group_fixed_features_weights, **group_prod_rating_weights, **group_sel_features_weights, **group_warranty_weights, **group_price_weights}

# Creating a DataFrame from the combined weights
weights_df = pd.DataFrame(list(all_weights.items()), columns=['Feature', 'Weight'])

feature_groups = {
    "Fixed Features": group_fixed_features,
    "Product Rating": group_prod_rating,
    "Seller Features": group_sel_features,
    "Warranty": group_warranty,
    "Price": group_price
}

order_of_importance = [5, 1, 1, 5, 1]

new_values = [(1 - value / sum(order_of_importance)) for value in order_of_importance]

# Creating the dictionary
importance_dict = dict(zip(feature_groups.keys(), new_values))

# Grouping the features according to their category
feature_to_group = {
    'Active Noise Cancellation (ANC)': 'Fixed Features',
    'Water/Sweat Resistance': 'Fixed Features',
    'Bluetooth Version': 'Fixed Features',
    'Touch Control': 'Fixed Features',
    'Rating Score': 'Product Rating',
    'Total Review Count': 'Product Rating',
    'Favorite Count': 'Product Rating',
    'Seller Rating': 'Seller Features',
    'Delivery Duration Text Value': 'Seller Features',
    'Warranty Period': 'Warranty',
    'Warranty Type': 'Warranty',
    'Total Price (TL)': 'Price'
}

# Multiplying weights in weights_df by their corresponding group importance value
weights_df['Adjusted Weight'] = weights_df['Feature'].map(feature_to_group).map(importance_dict) * weights_df['Weight']


def mcdm_project(df_data,weights):
    # Normalize the data
    normalized_df = df_data / np.sqrt((df_data**2).sum())

    normalized_df['Total Price (TL)'] = 1 - (df['Total Price (TL)'] / df['Total Price (TL)'].max())

    # Applying the weights
    weighted_normalized_df = normalized_df.multiply(list(weights))

    # Positive Ideal Solution (PIS) and Negative Ideal Solution (NIS)
    pis = weighted_normalized_df.max()
    nis = weighted_normalized_df.min()

    # Calculate the Separation Measures
    distance_from_pis = np.sqrt((weighted_normalized_df - pis)**2).sum(axis=1)
    distance_from_nis = np.sqrt((weighted_normalized_df - nis)**2).sum(axis=1)

    # Calculate the Relative Closeness to the Ideal Solution
    relative_closeness = distance_from_nis / (distance_from_nis + distance_from_pis)

    # Ranking the Alternatives
    ranking = relative_closeness.rank(ascending=False)

    # Combine the scores and rankings for display
    topsis_results = pd.DataFrame({
        'Score': relative_closeness,
        'Rank': ranking
    }).sort_values('Rank')

    return df_cop_1.loc[topsis_results.index[:4]]

def main():
    st.markdown("""
        <style>
            .stSlider > div > div {
                width: 80% !important;
            }
            .group-name {
                font-size: 14px; /* Font size for group names */
                font-weight: bold;
            }
            .features-list {
                font-size: 14  px; /* Font size for feature names */
            }
            .dataframe {  /* Style for the DataFrame */
                font-size: 12px; /* Reduced font size */
                width: 100% !important; /* Full width of the page */
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='font-size: 24px;'>MCDM Project</h1>", unsafe_allow_html=True)

    # Display all feature groups and their features
    st.markdown("<h2 style='font-size: 18px;'>Feature Groups:</h2>", unsafe_allow_html=True)
    for group, features in feature_groups.items():
        st.markdown(f"**{group}**: {' | '.join(features)}")

    st.markdown("<h2 style='font-size: 18px;'>Rate the importance of each feature group (1-5):</h2>", unsafe_allow_html=True)

    # Create five columns for sliders
    col1, col2, col3, col4, col5 = st.columns(5)

    scores = {}
    # Display sliders and group names with their features
    for index, group in enumerate(feature_groups.keys()):
        column = (col1, col2, col3, col4, col5)[index]
        with column:
            st.markdown(f"<div class='group-name'>{group}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='features-list'></div>", unsafe_allow_html=True)
            score = st.slider("", min_value=1, max_value=5, value=3, key=f"slider_{group}")
            scores[group] = score

    # Recalculate the portion for each group based on user scores
    total_score = sum(scores.values())
    new_portion_for_groups = {group: scores[group] / total_score for group in scores}

    # Adjust weights for each feature based on the new portions
    adjusted_weights = all_weights.copy()
    for feature, group in feature_to_group.items():
        adjusted_weights[feature] = all_weights[feature] * new_portion_for_groups[group]

    # Perform MCDM with the adjusted weights
    if st.button('Calculate MCDM'):
        ranked_data = mcdm_project(df, adjusted_weights.values())

        # Making product links clickable
        ranked_data['Product Link'] = ranked_data['Product Link'].apply(
            lambda x: f'<a href="{x}" target="_blank">Link</a>')

        # Convert DataFrame to HTML
        ranked_data_html = ranked_data.to_html(escape=False, index=False)

        # Displaying MCDM Results with clickable links and custom table style
        st.markdown("<h2 style='font-size: 18px;'>MCDM Results</h2>", unsafe_allow_html=True)
        st.markdown(ranked_data_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



