import Tkinter
top = Tkinter.Tk()
top.geometry('250x150')

def resize(ev=None):
    label.config(font = 'Helvetica -%d bold' % scale.get())


label = Tkinter.Label(top,text='Hello World!',font = 'Helvetica -12 bold')
label.pack(fill = Tkinter.Y,expand=1)

scale = Tkinter.Scale(top,from_=10,to=40,orient=Tkinter.HORIZONTAL,command=resize)
scale.set(12)
scale.pack(fill = Tkinter.X,expand = 1)

quit = Tkinter.Button(top,text='Exit',command=top.quit,bg='red',fg='white')
quit.pack(fill=Tkinter.X,expand=1)

Tkinter.mainloop()
