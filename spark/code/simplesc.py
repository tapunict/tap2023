import pyspark
print("Start")
conf = pyspark.SparkConf().setAppName('SimpleSC').setMaster('local[8]')
sc = pyspark.SparkContext(conf=conf)
lotr1 = sc.textFile("spark/dataset/The Lord Of The Ring 1-The Fellowship Of The Ring_djvu.txt") 
numrows=lotr1.count()
print("Il numero di righe e' %s" % (numrows))
sc.stop()