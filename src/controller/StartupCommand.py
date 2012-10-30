"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import puremvc.interfaces
import puremvc.patterns.command

import sys
if ".." not in sys.path:
    sys.path.append("..")

from view.MyFormMediator import MyFormMediator
from model.DataModelProxy import DataModelProxy
    
class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "startup execute (command)"
        wxapp = notification.getBody()
        self.facade.registerMediator(MyFormMediator(wxapp.myForm))
        self.facade.registerProxy(DataModelProxy())
        