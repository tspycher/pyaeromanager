__author__ = 'tspycher'

from app.documents.flightplan import Flightplan
from app.documents.aerodrome import Aerodrome
from app.documents.airplane import Airplane

class Repository(object):
    def getAllAirplanes(self):
        return Airplane.objects()
        
    def getAllAerodromes(self):
        return Aerodrome.objects()

    def getAllFlightplans(self):
        return Flightplan.objects()