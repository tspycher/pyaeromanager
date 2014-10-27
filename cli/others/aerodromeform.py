__author__ = 'tspycher'
import npyscreen
from app.documents.aerodrome import Aerodrome

class AerodromeForm(npyscreen.ActionForm):
    document = None

    def create(self):
        if self.document is None:
            self.document = Aerodrome()

        self.code   = self.add(npyscreen.TitleText, name = "Code:",)
        self.name = self.add(npyscreen.TitleText, name = "Name:")
        self.msl = self.add(npyscreen.TitleText, name = "MSL (ft):")

    def beforeEditing(self):
        self.code.set_value(str(self.document.code))
        self.name.set_value(str(self.document.name))
        self.msl.set_value(str(self.document.msl))

    def on_ok(self):
        self.document.save()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.code = self.code.get_value()
        self.document.name = self.name.get_value()
        self.document.msl = self.msl.get_value()
