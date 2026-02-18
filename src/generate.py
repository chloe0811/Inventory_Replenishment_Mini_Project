import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_inventory_data(n_skus=50, n_weeks=12):
    """
    Generates realistic synthetic daily sales and inventory data for SKUs.
    Features:
    - Trend (Assigned randomly per SKU: up, down, or flat)
    - Seasonality (Weekly pattern)
    - Realistic Replenishment (Sawtooth pattern using reorder points)
    
    Returns:
    - pd.DataFrame: Raw data with columns [Date, SKU, Sales, On_Hand, Lead_Time_Days]
    """
    np.random.seed(42)
    start_date = datetime.now().date() - timedelta(weeks=n_weeks)
    total_days = n_weeks * 7
    date_range = [start_date + timedelta(days=i) for i in range(total_days)]
    
    data = []
    
    # Define weekly seasonality factors (0=Mon, 6=Sun)
    # Fri, Sat, Sun have higher demand
    weekly_seasonality = np.array([0.8, 0.8, 0.9, 1.0, 1.2, 1.4, 1.3])
    
    for i in range(1, n_skus + 1):
        sku_id = f'SKU_{i:03d}'
        
        # 1. Demand Parameters
        base_demand = np.random.randint(10, 50)
        
        # Trend: Random slope between -0.05% and +0.05% per day
        trend_slope = np.random.uniform(-0.0005, 0.0005)
        trend_factors = 1 + np.linspace(0, trend_slope * total_days, total_days)
        
        # 2. Supply Parameters
        lead_time = np.random.randint(3, 10)
        # Reorder Point (approx logic for simulation: demand * lead_time + safety_buffer)
        # We don't calc exact SS here, just an approximation for the simulation to work
        sim_rop = base_demand * lead_time + (base_demand * 3) 
        sim_order_qty = base_demand * 14 # Order 2 weeks worth of stock
        
        # Initial State
        current_inv = sim_rop + sim_order_qty # Start full
        pipeline_orders = [] # List of tuples (arrival_date, qty)
        
        for day_idx, date in enumerate(date_range):
            # --- Daily Demand Generation ---
            day_of_week = date.weekday()
            seasonality_factor = weekly_seasonality[day_of_week]
            
            # Add some daily noise
            noise = np.random.normal(1.0, 0.1)
            
            # expected demand = base * trend * seasonality * noise
            lambda_param = base_demand * trend_factors[day_idx] * seasonality_factor * noise
            daily_sales = np.random.poisson(max(0, lambda_param))
            
            # Cap sales by availability
            actual_sales = min(daily_sales, current_inv)
            
            # --- Inventory Update ---
            # 1. Receive Orders
            arrived_qty = sum(qty for arrival, qty in pipeline_orders if arrival == date)
            current_inv += arrived_qty
            # Remove arrived orders
            pipeline_orders = [(arrival, qty) for arrival, qty in pipeline_orders if arrival > date]
            
            # 2. Fulfill Sales
            current_inv -= actual_sales
            
            # 3. Replenishment Check (Review at end of day)
            # If inventory + on_order < ROP, place order
            on_order = sum(qty for _, qty in pipeline_orders)
            inventory_position = current_inv + on_order
            
            if inventory_position <= sim_rop:
                arrival_date = date + timedelta(days=lead_time)
                # Ensure arrival doesn't go beyond our simulation checking if we need strict bounds, 
                # but for pandas df generation it's fine.
                pipeline_orders.append((arrival_date, sim_order_qty))
            
            data.append([date, sku_id, actual_sales, current_inv, lead_time])

    df = pd.DataFrame(data, columns=['Date', 'SKU', 'Sales', 'On_Hand', 'Lead_Time_Days'])
    return df

if __name__ == "__main__":
    df = generate_inventory_data()
    print(df.head())
    print(f"Generated {len(df)} rows.")
