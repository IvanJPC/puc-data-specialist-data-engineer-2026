# PUC-Data Specialist - Data Engineer
## Student: Ivan J P de Carvalho
### Date: Jul-Oct 2026


For this MVP, this project will be using the Brazil E-Commerce dataset available on: 
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Dataset credit: http://www.olist.com/


> &#9432; **License:** 
> 
> CC BY-NC-SA 4.0 - https://creativecommons.org/licenses/by-nc-sa/4.0/
>
> The use of this dataset in this project is for Non Commercial use only.

The reason behind the use of this dataset:
- It's a well documented dataset containing e-commerce information from 2016 to 2018
- BR e-commerce dataset
- Simple dataset
- A few EDA available in Kaggle for comparative


## Notebooks
Notebooks available in subfolders:

- 00 - Setup Schema and Catalog
    - Create Databricks catalog and schema based on medallion architecture
- 01 - Dataset Import
    - Import of the CSV files from Kaggle
    - Import by Kaggle API
    - Needs API Token set before run
- 02 - Bronze Ingestion
    - Create of Bronze tables 
    - Represent dataset import
    - No business or bigger changes
    - String and Number types only
- 03 - Silver - DEA and Transformations
- 04 - Gold Refinement 
    - Create facts and dims tables - DataMart layer
- 05 - EDA - Business Questions 
    - Business Data Analysis

---

## Business Questions to Answer
```
✅ Q1 - What are the top 10 cities of customers with most orders?
✅ Q2 - Is there any relation between ratings and delayed delivery?
✅ Q3 - Which categories are top performers each month?
✅ Q4 - Does the freight value of a product influenced on ratings or order cancelations?
✅ Q5 - What is the ranking sales per each category?
```

### EDA — Business Questions Answered

The `05 - EDA - Business Questions` notebook answers the 5 business questions defined in this README using the Gold-layer star schema tables with **PySpark DataFrames** and matplotlib visualizations.

### Q1: What are the top 10 cities of customers with most orders?

![Q1](Q1.png)

