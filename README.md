# Project 13: Road Accident Data Analysis System

Flask + MySQL web application for analyzing public, synthetic, or properly anonymized road accident records.

## Features
- Dashboard KPIs and Matplotlib charts
- Add records and import CSV
- Validate date/time, region, vehicle type and severity
- Group results by month, region, vehicle type and severity
- Missing-data summary and CSV export
- Synthetic demo-data generator

## Data boundaries
Do not store names, phone numbers, vehicle registration numbers, exact home addresses, or other personal identifiers. Document the source and geographic granularity of any real dataset. Results are operational counts and associations, not proof of causation or individual risk.

## Requirements
Python 3.10+, MySQL Server 8.x.

## Run on Windows PowerShell
1. Extract the ZIP and open the inner project folder in VS Code.
2. Create environment: `py -m venv .venv`
3. Install packages: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
4. Open MySQL Workbench and execute `schema.sql`.
5. Copy `.env.example` to `.env`; enter your MySQL username and password.
6. Generate synthetic records: `.\.venv\Scripts\python.exe -m scripts.seed_data`
7. Start app: `.\.venv\Scripts\python.exe app.py`
8. Open `http://127.0.0.1:5000`.

If PowerShell blocks activation, use the Python executable commands above directly. Never commit `.env`.

## CSV format
Required: `accident_datetime,region,vehicle_type,severity`
Optional: `road_name,weather`
Date format example: `2026-01-05 08:30`
Vehicle types: Car, Motorcycle, Bus, Truck, Van, Bicycle, Pedestrian, Other.
Severity: Minor, Serious, Fatal, Unknown.

## Push to GitHub
Create an empty GitHub repository named `road-accident-data-analysis`, then run:
```bash
git init
git add .
git commit -m "Initial commit: Road Accident Data Analysis System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/road-accident-data-analysis.git
git push -u origin main
```
If `origin` already exists, use `git remote set-url origin https://github.com/YOUR-USERNAME/road-accident-data-analysis.git`.
