import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from googleapiclient.discovery import build

# Define file path
input_file_path = 'top_5_models_per_brand.xlsx'  # Update this path

# Load the data from the Excel file with error handling
try:
    df = pd.read_excel(input_file_path, sheet_name='Top Models')
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Set up the Streamlit app
st.title('Top 5 Smartphone Models per Brand')

# Display a dataframe with a scroll bar
st.dataframe(df, use_container_width=True)

# Create charts for each phone model
brands = df['Brand Name'].unique()

# Option to select a brand to view its models
selected_brand = st.selectbox('Select Brand:', brands)

# Filter data for the selected brand
brand_data = df[df['Brand Name'] == selected_brand]

# Show details of the selected brand
st.subheader(f'Models of {selected_brand}')

# Google Custom Search API setup
api_key = 'API_KEY'  # Replace with your API key
cse_id = 'CSE_ID'  # Replace with your Custom Search Engine ID

@st.cache_data
def get_image_url(model_name):
    service = build("customsearch", "v1", developerKey=api_key)
    start_index = 1
    while True:
        try:
            res = service.cse().list(
                q=model_name, cx=cse_id, searchType='image', num=10, start=start_index
            ).execute()
            if 'items' in res and len(res['items']) > 0:
                for item in res['items']:
                    image_url = item.get('link')
                    if image_url:
                        return image_url
            if 'queries' in res and 'nextPage' in res['queries']:
                start_index = res['queries']['nextPage'][0].get('startIndex', None)
                if start_index is None:
                    break
            else:
                break
        except Exception as e:
            st.error(f"Error fetching image: {e}")
            break
    return None

# Display each model's details
for index, row in brand_data.iterrows():
    st.subheader(f"Model: {row['Model']}")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write(f"**Price:** {row['Price']}")
        st.write(f"**Battery Capacity:** {row['Battery Capacity']}")
        st.write(f"**RAM:** {row['RAM']}")
        st.write(f"**ROM:** {row['ROM']}")
        st.write(f"**Chipset:** {row['Chipset']}")
        st.write(f"**Processor Speed:** {row['Processor Speed']}")
        st.write(f"**Front Camera:** {row['Front Camera']}")
        st.write(f"**Rear Camera:** {row['Rear Camera']}")
    
    st.write("---")

    with col2:
        image_url = get_image_url(row['Model'])
        if image_url:
            st.image(image_url, caption=row['Model'], use_column_width=True)
        else:
            st.write("Image not found.")
        
# Function to plot advanced interactive bar charts for different criteria
def plot_advanced_charts(df, criteria, kind='min'):
    if criteria not in df.columns:
        raise ValueError(f"Criteria '{criteria}' not found in DataFrame columns.")
    
    # Filter data based on the criteria
    if kind == 'min':
        top_models = df.loc[df.groupby('Brand Name')[criteria].idxmin()]
    elif kind == 'max':
        top_models = df.loc[df.groupby('Brand Name')[criteria].idxmax()]
    else:
        raise ValueError("Kind must be either 'min' or 'max'.")

    # Convert criteria to numeric for plotting
    top_models[criteria] = top_models[criteria].astype(str).str.replace(r'[^\d.]', '', regex=True)
    top_models[criteria] = pd.to_numeric(top_models[criteria], errors='coerce')

    # Create the interactive bar chart using Plotly
    fig = px.bar(top_models, x='Brand Name', y=criteria, color='Model', text='Model',
                 title=f"{kind.capitalize()} {criteria} Phone from Each Brand",
                 labels={criteria: criteria.replace('_', ' ').title()},
                 height=600)
    
    # Update the layout for better aesthetics
    fig.update_traces(texttemplate='%{text}<br>%{y:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title='Brand',
        yaxis_title=criteria.replace('_', ' ').title(),
        legend_title_text='Model',
        legend=dict(font=dict(size=10)),
        xaxis=dict(tickmode='linear'),
        yaxis=dict(range=[0, top_models[criteria].max() * 1.1])
    )
    
    return fig

# User selection for criteria visualization
criteria_options = ['Price', 'Battery Capacity', 'Processor Speed']
selected_criteria = st.selectbox('Select Criteria for Visualization:', criteria_options)

# User selection for min or max
kind_options = ['min', 'max']
selected_kind = st.selectbox('Select Min or Max:', kind_options)

# Plot advanced interactive bar charts based on user selection
fig = plot_advanced_charts(df, selected_criteria, kind=selected_kind)
st.plotly_chart(fig, use_container_width=True)
