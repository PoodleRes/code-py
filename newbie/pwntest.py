import hashlib
import random
import urllib2
import re

reg = re.compile('substr[(]md5[(]captcha[)], 0, 4[)]=([a-f0-9]{4})')
strpol = '0123456789abcdefghijklmnopqrstuvwxyz'
url = 'http://54.223.59.178/flag.php'
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.5",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "DNT":"1",
            "Host":"54.223.59.178",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"}

def product_36_code():
    k = list(strpol)
    random.shuffle(k)
    k = "".join(k)
    return k

def get_md5(strs):
    k = product_36_code()
    myMd5 = hashlib.md5()
    myMd5.update(k)
    myMd5_Digest = myMd5.hexdigest()
    while myMd5_Digest[0:4] != strs:
        k = product_36_code()
        myMd5 = hashlib.md5()
        myMd5.update(k)
        myMd5_Digest = myMd5.hexdigest()
    return k

def get_md5_4():
    #url = 'http://54.223.59.178/flag.php'
    req = urllib2.Request(url);
    while True:
        try:
            data = urllib2.urlopen(req).read()
            break
        except:
            pass
    md5_code = re.findall(reg,data)[0]
    return md5_code

def post_36_code():
    strs = get_md5_4()
    right = get_md5(strs)
    product_36 = product_36_code()
    text = {"captcha":right,"duihuanma":product_36};
    req = urllib2.Request(url=url,data=text,headers=headers)
    data = urllib2.urlopen(req).read()
