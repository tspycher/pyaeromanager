__author__ = 'tspycher'
import mongoengine
from app import Isa
from app.documents.aerodrome import Aerodrome

class Takeoff(mongoengine.EmbeddedDocument):
    RWY_TYPE_GRASS = 'grass'
    RWY_TYPE_ASPH = 'asph'

    qnh = mongoengine.IntField(required=True, default=int(Isa.base_qnh))
    oat = mongoengine.IntField(required=True, default=Isa.tmp_ams)

    rwy_no = mongoengine.IntField(required=False, default=0)
    rwy_lenght = mongoengine.IntField(required=False, default=1640)
    rwy_type = mongoengine.StringField(required=False, choices=[RWY_TYPE_GRASS, RWY_TYPE_ASPH], default=RWY_TYPE_ASPH)
    aerodrome = mongoengine.ReferenceField(Aerodrome, dbref=True, default=Aerodrome())

    def get_pa(self):
        delta_hpa = int(Isa.base_qnh) - self.qnh
        return self.aerodrome.msl + (delta_hpa * Isa.ft_per_hpa)

    def get_da(self):
        x = (self.get_pa() / 1000) * Isa.subtract_c_per_tousandfeet
        y = Isa.tmp_ams - x
        z = (self.oat - y) * Isa.feet_per_c
        return self.get_pa() + z