import socket
import random
from timeit import default_timer as timer

words = ['a', 'aa', 'aaa', 'aaaa', 'b', 'bb', 'bbb', 'bbbb', 'ab', 'ba']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s.bind(('localhost', 65434))
s.listen()
conn, addr = s.accept()
with conn:
start = timer()
        for i in range(10000000):
            print(i+1)
            word = random.choice(words)
            conn.sendall(bytes(word, "utf-8"))
            conn.sendall(bytes('\n', "utf-8"))
        xr = timer() - start
        print("execution time: ", round(xr, 3), "sec")
