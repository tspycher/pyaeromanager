__author__ = 'tspycher'
import npyscreen
from app.documents.flightplan.performance import Takeoff
from pprint import pformat

class TakeoffForm(npyscreen.FormMultiPageActionWithMenus):
    document = None

    def create(self):
        main = self.new_menu("Takeoff Menu")
        main.addItemsFromList([
            ("Edit selected Aerodrome", self._edit_aerodrome, "a"),
        ])

        self.lt = self.add(npyscreen.TitleDateCombo, name = "LT:")
        self.oat = self.add(npyscreen.TitleText, name = "OAT (C):")
        self.qnh = self.add(npyscreen.TitleText, name = "QNH (hpA):")
        self.pa = self.add(npyscreen.TitleFixedText, name = "PA:")
        self.da = self.add(npyscreen.TitleFixedText, name = "DA:")
        self.ad_elv   = self.add(npyscreen.TitleFixedText, name = "AD El (ft):",)
        self.add_page()

        self.rwy_lenght = self.add(npyscreen.TitleText, name="RWY L (ft):")
        self.rwy_type = self.add(npyscreen.TitleSelectOne, max_height=2, scroll_exit=True, value=[0,], name="RWY Type:", values=[Takeoff.RWY_TYPE_GRASS, Takeoff.RWY_TYPE_ASPH])
        self.rwy_no = self.add(npyscreen.TitleText, name = "RWY No:")
        self.rwy_percent_additional = self.add(npyscreen.TitleText, name = "RWY Add (%):")
        self.aerodrome = self.add(npyscreen.TitleSelectOne, name="Aerodrome:", max_height=2, value=[0,], scroll_exit=True, values=self.parentApp.repository.getAllAerodromes())
        self.add_page()

        self.flaps = self.add(npyscreen.TitleText, name = "Flaps (grd):")
        self.wind_kt = self.add(npyscreen.TitleText, name = "Wind kt:")
        self.wind_dir_head = self.add(npyscreen.TitleSelectOne, name = "Wind dir:", scroll_exit=True, values=[Takeoff.WIND_TAIL, Takeoff.WIND_HEAD])
        self.add_page()

        self.add(npyscreen.FixedText, value="Please consult the airplane charts to get the following values")
        self.tkoff_gr_roll = self.add(npyscreen.TitleText, name = "TO Ground Roll:")
        self.tkoff_performance = self.add(npyscreen.TitleText, name = "TO Performance:")
        self.tkoff_total_gr_roll = self.add(npyscreen.TitleFixedText, name = "SUM TO Ground Roll:")
        self.tkoff_total_performance = self.add(npyscreen.TitleFixedText, name = "SUM Performance:")
        self.switch_page(0)

    def _edit_aerodrome(self):
        self.parentApp.getForm('AERODROME').document = self.aerodrome.get_selected_objects()[0]
        self.parentApp.switchForm('AERODROME')

    def beforeEditing(self):
        self.lt.set_value(str(self.document.localtime))
        self.oat.set_value(str(self.document.oat))
        self.qnh.set_value(str(self.document.qnh))

        #self.rwy_type.set_value(str(self.document.rwy_type))
        self.rwy_type.value = [self.rwy_type.values.index(str(self.document.rwy_type)), ]
        self.rwy_lenght.set_value(str(self.document.rwy_lenght))
        self.rwy_no.set_value(str(self.document.rwy_no))
        self.rwy_percent_additional.set_value(str(self.document.rwy_percent_additional))
        for i, val in enumerate(self.aerodrome.values):
            if val == self.document.aerodrome:
                self.aerodrome.value = i
                break

        self.flaps.set_value(str(self.document.flaps))
        self.wind_kt.set_value(str(self.document.wind_kt))
        self.wind_dir_head.set_value(int(self.document.wind_dir_head))

        self.tkoff_gr_roll.set_value(str(self.document.tkoff_gr_roll))
        self.tkoff_performance.set_value(str(self.document.tkoff_performance))

        self._show_calculated()

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def _show_calculated(self):
        self.pa.set_value(self.document.get_pa())
        self.da.set_value(self.document.get_da())
        self.ad_elv.set_value(self.document.aerodrome.msl)
        self.tkoff_total_gr_roll.set_value(self.document.get_total_to_groundroll())
        self.tkoff_total_performance.set_value(self.document.get_total_to_performance())

    def while_editing(self, *args, **keywords):
        #self.document.localtime = int(self.lt.get_value())
        self.document.oat = int(self.oat.get_value())
        self.document.qnh = int(self.qnh.get_value())

        self.document.rwy_type = str(self.rwy_type.values[self.rwy_type.value[0]])
        self.document.rwy_lenght = int(self.rwy_lenght.get_value())
        self.document.rwy_no = int(self.rwy_no.get_value())
        self.document.rwy_percent_additional = int(self.rwy_percent_additional.get_value())
        self.document.aerodrome = self.aerodrome.get_selected_objects()[0] if self.aerodrome.get_selected_objects() else None

        self.document.flaps = int(self.flaps.get_value())
        self.document.wind_kt = int(self.wind_kt.get_value())
        self.document.wind_dir_head = True if self.flaps.get_value() == 1 else False

        self.document.tkoff_gr_roll = int(self.tkoff_gr_roll.get_value())
        self.document.tkoff_performance = int(self.tkoff_performance.get_value())

        self._show_calculated()
