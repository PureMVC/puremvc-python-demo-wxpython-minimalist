"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import wx

from view.AppFrame import AppFrame

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
    