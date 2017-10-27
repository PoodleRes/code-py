import wx

def load(event):
    with open(filename.GetValue()) as file:
        contents.SetValue(file.read())

def save(event):
    with open(filename.GetValue(),"w") as file:
        file.write(contents.GetValue)


app = wx.App()
win = wx.Frame(None,title = "Simple Window",size = (410,335))
bkg = wx.Panel(win)

loadbtn = wx.Button(bkg,label = "Open")
loadbtn.Bind(wx.EVT_BUTTON,load)

savebtn = wx.Button(bkg,label = "Save")
savebtn.Bind(wx.EVT_BUTTON,save)

filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg,style = wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(filename,proportion = 1,flag = wx.EXPAND)
hbox.Add(loadbtn,proportion = 1,flag =wx.LEFT,border = 5)
hbox.Add(savebtn,proportion = 1,flag = wx.LEFT,border = 5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion = 0, flag = wx.EXPAND | wx.ALL,border = 5)
vbox.Add(contents,proportion = 1,flag = wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,border = 5)

bkg.SetSizer(vbox)
win.Show()
app.MainLoop()
