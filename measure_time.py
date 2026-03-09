import sys
import time
import os

if len(sys.argv) < 3:
    print("invalid")
    exit(1)

arg1 = sys.argv[1]
arg2 = sys.argv[2]
time1 = time.time()

os.system(arg1)
time1 = time.time()-time1
print(f"finished first program")

time2 = time.time()
os.system(arg2)
time2 = time.time() - time2
print(f"finished second program")

print(f"Time 1: {time1:.2f}s")
print(f"Time 2: {time2:.2f}s")
if time2 >= time1:
    print(f"Second program is slower than first, second is {time2/time1:.2f}% slower than first (measured in seconds)")
else:
    print(f"Second program is faster than first, second is {time2/time1:.2f}% faster than first (measured in seconds)")
