#-*- coding: utf-8 -*
import socket
import struct
import os

class Server:
    def __init__(self,ip,port):
        self.addr = (ip,port)
        print "[+]Init Successfully"


    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen(5)
        print "[+]Listening...Address:%s:%s"%self.addr


    def check(self):
        while True:
            print "[+]Waiting..."
            cli, (ip, port) = self.sock.accept()
            try:
                print "[+]Connect from:"+ip+':'+str(port)
                while True:
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
                    elif sendcmd == "close":
                        self.close(cli)
                        break
                    elif sendcmd == "end":
                        cli.sendall("end")
                    else:
                        print "No this Function"
                        continue
            except Exception as e:
                print "[-]disconnect"
                cli.close()


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
                total = int(cli.recv(1024))
                recv_size = 0
                data = ""
                while not total == recv_size:
                    if total - recv_size > 1024:
                        data += cli.recv(1024)
                        recv_size += 1024
                    else:
                        data += cli.recv(total - recv_size)
                        recv_size = total
                        break
                print data
            except Exception as e:
                print "[-]shell:"+str(e)
                break


def main():
    ss = Server('0.0.0.0',12315)
    ss.bind()
    while True:
        ss.check()


if __name__ == '__main__':
    main()