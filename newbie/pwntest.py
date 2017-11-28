import urllib2
import re

reg = re.compile('KEY{[^}]*}')

def main():
    url = "http://103.238.227.13:10083/?id="
    for i in range(1,2):
        data = urllib2.urlopen(url + str(i)).read()
        print url + str(i)
        print data
        if re.findall(reg,data):
            print data



if __name__ == '__main__':
    main()
