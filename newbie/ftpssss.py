from ftplib import FTP
import os
import socket

HOST = 'ftp.redhat.com'
DIR = 'redhat/3scale/3scale-2.0.0.CR2'
FILE = '3scale-amp20-backend-1.0-2.tar.gz'

def main():
    try:
        f = FTP(HOST)
    except (socket.error,socket.gaierror) as e:
        print "Error:cannot reach %s" % HOST
        return

    print '[+]Connected to host:%s' % HOST

    try:
        f.login()
    except ftplib.error_perm:
        print '[-]Error:cannot login anonymously'
        f.quit()
        return

    print '[+]Logged in as anonymous.'

    try:
        f.cwd(DIR)
    except ftplib.error_perm:
        print '[-]Error:cannot chdir to %s' % DIR
        f.quit()
        return

    print '[+]Changed to folder:%s' % DIR

    try:
        f.retrbinary('RETR %s' % FILE,open(FILE,'wb').write)
    except ftplib.error_perm:
        print '[-]Error:cannot read file %s' % FILE
        os.unlink(FILE)
    else:
        print '[+]Downloaded %s to CWD' % FILE
    f.quit()

if __name__ == '__main__':
    main()
