from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

# Create a Spark Session 

spark = SparkSession \
    .builder \
    .appName("Streaming Table") \
    .getOrCreate()


# Create a streaming DataFrame
df = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 10) \
    .load()

# Write the streaming DataFrame to a table
q=df.writeStream \
    .option("checkpointLocation", "/tmp/") \
    .toTable("myTable") 

# Check the table result
spark.read.table("myTable").show()

q.awaitTermination()
