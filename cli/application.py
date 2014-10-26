__author__ = 'tspycher'
import npyscreen
import curses
from cli.performance import TakeoffForm


class Splash(npyscreen.FormWithMenus):
    def create(self):
        main = self.new_menu("Main Menu")
        main.addItemsFromList([
            ("Exit Application", self.exit_application, "e"),
        ])

        performance = self.new_menu("Performance")
        performance.addItemsFromList([
            ("Takeoff", self.performance_takeoff, "t"),

        ])

    def performance_takeoff(self):
        self.parentApp.switchForm('PERFORMANCE_TAKEOFF')

    def exit_application(self):
        curses.beep()
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", TakeoffForm)
        self.addForm("PERFORMANCE_TAKEOFF", TakeoffForm)