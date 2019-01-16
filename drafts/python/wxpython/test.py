import wx
import cv2

pause = False

APP_PAUSE = 1
class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        menubar     = wx.MenuBar()
        fileMenu    = wx.Menu()
        qmi = wx.MenuItem(fileMenu, APP_PAUSE, '&Pause\tP')
        #qmi.SetBitmap(wx.Bitmap('exit.png'))
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.onPause, id=APP_PAUSE)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.SetSize((300, 200))
        self.SetTitle('Simple menu')
        self.Centre()

    def onPause(self, e):
        global pause
        pause = True


class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, size=(640, 480), fps=15):
        wx.Panel.__init__(self, parent)

        self.size = size
        self.capture = capture
        ret, frame = self.capture.read()
        frame = cv2.resize(frame, self.size)

        height, width = frame.shape[:2]
        parent.SetSize((width, height))
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

capture = cv2.VideoCapture()
capture.open('/Users/behnamrasoolian/Movies/Only.Lovers.Left.Alive.2013.720p.BluRay.x264.YIFY.mp4')
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

app = wx.App()
#frame = wx.Frame(None)
frame = Example(None)
cap = ShowCapture(frame, capture)
frame.Show()
app.MainLoop()
