import pandas as pd

def clean_data(df):
    """
    Performs basic data cleaning on the input DataFrame.
    """
    # Ensure correct data types
    df['Date'] = pd.to_datetime(df['Date'])
    df['Sales'] = df['Sales'].astype(int)
    df['On_Hand'] = df['On_Hand'].astype(int)
    df['Lead_Time_Days'] = df['Lead_Time_Days'].astype(int)
    
    # Handle missing values (though synthetic generation shouldn't produce any)
    df.fillna(0, inplace=True)
    
    # Sort by Date and SKU
    df.sort_values(by=['Date', 'SKU'], inplace=True)
    
    return df
