from functools import partial as pto
from Tkinter import Tk,Button,X
from tkMessageBox import showinfo,showwarning,showerror

WARN = 'warn'
CRIT = 'crit'
REGU = 'regu'

SIGN = {
    'do not enter':CRIT,
    'railroad crossing':WARN,
    '55\nspeed limit':REGU,
    'wrong way':CRIT,
    'merging traffic':WARN,
    'one way':REGU
}

critCB = lambda:showerror('Error','Error Button Pressed!')
warnCB = lambda:showwarning('Warning','Warning Button Pressed')
infoCB = lambda:showinfo('Info','Info Button Pressed!')

top = Tk()
top.title('Road Signs')
Button(top,text='quit',command = critCB,bg='white',fg='red').pack()

MyButton = pto(Button,top)
CritButton = pto(MyButton,command = critCB,bg = 'white',fg = 'red')
WarnButton = pto(MyButton,command = warnCB,bg = 'goldenrod1')
ReguButton = pto(MyButton,command = infoCB,bg = 'white')

for eachSign in SIGN:
    signtype = SIGN[eachSign]
    cmd = '%sButton(text=%r%s).pack(fill=X,expand=True)' % (signtype.title(),
    eachSign,'.upper()' if signtype == CRIT else '.title')
    eval(cmd)

top.mainloop()
