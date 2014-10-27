__author__ = 'tspycher'
import mongoengine


class Airplane(mongoengine.Document):
    code = mongoengine.StringField(max_length=5, required=True, primary_key=True, unique=True)
    name = mongoengine.StringField(required=True)
    manufacturer = mongoengine.StringField(required=True)

    def __str__(self):
        return "%s %s (%s)" % (self.manufacturer, self.name, self.code)

