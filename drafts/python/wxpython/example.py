#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wx
APP_EXIT = 1

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        menubar     = wx.MenuBar()
        fileMenu    = wx.Menu()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        #qmi.SetBitmap(wx.Bitmap('exit.png'))
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.SetSize((300, 200))
        self.SetTitle('Simple menu')
        self.Centre()

    def onQuit(self, e):
        print("mardas")
        self.Close()

def main():
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
