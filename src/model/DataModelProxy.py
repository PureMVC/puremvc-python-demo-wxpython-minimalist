"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import puremvc.patterns.proxy

from Data import Data

import sys;
if ".." not in sys.path:
    sys.path.append("..")
   
from AppFacade import AppFacade

class DataModelProxy(puremvc.patterns.proxy.Proxy):
    NAME = "DataModelProxy"
    
    def __init__(self):
        super(DataModelProxy, self).__init__(DataModelProxy.NAME, [])
        self.realdata = Data()
        self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)

    def setData(self, data):
        self.realdata.data = data
        print "setData (model) to", data
        self.sendNotification(AppFacade.DATA_CHANGED, self.realdata.data)
        