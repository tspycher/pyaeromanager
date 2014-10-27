__author__ = 'tspycher'
import npyscreen

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
        self.ad_elv   = self.add(npyscreen.TitleFixedText, name = "AD Elev. (ft):",)
        self.aerodrome = self.add(npyscreen.TitleSelectOne, name="Aerodrome:", values=self.parentApp.repository.getAllAerodromes())

    def _edit_aerodrome(self):
        self.parentApp.getForm('AERODROME').document = self.aerodrome.get_selected_objects()[0]
        self.parentApp.switchForm('AERODROME')

    def beforeEditing(self):
        self.oat.set_value(str(self.document.oat))
        self.qnh.set_value(str(self.document.qnh))
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
        self.document.aerodrome = self.aerodrome.get_selected_objects()[0] if self.aerodrome.get_selected_objects() else None
        self._show_calculated()
