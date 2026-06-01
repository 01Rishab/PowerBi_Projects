import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# ── STYLE SETUP ───────────────────────────────────────────
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.facecolor": "#0d0f14",
    "axes.facecolor":   "#161a23",
    "axes.edgecolor":   "#2a3045",
    "axes.labelcolor":  "#e8ecf4",
    "xtick.color":      "#7a849e",
    "ytick.color":      "#7a849e",
    "text.color":       "#e8ecf4",
    "grid.color":       "#2a3045",
    "grid.linewidth":   0.5,
})

# Output folder
os.makedirs("reports/charts", exist_ok=True)
print("✅ Setup complete — ready to plot")

# ── CHART 1 · Revenue by Category ────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

categories = ["Clothing", "Accessories", "Footwear", "Outerwear"]
revenues   = [104264, 74200, 36093, 18524]
colors     = ["#f0b429", "#4ecdc4", "#a78bfa", "#e05c5c"]

bars = ax.bar(categories, revenues, color=colors, width=0.5, zorder=3)

for bar, val in zip(bars, revenues):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 800,
        f"${val:,}",
        ha="center", va="bottom",
        fontsize=10, color="#e8ecf4", fontweight="bold"
    )

ax.set_title("Revenue by Category", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Category", fontsize=11)
ax.set_ylabel("Total Revenue (USD)", fontsize=11)
ax.set_ylim(0, 120000)

plt.tight_layout()
plt.savefig("reports/charts/01_category_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 1 saved → reports/charts/01_category_revenue.png")


# ── CHART 2 · Loyalty Tier Distribution ──────────────────
fig, ax = plt.subplots(figsize=(8, 5))

tiers  = ["Regular", "Loyal", "New", "Champion"]
counts = [1181, 1170, 784, 765]
colors = ["#7a849e", "#4ecdc4", "#a78bfa", "#f0b429"]

bars = ax.barh(tiers, counts, color=colors, height=0.5, zorder=3)

for bar, val in zip(bars, counts):
    ax.text(
        bar.get_width() + 15,
        bar.get_y() + bar.get_height() / 2,
        f"{val:,} customers",
        va="center", fontsize=10, color="#e8ecf4"
    )

ax.set_title("Customer Loyalty Tier Distribution", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Number of Customers", fontsize=11)
ax.set_xlim(0, 1400)

plt.tight_layout()
plt.savefig("reports/charts/02_loyalty_tiers.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 2 saved → reports/charts/02_loyalty_tiers.png")

# ── CHART 3 · Seasonal Revenue Trend ─────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

seasons  = ["Spring", "Summer", "Fall", "Winter"]
revenues = [58679, 55777, 60018, 58607]
colors   = ["#4ecdc4", "#f0b429", "#e05c5c", "#a78bfa"]

ax.plot(seasons, revenues, color="#f0b429", linewidth=2.5,
        marker="o", markersize=8, zorder=3)

# Fill area under the line
ax.fill_between(seasons, revenues, alpha=0.15, color="#f0b429")

# Add value labels above each point
for i, (season, val) in enumerate(zip(seasons, revenues)):
    ax.text(i, val + 300, f"${val:,}",
            ha="center", fontsize=10,
            color="#e8ecf4", fontweight="bold")

# Highlight the peak season
ax.annotate("Peak Season",
            xy=(2, 60018),
            xytext=(2.3, 61500),
            fontsize=9, color="#e05c5c",
            arrowprops=dict(arrowstyle="->", color="#e05c5c"))

ax.set_title("Revenue by Season", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Season", fontsize=11)
ax.set_ylabel("Total Revenue (USD)", fontsize=11)
ax.set_ylim(53000, 64000)

plt.tight_layout()
plt.savefig("reports/charts/03_seasonal_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 3 saved → reports/charts/03_seasonal_revenue.png")


# ── CHART 4 · Discount Impact ─────────────────────────────
fig, ax1 = plt.subplots(figsize=(8, 5))

labels     = ["No Discount", "Discount Applied"]
avg_spend  = [60.13, 59.28]
avg_rating = [3.76, 3.74]
x          = [0, 1]
colors     = ["#4ecdc4", "#e05c5c"]

# Bar chart for avg spend
bars = ax1.bar(x, avg_spend, color=colors, width=0.4, zorder=3)
ax1.set_ylabel("Avg Spend (USD)", fontsize=11)
ax1.set_ylim(58, 61)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=11)

for bar, val in zip(bars, avg_spend):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.02,
        f"${val}",
        ha="center", fontsize=11,
        color="#e8ecf4", fontweight="bold"
    )

# Second Y axis for avg rating
ax2 = ax1.twinx()
ax2.plot(x, avg_rating, color="#f0b429", linewidth=2.5,
         marker="o", markersize=8, zorder=4)
ax2.set_ylabel("Avg Rating", fontsize=11, color="#f0b429")
ax2.set_ylim(3.5, 4.0)
ax2.tick_params(axis="y", colors="#f0b429")

for i, val in enumerate(avg_rating):
    ax2.text(i, val + 0.01, f"{val} stars",
             ha="center", fontsize=10, color="#f0b429")

ax1.set_title("Discount Impact on Spend & Satisfaction",
              fontsize=14, fontweight="bold", pad=15)

plt.tight_layout()
plt.savefig("reports/charts/04_discount_impact.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 4 saved → reports/charts/04_discount_impact.png")

# ── CHART 5 · Age Group Revenue ───────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

age_groups = ["18-25", "26-35", "36-45", "46-55", "56-70"]
revenues   = [34630, 44342, 43234, 45619, 65256]
discounts  = [43.3, 43.5, 41.4, 43.3, 43.3]
colors     = ["#a78bfa", "#4ecdc4", "#f0b429", "#e05c5c", "#34d399"]

bars = ax.bar(age_groups, revenues, color=colors, width=0.5, zorder=3)

for bar, rev, disc in zip(bars, revenues, discounts):
    # Revenue label on top
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 500,
        f"${rev:,}",
        ha="center", fontsize=9,
        color="#e8ecf4", fontweight="bold"
    )
    # Discount % inside bar
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        f"{disc}%\ndisc",
        ha="center", fontsize=8,
        color="#0d0f14", fontweight="bold"
    )

