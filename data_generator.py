import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_warehouse_data(rows=500):
    np.random.seed(42)
    start_date = datetime(2023, 1, 1)
    
    data = {
        'Date': [start_date + timedelta(days=i) for i in range(rows)],
        'Product_Category': np.random.choice(['Electronics', 'Apparel', 'Home', 'Toys'], rows),
        'Previous_Stock': np.random.randint(100, 1000, rows),
        'Units_Sold_Last_Week': np.random.randint(50, 400, rows),
        'Promotion_Active': np.random.choice([0, 1], rows, p=[0.7, 0.3]),
        'Inventory_Cost': np.random.uniform(10.0, 500.0, rows)
    }
    
    df = pd.DataFrame(data)
    # Target Demand: Based on previous sales + a random noise factor + promotion impact
    df['Target_Demand'] = (df['Units_Sold_Last_Week'] * 1.2 + 
                           df['Promotion_Active'] * 50 + 
                           np.random.normal(0, 20, rows)).astype(int)
    
    df.to_csv('warehouse_data.csv', index=False)
    print("Random dataset 'warehouse_data.csv' generated.")

if __name__ == "__main__":
    generate_warehouse_data()
