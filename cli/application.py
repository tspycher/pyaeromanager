__author__ = 'tspycher'

import npyscreen
import curses
from cli.performance import TakeoffForm, FlightplanForm, FlightplanListDisplay

from app.documents.flightplan import Flightplan

class Application(npyscreen.NPSAppManaged):
    currentFlightplan = None

    def setCurrentFlightplan(self, flightplan):
        self.currentFlightplan = flightplan

    def getFlightplans(self):
        return Flightplan.objects()

    def onStart(self):
        self.addForm("MAIN", FlightplanListDisplay)
        self.addForm("FLIGHTPLAN", FlightplanForm)
        self.addForm("PERFORMANCE_TAKEOFF", TakeoffForm)