"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import puremvc.interfaces
import puremvc.patterns.command

import sys
if ".." not in sys.path:
    sys.path.append("..")

from model.DataModelProxy import DataModelProxy

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "submit execute (command)", notification.getBody()
        mydata = notification.getBody()
        self.datamodelProxy = self.facade.retrieveProxy(DataModelProxy.NAME)
        self.datamodelProxy.setData(mydata.upper())
        