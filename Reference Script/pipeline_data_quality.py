# Databricks notebook cell(s) -- UNTESTED here (needs your workspace). Adjust paths/table names.
# Purpose: log row counts, duplicates and nulls for every table in every layer into an audit Delta table,
# so you can show "continuous monitoring / audit-ready lineage" for the pipeline.
import json
from datetime import datetime
from pyspark.sql import functions as F

AUDIT_PATH = "/mnt/gold/audit/pipeline_audit"
TABLES = ["Customers", "Products", "Sales_2015", "Sales_2016", "Sales_2017"]      # your table names
LAYERS = {"bronze": ("/mnt/bronze/{t}", "csv"), "silver": ("/mnt/silver/{t}", "delta")}  # edit to your real paths/formats

def read(path, fmt):
    r = spark.read.format(fmt)
    return r.option("header", True).option("inferSchema", True).load(path) if fmt == "csv" else r.load(path)

records = []
for layer, (pattern, fmt) in LAYERS.items():
    for t in TABLES:
        sdf = read(pattern.format(t=t), fmt)
        total = sdf.count()
        nulls = sdf.select([F.sum(F.col(c).isNull().cast("int")).alias(c) for c in sdf.columns]).first().asDict()
        records.append((datetime.utcnow().isoformat(), layer, t, total, total - sdf.dropDuplicates().count(), json.dumps(nulls)))

audit = spark.createDataFrame(records, "run_ts string, layer string, table_name string, row_count long, duplicate_rows long, null_counts string")
audit.write.format("delta").mode("append").save(AUDIT_PATH)

# Reconciliation view: how many rows were removed between Bronze and Silver per table (explainable = audit-ready)
a = spark.read.format("delta").load(AUDIT_PATH)
latest = a.filter(F.col("run_ts") == a.agg(F.max("run_ts")).first()[0])
recon = (latest.groupBy("table_name").pivot("layer", ["bronze", "silver"]).agg(F.first("row_count"))
         .withColumn("rows_removed", F.col("bronze") - F.col("silver"))
         .withColumn("removed_pct", F.round(F.col("rows_removed") / F.col("bronze") * 100, 2)))
display(recon)
