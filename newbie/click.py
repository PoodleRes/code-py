import requests
import base64

def main():
    url = 'http://120.24.86.145:8002/web6/'
    r = requests.Session()
    s = r.get(url)
    text = base64.b64decode(base64.b64decode(s.headers['flag'])[-8:])
    data = {'margin':text}
    s = r.post(url,data)
    print s.text

if __name__ == '__main__':
    main()
