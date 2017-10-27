from selenium import webdriver
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

url = raw_input('URL:')
reg = re.compile('/([^./]+[.][^.]*)$')
try:
    name = re.findall(reg,url)[0]
except:
    name = '1.html'
driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
driver.get(url)
data = driver.page_source;
driver.close()
#print data
with open(name,'w+') as files:
    files.write(data)
os.system('rm ghostdriver.log')
