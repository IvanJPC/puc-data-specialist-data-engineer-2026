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

The reason behind this is it's a well documented dataset containing e-commerce information from 2016 to 2018

All notebooks available in 


## Planned Workflow:
1 - Setup a new Unity Catalog and Schemas to store RAW, transformed and analytic data using Data warehouse concepts and Medalion architecture pattern through notebooks

    	1.1 - Create Schemas - done

        1.2 - Create RAW volume in raw layer and data import


## Notebooks
- /00 - Setup Catalog/00 - Setup Schema and Catalog
- /01 - Dataset Import
- /02 - Bronze Data Ingestion/02 - Bronze Ingestion
- /03 - Silver Refinement/03 - Silver - DEA and Transformations
- /04 - Gold Refinement

## Questions to Answer
```
- What are the ratings that have the order delivered after the estimated time?
- Which categories are top performers each month?
- Does the freight value of a product influenced on ratings or order cancelations?
- What are the top 10 cities of customers with most orders?
- What is the ranking sales per each category?
- 
```

## Problems found
- When ingesting the order_reviews into silver layer, it has been discovered, during the Data Analysis from bronze layer, that the data ingestion into bronze layer was not correct for csv olist_order_reviews_dataset.csv. The method used to create the bronze table using read_file function has messed it up the comments when they have commas and bronze layer has received many invalid records and they was not trustable. 
    - See invalid data in order_reviews table below:
    ![](invalid_data_review.png)
    - A new solution needs to be found (tech debit)
    - Decision: postpone the import of the order review data into silver layer to a after the tech debit is solved
