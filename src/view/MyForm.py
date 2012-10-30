"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import wx

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)
        