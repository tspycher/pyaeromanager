__author__ = 'tspycher'
import npyscreen
from app.documents.airplane import Airplane, PerformanceChart
from cli import MultilineManage

class AirplaneChartForm(npyscreen.ActionPopup):
    parent_document = None
    document = None
    update = False

    def create(self):
        self.name = self.add(npyscreen.TitleText, name="Name:")
        self.description = self.add(npyscreen.TitleText, name="Descr.:")
        self.add(npyscreen.MiniButtonPress, name="Select File", when_pressed_function=self._select_file)

    def _select_file(self):
        t = npyscreen.selectFile('~/',confirm_if_exists=False, must_exist=True)
        chartFile = open(t, 'rb')
        self.document.file.put(chartFile)

    def beforeEditing(self):
        if self.document is None:
            self.document = PerformanceChart()

        self.name.set_value(str(self.document.name))
        self.description.set_value(str(self.document.description))

    def on_ok(self):
        if self.update:
            pass
        else:
            self.parent_document.charts.append(self.document)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.name = self.name.get_value()
        self.document.description = self.description.get_value()


class AirplaneForm(npyscreen.ActionForm): #.FormMultiPageAction):
    document = None

    def create(self):
        if self.document is None:
            self.document = Airplane()

        self.code   = self.add(npyscreen.TitleText, name = "Code:",)
        self.name = self.add(npyscreen.TitleText, name = "Name:")
        self.manufacturer = self.add(npyscreen.TitleText, name = "Manufacturer:")
        self.add(npyscreen.MiniButtonPress, name="Add Chart", when_pressed_function=self._new_Chart)
        self.charts = self.add(MultilineManage, name="Available Charts:", slow_scroll=False, scroll_exit=True)
        self.charts.setActions(action_on_enter=self._select_Chart, action_on_x=self._delete_Chart)

    def _delete_Chart(self, act_on_this):
        self.document.charts.remove(act_on_this)
        self.charts.values = self.document.charts

    def _select_Chart(self, act_on_this):
        self.parentApp.getForm('AIRPLANECHART').parent_document = self.document
        self.parentApp.getForm('AIRPLANECHART').document = act_on_this
        self.parentApp.getForm('AIRPLANECHART').update = True
        self.parentApp.switchForm('AIRPLANECHART')

    def _new_Chart(self):
        self.parentApp.getForm('AIRPLANECHART').parent_document = self.document
        self.parentApp.getForm('AIRPLANECHART').document = None
        self.parentApp.getForm('AIRPLANECHART').update = False
        self.parentApp.switchForm('AIRPLANECHART')

    def beforeEditing(self):
        self.code.set_value(str(self.document.code))
        self.name.set_value(str(self.document.name))
        self.manufacturer.set_value(str(self.document.manufacturer))
        self.charts.values = self.document.charts

    def on_ok(self):
        self.document.save()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def while_editing(self, *args, **keywords):
        self.document.code = self.code.get_value()
        self.document.name = self.name.get_value()
        self.document.manufacturer = self.manufacturer.get_value()
