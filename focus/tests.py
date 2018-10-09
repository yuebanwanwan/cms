import time,threading

balance = 0

lock = threading.Lock()

def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(1000000):
        #在线程访问资源前上锁，保证在该线程访问资源结束前其他线程不能访问
        lock.acquire()
        try:
            change_it(n)
        finally:
            #要有职业道德在访问完资源后一定要记得释放锁，不然其他线程无法访问该资源
            lock.release()

t1 = threading.Thread(target=run_thread,args=(5,),name='Change_it_Thread')
t2 = threading.Thread(target=run_thread,args=(8,),name='Change_it_Thread')
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)