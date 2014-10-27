__author__ = 'tspycher'
import mongoengine

class Weightbalance(mongoengine.EmbeddedDocument):

    weight = mongoengine.IntField(required=True, default=0)