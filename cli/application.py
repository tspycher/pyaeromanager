__author__ = 'tspycher'

import npyscreen
from cli.performance import TakeoffForm, FlightplanForm, FlightplanListDisplay, WeightbalanceForm
from cli.others import AerodromeForm, AirplaneForm, AirplaneChartForm
from .repository import Repository

class Application(npyscreen.NPSAppManaged):
    repository = None

    def onStart(self):
        #npyscreen.setTheme(npyscreen.Themes.TransparentThemeDarkText)
        npyscreen.notify("""Aeromanger 1.0
        2014/ by zerodine GmbH""")
        self.repository = Repository()
        self.addForm("MAIN", FlightplanListDisplay, name="Available Flightplans")
        self.addForm("FLIGHTPLAN", FlightplanForm, name="Flightplan Editor")
        self.addForm("PERFORMANCE_TAKEOFF", TakeoffForm, name="Takeoff Performance")
        self.addForm("AERODROME", AerodromeForm, name="Aerodrome")
        self.addForm("AIRPLANE", AirplaneForm, name="Airplane")
        self.addForm("AIRPLANECHART", AirplaneChartForm, name="Airplane")

        self.addForm("PERFORMANCE_WEIGHTBALANCE", WeightbalanceForm, name="Weight and Balance")