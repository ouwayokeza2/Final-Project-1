# U.S. Labor Market Dashboard with Healthcare Focus

## Project Overview

This project creates an interactive Streamlit dashboard that analyzes major U.S. labor market indicators using data from the U.S. Bureau of Labor Statistics (BLS). The dashboard also connects national labor market trends to healthcare workforce conditions, which supports the project focus in Healthcare Management, Supply Chain, staffing, and operations.

The dashboard uses the BLS Public Data API to collect monthly labor statistics, cleans and organizes the data using Python and pandas, and visualizes the trends using Streamlit and Plotly.

## Live Deliverables

After publishing, replace these placeholders with your actual links:

1. **GitHub Repository:** Add your GitHub link here
2. **Streamlit Dashboard:** Add your Streamlit link here
3. **YouTube Presentation:** Add your YouTube link here
4. **Write-Up:** Submit your final write-up document separately or include it in this repository

## Labor Market Indicators Included

The dashboard includes:

- Unemployment Rate
- Total Nonfarm Employment
- Labor Force Participation Rate
- Average Hourly Earnings
- Average Weekly Hours
- Healthcare Employment

These indicators help explain broader workforce trends and show how healthcare employment compares with the overall labor market.

## Project Structure

```text
us_labor_healthcare_dashboard/
│
├── app.py
├── fetch_bls_data.py
├── requirements.txt
├── README.md
├── data/
│   └── bls_labor_data.csv
└── .github/
    └── workflows/
        └── update_bls_data.yml
```

## How the Project Works

1. `fetch_bls_data.py` pulls labor market data from the BLS API.
2. The script cleans and organizes the data into a CSV file.
3. `app.py` reads the CSV file and creates an interactive Streamlit dashboard.
4. GitHub Actions can automatically update the dataset each month when new labor data are released.

## How to Run Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

Pull or refresh the BLS data:

```bash
python fetch_bls_data.py
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

## Data Source

Data are collected from the U.S. Bureau of Labor Statistics Public Data API.

Main API documentation: https://www.bls.gov/developers/home.htm

## Notes

This project was created for ECON 8320 - Tools for Data Analysis. It demonstrates API data collection, data cleaning, time-series analysis, dashboard design, and automated data updates using GitHub Actions.
