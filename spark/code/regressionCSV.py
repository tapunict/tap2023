from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext
from pyspark.sql import SparkSession
import pyspark.sql.types as tp
from pyspark.ml.feature import VectorAssembler

sparkConf = SparkConf()
sc = SparkContext(appName="TapSentiment", conf=sparkConf)
spark = SparkSession(sc)

# Reduce the verbosity of logging messages
sc.setLogLevel("ERROR")

from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import Correlation

# Training Set Schema
schema = tp.StructType([
    tp.StructField(name= 'label',dataType= tp.IntegerType(),  nullable= True),
    tp.StructField(name= 'value',dataType= tp.IntegerType(),  nullable= True)
    ]
)

dataset=spark.read.csv("../tap/spark/dataset/regressionexample.txt",
                        schema=schema,
                         header=True,
                         sep=',')

dataset.printSchema()

assembler = VectorAssembler(inputCols=["value"],outputCol="features")

training = assembler.transform(dataset)

training.show()

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(training)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
trainingSummary.residuals.show()
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)

test = spark.createDataFrame([200], tp.IntegerType()).toDF("value")

test.show()

test2 = assembler.transform(test)

lrModel.transform(test2).show()

test = spark.createDataFrame([1], tp.IntegerType()).toDF("value")

test.show()

test2 = assembler.transform(test)

lrModel.transform(test2).show()