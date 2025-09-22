# COVID-19 Data Visualization Dashboard

This is an interactive dashboard built with Python and Streamlit to visualize COVID-19 data by country and continent.  
It fetches real-time data from [disease.sh API](https://disease.sh/) and provides charts, tables, and historical trends.

## Features
- Interactive bar charts for top N countries by cases, deaths, recovered, or active cases.
- Filters by continent and metric selection.
- View historical trend of cases for any country.
- Download CSV for top countries data.

## Technologies Used
- Python 3.11
- Streamlit
- Pandas
- Plotly
- Requests

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Vaishalij77/covid-dashboard.git
   cd covid-dashboard

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   # source venv/bin/activate  # macOS/Linux

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the Dashboard:
   ```bash
   streamlit run app.py

## Author
Vaishali J


