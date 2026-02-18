import numpy as np

def calculate_safety_stock_rop(df, service_level_z=1.65):
    """
    Calculates Safety Stock and Reorder Point.
    """
    # Safety Stock formula: Z * Demand_Std * sqrt(Lead_Time)
    df['Safety_Stock'] = service_level_z * df['Demand_Std'] * np.sqrt(df['Lead_Time_Days'])
    
    # Reorder Point formula: (Avg_Daily_Demand * Lead_Time) + Safety_Stock
    df['Reorder_Point'] = (df['Avg_Daily_Demand'] * df['Lead_Time_Days']) + df['Safety_Stock']
    
    return df
