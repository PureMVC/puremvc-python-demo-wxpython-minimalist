"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import wx

from MyForm import MyForm

import sys
if ".." not in sys.path:
    sys.path.append("..")

from AppFacade import AppFacade

class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="PureMVC Minimalist Demo",size=(200,100))
        self.myForm = MyForm(parent=self)
        self.mvcfacade = AppFacade.getInstance()
        self.mvcfacade.startup(self)
        