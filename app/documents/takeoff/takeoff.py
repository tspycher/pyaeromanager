__author__ = 'tspycher'
import mongoengine
from app import Isa

class Takeoff(mongoengine.Document):
    ad_elv = mongoengine.IntField(required=True,default=0)
    qnh = mongoengine.FloatField(required=True,default=0)
    oat = mongoengine.FloatField(required=True,default=0)

    def get_pa(self):
        delta_hpa = Isa.base_qnh - float(self.qnh)

        return self.ad_elv + (delta_hpa * Isa.ft_per_hpa)
