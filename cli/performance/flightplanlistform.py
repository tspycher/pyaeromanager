__author__ = 'tspycher'
import npyscreen
from app.documents.flightplan import Flightplan
from app.documents.aerodrome import Aerodrome
from app.documents.airplane import Airplane

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

        self.add(npyscreen.TitleText, name = "Text:", value= "Press Escape to quit application" )
        #self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application

        main = self.new_menu("Main Menu")
        main.addItemsFromList([
            ("New Flightplan", self._new_flightplan, "n"),
            ("New Aerodrome", self._new_aerodrome, "a"),
            ("New Airplane", self._new_airplane, "p"),

        ])

    def _new_flightplan(self):
        self.parentApp.getForm('FLIGHTPLAN').document = Flightplan()
        self.parentApp.switchForm('FLIGHTPLAN')

    def _new_aerodrome(self):
        self.parentApp.getForm('AERODROME').document = Aerodrome()
        self.parentApp.switchForm('AERODROME')

    def _new_airplane(self):
        self.parentApp.getForm('AIRPLANE').document = Airplane()
        self.parentApp.switchForm('AIRPLANE')

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.repository.getAllFlightplans()
        self.wMain.display()