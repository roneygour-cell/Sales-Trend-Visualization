# ============================================================
# Task: Sales Trend Visualization
# Internship: CodTech IT Solutions - Data Analytics
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Styling ──────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.facecolor": "#f9f9f9",
    "axes.facecolor":   "#ffffff",
    "font.family":      "DejaVu Sans",
})

# ── 1. Load Data ─────────────────────────────────────────────
df = pd.read_csv("sales_data.csv", parse_dates=["Date"])

# Derived columns
df["Month"]       = df["Date"].dt.to_period("M")
df["Month_Name"]  = df["Date"].dt.strftime("%b %Y")
df["Month_Num"]   = df["Date"].dt.month
df["Quarter"]     = df["Date"].dt.to_period("Q")

print("Dataset Shape :", df.shape)
print("\nFirst 5 rows:\n", df.head())
print("\nData Types:\n", df.dtypes)
print("\nBasic Stats:\n", df[["Quantity", "Unit_Price", "Total_Sales"]].describe())

# ── 2. Aggregations ──────────────────────────────────────────
monthly_sales  = df.groupby("Month")["Total_Sales"].sum().reset_index()
category_sales = df.groupby("Category")["Total_Sales"].sum().reset_index()
region_sales   = df.groupby("Region")["Total_Sales"].sum().reset_index()
quarterly_sales = df.groupby("Quarter")["Total_Sales"].sum().reset_index()
cat_month      = df.groupby(["Month", "Category"])["Total_Sales"].sum().unstack(fill_value=0)

monthly_sales["Month_Label"] = monthly_sales["Month"].astype(str)

# ── 3. Plot Layout ───────────────────────────────────────────
fig = plt.figure(figsize=(20, 22))
fig.suptitle("Sales Trend Analysis — 2024\nCodTech IT Solutions Internship | Task 1",
             fontsize=18, fontweight="bold", y=0.98, color="#2c2c2c")

# colour palette
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52",
           "#8172B2", "#937860", "#DA8BC3", "#8C8C8C"]

fmt = mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.1f}L")

# ─── Chart 1: Monthly Sales Trend (Line) ────────────────────
ax1 = fig.add_subplot(3, 2, 1)
ax1.plot(monthly_sales["Month_Label"], monthly_sales["Total_Sales"],
         marker="o", color="#4C72B0", linewidth=2.5, markersize=7)
ax1.fill_between(range(len(monthly_sales)), monthly_sales["Total_Sales"],
                 alpha=0.15, color="#4C72B0")
ax1.set_title("Monthly Sales Trend", fontsize=13, fontweight="bold")
ax1.set_xlabel("Month")
ax1.set_ylabel("Total Sales (₹)")
ax1.yaxis.set_major_formatter(fmt)
ax1.set_xticks(range(len(monthly_sales)))
ax1.set_xticklabels(monthly_sales["Month_Label"], rotation=45, ha="right", fontsize=8)
ax1.tick_params(axis="y", labelsize=9)

# ─── Chart 2: Sales by Category (Bar) ───────────────────────
ax2 = fig.add_subplot(3, 2, 2)
bars = ax2.bar(category_sales["Category"], category_sales["Total_Sales"],
               color=PALETTE[:len(category_sales)], edgecolor="white", linewidth=0.8)
ax2.set_title("Sales by Category", fontsize=13, fontweight="bold")
ax2.set_xlabel("Category")
ax2.set_ylabel("Total Sales (₹)")
ax2.yaxis.set_major_formatter(fmt)
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10000,
             f"₹{bar.get_height()/1e5:.1f}L", ha="center", va="bottom", fontsize=9, fontweight="bold")

# ─── Chart 3: Sales by Region (Pie) ─────────────────────────
ax3 = fig.add_subplot(3, 2, 3)
wedges, texts, autotexts = ax3.pie(
    region_sales["Total_Sales"],
    labels=region_sales["Region"],
    autopct="%1.1f%%",
    colors=PALETTE[:len(region_sales)],
    startangle=140,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(10)
    at.set_fontweight("bold")
ax3.set_title("Sales Distribution by Region", fontsize=13, fontweight="bold")

# ─── Chart 4: Quarterly Sales (Grouped Bar) ──────────────────
ax4 = fig.add_subplot(3, 2, 4)
q_labels = quarterly_sales["Quarter"].astype(str)
q_colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
ax4.bar(q_labels, quarterly_sales["Total_Sales"],
        color=q_colors, edgecolor="white", linewidth=0.8, width=0.5)
ax4.set_title("Quarterly Sales Performance", fontsize=13, fontweight="bold")
ax4.set_xlabel("Quarter")
ax4.set_ylabel("Total Sales (₹)")
ax4.yaxis.set_major_formatter(fmt)
for i, (q, val) in enumerate(zip(q_labels, quarterly_sales["Total_Sales"])):
    ax4.text(i, val + 20000, f"₹{val/1e5:.1f}L",
             ha="center", va="bottom", fontsize=10, fontweight="bold")

# ─── Chart 5: Category Sales Over Months (Stacked Area) ─────
ax5 = fig.add_subplot(3, 2, 5)
month_labels = [str(m) for m in cat_month.index]
ax5.stackplot(range(len(month_labels)), [cat_month[col] for col in cat_month.columns],
              labels=cat_month.columns, colors=PALETTE[:len(cat_month.columns)], alpha=0.85)
ax5.set_title("Category-wise Monthly Sales (Stacked Area)", fontsize=13, fontweight="bold")
ax5.set_xlabel("Month")
ax5.set_ylabel("Total Sales (₹)")
ax5.yaxis.set_major_formatter(fmt)
ax5.set_xticks(range(len(month_labels)))
ax5.set_xticklabels(month_labels, rotation=45, ha="right", fontsize=7)
ax5.legend(loc="upper left", fontsize=8, framealpha=0.7)

# ─── Chart 6: Top Products by Revenue (Horizontal Bar) ───────
ax6 = fig.add_subplot(3, 2, 6)
product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=True)
colors_bar = [PALETTE[i % len(PALETTE)] for i in range(len(product_sales))]
ax6.barh(product_sales.index, product_sales.values,
         color=colors_bar, edgecolor="white", linewidth=0.8)
ax6.set_title("Product-wise Total Revenue", fontsize=13, fontweight="bold")
ax6.set_xlabel("Total Sales (₹)")
ax6.xaxis.set_major_formatter(fmt)
for i, val in enumerate(product_sales.values):
    ax6.text(val + 5000, i, f"₹{val/1e5:.1f}L", va="center", fontsize=8, fontweight="bold")

# ── Final Layout & Save ──────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("sales_trend_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as 'sales_trend_analysis.png'")

# ── 4. Summary Statistics ────────────────────────────────────
print("\n" + "="*50)
print("SALES SUMMARY REPORT")
print("="*50)
print(f"Total Revenue         : ₹{df['Total_Sales'].sum():,.0f}")
print(f"Total Orders          : {len(df)}")
print(f"Average Order Value   : ₹{df['Total_Sales'].mean():,.0f}")
print(f"Best Month            : {monthly_sales.loc[monthly_sales['Total_Sales'].idxmax(), 'Month_Label']}")
print(f"Top Category          : {category_sales.loc[category_sales['Total_Sales'].idxmax(), 'Category']}")
print(f"Top Region            : {region_sales.loc[region_sales['Total_Sales'].idxmax(), 'Region']}")
print(f"Top Product           : {df.groupby('Product')['Total_Sales'].sum().idxmax()}")
print("="*50)
