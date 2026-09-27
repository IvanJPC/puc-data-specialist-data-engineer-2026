# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 1,EDA - Business Questions
# MAGIC %md
# MAGIC # EDA — Business Questions
# MAGIC
# MAGIC This notebook aims to answers the **5 business questions** defined in the project README using the Gold-layer star schema tables. All analyses use **PySpark DataFrames** and matplotlib visualizations.
# MAGIC
# MAGIC ### Questions to be answered:
# MAGIC 1. What are the top 10 cities of customers with most orders?
# MAGIC 2. What are the ratings that have the order delivered after the estimated time?
# MAGIC 3. Which categories are top performers each month?
# MAGIC 4. Does the freight value of a product influence ratings or order cancellations?
# MAGIC 5. What is the ranking sales per each category?

# COMMAND ----------

# DBTITLE 1,Python Init
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pyspark.sql import functions as F

# COMMAND ----------

# DBTITLE 1,Q1: Top 10 Cities by Order Count
# Q1: What are the top 10 cities of customers with most orders?


fact_orders = spark.table("puc_data_specialist_de_2026_09.`03-gold`.fact_orders")
dim_customer = spark.table("puc_data_specialist_de_2026_09.`03-gold`.dim_customer")

top_cities_orders = (
    fact_orders
    .join(dim_customer, "customer_key")
    .groupBy("customer_city")
    .agg(F.count("*").alias("order_count"))
    .orderBy(F.col("order_count").desc())
    .limit(10)
    .toPandas()
)

total_orders = fact_orders.join(dim_customer, "customer_key").count()
top_cities_orders['order_pct'] = top_cities_orders['order_count'] / total_orders * 100

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_cities_orders['customer_city'], top_cities_orders['order_pct'], color='steelblue')
ax.set_xlabel('% of Total Orders')
ax.set_title('Q1: Top 10 Cities by % of Total Orders', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for bar in bars:
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f'{bar.get_width():.1f}%', va='center', fontsize=9)
plt.tight_layout()
plt.show()

# COMMAND ----------

# DBTITLE 1,Q2: Delivery Delay vs Review Score
# Q2 -Is there any relation between ratings and delayed delivery?
delay_review = (
    fact_orders
    .filter(
        F.col("review_score").isNotNull() &
        F.col("is_delivery_delayed").isNotNull()
    )
    .groupBy("review_score", "is_delivery_delayed")
    .count()
    .orderBy("review_score", "is_delivery_delayed")
    .toPandas()
)

# Pivot: rows = review_score, columns = on-time vs delayed
pivot_df = delay_review.pivot(
    index='review_score', columns='is_delivery_delayed', values='count'
).fillna(0)
col_map = {col: 'On-time' if col == False else 'Delayed' for col in pivot_df.columns}
pivot_df = pivot_df.rename(columns=col_map)

# Percentage view (delay rate per review score)
pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: grouped bar chart (absolute counts)
x = range(len(pivot_df.index))
width = 0.35
ax1 = axes[0]
ax1.bar([i - width/2 for i in x], pivot_df['On-time'], width, label='On-time', color='#2ecc71')
ax1.bar([i + width/2 for i in x], pivot_df['Delayed'], width, label='Delayed', color='#e74c3c')
ax1.set_xlabel('Review Score')
ax1.set_ylabel('Number of Orders')
ax1.set_title('Delivery Delay by Review Score (Counts)', fontsize=12, fontweight='bold')
ax1.set_xticks(list(x))
ax1.set_xticklabels(pivot_df.index)
ax1.legend()

# Right: 100% stacked bar (delay rate %)
ax2 = axes[1]
ax2.barh(pivot_pct.index, pivot_pct['On-time'], label='On-time', color='#2ecc71')
ax2.barh(pivot_pct.index, pivot_pct['Delayed'], left=pivot_pct['On-time'], label='Delayed', color='#e74c3c')
ax2.set_xlabel('Percentage (%)')
ax2.set_ylabel('Review Score')
ax2.set_title('Delay Rate by Review Score (%)', fontsize=12, fontweight='bold')
ax2.legend(loc='lower right')
ax2.invert_yaxis()
ax2.set_yticks(pivot_pct.index)

plt.tight_layout()
plt.show()

# COMMAND ----------

# DBTITLE 1,Q3: Top Categories per Month
from pyspark.sql.window import Window

# Load additional Gold layer tables
fact_order_items = spark.table("puc_data_specialist_de_2026_09.`03-gold`.fact_order_items")
dim_product = spark.table("puc_data_specialist_de_2026_09.`03-gold`.dim_product")
dim_time = spark.table("puc_data_specialist_de_2026_09.`03-gold`.dim_time")

# ============================================================
# Q3: Which categories are top performers each month?
# ============================================================

# Aggregate sales by month and category
monthly_category = (
    fact_order_items
    .join(dim_product, "product_key")
    .join(dim_time, fact_order_items.purchase_date_key == dim_time.date_key)
    .groupBy("year_month", "product_category_name_clean")
    .agg(
        F.sum("total_value").alias("total_sales"),
        F.count("*").alias("item_count")
    )
)