**Insight:** São Paulo customers accounts for ~16% of all orders — more than double Rio de Janeiro. The top 3 cities contribute over 20% of total order volume. It`s also possible to observe a heavy concentration in major metropolitan areas and capitals.

### Q2: Is there any relation between ratings and delayed delivery?

![Q2](Q2.png)

**Insight:** Delivery delays have a major negative impact on customer satisfaction. While on-time deliveries achieve overwhelmingly positive reviews, delayed deliveries see a dramatic shift toward lower scores.

### Q3: Which categories are top performers each month?

Top 3 categories per month were identified using a window function ranking. The **top 5 overall categories** by total sales are:

1. **Beleza_saude** (Beauty & Health) — most stable performer
2. **Cama_mesa_banho** (Bed, Bath & Table) — strong from mid-2017 onward
3. **Esporte_lazer** (Sports & Leisure) — consistent growth
4. **Informatica_acessorios** (IT Accessories) — peak in Feb 2018
5. **Relogios_presentes** (Watches & Gifts) — strong seasonality, peaks in Q4/Q1

**Insight:** Watches & Gifts shows strong seasonality (holiday/gift-giving periods). Beauty & Health is the most stable performer. Growth accelerates from 2017 to 2018 across all top categories, matching overall business expansion.

### Q4: Does the freight value of a product influence ratings or order cancellations?

| Review Score | Avg Freight (R$) | Item Count |
| --- | --- | --- |
| 1 | 21.22 | 14,009 |
| 2 | 20.98 | 3,811 |
| 3 | 20.29 | 9,323 |
| 4 | 20.06 | 21,118 |
| 5 | 19.58 | 62,939 |

| Order Status | Avg Freight (R$) | Item Count |
| --- | --- | --- |
| DELIVERED | 19.95 | 110,197 |
| CANCELED | 19.65 | 542 |

**Insight:** There is a slight inverse relationship between freight costs and satisfaction — higher review scores correlate with ~R$ 1.60 lower freight charges. However, the difference is small (~8% variance), suggesting **freight is NOT a primary driver of dissatisfaction**. Canceled vs. delivered orders show almost identical freight costs, confirming freight is not a major cancellation factor.

### Q5: What is the ranking sales per each category?

74 categories total. Top 10 by total sales:

| Rank | Category | Total Sales (R$) | Items | Avg Value (R$) |
| --- | --- | --- | --- | --- |
| 1 | Beleza_saude | 1,441,248 | 9,670 | 149.04 |
| 2 | Relogios_presentes | 1,305,541 | 5,991 | 217.92 |
| 3 | Cama_mesa_banho | 1,241,681 | 11,115 | 111.71 |
| 4 | Esporte_lazer | 1,156,656 | 8,641 | 133.86 |
| 5 | Informatica_acessorios | 1,059,272 | 7,827 | 135.34 |
| 6 | Moveis_decoracao | 902,511 | 8,334 | 108.29 |
| 7 | Utilidades_domesticas | 778,397 | 6,964 | 111.77 |
| 8 | Cool_stuff | 719,329 | 3,796 | 189.50 |
| 9 | Automotivo | 685,384 | 4,235 | 161.84 |
| 10 | Ferramentas_jardim | 584,219 | 4,347 | 134.40 |

**Insight:** The top 5 categories account for ~R$ 5.8M (~51%) of total sales. PCs (rank 18) have the highest average order value (R$ 1,146). Beauty & Health leads in both volume AND revenue, making it the flagship category.

### Business Recommendations

1. **Geographic Focus** — São Paulo's dominance (~27% of orders) justifies targeted marketing and logistics optimization
2. **Delivery Is Critical** — On-time delivery is the strongest driver of customer satisfaction (73% score-5 rate); reducing the ~7% delay rate would significantly boost reviews
3. **Category Strategy** — Invest in Beauty & Health (stable, high volume) and Watches & Gifts (seasonal, high-value)
4. **Freight Is Not the Issue** — Shipping costs show minimal correlation with dissatisfaction or cancellations; focus on speed, not cost
5. **Seasonal Opportunities** — Q4/Q1 gift-giving periods (Nov–Jan) drive Watches & Gifts sales; prepare inventory accordingly


---

## Exploratory Data Analysis — fact_orders

A comprehensive exploratory data analysis was performed on the Gold layer `fact_orders` table. All analyses are available in the dedicated [05 - EDA - fact_orders](#notebook-2595984940181311) notebook, using **PySpark DataFrames** and matplotlib visualizations.

### Key Findings

**1. Order Status Distribution**
- The vast majority of orders (~96,000+) are **delivered** successfully, demonstrating strong operational performance
- **Canceled** orders represent the second largest category, indicating potential areas for customer retention improvement
- Small volumes of unavailable, invoiced, and processing orders show normal operational states
- **Business Impact**: The high delivery rate suggests reliable fulfillment, but the canceled orders warrant further investigation into cancellation reasons

**2. Monthly Order Trends (2016–2018)**
- Clear **upward growth trend** from late 2016 through 2018, with order volume and revenue tracking closely
- Peak activity occurs in **Q4 2017 and Q1 2018**, likely driven by seasonal shopping (holidays, New Year)
- Revenue ranges from ~100K to 1.6M+ per month at peak, showing business expansion
- **Business Impact**: The growth trajectory indicates successful market penetration; seasonal peaks should inform inventory and staffing decisions

**3. Review Score Distribution**
- Strong **positive skew** with the majority of reviews at score **5** (highest satisfaction)
- Low scores (1–2) represent a smaller but significant segment requiring attention
- **Business Impact**: High customer satisfaction overall, but low-scoring orders should be analyzed for improvement opportunities (delivery issues, product quality, etc.)

**4. Delivery Performance**
- **Left panel** (scatter plot): Most orders delivered close to estimated time (near red diagonal line), but visible dispersion shows variability
- **Right panel** (pie chart): Approximately **93% on-time delivery** rate with ~7% delayed
- **Business Impact**: Strong delivery performance overall, but the 7% delayed segment impacts customer experience and likely correlates with lower review scores

**5. Top 10 Cities by Revenue**
- **São Paulo** dominates revenue by a significant margin (~R$ 680K), followed by Rio de Janeiro, Belo Horizonte, and Brasília
- Revenue distribution follows typical Brazilian e-commerce patterns (concentration in major metropolitan areas)
- **Business Impact**: Geographic concentration suggests opportunities for targeted marketing and logistics optimization in high-revenue cities

**6. Delivery Delay vs. Review Score Correlation**
- **Left panel** (grouped bars): Delayed deliveries are more prevalent among **low-scoring reviews** (1–2), while on-time deliveries dominate high scores (4–5)
- **Right panel** (percentage view): Delay rate increases significantly for lower review scores — score 1 orders have the highest delay rate
- **Business Impact**: Strong negative correlation between delivery delay and customer satisfaction. Reducing delays is critical for improving review scores

**7. Review Comments by Score**
- **Left panel** (grouped bars): Customers with lower review scores (1–3) are significantly more likely to write comments than those with high scores (4–5)
- **Right panel** (percentage view): Comment rate reaches ~30–40% for score 1–2, compared to ~5–10% for score 5
- **Business Impact**: Dissatisfied customers provide written feedback explaining their dissatisfaction, while satisfied customers often just leave a high score. This qualitative data is valuable for root cause analysis

### Analysis Methodology

All analyses were conducted using:
- **PySpark DataFrame operations** (groupBy, agg, join, filter) for data transformation
- **Gold layer tables**: [puc_data_specialist_de_2026_09.03-gold.fact_orders](#table), [dim_time](#table), [dim_customer](#table)
- **Silver layer tables**: [puc_data_specialist_de_2026_09.02-silver.order_reviews](#table) for comment analysis
- **Visualization**: matplotlib for chart generation with appropriate color schemes (green/red for performance indicators)

### Recommendations

1. **Reduce delivery delays** — the strongest driver of negative reviews and customer dissatisfaction
2. **Analyze cancellation patterns** — investigate why orders are canceled to improve conversion
3. **Leverage seasonal peaks** — optimize inventory and marketing campaigns around Q4/Q1
4. **Mine low-score comments** — extract themes from written feedback on 1–2 star reviews for targeted improvements
5. **Geographic optimization** — focus logistics and marketing investment on top revenue cities


---


## Problems found
- When ingesting the order_reviews into silver layer, it has been discovered, during the Data Analysis from bronze layer, that the data ingestion into bronze layer was not correct for csv olist_order_reviews_dataset.csv. The method used to create the bronze table using read_file function has messed it up the comments when they have commas and bronze layer has received many invalid records and they was not reliable. 
    - See invalid data in order_reviews table below:
    ![](invalid_data_review.png)
    - A new solution needs to be found (tech debit)
    - Decision: postpone the import of the order review data into silver layer to a after the tech debit is solved
