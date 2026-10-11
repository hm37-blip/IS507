
# ORD Flight Delay Analysis

**IS507 – Data, Statistical Models, and Information | Fall 2026**

## Project Overview

This project investigates whether scheduled airport traffic volume has a nonlinear relationship with flight delays at Chicago O'Hare International Airport (ORD).

Using January 2026 flight data from the Bureau of Transportation Statistics (BTS), we examine how hourly scheduled traffic volume relates to arrival and departure delays.

## Research Question

**Is there a nonlinear relationship between scheduled airport traffic volume and flight delays at Chicago O'Hare International Airport (ORD)?**

## Dataset

- **Source:** Bureau of Transportation Statistics (BTS)
- **Period:** January 2026
- **Original dataset:** 61,446 records
- **Cleaned datasets:**
  - Arrival: 24,019 flights
  - Departure: 24,192 flights
- **Independent variable:** `TOTAL_SCHEDULED_TRAFFIC`
- **Dependent variables:** `ARR_DELAY`, `DEP_DELAY`

## Methodology

1. Data cleaning and preprocessing
2. Exploratory data analysis (EDA)
3. Pearson correlation analysis
4. Linear regression (baseline)
5. Quadratic regression (planned)
6. Model comparison using RMSE, MAE, and R²

## Preliminary Findings

- Departure flights have a higher average delay (22.50 min) than arrival flights (16.25 min).
- Both delay distributions are strongly right-skewed.
- Linear correlations between scheduled traffic volume and delays are very weak.
- Further modeling will investigate whether nonlinear relationships provide additional explanatory value.

## Project Status

**Midterm:** Data preprocessing and exploratory analysis completed.

**Next Steps:** Fit and evaluate linear and quadratic regression models.

## Data Source

[Bureau of Transportation Statistics – TranStats](https://www.transtats.bts.gov/)
