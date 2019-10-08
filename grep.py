from pyspark import SparkContext, SparkConf
import sys
from timeit import default_timer as timer
from pyspark import StorageLevel


filename = "/path/of/file/that/will/be/searched"
keyword = "wordForSearch"
saveFileName = "/path/of/output/file"

conf = SparkConf().setAppName("Grep App")

sc = SparkContext(conf=conf)

full_data = sc.textFile(filename)

start = timer()

result = full_data.filter(lambda x: keyword in x)

# MEMORY_AND_DISK
# result.persist(StorageLevel(True, True, False, False))

result.saveAsTextFile(saveFileName)

xr = timer() - start

print("execution time: ", round(xr,3), "sec")
print("Saved the result in " + saveFileName)

sc.stop()
