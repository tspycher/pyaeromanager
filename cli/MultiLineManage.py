__author__ = 'tspycher'

import npyscreen

class MultilineManage(npyscreen.MultiLineAction):
    _action_on_x = None
    _action_on_enter = None

    def setActions(self,action_on_enter=None,action_on_x=None):
        self._action_on_enter = action_on_enter
        self._action_on_x = action_on_x

    def __init__(self,*args, **keywords):
        super(MultilineManage, self).__init__(*args, **keywords)

    def actionHighlighted(self, act_on_this, key_press):
        if key_press == 120:
            self._x_pressed(act_on_this)
        elif key_press == 10:
            self._enter_pressed(act_on_this)

        #npyscreen.notify_confirm(message=str(key_press), title="key Pressed")

    def _x_pressed(self, act_on_this):
        if self._action_on_x is not None:
            self._action_on_x(act_on_this)

    def _enter_pressed(self, act_on_this):
        if self._action_on_enter is not None:
            self._action_on_enter(act_on_this)