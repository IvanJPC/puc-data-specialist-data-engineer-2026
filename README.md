# PUC-RJ - Data Specialist - Data Engineer MVP
- Student: Ivan J P de Carvalho
- Date: Jul-Oct 2026

---

## Dataset
For this MVP, this project will be using the Brazil E-Commerce dataset available on: 
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

### Dataset credit

- Owner: http://www.olist.com/


> &#9432; **License:** 
> 
> CC BY-NC-SA 4.0 - https://creativecommons.org/licenses/by-nc-sa/4.0/
>
> The use of this dataset in this project is for Non Commercial use only.


### Why this dataset

The dataset contains **~100K orders** placed between 2016 and 2018 across **4,000+ Brazilian cities**, spanning multiple dimensions: customers, sellers, products, reviews, payments, and logistics. This richness makes it an ideal candidate for a **data warehouse project** that follows the full data engineering lifecycle.

| Criterion | Rationale |
| --- | --- |
| **Realistic complexity** | 9 interconnected CSV files requiring joins, foreign keys, and star-schema modeling — mirrors real-world enterprise data |
| **Rich business dimensions** | Covers geographic, temporal, product, customer, and satisfaction dimensions — enough to build a full DataMart |
| **Well-documented** | Extensive community EDAs on Kaggle allow cross-validation of findings and data quality checks |
| **Brazilian context** | A regional e-commerce market underrepresented in typical data engineering tutorials |
| **Manageable scope** | Small enough to run on serverless compute, yet complex enough to demonstrate medallion architecture best practices |

---

## Data Pipeline (Pipeline de Dados)

### Notebooks
All notebooks are available in layer's subfolder:

![Data Pipeline Folders ](folders.png)

**__ATENTION__** : For a first run, all notebooks must be executed in order.

Each Silver and Gold notebooks contain the solution reasoning covering:

- Data Quality Analisys:
    - completeness (Completude)
    - Consistency (Consistência)
    - Uniqueness (Unicidade)
    - Precision (Acurácia)
    - Outliers
- Data Ingestions Scripts
    - It has been decided to use SQL only as much as possible
- Reconciliation SQL's to verify ingestion results


```
Data extract notebook does not contain the information above.
It has been verified, when ingestioning Gold layer, that a data quality verification was needed when ingestioning Bronze layer. 
See session Problems found later in this README.
```

#### Notebooks List: 

*Links to github.
- [00 - Setup Schema and Catalog](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/00%20-%20Setup%20Catalog/00%20-%20Setup%20Schema%20and%20Catalog.ipynb)
    - **Root catalog**: _puc_data_specialist_de_2026_09_
    - **Goal:** Creates the Databricks catalog and schemas based on medallion architecture for this MVP
    - RAW schema stores the dataset RAW files imported from the dataset cloud (Kaggle)
    - Each Medallion layer is represented by a schema

    ![schemas](schemas.png)

- [01 - Dataset Import](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/01%20-%20Dataset%20Import/01%20-%20Volume%20Create%20and%20Data%20Import.ipynb)
    - **Goal:** Import the CSV files from Kaggle
    - The CSV files will be stored into a volume in _00-raw_ schema
    - Stores the files into a  folder named with the import date as a metadata of import date
    - Import uses Kaggle API
    - Needs API Token set before run. See notebook pre-requisite session

- [02 - Bronze Ingestion](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/02%20-%20Bronze%20Data%20Ingestion/02%20-%20Bronze%20Ingestion.ipynb)
    - **Goal:** Data extraction and Bronze layer creation
    - **Schema:** _01-bronze_
    - Creates Bronze tables and injest data from imported files stored in _00-raw_ schema volume
    - Represents dataset imported
    - No business or bigger changes
    - String and Number types only
    - Specific details in the notebook comments