ax.set_title("Revenue by Age Group (with Discount Usage %)",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Total Revenue (USD)", fontsize=11)
ax.set_ylim(0, 75000)

plt.tight_layout()
plt.savefig("reports/charts/05_age_group_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 5 saved → reports/charts/05_age_group_revenue.png")

# ── CHART 6 · Payment Method Spend ───────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

methods   = ["Debit Card", "Credit Card", "Bank Transfer", "Cash", "PayPal", "Venmo"]
avg_spend = [60.92, 60.07, 59.71, 59.70, 59.25, 58.95]
colors    = ["#f0b429", "#4ecdc4", "#7a849e", "#a78bfa", "#e05c5c", "#34d399"]

bars = ax.barh(methods, avg_spend, color=colors, height=0.5, zorder=3)

for bar, val in zip(bars, avg_spend):
    ax.text(
        bar.get_width() - 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"${val}",
        va="center", ha="right",
        fontsize=10, color="#0d0f14", fontweight="bold"
    )

# Add a vertical reference line at overall average
ax.axvline(x=59.76, color="#e8ecf4", linewidth=1.5,
           linestyle="--", alpha=0.6, zorder=2)
ax.text(59.76, 5.6, "Avg $59.76",
        fontsize=8, color="#e8ecf4", ha="center")

ax.set_title("Avg Spend by Payment Method",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Average Spend (USD)", fontsize=11)
ax.set_xlim(58, 62)

plt.tight_layout()
plt.savefig("reports/charts/06_payment_spend.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 6 saved → reports/charts/06_payment_spend.png")


# ── CHART 7 · Shipping vs Satisfaction ───────────────────
fig, ax = plt.subplots(figsize=(9, 5))

shipping  = ["Standard", "Express", "2-Day", "Next Day Air", "Free Ship", "Store Pickup"]
ratings   = [3.819, 3.774, 3.766, 3.720, 3.717, 3.707]
colors    = ["#f0b429" if r == max(ratings) else
             "#e05c5c" if r == min(ratings) else
             "#4ecdc4" for r in ratings]

bars = ax.bar(shipping, ratings, color=colors, width=0.5, zorder=3)

for bar, val in zip(bars, ratings):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.002,
        f"{val}",
        ha="center", fontsize=10,
        color="#e8ecf4", fontweight="bold"
    )

# Reference line at average rating
avg = sum(ratings) / len(ratings)
ax.axhline(y=avg, color="#e8ecf4", linewidth=1.5,
           linestyle="--", alpha=0.6)
ax.text(5.4, avg + 0.002, f"Avg {avg:.3f}",
        fontsize=8, color="#e8ecf4")

ax.set_title("Shipping Type vs Customer Satisfaction",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Shipping Type", fontsize=11)
ax.set_ylabel("Avg Review Rating", fontsize=11)
ax.set_ylim(3.65, 3.87)

plt.tight_layout()
plt.savefig("reports/charts/07_shipping_satisfaction.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 7 saved → reports/charts/07_shipping_satisfaction.png")


# ── CHART 8 · Gender x Category Heatmap ──────────────────
import numpy as np

fig, ax = plt.subplots(figsize=(8, 5))

categories = ["Clothing", "Accessories", "Footwear", "Outerwear"]
genders    = ["Female", "Male"]
data       = [
    [33636, 23819, 11835, 5901],   # Female
    [70628, 50381, 24258, 12623],  # Male
]

im = ax.imshow(data, cmap="YlOrRd", aspect="auto")

# Add value labels inside each cell
for i in range(len(genders)):
    for j in range(len(categories)):
        ax.text(j, i, f"${data[i][j]:,}",
                ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="#0d0f14")

ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, fontsize=11)
ax.set_yticks(range(len(genders)))
ax.set_yticklabels(genders, fontsize=11)

plt.colorbar(im, ax=ax, label="Revenue (USD)")
ax.set_title("Revenue Heatmap — Gender x Category",
             fontsize=14, fontweight="bold", pad=15)

plt.tight_layout()
plt.savefig("reports/charts/08_gender_category_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 8 saved → reports/charts/08_gender_category_heatmap.png")

print("\n✅ All 8 charts saved → reports/charts/")