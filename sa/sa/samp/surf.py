from .bitstream import *

class SurfData:
    def __init__(self, vehicle_id, offset):
        self.vehicle_id = vehicle_id
        self.offset = offset
    
    def __str__(self):
        return f'<SurfData vehicle_id={self.vehicle_id} offset={self.offset}>'

def read_compressed_surf_data(self, surf_data):
    if has_surf := self.read_bit():
        vehicle_id = self.read_i16()
        offset = self.read_vec3()
        if vehicle_id > 0:
            return SurfData(vehicle_id, offset)
    else:
        return None

def write_compressed_surf_data(self, surf_data):
    if surf_data != None and surf_data.vehicle_id > 0:
        self.write_bit(1)
        self.write_i16(surf_data.vehicle_id)
        self.write_vec3(surf_data.offset)
    else:
        self.write_bit(0)

def read_surf_data(self):
    offset = self.read_vec3()
    vehicle_id = self.read_i16()
    if vehicle_id > 0:
        return SurfData(vehicle_id, offset)
    else:
        return None

def write_surf_data(self, surf_data):
    self.write_vec3(surf_data.offset)
    self.write_i16(surf_data.vehicle_id)

Bitstream.read_surf_data = read_surf_data
Bitstream.write_surf_data = write_surf_data
Bitstream.read_compressed_surf_data = read_compressed_surf_data
Bitstream.write_compressed_surf_data = write_compressed_surf_data
