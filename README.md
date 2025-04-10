# 📱 Emerging Trends and Analytical Perspectives in the Development of New Smartphones

This project aims to help customers make smart decisions when choosing a smartphone by identifying and analyzing the **top 5 models per brand** based on multiple performance and pricing criteria. Visualizations and an interactive interface have been created using **Streamlit**, making the experience engaging and insightful.

---

## 📊 Project Structure

### 1. Data Collection and Cleaning
- **File:** `smartphone_sales.xlsx`
- **Script:** `Data_clean.py`
- Filters relevant brands (`Nothing`, `Motorola`, `Poco`, `iQOO`, `Infinix`)  
- Cleans and formats the data (adds units, handles nulls, renames headers)
- Exports processed data to: `processed_smartphone_sales.xlsx`

### 2. Top Model Selection
- **Script:** `top5.py`
- Calculates a **performance score** for each smartphone using criteria:
  - Price (lower is better)
  - Battery Capacity
  - RAM & ROM
  - Processor Speed
  - Camera Specs (Front & Rear)
- Outputs: `top_5_models_per_brand.xlsx`

### 3. Interactive Dashboard
- **Script:** `visual.py`
- **Interface:** Built using **Streamlit**
- Features:
  - Selection of smartphone brand
  - Display of top 5 models with full specifications
  - Integrated image fetching via Google Custom Search API
  - Interactive charts (via Plotly) based on Price, Battery, Processor Speed

![Interface](Smartphones/Interface.png)

---

## 🖼️ Visualizations

Includes 6 analytical visualizations (e.g., best battery, lowest price) and 1 interface image showcasing the Streamlit app.

---

## 🚀 How to Run the Project

### Requirements
- Python 3.x
- Libraries:
  ```
  pandas
  streamlit
  plotly
  scikit-learn
  google-api-python-client
  xlsxwriter
  openpyxl
  ```

### Steps
1. Clean the data:
   ```bash
   python Data_clean.py
   ```
2. Generate top models:
   ```bash
   python top5.py
   ```
3. Run the dashboard:
   ```bash
   streamlit run visual.py
   ```

---

## 🔐 API Key Setup

- To use the image feature, add your **Google Custom Search API key** and **Custom Search Engine ID** inside `visual.py`:
  ```python
  api_key = 'YOUR_API_KEY'
  cse_id = 'YOUR_CSE_ID'
  ```

---

## 💡 Objective

To **reduce decision fatigue** for smartphone buyers by narrowing down their choices to the best models from each brand using a **data-driven approach**.

---

## 📁 Output Files

- `processed_smartphone_sales.xlsx`: Cleaned and formatted smartphone dataset
- `top_5_models_per_brand.xlsx`: Final top 5 smartphones per brand with scores and ratings

---

Let me know if you'd like me to include markdown image references or links for hosting the visualizations/screenshots too!
