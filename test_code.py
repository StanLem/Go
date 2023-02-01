'''import datetime
import time
import httprequests as req

r = req.get('ya.ru')
print(r.text)

print('time.time()', time.time())  #
print('time.gmtime()', time.gmtime())
print('time.gmtime(0)', time.gmtime(0))
print('time.thread_time()', time.thread_time())
print('time.asctime()', time.asctime())
print(time.localtime())
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
print(time.strftime('%Y-%m-%d'))'''

from numba import jit
from numba import cuda
import numpy as np
from timeit import default_timer as timer
# To run on CPU
def func(x):
    return x+1
# To run on GPU
@jit
def func2(x):
    return x+1
if __name__=="__main__":
    '''n = 10000000
    a = np.zeros(n, dtype = np.float64)
    print(type(a))
    print(a)
    start = timer()
    func(a)
    print("without GPU:", timer()-start)
    start = timer()
    func2(a)
    cuda.profile_stop()
    print("with GPU:", timer()-start)'''


    n = -5
    for i in range(0, n):
        print(i)
    for i in range(n):
        print(i)
