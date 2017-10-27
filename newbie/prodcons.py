from random import randint
from time import ctime,sleep
from Queue import Queue
from threading import Thread

def writeQ(queue):
    print 'producing object for Q ...'
    queue.put('xxx',1)
    print 'size now',queue.qsize()

def readQ(queue):
    val = queue.get(1);
    print 'consumer object from Q ...size now',queue.qsize()

def writer(queue,loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))

def reader(queue,loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [writer,reader]
nfuncs = range(len(funcs))

def main():
    print 'Staring'
    nloops = randint(2,5)
    q = Queue(32)

    threads = []

    for i in nfuncs:
        t = Thread(target=funcs[i],args=(q,nloops))
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print 'All done'

if __name__ == '__main__':
    main()
