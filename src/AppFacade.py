"""
Minimalist wxPython PureMVC demo, Version 1.0
Copyright (c) 2009 Andy Bulka, www.andypatterns.com
"""

import puremvc.patterns.facade

class AppFacade(puremvc.patterns.facade.Facade):
    STARTUP = "STARTUP"
    DATA_SUBMITTED = "DATA_SUBMITTED"
    DATA_CHANGED = "DATA_CHANGED"

    @staticmethod
    def getInstance():
        return AppFacade()

    def initializeController(self):
        super(AppFacade, self).initializeController()

        import sys
        if ".." not in sys.path:
            sys.path.append("..")
            
        from controller.StartupCommand import StartupCommand
        from controller.DataSubmittedCommand import DataSubmittedCommand

        super(AppFacade, self).registerCommand(AppFacade.STARTUP, StartupCommand)
        super(AppFacade, self).registerCommand(AppFacade.DATA_SUBMITTED, DataSubmittedCommand)

    def startup(self, app):
        self.sendNotification(AppFacade.STARTUP, app);
        