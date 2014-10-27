__author__ = 'tspycher'

import npyscreen
from cli.performance import TakeoffForm, FlightplanForm, FlightplanListDisplay
from cli.others import AerodromeForm, AirplaneForm
from .repository import Repository

class Application(npyscreen.NPSAppManaged):
    repository = None

    def onStart(self):
        self.repository = Repository()
        self.addForm("MAIN", FlightplanListDisplay)
        self.addForm("FLIGHTPLAN", FlightplanForm)
        self.addForm("PERFORMANCE_TAKEOFF", TakeoffForm)
        self.addForm("AERODROME", AerodromeForm)
        self.addForm("AIRPLANE", AirplaneForm)