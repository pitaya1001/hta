from sa.vehicle import Vehicle as SaVehicle

from .common import pretty_format

class Vehicle(SaVehicle):
    def __init__(self, id, model_id):
        super().__init__(id, model_id)
        self.plate = None

    def __str__(self):
        return pretty_format(self, 0)
