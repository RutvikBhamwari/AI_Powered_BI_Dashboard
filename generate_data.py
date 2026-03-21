import pandas as pd
import numpy as np
import random

# Set seed for reproducible results
random.seed(42)
np.random.seed(42)

products = ['Laptop', 'Phone', 'Tablet']
regions = ['North', 'South', 'East', 'West']

# Product base prices
prices = {'Laptop': 1500, 'Phone': 500, 'Tablet': 400}

# Generate 6 months of daily data
dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')

rows = []
for date in dates:
    # 3-5 transactions per day
    for _ in range(random.randint(3, 5)):
        product = random.choice(products)
        region = random.choice(regions)
        
        # Units sold varies by product and adds some randomness
        base_units = {'Laptop': 30, 'Phone': 100, 'Tablet': 70}
        units = max(1, int(np.random.normal(base_units[product], 15)))
        
        # Revenue = units * price with slight variation
        price_variation = np.random.uniform(0.95, 1.05)
        revenue = int(units * prices[product] * price_variation)
        
        # Returns = small percentage of units
        return_rate = {'Laptop': 0.02, 'Phone': 0.04, 'Tablet': 0.06}
        returns = max(0, int(np.random.poisson(units * return_rate[product])))
        
        rows.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Product': product,
            'Region': region,
            'Units_Sold': units,
            'Revenue': revenue,
            'Returns': returns
        })

df = pd.DataFrame(rows)
df.to_csv('sales_data_6months.csv', index=False)
print(f"Generated {len(df)} rows of sales data")
print(df.head(10))