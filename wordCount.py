from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import StorageLevel
from pyspark import SparkConf
import sys


# define the update function
def updateCount(newCounts, runningCount):
if runningCount is None:
runningCount= 0
return sum(newCounts, runningCount)


# Spark context definition
conf = SparkConf().setAppName("StreamWordCount").set("spark.dynamicAllocation.enabled", "false")
sc = SparkContext(conf=conf)

# Spark streaming context definition
ssc = StreamingContext(sc, 10)

# Checkpoint directory
ssc.checkpoint("/home/victor/Desktop/checkpoint")

# Socket stream definition - where the data come from
data = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

# Word count (on each duration) and total sum of each word
totalCounts = data.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).updateStateByKey(updateCount)

# DISK_ONLY
# totalCounts.persist(StorageLevel(True, False, False, False))

# MEMORY_AND_DISK
# totalCounts.persist(StorageLevel(True, True, False, False))

# MEMORY_ONLY (default)
# totalCounts.persist(StorageLevel(False, True, False, False))

totalCounts.pprint()

ssc.start()
ssc.awaitTermination()
