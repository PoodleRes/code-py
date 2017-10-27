import urllib2
import re

def main():
    url = raw_input('URL:')
    reg = re.compile('/([^./]+[.][^.]*)$')
    try:
        name = re.findall(reg,url)[0]
    except:
        name = '1.html'
    req = urllib2.Request(url);
    data = urllib2.urlopen(req).read()
    with open(name,'w+') as i:
        i.write(data)

if __name__ == '__main__':
    main()
