import pandas as pd

# Define file paths
input_file_path = 'smartphone_sales.xlsx'  # Update this path
output_file_path = 'processed_smartphone_sales.xlsx'  # Update this path

# List of required brands
brands = ['nothing', 'motorola', 'poco', 'iqoo', 'infinix']
specific_brand = 'nothing'  # Define the brand to prioritize

# Mapping of old headers to new headers
header_mapping = {
    'brand_name': 'Brand Name',
    'model': 'Model',
    'processor_brand': 'Chipset',
    'processor_speed': 'Processor Speed',
    'battery_capacity': 'Battery Capacity',
    'price': 'Price',
    'ram_capacity': 'RAM',
    'internal_memory': 'ROM',
    'primary_camera_front': 'Front Camera',
    'primary_camera_rear': 'Rear Camera'
}

# Read the Excel file with the first row as headers
df = pd.read_excel(input_file_path, header=0)

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Filter rows based on the specified brands
filtered_df = df[df['brand_name'].str.lower().isin(brands)]

# Fill null values with 'Nil'
filtered_df = filtered_df.fillna('Nil')

# Rename the columns based on the header_mapping
filtered_df = filtered_df.rename(columns=header_mapping)

# Capitalize the first letter of each brand name and processor
filtered_df.loc[:, 'Brand Name'] = filtered_df['Brand Name'].str.capitalize()
filtered_df.loc[:, 'Chipset'] = filtered_df['Chipset'].str.capitalize()

# Add units to the columns
filtered_df.loc[:, 'Price'] = filtered_df['Price'].apply(lambda x: f'₹{x:,.2f}' if x != 'Nil' else x)
filtered_df.loc[:, 'Battery Capacity'] = filtered_df['Battery Capacity'].apply(lambda x: f'{x} mAh' if x != 'Nil' else x)
filtered_df.loc[:, 'RAM'] = filtered_df['RAM'].apply(lambda x: f'{x} GB' if x != 'Nil' else x)
filtered_df.loc[:, 'ROM'] = filtered_df['ROM'].apply(lambda x: f'{x} GB' if x != 'Nil' else x)
filtered_df.loc[:, 'Processor Speed'] = filtered_df['Processor Speed'].apply(lambda x: f'{x} GHz' if x != 'Nil' else x)

# Select only the renamed columns
final_columns = list(header_mapping.values())
filtered_df = filtered_df[final_columns]

# Sort the DataFrame to show the specific brand first
filtered_df['Brand Name'] = filtered_df['Brand Name'].astype('category')
category_order = [specific_brand.capitalize()] + [b.capitalize() for b in brands if b != specific_brand]
filtered_df['Brand Name'] = filtered_df['Brand Name'].cat.set_categories(category_order)
filtered_df = filtered_df.sort_values(by=['Brand Name'])

# Display the final filtered data
print("Final Filtered Data:")
print(filtered_df.head())

# Save the filtered and formatted data to a new Excel file with formatting
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Processed Data')
    
    # Access the XlsxWriter workbook and worksheet
    workbook  = writer.book
    worksheet = writer.sheets['Processed Data']
    
    # Define cell formats
    price_format = workbook.add_format({'num_format': '₹#,##0.00'})
    battery_format = workbook.add_format({'num_format': '0 "mAh"'})
    ram_rom_format = workbook.add_format({'num_format': '0 "GB"'})
    processor_speed_format = workbook.add_format({'num_format': '0.0 "GHz"'})
    
    # Apply formats to columns
    worksheet.set_column('E:E', 15, price_format)  # Price column
    worksheet.set_column('D:D', 20, battery_format)  # Battery Capacity column
    worksheet.set_column('F:F', 10, ram_rom_format)  # RAM column
    worksheet.set_column('G:G', 10, ram_rom_format)  # ROM column
    worksheet.set_column('C:C', 15, processor_speed_format)  # Processor Speed column

print(f"Processed data saved to {output_file_path}")
