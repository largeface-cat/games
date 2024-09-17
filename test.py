import threading
import time
import numpy as np
teststr = 'test'
Lock = threading.RLock()

class TestThread1(threading.Thread):
    def __init__(self):
        super(TestThread1, self).__init__()

    def run(self):
        global teststr
        while True:
            Lock.acquire()
            print(teststr)
            Lock.release()
            time.sleep(1)


class TestThread2(threading.Thread):
    def __init__(self):
        super(TestThread2, self).__init__()

    def run(self):
        global teststr
        while True:
            Lock.acquire()
            Lock.acquire()
            teststr = np.random.rand()
            Lock.release()
            Lock.release()

if __name__ == '__main__':
    test_thread1 = TestThread1()
    test_thread2 = TestThread2()
    test_thread1.start()
    test_thread2.start()
    test_thread1.join()
    test_thread2.join()
    print('main')
