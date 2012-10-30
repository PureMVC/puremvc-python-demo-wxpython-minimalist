#!/usr/bin/env python

"""
PureMVC minimalist wxpython example.  Version 1.0, March 2009.
Copyright (c) 2009 Andy Bulka, www.andypatterns.com

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

                    -----------

A blog explaining the code can be found at
http://www.andypatterns.com/index.php/blog/puremvc_minimal_wxpython/

This demo illustrates the simplest way (that I could think of) to build a
PureMVC application in python using wxPython as the GUI. A string in the model
is displayed in the GUI in a textfield. Anything you type gets converted to
uppercase and stored back in the model, courtesy of a command class triggered
when you hit the ENTER key in the GUI.

We are modelling and visualising a single string of a model class Data. If you
want to imagine a sequence diagram... On startup, the model's data is pushed
to the GUI. When the user hits ENTER in the GUI, the mediator picks up on this
wx event and broadcasts the pureMVC message DATA_SUBMITTED. A command class thus
gets triggered which converts the text to uppercase (this is the business logic)
and stuffs the info into the model. The model's setter broadcasts a DATA_CHANGED
message, which the mediator intercepts, updating the GUI.

Thus anything you type gets converted to uppercase and stored in the model.

"Model"
DataModelProxy is the proxy for class Data. The "Model" in pureMVC is the entire
system comprised of class Model (part of the pureMVC framework) which holds
references to one or more proxies (e.g. DataModelProxy) each of which looks
after a model (e.g. Data). Note that a model class could be more complex and the
associated proxy could look after looping and pulling out larger chunks of
information.

"View"
MyForm is the GUI, built in wxpython. MyFormMediator is the mediator which knows
about and specifically looks after MyForm, intercepting wx events from the GUI
and broadcasting pureMVC notification messages. The mediator also listens for
pureMVC notification messages and stuffs data back into the GUI. The "View" in
pureMVC is the entire system comprised of class View (part of the pureMVC
framework) which holds references to one or more mediators, each of which looks
after a GUI form or part of a GUI.

"Controller"
StartupCommand and DataSubmittedCommand are the command classes, triggered by
notification messages AppFacade.STARTUP and AppFacade.DATA_SUBMITTED
respectively. The "Controller" in pureMVC is the entire system comprised of
class Controller (part of the pureMVC framework) which holds references to one
or more commands.

The facade is a singleton and is where you define all messages types (all just
strings) and where you associate command classes with particular messages. There
can be messages NOT associated with commands, which are used for mediators to
listen to (e.g. model indirectly talking to mediators).

Notification messages have a .getName(), .getBody() and .getType(). Except for
the name, you can pass any info you like in the second two parameters, its up to
you. Typical parameters are references to forms, apps, data that has changed,
reference to objects, other string messages of your own devising. You could use
more than one parameter if say, you wanted to broadcast both the data that changed
and an actual reference to the object whose data had changed.
"""

import wx
import puremvc.interfaces
import puremvc.patterns.facade
import puremvc.patterns.command
import puremvc.patterns.mediator
import puremvc.patterns.proxy

class MyForm(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,id=3)
        self.inputFieldTxt = wx.TextCtrl(self, -1, size=(170,-1), pos=(5, 10), style=wx.TE_PROCESS_ENTER)

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


class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "startup execute (command)"
        wxapp = notification.getBody()
        self.facade.registerMediator(MyFormMediator(wxapp.myForm))
        self.facade.registerProxy(DataModelProxy())

class DataSubmittedCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, notification):
        print "submit execute (command)", notification.getBody()
        mydata = notification.getBody()
        self.datamodelProxy = self.facade.retrieveProxy(DataModelProxy.NAME)
        self.datamodelProxy.setData(mydata.upper())

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

class Data:
    def __init__(self):
        self.data = "Hello - hit enter"
    
class AppFacade(puremvc.patterns.facade.Facade):
    STARTUP = "STARTUP"
    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        super(AppFacade, self).registerCommand(AppFacade.STARTUP, StartupCommand)
        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)

    def startup(self, app):
        self.sendNotification(AppFacade.STARTUP, app);
        
class AppFrame(wx.Frame):
    myForm = None
    mvcfacade = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="PureMVC Minimalist Demo",size=(200,100))
        self.myForm = MyForm(parent=self)
        self.mvcfacade = AppFacade.getInstance()
        self.mvcfacade.startup(self)

class WxApp(wx.App):
    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        self.appFrame.Show()
        return True

if __name__ == '__main__':
    wxApp = WxApp(redirect=False)
    wxApp.MainLoop()
