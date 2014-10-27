__author__ = 'tspycher'
import mongoengine

class Aerodrome(mongoengine.Document):
    code = mongoengine.StringField(max_length=4, required=True, primary_key=True, unique=True)
    name = mongoengine.StringField(required=True)
    msl = mongoengine.IntField(default=0)

    def __str__(self):
        return "%s - %s" % (self.code, self.name)

