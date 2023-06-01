from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import from_json
import pyspark.sql.types as tp
from pyspark.ml import Pipeline
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.classification import LogisticRegression
from pyspark import SparkContext
from pyspark.sql import SparkSession

kafkaServer="kafkaServer:9092"
topic = "fluentd"

# Define Training Set Structure
tweetKafka = tp.StructType([
    tp.StructField(name= 'id', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'created_at', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'content',       dataType= tp.StringType(),  nullable= True)
])

# Training Set Schema
schema = tp.StructType([
    tp.StructField(name= 'id', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'subjective',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'positive',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'negative',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'ironic',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'lpositive',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'lnegative',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'top',       dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'content',       dataType= tp.StringType(),   nullable= True)
])

sparkConf = SparkConf()
sc = SparkContext(appName="TapSentiment", conf=sparkConf)
spark = SparkSession(sc)

# Reduce the verbosity of logging messages
sc.setLogLevel("ERROR")

print("Reading training set...")
# read the dataset  
training_set = spark.read.csv('../tap/spark/dataset/training_set_sentipolc16.csv',
                         schema=schema,
                         header=True,
                         sep=',')
print("Done.")

tokenizer = Tokenizer(inputCol="content", outputCol="words")
ita=StopWordsRemover.loadDefaultStopWords("italian")
stopWords = StopWordsRemover(inputCol= 'words', outputCol= 'filtered_words',stopWords=ita)
hashtf = HashingTF(numFeatures=2**16, inputCol="filtered_words", outputCol='tf')
idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5) #minDocFreq: remove sparse terms
model = LogisticRegression(featuresCol= 'features', labelCol= 'positive',maxIter=100)
pipeline = Pipeline(stages=[tokenizer, stopWords,hashtf, idf, model])

print("Training model...")
# fit the pipeline model with the training data
pipelineFit = pipeline.fit(training_set)
print("Done.")

modelSummary=pipelineFit.stages[-1].summary
print ("Model Accuracy:")
print(modelSummary.accuracy)
# Streaming Query

print("Reading stream from kafka...")
# Read the stream from kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafkaServer) \
    .option("subscribe", topic) \
    .load()


# Cast the message received from kafka with the provided schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", tweetKafka).alias("data")) \
    .select("data.*")

# Apply the machine learning model and select only the interesting columns
df = pipelineFit.transform(df) \
    .select("id", "created_at", "content", "prediction")

 
df.writeStream \
    .format("console") \
    .option("truncate",False) \
    .start() \
    .awaitTermination()