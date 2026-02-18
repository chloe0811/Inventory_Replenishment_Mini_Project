# Inventory Replenishment Analytics Demo

## Executive Summary
This project simulates a real-world inventory replenishment workflow from a Data Analyst perspective.

The objective is to transform daily sales and inventory data into actionable purchasing decisions that help operations teams reduce stockouts while avoiding unnecessary overstock.

Unlike academic exercises, this repository focuses on business-ready outputs that could be directly used by retail, supply chain, or operations teams.

The pipeline is implemented in Python using pandas for data processing and matplotlib for visualisation.

## Business Context

In many retail and supply chain environments, analysts are responsible for monitoring inventory levels and recommending when to reorder products.

This project recreates that real-world scenario by building a lightweight replenishment decision pipeline using Python and pandas.

The workflow reflects how analytics is typically used in production business environments rather than academic modelling exercises.

## Overview

This project supports replenishment decisions across approximately 50 SKUs by:
1.  Generates 12 weeks of daily sales and inventory history.
2.  Computes a 14-day rolling average demand and standard deviation.
3.  Calculates Safety Stock (SS) and Reorder Point (ROP) for a 95% service level.
4.  Identifies SKUs that have fallen below their ROP and suggests order quantities.

## Example Business Questions This Project Answers

- Which SKUs are at risk of stockout today?
- How much inventory should be ordered to maintain a 95% service level?
- Which products require immediate purchasing attention?
- How does demand variability affect safety stock requirements?

## Project Structure

```
├── data/
│   ├── raw/             # Generated raw data
│   └── processed/       # Data with features (rolling avg, ROP, etc.)
├── notebooks/
│   └── 01_eda.ipynb     # Exploratory Data Analysis
├── outputs/
│   ├── figures/         # Generated charts
│   └── replenishment_recommendations.csv # Final output
├── src/
│   ├── clean.py         # Data cleaning
│   ├── features.py      # Feature engineering
│   ├── forecast.py      # SS and ROP calculations
│   ├── generate.py      # Synthetic data generation
│   └── recommend.py     # Reorder logic
├── run_pipeline.py      # Main execution script
└── requirements.txt     # Dependencies
```

## Business Logic & Formulas

-   **Avg Daily Demand**: Rolling mean of daily sales (14-day window).
-   **Demand Std Dev**: Rolling standard deviation of daily sales (14-day window).
-   **Safety Stock (SS)**: Buffer stock to mitigate risk of stockouts.
    $$ SS = Z \times \sigma_{d} \times \sqrt{L} $$
    -   $Z = 1.65$ (95% Service Level)
    -   $\sigma_{d}$ = Demand Standard Deviation
    -   $L$ = Lead Time (Days)
-   **Reorder Point (ROP)**: Inventory level at which a new order should be placed.
    $$ ROP = (Avg\_Daily\_Demand \times L) + SS $$
-   **Suggested Order Qty**:
    $$ Qty = \max(0, ROP - Current\_On\_Hand) $$

## How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Pipeline**:
    ```bash
    python run_pipeline.py
    ```

3.  **Check Outputs**:
    -   View recommendations in `outputs/replenishment_recommendations.csv`.
    -   See validation charts in `outputs/figures/`.

## Outputs

-   **Replenishment Table**: A CSV file listing SKUs that need restocking, including their current stock, ROP, and suggested order quantity.
-   **Stockout Risk Chart**: Visualizes the top 10 SKUs most in danger of stockout.
-   **Demand Trends**: Sample plots showing sales vs. inventory levels over time.

## Future Improvements

-   Implement more sophisticated forecasting (e.g., ARIMA, Prophet).
-   Add seasonality and trend components to synthetic data.
-   Optimize order quantities using EOQ (Economic Order Quantity).
-   Build a Streamlit dashboard for interactive analysis.

## Author

Built as a portfolio project to demonstrate practical analytics skills for Data Analyst and Operations Analyst roles.