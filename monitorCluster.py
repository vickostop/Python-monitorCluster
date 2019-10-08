import subprocess
import time


# function that takes a specific metric from Ganglia
def gnglMetric(rrd):
    command = "rrdtool lastupdate '/var/lib/ganglia/rrds/vmcluster/" + ip[0] + "/" + rrd + ".rrd'"
    output = subprocess.check_output(command, shell=True)
    # splitting the sentence into two parts, before ':' and after ':'
    afterDots = output.decode().split(":", 1)
    # taking the second part of the above outcome and splitting it into words - splitting string is space
    lastPart = afterDots[1].split(" ")
    # taking the second element as the percentage - parse it to float
    percent = float(lastPart[1])
    return percent


print('Give IP addresses of existing nodes -use "space" between them, "enter" to end')
ip = list(input().split())

print("Give memory upper threshold (%) for node addition")
memUpThres = float(input())

print("Give memory lower threshold (%) for node removal")
memLowThres = float(input())

print("Give CPU upper threshold (%) for node addition")
cpuUpThres = float(input())

print("Give CPU lower threshold (%) for node removal")
cpuLowThres = float(input())

print("Give sampling time (in sec)")
samplTime = int(input())

# The algorithm will follow a LIFO architecture, meaning that when a
# new node will be added, when the system's resources are once again
# in satisfying levels, that same node will be removed
i = 0

while 1:

    percMemFr = (gnglMetric("mem_free") + gnglMetric("mem_cached") + gnglMetric("mem_buffers")) / gnglMetric("mem_total") * 100
    percMemUs = 100 - percMemFr
    cpuUsage = gnglMetric("cpu_user") + gnglMetric("cpu_system")
    print("Executor node's memory usage:", round(percMemUs, 1), "% ,", "CPU usage:", round(cpuUsage, 1), "%")
    if percMemUs >= memUpThres and cpuUsage >= cpuUpThres:
        print("\t\t\t\t\tAttention! System overload on the executor node!")
        # Check if there are any available nodes
        if len(ip) > i + 1:
            print("Adding a slave node to the application...")
            subprocess.run(["ssh", "username@" + ip[i],
                "/path/to/Sparkfolder/spark-2.4.0-bin-hadoop2.7/sbin/start-slave.sh spark://192.168.1.149:7077"],
                shell=False, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            # Waiting time until the system gets aware of the node addition
            time.sleep(45)
            i = i + 1
        else:
            print("No more available nodes in the cluster!")

    elif percMemUs <= memLowThres and cpuUsage <= cpuLowThres:
        print("\t\t\t\t\tAttention! System overkill!")
        if i > 0:
            print("Removing a slave node from the application...")
            subprocess.run(["ssh", "username@" + ip[i],                                "/path/to/Sparkfolder/spark-2.4.0-bin-hadoop2.7/sbin/stop-slave.sh"],
                shell=False, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            # Waiting time until the system gets aware of the node removal
            time.sleep(45)
            i = i - 1

    print("----------------------")
    time.sleep(samplTime)
