import wx
import cv2

pause = False

APP_PAUSE   = 1
APP_CLOSE   = 2

capture = cv2.VideoCapture()
capture.open('/home/bzr0014/Videos/720')
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
numFrames = capture.get(cv2.CAP_PROP_FRAME_COUNT)

fields = dict([("field%02d"%i, "field%02d_default"%i) for i in range(1, 5+1)])
print(fields)

class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, size=(640, 480), fps=15):
        wx.Panel.__init__(self, parent)

        self.size = size
        self.capture = capture
        ret, frame = self.capture.read()
        frame = cv2.resize(frame, self.size)

        height, width = frame.shape[:2]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)


    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        global pause
        if pause:
            return
        ret, frame = self.capture.read()
        frame = cv2.resize(frame, self.size)
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.texts = {}
        self.InitUI()

    def createMenu(self, ID, shortcutText, fun):
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, ID, shortcutText)
        fileMenu.Append(qmi)
        self.Bind(wx.EVT_MENU, fun, id=ID)
        return fileMenu

    def InitUI(self):
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        menubar     = wx.MenuBar()

        menubar.Append(
            self.createMenu(APP_CLOSE, '&Quit\tCtrl+Q', self.onClose),
            '&File')
        menubar.Append(
            self.createMenu(APP_PAUSE, '&Pause\tCtrl+Space', self.onPause),
            '&Playback')

        self.SetMenuBar(menubar)

        self.SetSize((640, 480))
        self.SetTitle('Simple menu')
        self.Centre()

        panel = wx.Panel(self)
        #panel.SetBackgroundColour('#4f5049')

        vbox = wx.BoxSizer(wx.VERTICAL)

        video_panel = ShowCapture(panel, capture)
        vbox.Add(video_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)


        hbox0    = wx.BoxSizer(wx.HORIZONTAL)
        button01 = wx.Button(panel, label = " > ")
        button01.Bind(wx.EVT_BUTTON, self.onFastForward)
        button02 = wx.Button(panel, label = " >> ")
        button02.Bind(wx.EVT_BUTTON, self.onFastFastForward)

        button03 = wx.Button(panel, label = " < ")
        button03.Bind(wx.EVT_BUTTON, self.onFastBackward)
        button04 = wx.Button(panel, label = " << ")
        button04.Bind(wx.EVT_BUTTON, self.onFastFastBackward)

        button05 = wx.Button(panel, label = " Paus/Play ")
        button05.Bind(wx.EVT_BUTTON, self.onPause)

        hbox0.Add(button04)
        hbox0.Add(button03)
        hbox0.Add(button05)
        hbox0.Add(button01)
        hbox0.Add(button02)

        vbox.Add(hbox0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=100)
        vbox.Add((-1, 10))


        self.createTextFields(panel, vbox)


        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button1 = wx.Button(panel, label = "Submit")
        button1.Bind(wx.EVT_BUTTON, self.onSubmit)
        button2 = wx.Button(panel, label = "Clear")
        button2.Bind(wx.EVT_BUTTON, self.onClear)
        hbox2.Add(button1)
        hbox2.Add(button2)

        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        panel.SetSizer(vbox)

    def createTextFields(self, panel, vbox):
        c = 0
        hboxes = []
        for key, value in fields.items():
            if c%2 == 0:
                hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            st   = wx.StaticText(panel, label="  "+key+": ")
            st.SetFont(self.font)
            hbox1.Add(st, border=5)
            tc   = wx.TextCtrl(panel)
            tc.SetValue(value)
            hbox1.Add(tc, proportion=1, border=5)
            self.texts[key] = tc
            if c%2 == 1:
                vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
                #vbox.Add((-1, 10))
            c += 1
        if c%2 == 1:
            tc   = wx.StaticText(panel)
            hbox1.Add(tc, proportion=1, border=2)
            vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)




    def onFastBackward(self, e):
        currentPos = capture.get(cv2.CAP_PROP_POS_FRAMES)
        nextPos    = currentPos-20
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(nextPos) if nextPos > 0 else 0)
        print("%2f/%2f"%(nextPos,numFrames))

    def onFastFastBackward(self, e):
        currentPos = capture.get(cv2.CAP_PROP_POS_FRAMES)
        nextPos    = currentPos-numFrames/100
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(nextPos) if nextPos > 0 else 0)
        print("%2f/%2f"%(nextPos,numFrames))

    def onFastForward(self, e):
        currentPos = capture.get(cv2.CAP_PROP_POS_FRAMES)
        nextPos    = currentPos+20
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(nextPos) if nextPos < numFrames else currentPos)
        print("%2f/%2f"%(nextPos,numFrames))

    def onFastFastForward(self, e):
        currentPos = capture.get(cv2.CAP_PROP_POS_FRAMES)
        nextPos    = currentPos+numFrames/100
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(nextPos) if nextPos < numFrames else currentPos)
        print("%2f/%2f"%(nextPos,numFrames))

    def onClear(self, e):
        for key, t  in self.texts.items():
            t.SetValue('')

    def onSubmit(self, e):
        for key, t  in self.texts.items():
            print("%s: %s"%(key, t.GetValue()))
            t.SetValue('')

    def onPause(self, e):
        global pause
        pause = not pause

    def onClose(self, e):
        self.Close()



app = wx.App()
frame = Example(None)
frame.Show()
app.MainLoop()
