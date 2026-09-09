# Azure End-To-End Data Engineering Pipeline: AdventureWorks 🚀

An end-to-end data engineering project that ingests, transforms, and serves AdventureWorks business data using Microsoft Azure's modern data stack. The pipeline follows the **Medallion Architecture** (Bronze, Silver, Gold) to ensure data quality and scalability.

## 🏗️ Architecture Overview

The project implements a fully automated ETL/ELT pipeline utilizing the following Azure services:
*   **Data Ingestion:** Azure Data Factory (ADF) extracts raw data from an HTTP API (GitHub) and loads it into the Data Lake.
*   **Data Storage:** Azure Data Lake Storage Gen2 (ADLS Gen2) serves as the foundational storage for the Bronze, Silver, and Gold layers.
*   **Data Transformation:** Azure Databricks (using PySpark) cleanses and transforms the data from Bronze (Raw) -> Silver (Cleansed) -> Gold (Aggregated).
*   **Data Warehousing & Serving:** Azure Synapse Analytics hosts the relational data models built with SQL for downstream consumption.
*   **Business Intelligence:** Power BI connects to the Synapse SQL pool for interactive dashboarding and reporting.

*(Note: Add an architecture diagram image here if you have one!)*

## 🛠️ Technology Stack
*   **Cloud Platform:** Microsoft Azure
*   **Orchestration:** Azure Data Factory (ADF)
*   **Data Lake:** Azure Data Lake Storage (ADLS Gen2)
*   **Big Data Compute:** Azure Databricks (PySpark, Python)
*   **Data Warehouse:** Azure Synapse Analytics (SQL)
*   **Data Visualization:** Power BI
*   **AI Developer Tools:** GitHub Copilot / Cursor (utilized for rapid pipeline development and documentation)

## ⚙️ Pipeline Execution Flow (Medallion Architecture)

1.  **Ingestion (Source to Bronze):** 
    *   Configured linked services and datasets in Azure Data Factory.
    *   Built dynamic pipelines using parameters and loops to fetch raw CSV data from the GitHub API and land it in the `bronze` container in ADLS Gen2 in its raw format.
2.  **Transformation (Bronze to Silver):**
    *   Mounted ADLS Gen2 to Databricks.
    *   Processed the raw data using PySpark. Applied schema validation, dropped duplicates, handled null values, and converted data types.
    *   Saved the cleansed data in Delta format into the `silver` container.
3.  **Aggregation (Silver to Gold):**
    *   Performed business-level aggregations and joins in Databricks.
    *   Structured the data into fact and dimension tables (Star Schema) and pushed the finalized data to the `gold` container.
4.  **Serving (Gold to Synapse):**
    *   Utilized Azure Synapse Analytics to create external tables pointing to the Gold data lake.
    *   Wrote SQL views to serve structured analytics-ready data to downstream BI tools.
5.  **Reporting:**
    *   Connected Power BI directly to Azure Synapse via DirectQuery.
    *   Built interactive KPI dashboards to visualize sales, customer trends, and product performance.

## 📂 Repository Structure
*   `/Data`: Contains sample schemas or configuration files.
*   `/Reference Script`: Contains the PySpark notebooks and SQL scripts used in Databricks and Synapse.

## 🚀 How to Run (Prerequisites)
To replicate this project, you will need:
1.  An active Microsoft Azure Subscription.
2.  Provisioned resources: Resource Group, ADLS Gen2 account, Azure Data Factory, Azure Databricks Workspace, and Azure Synapse workspace.
3.  Appropriate IAM role assignments (e.g., Storage Blob Data Contributor) managed via Managed Identities for secure resource interaction.