- [03 - Silver - DEA and Transformations](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/03%20-%20Silver%20Refinement/03%20-%20Silver%20-%20DEA%20and%20Transformations.ipynb)
    - **Goal:** Silver layer creation with data quality check
    - **Schema:** _02-silver_
    - Creates Silver tables and injest data from Bronze layer
    - Execute bronze data checks for data transformation decisions
    - Data refinements
    - Type casts 
    - Value checks 
    - Deduplication and nullable checks
    - Reconciliation checks
    - Specific details in the notebook comments
- [04 - Gold Refinement ](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/04%20-%20Gold%20Refinement/04%20-%20Gold%20Refinement.ipynb)
    - **Goal:** Business data creation using DW architecture, facts and dims tables 
    - **Schema:** _03-gold_
    - Data Warehouse layer
    - All columns and all tables contains comments to assist on a data catalog creation
    - Schema to be used: Star
    - Specific details in the notebook comments

- [05 - EDA - Business Questions](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/04%20-%20Gold%20Refinement/05%20-%20EDA%20-%20Business%20Questions.py) 
    - **GOal:** Business Data Analysis
    - **Schema:** _03-gold_
    - Created using AI assistent for speed delivery

- [07 - Data Catalog](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/04%20-%20Gold%20Refinement/07%20-%20Data%20Catalog.ipynb)
    - **Goal:** Generate a data catalog from Unity Catalog `information_schema` for the Gold layer
    - **Schema:** _03-gold_
    - Queries all table and column comments from the information_schema
    - Identifies and applies missing column comments via `ALTER TABLE`
    - Tags tables with their star-schema role (fact/dimension) and grain
    - Created using AI assistent
    - Creates a `v_data_catalog` view for downstream consumption




### Proof of resources and table creation after running all ETL notebooks:
#### Raw volumes and Bronze tables
![Raw volumes and Bronze tables](raw_bronze.png)

#### Silver and Gold tables

![Silver and Gold tables](silver_gold.png)


---

## Business Context and questions (Contexto de Negócios e Perguntas)

### The scenario

Olist is a Brazilian marketplace that connects small and medium-sized sellers to customers across the country. When a customer purchases a product on an Olist store, the seller is notified to fulfill that order. Once the customer receives the product — or the estimated delivery date is past due — the customer gets a satisfaction survey by email where they can leave a review score (1–5) and optionally write a comment about their experience.

### Business Questions

**1. Customer & Geographic Intelligence**
- What are the top 10 cities of customers with most orders?

**2. Logistics & Delivery Performance**
- Is there any relation between ratings and delayed delivery

**3. Product & Category Strategy**
- Which categories are top performers each month?
- What is the ranking sales per each category?

**4. Customer Satisfaction Drivers**
- Does the freight value of a product influence ratings or order cancellations?


---
## Data Analisys (Análise de Dados)

The `05 - EDA - Business Questions` notebook answers the business questions defined in this README using the Gold-layer star schema tables.

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
| 1 | 21,22 | 14.009 |
| 2 | 20,98 | 3.811 |
| 3 | 20,29 | 9.323 |
| 4 | 20,06 | 21.118 |
| 5 | 19,58 | 62.939 |

| Order Status | Avg Freight (R$) | Item Count |
| --- | --- | --- |
| DELIVERED | 19,95 | 110.197 |
| CANCELED | 19,65 | 542 |

**Insight:** There is a slight inverse relationship between freight costs and satisfaction. However, the difference is small, suggesting **freight is NOT a primary driver of dissatisfaction**. Canceled vs. delivered orders show almost identical freight costs, confirming freight is not a major cancellation factor.

### Q5: What is the ranking sales per each category?

74 categories total. Top 10 by total sales:

