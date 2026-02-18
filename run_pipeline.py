import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from src.generate import generate_inventory_data
from src.clean import clean_data
from src.features import engineer_features
from src.forecast import calculate_safety_stock_rop
from src.recommend import generate_recommendations

def run_pipeline():
    print("Starting Inventory Replenishment Pipeline...")
    
    # 1. Generate Data
    print("Generating synthetic data...")
    df_raw = generate_inventory_data()
    # Save raw data
    df_raw.to_csv('data/raw/inventory_data_raw.csv', index=False)
    
    # 2. Clean Data
    print("Cleaning data...")
    df_clean = clean_data(df_raw)
    
    # 3. Feature Engineering
    print("Engineering features...")
    df_features = engineer_features(df_clean)
    
    # 4. Forecast & Safety Stock
    print("Calculating safety stock and reorder points...")
    df_forecast = calculate_safety_stock_rop(df_features)
    
    # 5. Recommendations
    print("Generating recommendations...")
    recommendations_df, to_order_df = generate_recommendations(df_forecast)
    
    # Save processed data and recommendations
    df_forecast.to_csv('data/processed/inventory_data_processed.csv', index=False)
    to_order_df.to_csv('outputs/replenishment_recommendations.csv', index=False)
    print(f"Recommendations saved to outputs/replenishment_recommendations.csv ({len(to_order_df)} SKUs to order)")
    
    # 6. Generate Charts
    print("Generating charts...")
    generate_charts(to_order_df, df_forecast)
    
    print("Pipeline completed successfully!")

def generate_charts(to_order_df, full_df):
    # Chart 1: Top 10 SKUs by Stockout Risk
    plt.figure(figsize=(10, 6))
    top_10_risk = to_order_df.nlargest(10, 'Stockout_Risk')
    sns.barplot(data=top_10_risk, x='Stockout_Risk', y='SKU', hue='SKU', palette='viridis', legend=False)
    plt.title('Top 10 SKUs by Stockout Risk (Reorder Point - On Hand)')
    plt.xlabel('Stockout Risk Units')
    plt.tight_layout()
    plt.savefig('outputs/figures/top_10_stockout_risk.png')
    plt.close()
    
    # Chart 2: Demand Trend for a specific SKU
    # Pick a random SKU to show
    example_sku = full_df['SKU'].unique()[0]
    sku_data = full_df[full_df['SKU'] == example_sku]
    
    plt.figure(figsize=(12, 6))
    plt.plot(sku_data['Date'], sku_data['Sales'], label='Daily Sales', alpha=0.5)
    plt.plot(sku_data['Date'], sku_data['Avg_Daily_Demand'], label='Avg Daily Demand (14d)', linewidth=2)
    plt.plot(sku_data['Date'], sku_data['On_Hand'], label='On Hand Inventory', linestyle='--')
    plt.axhline(y=sku_data['Reorder_Point'].iloc[-1], color='r', linestyle=':', label='Current Reorder Point')
    
    plt.title(f'Demand & Inventory Trend for {example_sku}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'outputs/figures/demand_trend_{example_sku}.png')
    plt.close()

if __name__ == "__main__":
    run_pipeline()
