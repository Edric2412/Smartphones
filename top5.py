import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Define file paths
input_file_path = 'processed_smartphone_sales.xlsx'  # Update this path
output_file_path = 'top_5_models_per_brand.xlsx'  # Update this path

# Load the processed data
df = pd.read_excel(input_file_path, sheet_name='Processed Data')

# Define a function to extract numeric values for calculations
def extract_numeric(value):
    if pd.isna(value):
        return None
    value_str = str(value)
    if '₹' in value_str:
        value_str = value_str.replace('₹', '').replace(',', '')
    if ' mAh' in value_str:
        value_str = value_str.replace(' mAh', '')
    if ' GB' in value_str:
        value_str = value_str.replace(' GB', '')
    if ' GHz' in value_str:
        value_str = value_str.replace(' GHz', '')
    try:
        return float(value_str)
    except ValueError:
        return None

# Apply conversion for calculations
df['Price Num'] = df['Price'].apply(extract_numeric)
df['Battery Capacity Num'] = df['Battery Capacity'].apply(extract_numeric)
df['RAM Num'] = df['RAM'].apply(extract_numeric)
df['ROM Num'] = df['ROM'].apply(extract_numeric)
df['Processor Speed Num'] = df['Processor Speed'].apply(extract_numeric)
df['Front Camera Num'] = df['Front Camera'].apply(extract_numeric)
df['Rear Camera Num'] = df['Rear Camera'].apply(extract_numeric)

# Drop rows with NaN values that might have resulted from conversion issues
df = df.dropna(subset=['Price Num', 'Battery Capacity Num', 'RAM Num', 'ROM Num', 'Processor Speed Num', 'Front Camera Num', 'Rear Camera Num'])

# Define a function to evaluate and rate models based on criteria
def rate_models(df, brand, top_n=5):
    # Filter models of the specific brand
    brand_df = df[df['Brand Name'] == brand]

    # Criteria weights (adjust these weights based on your preference)
    criteria_weights = {
        'Price Num': -1,  # Lower price is better
        'Battery Capacity Num': 1,  # Higher battery capacity is better
        'RAM Num': 1,  # Higher RAM is better
        'ROM Num': 1,  # Higher ROM is better
        'Processor Speed Num': 1,  # Higher processor speed is better
        'Front Camera Num': 1,  # Higher front camera value is better
        'Rear Camera Num': 1  # Higher rear camera value is better
    }
    
    # Apply weights and compute scores
    brand_df = brand_df.copy()
    brand_df['Score'] = (
        criteria_weights['Price Num'] * brand_df['Price Num'] +
        criteria_weights['Battery Capacity Num'] * brand_df['Battery Capacity Num'] +
        criteria_weights['RAM Num'] * brand_df['RAM Num'] +
        criteria_weights['ROM Num'] * brand_df['ROM Num'] +
        criteria_weights['Processor Speed Num'] * brand_df['Processor Speed Num'] +
        criteria_weights['Front Camera Num'] * brand_df['Front Camera Num'] +
        criteria_weights['Rear Camera Num'] * brand_df['Rear Camera Num']
    )
    
    # Normalize the scores to range between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    brand_df['Normalized Score'] = scaler.fit_transform(brand_df[['Score']])
    
    # Map normalized scores to ratings from 1 to 5
    brand_df['Rating'] = (brand_df['Normalized Score'] * 4 + 1).round().astype(int)
    
    # Sort by score and select top models
    brand_df = brand_df.sort_values(by='Score', ascending=False)
    top_models = brand_df.head(top_n)
    
    return top_models

# List of brands and the specific brand to prioritize
brands = df['Brand Name'].unique()
specific_brand = 'nothing'  # Define the brand to prioritize

# Select top models for each brand
top_models_df = pd.concat([rate_models(df, brand) for brand in brands])

# Save the top models to a new Excel file
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    top_models_df.to_excel(writer, index=False, sheet_name='Top Models')
    
    # Access the XlsxWriter workbook and worksheet
    workbook  = writer.book
    worksheet = writer.sheets['Top Models']
    
    # Define cell formats
    price_format = workbook.add_format({'num_format': '₹#,##0.00'})
    battery_format = workbook.add_format({'num_format': '0 "mAh"'})
    ram_format = workbook.add_format({'num_format': '0 "GB"'})
    rom_format = workbook.add_format({'num_format': '0 "GB"'})
    processor_speed_format = workbook.add_format({'num_format': '0.0 "GHz"'})
    
    # Apply formats
    worksheet.set_column('E:E', 15, price_format)  # Price column
    worksheet.set_column('F:F', 20, battery_format)  # Battery Capacity column
    worksheet.set_column('G:G', 10, ram_format)  # RAM column
    worksheet.set_column('H:H', 10, rom_format)  # ROM column
    worksheet.set_column('C:C', 15, processor_speed_format)  # Processor Speed column

print(f"Top models data saved to {output_file_path}")
