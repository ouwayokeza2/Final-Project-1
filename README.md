# U.S. Labor Market Dashboard with Healthcare Focus

## ECON 8320 – Tools for Data Analysis

This project creates an interactive Streamlit dashboard using official U.S. Bureau of Labor Statistics data. The purpose of the project is to connect labor market trends to workforce challenges in healthcare, operations, and supply chain management.

## Live Project Deliverables

1. Repository: Add your GitHub repository link here  
2. Streamlit Dashboard: Add your Streamlit link here  
3. YouTube Presentation: Add your YouTube link here  
4. Semester Project Write-Up: Submit the written report document  

## Project Overview

The dashboard uses the BLS public API to collect labor market data and display it in a clean, interactive format. The dashboard includes broad labor market indicators and a healthcare-specific employment measure to connect the project to healthcare workforce planning.

## Indicators Included

- Unemployment Rate
- Total Nonfarm Employment
- Healthcare Employment
- Labor Force Participation Rate
- Average Hourly Earnings
- Average Weekly Hours

## Why This Project Matters

Labor market trends affect staffing, budgeting, wages, scheduling, and long-term workforce planning. This is especially important in healthcare, where employment shortages and wage changes can affect both operations and patient care.

## Tools Used

- Python
- pandas
- requests
- Plotly
- Streamlit
- GitHub
- GitHub Actions
- BLS Public API

## Dashboard Features

- Interactive labor market charts
- Date range filter
- Indicator selector
- Latest value snapshot
- Healthcare employment comparison
- Indexed employment growth chart
- Downloadable cleaned dataset
- Monthly automated data update through GitHub Actions

## How to Run the Project Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

Fetch the BLS data:

```bash
python fetch_bls_data.py
```

Run the dashboard:

```bash
streamlit run app.py
```

## Automation

The project includes a GitHub Actions workflow that runs monthly and can also be triggered manually. The workflow updates the BLS dataset and commits the new data file to the repository.

## Data Source

Data is collected from the U.S. Bureau of Labor Statistics public API.

## Author

Ornella Uwayo Keza  
MBA Candidate | Healthcare Management | Supply Chain & Operations
