import cv2
import socket
import pickle
import os

def recvobj(sock):
    length = int(sock.recv(1024))
    sock.sendall("recv_length")
    data = ""
    while not length == len(data):
        data += sock.recv(length * 2)
    sock.sendall("recv_data")
    data = pickle.loads(data)
    return data

def main():
    once = 1
    sock = socket.socket()
    print "ss"
    sock.connect(('120.78.136.136',12315))
    print "Connect Ok"
    while True:
        try:
            data = recvobj(sock)
            if data == "ScreenStream:END":
                break
            f = open("atemp.jpg", 'wb')
            f.write(data)
            f.close()
            frame = cv2.imread("atemp.jpg")
            cv2.imshow("vnc",frame)
            if once:
                once = 0
                cv2.namedWindow("vnc",0)
                cv2.resizeWindow("vnc",800,600)
            cv2.waitKey(1)
        except:
            break
    cv2.destroyAllWindows()
    os.remove("atemp.jpg")







if __name__ == '__main__':
    main()
