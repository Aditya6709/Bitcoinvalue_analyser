from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

# Create Spark session
spark = SparkSession.builder \
    .appName("CryptoStream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define schema of incoming JSON
schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType())

# 1️⃣ Read from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "crypto_prices") \
    .option("startingOffsets", "latest") \
    .load()

# 2️⃣ Parse JSON
clean_df = raw_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# 3️⃣ Function to write each micro-batch to MySQL
def write_to_mysql(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://mysql:3306/crypto_db") \
        .option("dbtable", "crypto_prices") \
        .option("user", "root") \
        .option("password", "Aditya123") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .mode("append") \
        .save()

# 4️⃣ Start streaming query
query = clean_df.writeStream \
    .foreachBatch(write_to_mysql) \
    .option("checkpointLocation", "/app/checkpoints") \
    .start()

query.awaitTermination()
