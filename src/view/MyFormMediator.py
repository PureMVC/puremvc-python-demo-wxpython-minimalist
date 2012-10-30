"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import wx
import puremvc.interfaces
import puremvc.patterns.mediator

import sys
if ".." not in sys.path:
    sys.path.append("..")

from AppFacade import AppFacade

class MyFormMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
    NAME = 'MyFormMediator'

    def __init__(self, viewComponent):
        super(MyFormMediator, self).__init__(MyFormMediator.NAME, viewComponent)
        self.viewComponent.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.viewComponent.inputFieldTxt)
        
    def listNotificationInterests(self):
        return [ AppFacade.DATA_CHANGED ]

    def handleNotification(self, notification):
        if notification.getName() == AppFacade.DATA_CHANGED:
            print "handleNotification (mediator) got", notification.getBody()
            mydata = notification.getBody()
            self.viewComponent.inputFieldTxt.SetValue(mydata)

    def onSubmit(self, evt):
        mydata = self.viewComponent.inputFieldTxt.GetValue()
        self.sendNotification(AppFacade.DATA_SUBMITTED, mydata)