__author__ = 'tspycher'
import npyscreen
from app.documents.airplane import Airplane

class AirplaneForm(npyscreen.ActionForm):
    document = None

    def create(self):
        if self.document is None:
            self.document = Airplane()

        self.code   = self.add(npyscreen.TitleText, name = "Code:",)
        self.name = self.add(npyscreen.TitleText, name = "Name:")
        self.manufacturer = self.add(npyscreen.TitleText, name = "Manufacturer:")

    def beforeEditing(self):
        self.code.set_value(str(self.document.code))
        self.name.set_value(str(self.document.name))
        self.manufacturer.set_value(str(self.document.manufacturer))

    def on_ok(self):
        self.document.save()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.code = self.code.get_value()
        self.document.name = self.name.get_value()
        self.document.manufacturer = self.manufacturer.get_value()
