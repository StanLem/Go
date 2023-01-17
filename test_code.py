import datetime
import time


print('time.time()', time.time())  #
print('time.gmtime()', time.gmtime())
print('time.gmtime(0)', time.gmtime(0))
print('time.thread_time()', time.thread_time())
print('time.asctime()', time.asctime())
print(time.localtime())
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
print(time.strftime('%Y-%m-%d'))


