__author__ = 'tspycher'
import time

class Isa(object):
    """
    Class which describes the ideal athmosphere
    """

    ft_per_hpa = 27
    subtract_c_per_tousandfeet = 2
    feet_per_c = 120
    base_qnh = 1013.25
    tmp_ams = 15

    earliest_sunset = "16:30"
    latest_sunrise = "08:30"

    def __set__(self, instance, value):
        raise Exception("not allowed to edit parameters")