import urllib2
import urlparse
import os
import re

def download(url):
    index = 'https://www.nvshens.com/'
    req = urllib2.Request(url)
    req.add_header('Referer',index)
    page = urllib2.urlopen(req).read()
    return page

def downloadPic(url):
    flag = False
    index = 'https://www.nvshens.com/'
    try:
        req = urllib2.Request(url)
        req.add_header('Referer',index)
        page = urllib2.urlopen(req).read()
        flag = True
    except urllib2.HTTPError:
        url = url.replace('/s/','/')
        req = urllib2.Request(url)
        req.add_header('Referer',index)
        try:
            page = urllib2.urlopen(req).read()
            flag = True
        except:
            pass
    reg = re.compile('(\d+.jpg)')
    name = re.findall(reg,url)[0]
    if flag:
        pic = open(name,'wb+')
        pic.write(page)
        pic.close()
        print "Download:",name
    else:
        print 'No Found:',name

def getNum(s):
    regstr = '[^0-9]*([0-9]+).*'
    reg = re.compile(regstr)
    num = re.findall(reg,s)
    return num[0]

def downloadAlbum(url,name):
    name = str(name)
    p = '00'
    htmlstr = '.html'
    indexnum = 1
    with open('album'+name+'.txt','w+') as picres:
        while True:
            res = download(url+p+str(indexnum)+htmlstr)
            regstr = "src='(https[^']*"+getNum(url)+"[/s]*/[0-9]*.jpg)'"
            reg = re.compile(regstr)
            flag = re.findall(reg,res)
            indexnum += 1
            if flag:
                for i in flag:
                    picres.write(i+'\n')
            else:
                break
    with open('album'+name+'.txt','r') as picres:
        tempdir = os.getcwd()
        if os.path.exists(name):
            pass
        else:
            os.mkdir(name)
        os.chdir(name)
        for lines in picres:
            downloadPic(lines.replace('\n',''))
        os.chdir(tempdir)
    os.remove('album'+name+'.txt')

def downloadUrls(url):
    index = 'https://www.nvshens.com/'
    page = download(url)
    regstr = "class='igalleryli_link' href='([^']*)'"
    reg = re.compile(regstr)
    urls = re.findall(reg,page)
    for i in range(0,len(urls)):
        urls[i] = urlparse.urljoin(index,urls[i])
    with open("urls.txt","w") as logrecord:
        for mp in urls:
            logrecord.write(mp + '\n')

def downloadAlbums():
    allurl = []
    albumnum = 1
    with open('urls.txt','r') as urls:
        for i in urls:
            allurl.append(i.replace('\n',''))

    for i in allurl:
        downloadAlbum(i,albumnum)
        albumnum += 1

    os.remove('urls.txt')


def main():
    os.chdir('F:\\MM')
    if os.path.exists("F:\\MM\\Keer"):
        pass
    else:
        os.mkdir("Keer")
    os.chdir("F:\\MM\\Keer")
    url = "https://www.nvshens.com/girl/17204/album/"
    downloadUrls(url)
    downloadAlbums()

if __name__ == '__main__':
    main()
