# Monitoring a cluster
A python app that monitors a cluster and adds or removes dynamically nodes depending to the general performance and the available resources.
A Spark and a Spark Streaming process are been used, as well as Ganglia monitoring system.

grep.py - <i>A simple grep process for resource consumption; it has to be applied in a very large file.</i>

monitorCluster.py - <i>The decision algorithm / main program that will monitor the system and will add or remove a helping node to the cluster accordingly.</i>

stream.py - <i>A stream that produces words; the input of the word count process.</i>

wordCount.py - <i>Another process for resource consumption: its input will be a word stream, so that the consumption can be achieved gradually.</i>

<br>

<b>More info:</b>


https://spark.apache.org/

http://ganglia.sourceforge.net/

https://www.usenix.org/conference/atc17/technical-sessions/presentation/iorgulescu
