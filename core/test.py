import time
import sys
import os

for i in range(60):
    print('transform...')
    time.sleep(1)
f = open(sys.argv[3], 'w')
f.write('haha')
f.close()