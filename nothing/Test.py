# -*- coding: utf-8 -*-
import pythoncom
import pyHook
def onKeyboardEvent(event):
    # 监听键盘事件
    print "Key:", event.Key
def main():
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()

    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()

    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
