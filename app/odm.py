__author__ = 'tspycher'

import mongoengine

def connect():
    mongoengine.connect('flightplan')