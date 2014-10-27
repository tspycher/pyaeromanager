__author__ = 'tspycher'

import npyscreen
from app.documents.flightplan import Flightplan

class FlightplanForm(npyscreen.ActionForm):
    document = None

    def create(self):
        if self.document is None:
            self.document = Flightplan()

        self.title = self.add(npyscreen.TitleText, name="Name:")
        self.add(npyscreen.ButtonPress, name="Takeoff Performance", when_pressed_function=self._show_takeoff_form)

    def _show_takeoff_form(self):
        self.parentApp.getForm('PERFORMANCE_TAKEOFF').document = self.document.performance_takeoff
        self.parentApp.switchForm('PERFORMANCE_TAKEOFF')

    def beforeEditing(self):
        self.title.set_value(self.document.title)

    def on_ok(self):
        self.document.save()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.title = self.title.get_value()
