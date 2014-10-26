__author__ = 'tspycher'
import npyscreen
from app.documents.takeoff import Takeoff

class TakeoffForm(npyscreen.ActionForm):
    def create(self):
        self.document = Takeoff()
        self.ad_elv   = self.add(npyscreen.TitleText, name = "AD Elev. (ft):",)
        self.oat = self.add(npyscreen.TitleText, name = "OAT (C):")
        self.qnh = self.add(npyscreen.TitleText, name = "QNH (hpA):")
        self.pa = self.add(npyscreen.TitleFixedText, name = "PA:")
        self.da = self.add(npyscreen.TitleFixedText, name = "DA:")

    def beforeEditing(self):
        self.ad_elv.set_value(str(self.document.ad_elv))
        self.oat.set_value(str(self.document.oat))
        self.qnh.set_value(str(self.document.qnh))
        self.pa.set_value("0")
        self.da.set_value("0")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.ad_elv = int(self.ad_elv.get_value())
        self.document.oat = int(self.oat.get_value())
        self.document.qnh = int(self.qnh.get_value())

        self.pa.set_value(self.document.get_pa())
        self.da.set_value(self.document.get_da())

