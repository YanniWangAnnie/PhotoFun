import time
import sys
import os

for i in range(10):
    print('transform...')
    time.sleep(1)
    f = open(sys.argv[2], 'w')
    f.write('haha')
    f.close()