# Rank categories within each month using window function
window = Window.partitionBy("year_month").orderBy(F.col("total_sales").desc())
top_per_month = (
    monthly_category
    .withColumn("rank", F.row_number().over(window))
    .filter(F.col("rank") <= 3)
    .orderBy("year_month", "rank")
    .select("year_month", "rank", "product_category_name_clean", "total_sales", "item_count")
    .toPandas()
)

print("=== Top 3 Categories per Month ===")
display(top_per_month)

# Line chart: top 5 overall categories — monthly sales trend
top5_categories = (
    monthly_category
    .groupBy("product_category_name_clean")
    .agg(F.sum("total_sales").alias("total"))
    .orderBy(F.col("total").desc())
    .limit(5)
    .select("product_category_name_clean")
    .toPandas()['product_category_name_clean']
    .tolist()
)

monthly_top5 = (
    monthly_category
    .filter(F.col("product_category_name_clean").isin(top5_categories))
    .orderBy("year_month")
    .toPandas()
)

pivot_top5 = monthly_top5.pivot(
    index='year_month', columns='product_category_name_clean', values='total_sales'
).fillna(0)

fig, ax = plt.subplots(figsize=(14, 6))
for col in pivot_top5.columns:
    ax.plot(pivot_top5.index, pivot_top5[col], marker='o', label=col, linewidth=2)
ax.set_xlabel('Year-Month')
ax.set_ylabel('Total Sales (R$)')
ax.set_title('Q3: Top 5 Categories — Monthly Sales Trend', fontsize=14, fontweight='bold')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

# DBTITLE 1,Q4: Freight Value vs Ratings/Cancellations
# ============================================================
# Q4: Does the freight value of a product influence ratings or order cancellations?
# ============================================================

# Part A: Average freight value by review score
freight_by_score = (
    fact_order_items
    .join(fact_orders.select("order_id", "review_score"), "order_id")
    .filter(F.col("review_score").isNotNull())
    .groupBy("review_score")
    .agg(
        F.avg("freight_value").alias("avg_freight"),
        F.avg("total_value").alias("avg_total"),
        F.count("*").alias("item_count")
    )
    .orderBy("review_score")
    .toPandas()
)

# Part B: Average freight value by order status (canceled vs delivered)
freight_by_status = (
    fact_order_items
    .join(fact_orders.select("order_id", "order_status_name"), "order_id")
    .filter(F.col("order_status_name").isin("CANCELED", "DELIVERED"))
    .groupBy("order_status_name")
    .agg(
        F.avg("freight_value").alias("avg_freight"),
        F.avg("total_value").alias("avg_total"),
        F.count("*").alias("item_count")
    )
    .orderBy("order_status_name")
    .toPandas()
)

print("=== Freight Value by Review Score ===")
display(freight_by_score)
print("\n=== Freight Value by Order Status ===")
display(freight_by_status)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Freight by review score
colors = ['#e74c3c', '#e74c3c', '#f39c12', '#2ecc71', '#2ecc71']
ax1 = axes[0]
bars = ax1.bar(freight_by_score['review_score'], freight_by_score['avg_freight'], color=colors)
ax1.set_xlabel('Review Score')
ax1.set_ylabel('Average Freight Value (R$)')
ax1.set_title('Freight Value vs Review Score', fontsize=12, fontweight='bold')
ax1.set_xticks(freight_by_score['review_score'])
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'R$ {bar.get_height():.2f}', ha='center', fontsize=9)

# Right: Freight by order status
# Sort so DELIVERED (green) comes first, CANCELED (red) second
freight_by_status = freight_by_status.sort_values('order_status_name').reset_index(drop=True)
status_colors = ['#2ecc71', '#e74c3c']
ax2 = axes[1]
bars2 = ax2.bar(freight_by_status['order_status_name'], freight_by_status['avg_freight'], color=status_colors)
ax2.set_xlabel('Order Status')
ax2.set_ylabel('Average Freight Value (R$)')
ax2.set_title('Freight Value vs Order Status', fontsize=12, fontweight='bold')
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'R$ {bar.get_height():.2f}', ha='center', fontsize=9)

plt.tight_layout()
plt.show()

# COMMAND ----------

# DBTITLE 1,Q5: Ranking Sales per Category
# ============================================================
# Q5: What is the ranking sales per each category?
# ============================================================
category_sales = (
    fact_order_items
    .join(dim_product, "product_key")
    .groupBy("product_category_name_clean")
    .agg(
        F.sum("total_value").alias("total_sales"),
        F.count("*").alias("item_count"),
        F.avg("total_value").alias("avg_order_value")
    )
    .orderBy(F.col("total_sales").desc())
    .toPandas()
)

# Show top 20 categories
print(f"=== Total Categories: {len(category_sales)} ===")
print("\n=== Top 20 Categories by Total Sales ===")
display(category_sales.head(20))

# Bar chart — top 20 categories
top20 = category_sales.head(20)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(top20['product_category_name_clean'], top20['total_sales'], color='steelblue')
ax.set_xlabel('Total Sales (R$)')
ax.set_title('Q5: Top 20 Categories by Total Sales', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for bar in bars:
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
            f'R$ {int(bar.get_width()):,}', va='center', fontsize=8)
plt.tight_layout()
plt.show()