__author__ = 'tspycher'
import mongoengine
from app import Isa

class Takeoff(mongoengine.Document):
    ad_elv = mongoengine.IntField(required=True, default=0)
    qnh = mongoengine.IntField(required=True, default=int(Isa.base_qnh))
    oat = mongoengine.IntField(required=True, default=Isa.tmp_ams)

    def get_pa(self):
        delta_hpa = int(Isa.base_qnh) - self.qnh
        return self.ad_elv + (delta_hpa * Isa.ft_per_hpa)

    def get_da(self):
        x = (self.get_pa() / 1000) * Isa.subtract_c_per_tousandfeet
        y = Isa.tmp_ams - x
        z = (self.oat - y) * Isa.feet_per_c
        return self.get_pa() + z