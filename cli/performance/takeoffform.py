__author__ = 'tspycher'
import npyscreen
from app.documents.flightplan.performance import Takeoff

class TakeoffForm(npyscreen.ActionFormWithMenus):
    document = None

    def create(self):
        main = self.new_menu("Takeoff Menu")
        main.addItemsFromList([
            ("Edit selected Aerodrome", self._edit_aerodrome, "a"),
        ])
        self.oat = self.add(npyscreen.TitleText, name = "OAT (C):")
        self.qnh = self.add(npyscreen.TitleText, name = "QNH (hpA):")
        self.pa = self.add(npyscreen.TitleFixedText, name = "PA:")
        self.da = self.add(npyscreen.TitleFixedText, name = "DA:")
        self.rwy_lenght = self.add(npyscreen.TitleText, name = "RWY L (ft):")
        self.rwy_type = self.add(npyscreen.TitleSelectOne, max_height=2, scroll_exit=True, value=[0,], name = "RWY Type:", values=[Takeoff.RWY_TYPE_GRASS,Takeoff.RWY_TYPE_ASPH])
        self.rwy_no = self.add(npyscreen.TitleText, name = "RWY No:")
        self.ad_elv   = self.add(npyscreen.TitleFixedText, name = "AD El (ft):",)
        self.aerodrome = self.add(npyscreen.TitleSelectOne, name="Aerodrome:", max_height=2, value=[0,],  scroll_exit=True, values=self.parentApp.repository.getAllAerodromes())

    def _edit_aerodrome(self):
        self.parentApp.getForm('AERODROME').document = self.aerodrome.get_selected_objects()[0]
        self.parentApp.switchForm('AERODROME')

    def beforeEditing(self):
        self.oat.set_value(str(self.document.oat))
        self.qnh.set_value(str(self.document.qnh))
        self.rwy_lenght.set_value(str(self.document.rwy_lenght))
        self.rwy_type.set_value(str(self.document.rwy_type))
        self.rwy_no.set_value(str(self.document.rwy_no))
        self.ad_elv.set_value(str(self.document.aerodrome.msl))

        for i, val in enumerate(self.aerodrome.values):
            if val == self.document.aerodrome:
                self.aerodrome.value = i
                break

        self._show_calculated()

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def _show_calculated(self):
        self.pa.set_value(self.document.get_pa())
        self.da.set_value(self.document.get_da())
        self.ad_elv.set_value(self.document.aerodrome.msl)

    def while_editing(self, *args, **keywords):
        self.document.oat = int(self.oat.get_value())
        self.document.qnh = int(self.qnh.get_value())

        self.document.rwy_type = self.rwy_type.get_value()
        self.document.rwy_lenght = int(self.rwy_lenght.get_value())
        self.document.rwy_no = int(self.rwy_no.get_value())

        self.document.aerodrome = self.aerodrome.get_selected_objects()[0] if self.aerodrome.get_selected_objects() else None
        self._show_calculated()
