__author__ = 'tspycher'
import mongoengine
from app import Isa
from app.documents.aerodrome import Aerodrome
from datetime import datetime

class Takeoff(mongoengine.EmbeddedDocument):
    RWY_TYPE_GRASS = 'grass'
    RWY_TYPE_ASPH = 'asph'

    WIND_HEAD = 'head'
    WIND_TAIL = 'tail'

    qnh = mongoengine.IntField(required=True, default=int(Isa.base_qnh))
    oat = mongoengine.IntField(required=True, default=Isa.tmp_ams)

    rwy_no = mongoengine.IntField(required=False, default=0)
    rwy_lenght = mongoengine.IntField(required=False, default=1640)
    rwy_type = mongoengine.StringField(required=False, default=RWY_TYPE_ASPH )#, choices=[RWY_TYPE_GRASS, RWY_TYPE_ASPH])
    rwy_percent_additional = mongoengine.IntField(required=False, default=0)

    aerodrome = mongoengine.ReferenceField(Aerodrome, dbref=True, default=Aerodrome())

    wind_kt = mongoengine.IntField(required=False, default=0)
    wind_dir_head = mongoengine.BooleanField(default=False)
    flaps = mongoengine.IntField(required=False, default=0)

    tkoff_gr_roll = mongoengine.IntField(required=False, default=0)
    tkoff_performance = mongoengine.IntField(required=False, default=0)

    localtime = mongoengine.DateTimeField(required=True, default=datetime.now())

    def get_pa(self):
        delta_hpa = int(Isa.base_qnh) - self.qnh
        return self.aerodrome.msl + (delta_hpa * Isa.ft_per_hpa)

    def get_da(self):
        x = (self.get_pa() / 1000) * Isa.subtract_c_per_tousandfeet
        y = Isa.tmp_ams - x
        z = (self.oat - y) * Isa.feet_per_c
        return self.get_pa() + z

    def get_local_utc(self):
        return self.localtime

    def get_total_to_groundroll(self):
        return int(self.tkoff_gr_roll) / 100 * (100+int(self.rwy_percent_additional))

    def get_total_to_performance(self):
        return int(self.get_total_to_groundroll()) + (int(self.tkoff_performance)-int(self.tkoff_gr_roll))

    def get_wind_dir(self):
        if self.wind_dir_head:
            return self.WIND_HEAD
        return self.WIND_TAIL