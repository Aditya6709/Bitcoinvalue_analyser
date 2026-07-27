from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_json, struct
from pyspark.sql.types import StructType, StringType, DoubleType

# Create Spark session
spark = SparkSession.builder \
    .appName("CryptoStream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define schema
schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType())

# Read from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "crypto_prices") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON
clean_df = raw_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Convert rows back to JSON
output_df = clean_df.selectExpr(
    "CAST(symbol AS STRING) AS key",
    "to_json(struct(*)) AS value"
)

# Write to another Kafka topic
query = output_df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "crypto_analysis") \
    .option("checkpointLocation", "/app/checkpoints") \
    .start()

query.awaitTermination()