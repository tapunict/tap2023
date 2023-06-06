from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext
from pyspark.sql import SparkSession


sparkConf = SparkConf()
sc = SparkContext(appName="TapSentiment", conf=sparkConf)
spark = SparkSession(sc)

# Reduce the verbosity of logging messages
sc.setLogLevel("ERROR")

from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import Correlation

datasetA = [1.0]
datasetB = [2.0]

data = [
        (1,Vectors.dense(datasetA),),
        (2,Vectors.dense(datasetB),)
       ]

df = spark.createDataFrame(data, ["label","features"])
df.show()

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(df)

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


datasetC = [3.0]
dataToBeEvaluated = [
        (Vectors.dense(datasetC),)
       ]

dataFrameToEvaluate = spark.createDataFrame(dataToBeEvaluated, ["features"])
dataFrameToEvaluate.show()
lrModel.transform(dataFrameToEvaluate).show()