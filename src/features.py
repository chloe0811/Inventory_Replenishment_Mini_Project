import pandas as pd

def engineer_features(df):
    """
    Calculates rolling statistics for demand forecasting.
    """
    # Ensure data is sorted by SKU then Date for rolling calculations
    df = df.sort_values(by=['SKU', 'Date'])
    
    # Calculate rolling mean and standard deviation of sales (demand)
    # Using a 14-day window as per requirements
    df['Avg_Daily_Demand'] = df.groupby('SKU')['Sales'].transform(lambda x: x.rolling(window=14, min_periods=1).mean())
    df['Demand_Std'] = df.groupby('SKU')['Sales'].transform(lambda x: x.rolling(window=14, min_periods=1).std())
    
    # Fill NaN values for the first few days where rolling std might be undefined
    df['Demand_Std'].fillna(0, inplace=True)
    
    return df
