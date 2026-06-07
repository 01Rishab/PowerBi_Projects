import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ── STEP 1: DATA UNDERSTANDING ─────────────────────────────────

# Load the data
df = pd.read_csv("sales_data.csv")

# 1. Shape - how many rows and columns?
print("Shape:", df.shape)

# 2. Column names and data types
print("\nInfo:")
print(df.info())

# 3. Statistical summary of numeric columns
print("\nDescribe:")
print(df.describe())

# 4. Check for null values
print("\nNull values per column:")
print(df.isnull().sum())

# 5. Preview first 5 rows
print("\nFirst 5 rows:")
print(df.head())


# ── STEP 2: DATA CLEANING ──────────────────────────────────────

# 1. Convert Order_Date from text to proper date format
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
print("\nOrder_Date dtype after conversion:", df['Order_Date'].dtype)

# 2. Standardize text columns - strip spaces, fix casing
for col in ['Category', 'City', 'Region', 'Sales_Channel', 'Customer_Segment', 'Payment_Method', 'Return_Flag']:
    df[col] = df[col].str.strip().str.title()

# Fix SME casing - .title() made it 'Sme' which is wrong
df['Customer_Segment'] = df['Customer_Segment'].replace('Sme', 'SME')

# Check unique values to confirm everything is clean
print("\nUnique Categories:", df['Category'].unique())
print("Unique Cities:", df['City'].unique())
print("Unique Regions:", df['Region'].unique())
print("Unique Sales Channels:", df['Sales_Channel'].unique())
print("Unique Customer Segments:", df['Customer_Segment'].unique())
print("Unique Return Flags:", df['Return_Flag'].unique())

# 3. Spot-check: verify Total_Revenue_INR = Quantity x Unit_Price_INR
df['Revenue_Check'] = (df['Quantity'] * df['Unit_Price_INR']).round(2)
mismatch = df[df['Revenue_Check'] != df['Total_Revenue_INR'].round(2)]
print("\nRevenue mismatches:", len(mismatch))

# 4. Create a new column: Revenue set to 0 for returned orders
df['Net_Revenue_INR'] = df.apply(
    lambda row: 0 if row['Return_Flag'] == 'Yes' else row['Total_Revenue_INR'],
    axis=1
)
print("\nNet Revenue column created. Sample:")
print(df[['Order_ID', 'Total_Revenue_INR', 'Return_Flag', 'Net_Revenue_INR']].head(10))

# 5. Decision on Customer_Rating nulls - we leave them as NaN
# We will DROP nulls only when doing rating-specific analysis
# For revenue analysis we keep all 1000 rows
print("\nFinal shape after cleaning:", df.shape)
print("Cleaning complete.")


# ── STEP 3: EDA ────────────────────────────────────────────────

sns.set_theme(style="whitegrid")

# ── 3.1 REVENUE & SALES TRENDS ─────────────────────────────────

# Total revenue for FY2024
total_revenue = df['Total_Revenue_INR'].sum()
total_orders = df['Order_ID'].nunique()
avg_order_value = df['Total_Revenue_INR'].mean()

print("\n" + "=" * 45)
print("HIGH-LEVEL SUMMARY")
print("=" * 45)
print(f"Total Revenue FY2024 : ₹{total_revenue:,.0f}")
print(f"Total Orders         : {total_orders}")
print(f"Avg Order Value      : ₹{avg_order_value:,.0f}")

# Monthly revenue trend
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
monthly_revenue = df.groupby('Month')['Total_Revenue_INR'].sum()
monthly_revenue = monthly_revenue.reindex(month_order).dropna()

plt.figure(figsize=(12, 5))
plt.plot(monthly_revenue.index, monthly_revenue.values, marker='o', color='steelblue', linewidth=2)
plt.title('Monthly Revenue Trend - FY2024')
plt.xlabel('Month')
plt.ylabel('Total Revenue (INR)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_revenue_trend.png', dpi=150)
plt.close()
print("\nMonthly Revenue:")
print(monthly_revenue.apply(lambda x: f"₹{x:,.0f}"))

