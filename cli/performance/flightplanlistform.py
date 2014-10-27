__author__ = 'tspycher'
import npyscreen
from app.documents.flightplan import Flightplan

class FlightplanList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        self.parent.parentApp.getForm('FLIGHTPLAN').document = act_on_this
        self.parent.parentApp.switchForm('FLIGHTPLAN')

    def display_value(self, vl):
        return vl.title

class FlightplanListDisplay(npyscreen.FormMuttWithMenus):
    MAIN_WIDGET_CLASS = FlightplanList

    def create(self):
        super(FlightplanListDisplay, self).create()
        main = self.new_menu("Main Menu")
        main.addItemsFromList([
            ("New Flightplan", self._new_flightplan, "n"),
        ])

    def _new_flightplan(self):
        self.parentApp.getForm('FLIGHTPLAN').document = Flightplan()
        self.parentApp.switchForm('FLIGHTPLAN')

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.getFlightplans()
        self.wMain.display()