| Rank | Category | Total Sales (R$) | Items | Avg Value (R$) |
| --- | --- | --- | --- | --- |
| 1 | Beleza_saude | 1.441.248 | 9.670 | 149,04 |
| 2 | Relogios_presentes | 1.305.541 | 5.991 | 217,92 |
| 3 | Cama_mesa_banho | 1.241.681 | 11.115 | 111,71 |
| 4 | Esporte_lazer | 1.156.656 | 8.641 | 133,86 |
| 5 | Informatica_acessorios | 1.059.272 | 7.827 | 135,34 |
| 6 | Moveis_decoracao | 902.511 | 8.334 | 108,29 |
| 7 | Utilidades_domesticas | 778.397 | 6.964 | 111,77 |
| 8 | Cool_stuff | 719.329 | 3.796 | 189,50 |
| 9 | Automotivo | 685.384 | 4.235 | 161,84 |
| 10 | Ferramentas_jardim | 584.219 | 4.347 | 134,40 |

**Insight:** The top 5 categories account for R$ 5,8M of total sales.
Beauty & Health leads in both volume AND revenue, making it the flagship category.


---

## Data Load (Carga dos Dados)

This project transforms raw e-commerce transactional data into a **structured analytical data product** using the Medallion architecture pattern. Data flows through four layers — RAW → Bronze → Silver → Gold — each adding progressively more structure, quality, and business meaning.

### Loading Strategy

A **SQL-first approach** was adopted for Silver and Gold layers to keep transformations readable, auditable, and easy to reconcile. Bronze ingestion uses Databricks `read_file` function for simplicity. Each layer is materialized as managed Delta tables in Unity Catalog.

| Layer | Schema | Method | Purpose |
| --- | --- | --- | --- |
| **RAW** | `00-raw` | Kaggle API → UC Volume | Source CSV files stored as-is in a volume |
| **Bronze** | `01-bronze` | `read_file` / `COPY INTO` | Raw data ingested into Delta tables, string and number types only |
| **Silver** | `02-silver` | SQL `CREATE TABLE AS SELECT` | Cleaned, typed, deduplicated, Data Quality checked, ready for modeling |
| **Gold** | `03-gold` | SQL `CREATE TABLE` + `INSERT` | Kimball proposal, Star schema with facts, dimensions |

### Layer-by-Layer Details

**1. RAW Layer (`00-raw`)**
- Notebook: [01 - Dataset Import](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/01%20-%20Dataset%20Import/01%20-%20Volume%20Create%20and%20Data%20Import.ipynb)
- 9 CSV files downloaded from Kaggle via the Kaggle API
- Files stored in a UC volume under `00-raw`, organized in a folder named by import date
- No transformations — files preserved in original format for auditability
- Requires Kaggle API token configured before execution