# Quarterly performance
quarterly_revenue = df.groupby('Quarter')['Total_Revenue_INR'].sum().sort_index()
print("\nQuarterly Revenue:")
print(quarterly_revenue.apply(lambda x: f"₹{x:,.0f}"))

plt.figure(figsize=(7, 4))
bars = plt.bar(quarterly_revenue.index, quarterly_revenue.values, color=['#2196F3','#4CAF50','#FF9800','#E91E63'])
plt.title('Revenue by Quarter - FY2024')
plt.xlabel('Quarter')
plt.ylabel('Total Revenue (INR)')
for bar, val in zip(bars, quarterly_revenue.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
             f'₹{val:,.0f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('quarterly_revenue.png', dpi=150)
plt.close()

# Revenue by Category
category_revenue = df.groupby('Category')['Total_Revenue_INR'].sum().sort_values(ascending=False)
print("\nRevenue by Category:")
print(category_revenue.apply(lambda x: f"₹{x:,.0f}"))

plt.figure(figsize=(7, 4))
bars = plt.bar(category_revenue.index, category_revenue.values, color=['#3F51B5','#009688','#FF5722'])
plt.title('Revenue by Category - FY2024')
plt.xlabel('Category')
plt.ylabel('Total Revenue (INR)')
for bar, val in zip(bars, category_revenue.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30000,
             f'₹{val:,.0f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('category_revenue.png', dpi=150)
plt.close()


# ── 3.2 PRODUCT PERFORMANCE ────────────────────────────────────

# Top 5 and Bottom 5 products by revenue
product_revenue = df.groupby('Product_Name')['Total_Revenue_INR'].sum().sort_values(ascending=False)
top5 = product_revenue.head(5)
bottom5 = product_revenue.tail(5)

print("\nTop 5 Products by Revenue:")
print(top5.apply(lambda x: f"₹{x:,.0f}"))
print("\nBottom 5 Products by Revenue:")
print(bottom5.apply(lambda x: f"₹{x:,.0f}"))

# Discount vs Revenue per unit analysis
discount_analysis = df.groupby('Discount_Percent').agg(
    Avg_Unit_Price=('Unit_Price_INR', 'mean'),
    Total_Quantity=('Quantity', 'sum'),
    Total_Revenue=('Total_Revenue_INR', 'sum'),
    Order_Count=('Order_ID', 'count')
).reset_index()
print("\nDiscount Analysis:")
print(discount_analysis)

# Return rate by category
return_by_category = df.groupby('Category')['Return_Flag'].apply(
    lambda x: (x == 'Yes').sum() / len(x) * 100
).round(2)
print("\nReturn Rate by Category (%):")
print(return_by_category)


# ── 3.3 REGIONAL & CITY ANALYSIS ───────────────────────────────

# Revenue by Region
region_revenue = df.groupby('Region')['Total_Revenue_INR'].sum().sort_values(ascending=False)
print("\nRevenue by Region:")
print(region_revenue.apply(lambda x: f"₹{x:,.0f}"))

# Revenue by City
city_revenue = df.groupby('City')['Total_Revenue_INR'].sum().sort_values(ascending=False)
print("\nRevenue by City:")
print(city_revenue.apply(lambda x: f"₹{x:,.0f}"))

# City x Category heatmap
city_category = df.pivot_table(index='City', columns='Category',
                                values='Total_Revenue_INR', aggfunc='sum')
plt.figure(figsize=(9, 6))
sns.heatmap(city_category, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('Revenue Heatmap: City vs Category')
plt.tight_layout()
plt.savefig('city_category_heatmap.png', dpi=150)
plt.close()


# ── 3.4 CUSTOMER & CHANNEL INSIGHTS ───────────────────────────

# Revenue and volume by Sales Channel
channel_analysis = df.groupby('Sales_Channel').agg(
    Total_Revenue=('Total_Revenue_INR', 'sum'),
    Total_Orders=('Order_ID', 'count'),
    Avg_Order_Value=('Total_Revenue_INR', 'mean')
).sort_values('Total_Revenue', ascending=False)
print("\nSales Channel Analysis:")
print(channel_analysis)

# Average Order Value by Customer Segment
segment_aov = df.groupby('Customer_Segment')['Total_Revenue_INR'].mean().sort_values(ascending=False)
print("\nAvg Order Value by Customer Segment:")
print(segment_aov.apply(lambda x: f"₹{x:,.0f}"))

# Payment method distribution
payment_counts = df['Payment_Method'].value_counts()
print("\nPayment Method Distribution:")
print(payment_counts)


# ── 3.5 CUSTOMER SATISFACTION ──────────────────────────────────

# Use only rows where rating is available
df_rated = df.dropna(subset=['Customer_Rating'])

# Overall average rating
print(f"\nOverall Avg Rating: {df_rated['Customer_Rating'].mean():.2f} / 5")

# Rating by Category
rating_by_category = df_rated.groupby('Category')['Customer_Rating'].mean().round(2)
print("\nAvg Rating by Category:")
print(rating_by_category)

# Rating by City
rating_by_city = df_rated.groupby('City')['Customer_Rating'].mean().round(2).sort_values(ascending=False)
print("\nAvg Rating by City:")
print(rating_by_city)

# Correlation: Discount vs Rating
correlation = df_rated[['Discount_Percent', 'Customer_Rating']].corr()
print("\nCorrelation - Discount vs Rating:")
print(correlation)

print("\nEDA Complete. Charts saved.")

# ── STEP 4: INSIGHT GENERATION ─────────────────────────────────

print("\n" + "=" * 55)
print("STEP 4: KEY INSIGHTS")
print("=" * 55)

insights = """
REVENUE & TRENDS
- Total FY2024 revenue: ₹5.08 crore from 1,000 orders
- Q4 is the strongest quarter (₹1.65 cr), driven by October
  alone (₹77.5 lakh) — likely festive season demand spike
- Q3 is the weakest (₹1.05 cr) — July to September needs
  a targeted sales push next year

PRODUCT PERFORMANCE
- Laptop Pro 15 generates ₹2.3 crore — 45% of total revenue
  from a single product. This is a concentration risk.
- Bottom 5 products are all Stationery — combined revenue
  under ₹6.5 lakh for the full year
- Discount strategy is ineffective: 0% discount orders
  outperform 20% discount orders in total revenue
- Stationery has the highest return rate (7%) despite being
  the lowest revenue category — poor value for business

REGIONAL & CITY
- South region contributes ₹1.97 crore — nearly 39% of
  total revenue. Heavy geographic concentration
- Chennai is the top city (₹76 lakh), Delhi is the weakest
  (₹55 lakh) despite being a major metro
- Northeast (Guwahati) performs on par with East (Kolkata)
  which is unexpected and positive for a Tier-2 city

CHANNEL & CUSTOMER
- All 3 channels are nearly equal in revenue — no single
  channel dominates, which is healthy diversification
- Individual customers have higher AOV (₹53,541) than
  Enterprise (₹51,587) — investigate if Enterprise deals
  include bulk discounts that suppress per-order value
- Cash is the top payment method (213 orders) — unusual
  for a B2B business. May indicate retail walk-ins

CUSTOMER SATISFACTION
- Overall rating of 3.01/5 is below average — improvement
  needed across the board
- Bangalore has the lowest avg rating (2.85) — delivery,
  product quality, or service issues need investigation
- Discount level has near-zero correlation with rating (0.02)
  — customers don't rate better just because they got a deal
"""

print(insights)
print("Insights complete.")


# ── STEP 5: DASHBOARD ──────────────────────────────────────────

fig, axes = plt.subplots(3, 2, figsize=(18, 20))
fig.suptitle('FY2024 Sales Performance Dashboard\nB2B Office Supplies', 
             fontsize=18, fontweight='bold', y=0.98)

# ── Chart 1: Monthly Revenue Trend ─────────────────────────────
ax1 = axes[0, 0]
ax1.plot(monthly_revenue.index, monthly_revenue.values, 
         marker='o', color='steelblue', linewidth=2.5)
ax1.fill_between(range(len(monthly_revenue)), monthly_revenue.values, 
                 alpha=0.1, color='steelblue')
ax1.set_title('Monthly Revenue Trend', fontweight='bold')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue (INR)')
ax1.set_xticks(range(len(monthly_revenue)))
ax1.set_xticklabels(monthly_revenue.index, rotation=45, ha='right')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/100000:.1f}L'))

# ── Chart 2: Revenue by Quarter ─────────────────────────────────
ax2 = axes[0, 1]
colors_q = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']
bars = ax2.bar(quarterly_revenue.index, quarterly_revenue.values, color=colors_q, width=0.5)
ax2.set_title('Revenue by Quarter', fontweight='bold')
ax2.set_xlabel('Quarter')
ax2.set_ylabel('Revenue (INR)')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/100000:.1f}L'))
for bar, val in zip(bars, quarterly_revenue.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100000,
             f'₹{val/100000:.1f}L', ha='center', fontsize=9, fontweight='bold')

# ── Chart 3: Revenue by Category ───────────────────────────────
ax3 = axes[1, 0]
colors_c = ['#3F51B5', '#009688', '#FF5722']
wedges, texts, autotexts = ax3.pie(
    category_revenue.values,
    labels=category_revenue.index,
    autopct='%1.1f%%',
    colors=colors_c,
    startangle=90,
    pctdistance=0.75
)
for text in autotexts:
    text.set_fontweight('bold')
ax3.set_title('Revenue Share by Category', fontweight='bold')

# ── Chart 4: Top 5 Products ─────────────────────────────────────
ax4 = axes[1, 1]
top5_sorted = top5.sort_values()
bars = ax4.barh(top5_sorted.index, top5_sorted.values, color='#1976D2')
ax4.set_title('Top 5 Products by Revenue', fontweight='bold')
ax4.set_xlabel('Revenue (INR)')
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/100000:.0f}L'))
for bar, val in zip(bars, top5_sorted.values):
    ax4.text(bar.get_width() + 20000, bar.get_y() + bar.get_height()/2,
             f'₹{val/100000:.1f}L', va='center', fontsize=9)

# ── Chart 5: Revenue by City ────────────────────────────────────
ax5 = axes[2, 0]
city_colors = ['#388E3C' if v == city_revenue.max() else 
               '#F44336' if v == city_revenue.min() else 
               '#90A4AE' for v in city_revenue.values]
bars = ax5.bar(city_revenue.index, city_revenue.values, color=city_colors)
ax5.set_title('Revenue by City  (Green=Top, Red=Bottom)', fontweight='bold')
ax5.set_xlabel('City')
ax5.set_ylabel('Revenue (INR)')
ax5.set_xticklabels(city_revenue.index, rotation=30, ha='right')
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/100000:.0f}L'))

# ── Chart 6: Return Rate by Category ───────────────────────────
ax6 = axes[2, 1]
bars = ax6.bar(return_by_category.index, return_by_category.values,
               color=['#FF7043', '#FFA726', '#FFCA28'], width=0.4)
ax6.set_title('Return Rate by Category (%)', fontweight='bold')
ax6.set_xlabel('Category')
ax6.set_ylabel('Return Rate (%)')
ax6.set_ylim(0, 12)
for bar, val in zip(bars, return_by_category.values):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val}%', ha='center', fontsize=11, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("Dashboard saved as dashboard.png")