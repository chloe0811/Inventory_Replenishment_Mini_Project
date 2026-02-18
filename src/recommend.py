import pandas as pd

def generate_recommendations(df):
    """
    Generates purchase recommendations based on current inventory levels and reorder points.
    Returns the latest snapshot with recommendations.
    """
    # Get the latest date for each SKU to make current recommendations
    latest_date = df['Date'].max()
    current_status = df[df['Date'] == latest_date].copy()
    
    # Calculate Suggested Order Quantity
    # Logic: If On_Hand < Reorder_Point, order up to a certain level? 
    # Simplified requirement: max(0, reorder_point - current_on_hand)
    # This implies we just want to bring inventory back to the reorder point level, 
    # which is a bit conservative (usually order up to Max), but fits the requirement.
    
    current_status['Suggested_Order_Qty'] = (current_status['Reorder_Point'] - current_status['On_Hand']).clip(lower=0)
    
    # Add a flag for urgency
    current_status['Stockout_Risk'] = current_status['Reorder_Point'] - current_status['On_Hand']
    
    # Select relevance columns
    recommendations = current_status[['Date', 'SKU', 'On_Hand', 'Lead_Time_Days', 
                                      'Avg_Daily_Demand', 'Safety_Stock', 'Reorder_Point', 
                                      'Suggested_Order_Qty', 'Stockout_Risk']]
    
    # Identify items to order
    to_order = recommendations[recommendations['Suggested_Order_Qty'] > 0].sort_values(by='Stockout_Risk', ascending=False)
    
    return recommendations, to_order
