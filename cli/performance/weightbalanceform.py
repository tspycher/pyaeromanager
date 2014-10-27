__author__ = 'tspycher'
import npyscreen

class WeightbalanceForm(npyscreen.ActionFormWithMenus):
    document = None

    def create(self):
        self.weight = self.add(npyscreen.TitleText, name = "Weight (lbs):")

    def beforeEditing(self):
        self.weight.set_value(str(self.document.weight))

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.weight = int(self.weight.get_value())