# SMBUD_project_24

This repository is for the project 24/25 of the course `System and Methods for Big and Unstructured Data` at PoliMi.

## Project description and folder structure

The assignment can be found at [SMBUD Project-2024_2025.pdf](Assignment/SMBUD_Project_2024_2025.pdf).

In a nutshell, the project consists in finding a dataset of at least 20,000 records, and then use two different NoSQL databases to store and query the data. The two chosen database technologies are `Neo4j` and `ElasticSearch`.

The chosen dataset is the [Food.com - Recipes and Review](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews/data) dataset which contains 522,517 recipes from 312 different categories and 1,401,982 reviews from 271,907 different users.

The assignment required to write 10 queries for each database, that can be found here: [Neo4J Queries](Neo4J/QueriesNeo4J.md) and [ElasticSearch Queries](Elasticsearch/queriesElasticsearch.md).

The dataset is first sampled to reduce its size, and then it is preprocessed. These steps are performed by several python scripts that can be found in the [DataWrangling](DataWrangling) folder.

> As an extra, a webapp called [Taste trios](https://taste-trios-front-end.vercel.app/) has been developed to interact with the databases via a small selection of features. In order to access the database, they have both been hosted.

The hosting of the databeses also allowed for some data analysis to be performed using a Python Notebook available [here](DataAnalysis/DataAnalysis.ipynb). Unfortunatly the notebook is not runnable without the credentials to the databases.

Finally, a thorough report of the project can be found [here](Report/Report.pdf).
