import urllib2
import urlparse
import os
import re
import time
import shutil
from threading import Thread,Lock

def download(url):
    req = urllib2.Request(url)
    data = urllib2.urlopen(req,timeout=30).read()
    return data

def get_page(url):
    MAX_PAGE = 10
    fp = open('subjectV.txt','w+')
    data = download(url)
    reg = 'href="(/htm/[^"]+)" class="img"'
    reg = re.compile(reg)
    urls = re.findall(reg,data)
    for i in range(len(urls)):
        urls[i] = urlparse.urljoin('http://www.44wn.com/',urls[i])
        fp.write(urls[i]+'\n')

    for i in range(MAX_PAGE,1,-1):
        list_page = 'list_'+str(i)+'.html'
        url = urlparse.urljoin(url,list_page)
        try:
            data = download(url)
            urls = re.findall(reg,data)
            for i in range(len(urls)):
                urls[i] = urlparse.urljoin('http://www.44wn.com/',urls[i])
                fp.write(urls[i]+'\n')
        except urllib2.HTTPError:
            pass

    fp.close()

def read_page():
    fp = open('subjectV.txt','r')
    data = []
    for i in fp:
        data.append(i.replace('\n',''))
    print '[+]Got URL list'
    return data

def get_js_file():
    url = 'http://www.44wn.com/js/sp.js'
    if os.path.exists('js.txt'):
        with open('js.txt') as source:
            return source.read()
    else:
        with open('js.txt','w+') as source:
            source.write(download(url))
            return source.read()

def get_m3u8_url(url):
    reg = '"(http://)"[+](s[0-9]*)[+]"([^"]*)"'
    reg = re.compile(reg)
    data = download(url)
    vurl = re.findall(reg,data)[0]
    numstr = vurl[1][2] if vurl[1][1] == '0' else vurl[1][1:]
    js_str = 'ipp'+numstr+'[.]push[(]["]([^"]*)["][)];'
    js_reg = re.compile(js_str)
    js_data = get_js_file()
    ip = re.findall(js_reg,js_data)[0] + ':8011'
    com_url = vurl[0] + ip + vurl[2]
    print '[+]Got m3u8:',com_url
    return com_url

def ana_m3u8(url):
    print '[+]Analyze m3u8...'
    name_reg = re.compile('([^/]+[.]m3u8)')
    filename = re.findall(name_reg,url)[0].replace('.m3u8','.mp4')
    data = download(url)
    reg = '([^.,\s]+[.]ts)'
    reg = re.compile(reg)
    names = re.findall(reg,data)
    urls = []
    for i in range(len(names)):
        urls.append(urlparse.urljoin(url,names[i]))
    return urls,names,filename

def video_down(url,name,lock):
    while True:
        try:
            data = download(url)
            break
        except:
            pass
    with open(name,'wb') as video:
        video.write(data)
    lock.acquire()
    print '[+]Downloaded:',name
    lock.release()

def count_time(MAX_WAIT,cwd,dirname):
    time.sleep(MAX_WAIT)
    if not os.listdir(cwd+os.sep+dirname):
        os.remove(dirname)
        os.chdir(cwd)
        raise urllib2.HTTPError

def video_downloader(urls,names,filename):
    print '[+]Begin Downloading...'
    threads = []
    lock = Lock()
    cwd = os.getcwd()
    dirname = (filename + 'dir').replace('.','')
    if os.path.exists(dirname):
        pass
    else:
        os.mkdir(dirname)
    os.chdir(dirname)
    for i in range(len(urls)):
        t = Thread(target=video_down,args=(urls[i],names[i],lock))
        threads.append(t)
    ct = Thread(target=count_time,args=(30,cwd,dirname))
    threads.append(ct)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    with open(names[0],'ab+') as video:
        for i in names[1:]:
            temp = open(i,'rb')
            data = temp.read()
            video.write(data)
            temp.close()
    os.rename(names[0],filename)
    shutil.copyfile(filename,cwd+os.sep+filename)
    os.remove(filename)
    for i in names[1:]:
        os.remove(i)
    os.chdir(cwd)
    os.rmdir(dirname)
    print '[+]Downloaded:',filename

def get_subject(url):
    if os.path.exists('subjectV.txt'):
        pass
    else:
        get_page(url)
    urls = read_page()
    for i in urls:
        try:
            url_v = get_m3u8_url(i)
            url_v_s,names,filename = ana_m3u8(url_v)
            video_downloader(url_v_s,names,filename)
        except:
            pass
    os.remove('subjectV.txt')

def main():
    os.chdir('F:\\video')
    url_index = 'http://www.44wn.com/s04/index.html'
    get_subject(url_index)

if __name__ == '__main__':
    main()
