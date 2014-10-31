__author__ = 'tspycher'
import mongoengine
from app.documents.flightplan.performance import Takeoff, Weightbalance
from app.documents.airplane import Airplane


class Flightplan(mongoengine.Document):
    performance_takeoff = mongoengine.EmbeddedDocumentField(Takeoff, default=Takeoff())
    performance_weightbalance = mongoengine.EmbeddedDocumentField(Weightbalance, default=Weightbalance())

    title = mongoengine.StringField(max_length=200, required=True, default="unnamed Flightplan")
    airplane = mongoengine.ReferenceField(Airplane, dbref=True)

    def __str__(self):
        return self.title