from threading import Lock,Thread
from time import sleep,ctime

loops = [4,2]
lock = Lock()

class MyThread(Thread):
    def __init__(self,func,args,name =''):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(*self.args)



def loop(nloop,nsec):
    lock.acquire()
    print 'Loop Starting at:',nloop,'at:',ctime()
    lock.release()
    sleep(nsec)
    lock.acquire()
    print 'loop',nloop,'done at:',ctime()
    lock.release()

def main():
    print 'Main starting at:',ctime()
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = MyThread(loop,(i,loops[i]),loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print 'All Done at:',ctime()

if __name__ == '__main__':
    main()
