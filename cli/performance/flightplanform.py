__author__ = 'tspycher'

import npyscreen
from app.documents.flightplan import Flightplan
from app import FlightplanBuilder

class FlightplanForm(npyscreen.ActionFormWithMenus):
    document = None

    def create(self):
        if self.document is None:
            self.document = Flightplan()

        main = self.new_menu("Flightplan Menu")
        main.addItemsFromList([
            ("Create PDF Flightplan", self._pdf_flightplan, "p"),
            ("Edit selected Airplane", self._edit_airplane, "a"),
        ])

        self.title = self.add(npyscreen.TitleText, name="Name:")
        self.add(npyscreen.ButtonPress, name="Takeoff Performance", when_pressed_function=self._show_takeoff_form)
        self.airplane = self.add(npyscreen.TitleSelectOne, name="Airplane:", max_height=2, value=[0,],  scroll_exit=True, values=self.parentApp.repository.getAllAirplanes())

    def _pdf_flightplan(self):
        return FlightplanBuilder(self.document).buildPdf()

    def _edit_airplane(self):
        self.parentApp.getForm('AIRPLANE').document = self.airplane.get_selected_objects()[0]
        self.parentApp.switchForm('AIRPLANE')

    def _show_takeoff_form(self):
        self.parentApp.getForm('PERFORMANCE_TAKEOFF').document = self.document.performance_takeoff
        self.parentApp.switchForm('PERFORMANCE_TAKEOFF')

    def beforeEditing(self):
        self.title.set_value(self.document.title)
        for i, val in enumerate(self.airplane.values):
            if val == self.document.airplane:
                self.airplane.value = i
                break

    def on_ok(self):
        self.document.save()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.title = self.title.get_value()
        self.document.airplane = self.airplane.get_selected_objects()[0] if self.airplane.get_selected_objects() else None

