import wx
import cv2

import numpy as np
import cv2
import random
import string
import time

import logging

num_test_episodes = 3
num_episodes = 5
episode_length = 2

class ShowCapture(wx.Panel):
    def __init__(self, parent, size=(640, 640), fps=15):
        self.print = False
        wx.Panel.__init__(self, parent)

        self.mode = 'test'
        self.size = size
        self.start = time.time()
        self.ResetImage()

        height, width = size
        parent.SetSize((width, height))

        self.bmp = wx.BitmapFromBuffer(width, height, self.img)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.episode = 0
        self.answers = []
        self.c = ''

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

        self.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
        #self.Bind(wx.EVT_TEXT, self.KeyDown)

        #main_sizer = wx.BoxSizer(wx.VERTICAL)
        #font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        #self.solution = wx.TextCtrl(self, style=wx.TE_RIGHT)
        #self.solution.SetFont(font)
        #self.solution.Bind(wx.EVT_TEXT, self.KeyDown)
        #main_sizer.Add(self.solution, 0, wx.EXPAND|wx.ALL, 5)
        #self.running_total = wx.StaticText(self)
        #main_sizer.Add(self.running_total, 0, wx.ALIGN_RIGHT)

    def ResetImage(self, printAnswer=False, scale=1):
        M, N = self.size
        pad = 0
        self.img = np.zeros((M + pad, N + pad, 3)).astype(np.uint8)
        font = cv2.FONT_HERSHEY_COMPLEX
        if self.mode == 'wait':
            text = 'press Space to continue...'
            cv2.putText(self.img,text,(150*scale,200*scale), font, 1, 255, 4*scale, cv2.LINE_AA)
        else:
            imgs = [[None, None], [None, None]]
            imgs[0][0] = self.img[pad//2:M//2, pad//2:N//2]
            imgs[0][1] = self.img[pad+M//2:M+pad]
            imgs[1][0] = self.img[pad//2:M//2, pad+N//2:N]
            imgs[1][1] = self.img[pad+M//2:M, pad+N//2:N]

            imgs[0][1][:, :] = [50, 50, 50]
            imgs[1][0][:, :] = [100, 100, 100]
            imgs[1][1][:, :] = [200, 200, 200]

            index = random.randint(0, 3)
            i = index // 2
            j = index % 2
            letter = random.choice(string.ascii_letters).upper()
            digit = random.randint(1, 9)
            text = "%s%d"%(letter, digit)
            #text = 'b2'
            cv2.putText(imgs[i][j],text,(100*scale,100*scale), font, 4, 255, 4*scale, cv2.LINE_AA)

            vowels = ['A', 'E', 'I', 'O', 'U']
            self.correct = ""
            if i == 0:
                self.correct = 'N' if letter in vowels else 'B'
            else:
                self.correct = 'B' if digit % 2 else 'N'

            #for test cases, the correct answer is shown
            if printAnswer:
                cv2.putText(self.img, 'Correct answer: %s'%self.correct, (100, 500), font, 1, 255, 4*scale, cv2.LINE_AA)
        #cv2.putText(self.img, 'Current answer: %s'%self.correct, (500, 600), font, .2, 255, 1*scale, cv2.LINE_AA)


    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        #print(time.time() - self.start)
        if time.time() - self.start > episode_length:
            self.episode += 1
            self.start = time.time()
            # gather current state: user answer and correct answer
            # You could capture a copy of the image for reporting purposes
            self.answers.append((self.c, self.correct))
            #increment episode
            #reset answer
            #for test cases, the correct answer is shown
            if self.mode == 'test':
                print(time.time()-self.start)
                if time.time() - self.start > episode_length / 5:
                    self.ResetImage(printAnswer=True)
                if self.episode == num_test_episodes:
                    self.mode = 'wait'
            elif self.mode == 'wait':
                if self.c == ' ':
                    self.mode = 'actual'
                    self.episode = 0
                else:
                    return
            elif self.episode >= num_episodes:
                self.c = ''
                #print answers only once
                if not self.print:
                    print(self.answers)
                    self.print = True
                #self.Destroy()
                return
            self.ResetImage()
            self.bmp.CopyFromBuffer(self.img)
            self.Refresh()

    def KeyDown(self, event=None):
        logging.warning("OnKeyDown event %s" % (event))
        keycode = event.GetUnicodeKey()
        self.c = chr(keycode)
        print(self.c)


app = wx.App()
frame = wx.Frame(None)
cap = ShowCapture(frame)
frame.Show()
app.MainLoop()
