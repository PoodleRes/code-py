import weTest

data = weTest.download("https://www.baidu.com/")
with open("1.html",'w+') as datastore:
    datastore.write(data)