**2. Bronze Layer (`01-bronze`)**
- Notebook: [02 - Bronze Ingestion](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/02%20-%20Bronze%20Data%20Ingestion/02%20-%20Bronze%20Ingestion.ipynb)
- 9 Bronze tables created from RAW CSV files using Databricks `read_file` function
- Schema enforced with string and number types only — no business logic applied
- Represents the dataset as-imported, with minimal changes
- **Known issue:** `read_file` corrupts CSV fields containing embedded commas (e.g., review comments). See [Problems Found](#problems-found-throughout-the-project) for details

**3. Silver Layer (`02-silver`)**
- Notebook: [03 - Silver - DEA and Transformations](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/03%20-%20Silver%20Refinement/03%20-%20Silver%20-%20DEA%20and%20Transformations.ipynb)
- Bronze data checked for quality across 5 dimensions: completeness, consistency, uniqueness, accuracy, and outliers
- Transformations applied using SQL `CREATE TABLE AS SELECT`:
  - Type casts (e.g., string → date, string → double)
  - Value checks and standardization (e.g., title-casing city names)
  - Deduplication and nullable checks
  - SCD Type 7 applied for Slowly Changing Dimensions where applicable
- Reconciliation SQL validates row counts and data integrity between Bronze and Silver

**4. Gold Layer (`03-gold`)**
- Notebook: [04 - Gold Refinement](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/04%20-%20Gold%20Refinement/04%20-%20Gold%20Refinement.ipynb)
- Star schema built from Silver tables with 3 fact tables and 4 dimension tables:

| Table | Type | Description |
| --- | --- | --- |
| `fact_orders` | Fact | Order-grain measures: total price, freight, order value, payment value, delivery metrics, review score |
| `fact_order_items` | Fact | Item-grain measures: price, freight_value, total_value per order item |
| `fact_order_payments` | Fact | Payment-grain measures: payment value, installments per payment record |
| `dim_customer` | Dimension | Customer location attributes (city, state, city_state) |
| `dim_product` | Dimension | Product category and physical attributes (weight, dimensions, volume) |
| `dim_time` | Dimension | Calendar attributes with Brazilian holiday flags |
| `dim_payment_type` | Dimension | Payment type lookup (boleto, credit card, voucher, etc.) |

- All tables and columns include comments for data catalog discoverability
- Surrogate keys generated via `ROW_NUMBER()` for all dimensions
- Degenerate dimensions (`order_id`, `order_item_id`) retained in fact tables for traceability
- Computed measures: `is_delivery_delayed`, `is_good_review`, `review_classification`, `estimated_delivery_days`, `actual_delivery_days`


### Reconciliation & Validation

Each layer includes reconciliation SQL scripts to validate data integrity:
- **Row count checks** — verify no data loss between layers
- **Null rate checks** — ensure critical columns are not unexpectedly null
- **Sum checks** — verify aggregate measures match between source and target
- **Foreign key integrity** — validate that all fact table FKs resolve to dimension tables

---

## Design and Data Catalog (Modelagem e Catálogo de Dados)

The data catalog is only available for Gold layer

A export of the Data Catalog is available as the spread sheet [data_catalog_2026_09_26.xlsx](https://github.com/IvanJPC/puc-data-specialist-data-engineer-2026/blob/main/data_catalog_2026_09_26.xlsx) available in Github.

### Star Schema Design

The Gold layer follows a **Kimball proposal (bottom-up), star schema** with two fact-table grains and four conformed dimensions:

| Table | Type | Grain | Key Columns |
| --- | --- | --- | --- |
| `fact_orders` | Fact | One row per order | `order_key` (PK), `customer_key` (FK), `purchase_date_key` (FK) |
| `fact_order_items` | Fact | One row per order item | `order_item_fact_key` (PK), `product_key` (FK), `customer_key` (FK) |
| `fact_order_payments` | Fact | One row per payment record | `order_payment_fact_key` (PK), `payment_type_key` (FK) |
| `dim_customer` | Dimension | One row per customer | `customer_key` (PK), `customer_id` (NK) |
| `dim_product` | Dimension | One row per product | `product_key` (PK), `product_id` (NK) |
| `dim_time` | Dimension | One row per calendar date | `date_key` (PK) |
| `dim_payment_type` | Dimension | One row per payment type | `payment_type_key` (PK) |

### Data Catalog

A complete data catalog is generated by the [07 - Data Catalog](#notebook-1350675712732780) notebook, which:

- Queries the Unity Catalog `information_schema` for all Gold layer tables and columns
- Tags tables with their star-schema role (`table_role`: fact/dimension) and grain
- Creates a `v_data_catalog` view for downstream consumption

**Catalog name:** `puc_data_specialist_de_2026_09`  
**Schema:** `03-gold`  
**Tables:** 7 (3 facts + 4 dimensions)  
**Columns:** 71 (all with comments)  


---

## Self-review (Autoavaliação)

### Research Areas (Pontos de Pesquisa)

Throughout the project, the following key topics were researched and applied:

**1. Medallion Architecture on Databricks**
- Studied the Bronze → Silver → Gold layer pattern for organizing data by quality and purpose
- Researched how Unity Catalog schemas can map to medallion layers (`00-raw`, `01-bronze`, `02-silver`, `03-gold`)
- Investigated volume-based file storage in UC volumes for raw CSV ingestion via Kaggle API
- Studied the application of
 Slowly Changing Dimensions Type 7 when ingesting Silver layer 

**2. Star Schema Modeling for E-Commerce**
- Researched Kimball-style fact and dimension table design for an e-commerce marketplace
- Modeled `fact_orders` (order-grain) and `fact_order_items` (item-grain) as separate fact tables to avoid double-counting measures
- Designed `dim_time` with holiday flags (Brazilian national holidays) and `dim_customer` with costomer location attributes
- Studied degenerate dimensions (e.g., `order_id` kept in fact tables for traceability without a dedicated dimension)

 **3. Data Quality**
- Researched and applied 5 data quality dimensions: completeness, consistency, uniqueness, accuracy (precision), and outlier detection
- Investigated Databricks `read_file` function limitations — discovered that CSV files with embedded commas in text fields (e.g., review comments) get corrupted during Bronze ingestion
- Explored reconciliation SQL patterns (row counts, sum checks, null counts) to validate data integrity across layers
- Understanding of Unity Catallog information_schema to assist on creation of a Data Catalog

**4. Databricks Secrets Management**
- Researched Databricks secret scopes and how to securely store API tokens for Kaggle access
- Discovered late in the project that secrets should be stored via Databricks CLI or API rather than hardcoded — documented as a learning in the Problems Found section

---

### What Worked Well

- **Medallion architecture** successfully separated raw ingestion from business logic, making the pipeline modular and debuggable
- **Star schema** in the Gold layer enabled clean, efficient joins for all 5 business questions without complex transformations
- **SQL-first approach** in Silver and Gold layers made the transformations readable, auditable, and easy to reconcile
- **Data quality checks** at the Silver layer caught issues early (null counts, type mismatches, deduplication)
- **Column comments** on all Gold tables provided a foundation for a data catalog without additional tooling
- **EDA notebook** with PySpark + matplotlib delivered clear visual answers to all 5 business questions

---

### Points of Improvement (Pontos de Melhora)

**Technical Debt**

1. **Order reviews Bronze ingestion (HIGH)** — The `read_file` function corrupts CSV fields containing commas (review comments). The current workaround loads review data directly from Silver, bypassing the Bronze layer for this table. **Recommendation:** Replace `read_file` with `COPY INTO` or `AUTO LOADER` with proper CSV parsing options (`escape`, `quote`), or use a notebook-based `spark.read.csv()` with `escape='"'` and multiLine mode.

2. **Secrets management (MEDIUM)** — Kaggle API credentials are not yet stored in Databricks secret scopes. **Recommendation:** Create a secret scope via Databricks CLI (`databricks secrets create-scope`) and store the Kaggle token using `databricks secrets put-secret`, then reference it in the import notebook via `dbutils.secrets.get()`.

3. **Bronze layer data quality checks (MEDIUM)** — Data quality verification was added retroactively after discovering issues during Gold ingestion. **Recommendation:** Add Data Quality checks (row counts, null rates, schema validation) immediately after Bronze ingestion as a dedicated step, not as an afterthought.

**Architecture & Scalability**

4. **No pipeline orchestration** — Notebooks are executed manually in sequence. **Recommendation:** Create a Databricks Job or Lakeflow pipeline that orchestrates all notebooks with dependencies, retries, and alerting. This would enable scheduled refreshes if new data arrives.

5. **No incremental loading** — Bronze and Silver layers use full table recreations. **Recommendation:** For production use, implement incremental ingestion with `MERGE INTO` or Auto Loader for streaming append patterns, especially if the dataset grows.




### Problems Found Throughout the Project
- **Secrets management** - I've tryed to use Dababricks secrets but I've just discovered how to store secrets into Dababricks later. See more details in notebook `01 - Volume Create and Data Import`.
- **order_reviews extraction** - When ingesting the order_reviews into silver layer, it has been discovered, during the Data Analysis from bronze layer, that the data ingestion into bronze layer was not correct for csv olist_order_reviews_dataset.csv. The method used to create the bronze table using read_file function has messed it up the comments when they have commas and bronze layer has received many invalid records and they was not reliable. 
    - See invalid data in order_reviews table below:
    ![](invalid_data_review.png)
    - A new solution needs to be found (tech debit)
    - Decision: postpone the import of the order review data into silver layer to a after the tech debit is solved
