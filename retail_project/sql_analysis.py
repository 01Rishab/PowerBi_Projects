import sqlite3
import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# Create SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("data/retail.db")

# Load dataframe into a SQL table called 'transactions'
df.to_sql("transactions", conn, if_exists="replace", index=False)

print("✅ Database created → data/retail.db")
print(f"   Rows loaded: {len(df):,}")

# Helper function — runs a query and prints results neatly
def run_query(title, sql):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))
    return result

run_query(
    "Q1 · Revenue & Volume by Category",
    """
    SELECT
        category,
        COUNT(*)                           AS total_orders,
        SUM(purchase_amount_usd)           AS total_revenue,
        ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value,
        ROUND(AVG(review_rating), 2)       AS avg_rating
    FROM transactions
    GROUP BY category
    ORDER BY total_revenue DESC
    """
)

run_query(
    "Q2 · Loyalty Tier Performance",
    """
    SELECT
        loyalty_tier,
        COUNT(*)                               AS customers,
        SUM(purchase_amount_usd)               AS total_revenue,
        ROUND(AVG(purchase_amount_usd), 2)     AS avg_spend,
        ROUND(AVG(review_rating), 2)           AS avg_rating,
        SUM(CASE WHEN subscription_status = 1
            THEN 1 ELSE 0 END)                 AS subscribers,
        ROUND(100.0 * SUM(CASE WHEN subscription_status = 1
            THEN 1 ELSE 0 END) / COUNT(*), 1)  AS sub_pct
    FROM transactions
    GROUP BY loyalty_tier
    ORDER BY avg_spend DESC
    """
)

run_query(
    "Q3 · Discount Impact on Spend & Satisfaction",
    """
    SELECT
        discount_applied,
        promo_code_used,
        COUNT(*)                             AS orders,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_spend,
        SUM(purchase_amount_usd)             AS total_revenue,
        ROUND(AVG(review_rating), 2)         AS avg_rating
    FROM transactions
    GROUP BY discount_applied, promo_code_used
    ORDER BY avg_spend DESC
    """
)

run_query(
    "Q4 · Seasonal Revenue Trends",
    """
    SELECT
        season,
        COUNT(*)                             AS orders,
        SUM(purchase_amount_usd)             AS revenue,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_order,
        ROUND(AVG(review_rating), 2)         AS avg_rating,
        SUM(CASE WHEN discount_applied = 1
            THEN 1 ELSE 0 END)               AS discount_orders
    FROM transactions
    GROUP BY season
    ORDER BY season_order
    """
)

run_query(
    "Q5 · Top 10 Products by Revenue",
    """
    SELECT
        item_purchased,
        category,
        COUNT(*)                             AS orders,
        SUM(purchase_amount_usd)             AS revenue,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_price,
        ROUND(AVG(review_rating), 2)         AS avg_rating
    FROM transactions
    GROUP BY item_purchased
    ORDER BY revenue DESC
    LIMIT 10
    """
)

run_query(
    "Q6 · Payment Method Preferences",
    """
    SELECT
        payment_method,
        COUNT(*)                                        AS orders,
        ROUND(100.0 * COUNT(*) / 
            (SELECT COUNT(*) FROM transactions), 1)     AS pct_share,
        ROUND(AVG(purchase_amount_usd), 2)              AS avg_spend,
        ROUND(AVG(review_rating), 2)                    AS avg_rating
    FROM transactions
    GROUP BY payment_method
    ORDER BY orders DESC
    """
)

run_query(
    "Q7 · Age Group Purchasing Behaviour",
    """
    SELECT
        age_group,
        COUNT(*)                             AS orders,
        SUM(purchase_amount_usd)             AS revenue,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_spend,
        ROUND(AVG(review_rating), 2)         AS avg_rating,
        SUM(CASE WHEN any_discount_used = 1
            THEN 1 ELSE 0 END)               AS discount_users,
        ROUND(100.0 * SUM(CASE WHEN any_discount_used = 1
            THEN 1 ELSE 0 END) / COUNT(*), 1) AS discount_pct
    FROM transactions
    GROUP BY age_group
    ORDER BY age_group
    """
)

run_query(
    "Q8 · Shipping Type vs Customer Satisfaction",
    """
    SELECT
        shipping_type,
        COUNT(*)                             AS orders,
        ROUND(AVG(review_rating), 3)         AS avg_rating,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_spend
    FROM transactions
    GROUP BY shipping_type
    ORDER BY avg_rating DESC
    """
)

run_query(
    "Q9 · Gender x Category Spending Matrix",
    """
    SELECT
        gender,
        category,
        COUNT(*)                             AS orders,
        SUM(purchase_amount_usd)             AS revenue,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_spend
    FROM transactions
    GROUP BY gender, category
    ORDER BY gender, revenue DESC
    """
)

run_query(
    "Q10 · High Value Customer Profile (Top 20% Spenders)",
    """
    WITH ranked AS (
        SELECT *,
            NTILE(5) OVER (ORDER BY purchase_amount_usd DESC) AS spend_quintile
        FROM transactions
    )
    SELECT
        age_group,
        gender,
        loyalty_tier,
        payment_method,
        COUNT(*)                             AS customers,
        ROUND(AVG(purchase_amount_usd), 2)   AS avg_spend,
        ROUND(AVG(review_rating), 2)         AS avg_rating
    FROM ranked
    WHERE spend_quintile = 1
    GROUP BY age_group, gender, loyalty_tier, payment_method
    ORDER BY customers DESC
    LIMIT 10
    """
)

conn.close()
print("\n✅ SQL Analysis Complete. Database closed.")