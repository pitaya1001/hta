import enum
import struct

from .bitstream import *
from .raknet import Message, MSG
from sa.weapon import WEAPON
from sa.skin import SKIN
from sa.vehicle import VEHICLE

from .common import *

'''
These are raknet messages defined by SA-MP.

'''

''' S2C and C2S
Client sends this message when it is driving a vehicle
Server sends this message when there are players driving vehicles in the FOV of the client
'''
class DriverSync(Message):
    def __init__(self, driver_id, vehicle_id, lr_keys, ud_keys, keys, dir, pos, velocity, vehicle_health, driver_health, driver_armor, driver_weapon_id, additional_key, siren=0, landing_gear=0, trailer_id=None, extra=None):
        super().__init__(MSG.DRIVER_SYNC)
        self.driver_id = driver_id # player id of the driver
        self.vehicle_id = vehicle_id
        self.lr_keys = lr_keys
        self.ud_keys = ud_keys
        self.keys = keys
        self.dir = dir # vehicle direction as Quat
        self.pos = pos # vehicle position as Vec3
        self.velocity = velocity # vehicle velocity as Vec3
        self.vehicle_health = vehicle_health
        self.driver_health = driver_health
        self.driver_armor = driver_armor
        self.driver_weapon_id = driver_weapon_id
        self.additional_key = additional_key
        self.siren = siren # 1=on; 0=off
        self.landing_gear = landing_gear # landing_gear: 1 if retracted, 0 if in normal state
        self.trailer_id = trailer_id # None if invalid
        self.extra = extra # extra(4 bytes): vehicle specific; may be train_speed(float), bike_inclination(float) or hydra_thrust_angle(uint32)
        if self.extra != None:
            self.train_speed = self.bike_inclination = struct.unpack('f', extra)[0]
            self.hydra_thrust_angle = struct.unpack('I', extra)[0]
        else:
            self.train_speed = self.bike_inclination = self.hydra_thrust_angle = None

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_i16(self.driver_id)
        bs.write_i16(self.vehicle_id)
        bs.write_u16(self.lr_keys)
        bs.write_u16(self.ud_keys)
        bs.write_u16(self.keys)
        bs.write_norm_quat(self.dir)
        bs.write_vec3(self.pos)
        bs.write_compressed_vec3(self.velocity)
        bs.write_u16(self.vehicle_health)
        bs.write_u8(((int(self.driver_health)&0xff)//7<<4) | ((int(self.driver_armor)//7)&0x0f))
        bs.write_bits_num(self.driver_weapon_id, 6)
        bs.write_bits_num(self.additional_key, 2)
        bs.write_bit(self.siren)
        bs.write_bit(self.landing_gear)

        if self.has_extra != None:
            bs.write_bit(1)
            bs.write_buffer(self.extra, 32)
        else:
            bs.write_bit(0)

        if self.trailer_id != None:
            bs.write_bit(1)
            bs.write_i16(self.trailer_id)
        else:
            bs.write_bit(0)

        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_i16(self.vehicle_id)
        bs.write_u16(self.lr_keys)
        bs.write_u16(self.ud_keys)
        bs.write_u16(self.keys)
        bs.write_quat(self.dir)
        bs.write_vec3(self.pos)
        bs.write_vec3(self.velocity)
        bs.write_float(self.vehicle_health)
        bs.write_u8(self.driver_health)
        bs.write_u8(self.driver_armor)
        bs.write_bits_num(self.driver_weapon_id, 6)
        bs.write_bits_num(self.additional_key, 2)
        bs.write_u8(self.siren)
        bs.write_u8(self.landing_gear)
        bs.write_i16(self.trailer_id)

        if self.extra == None:
            bs.write_buffer(bytearray(4), 32)
        else:
            bs.write_buffer(self.extra, 32)

        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        driver_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        lr_keys = bs.read_u16()
        ud_keys = bs.read_u16()
        keys = bs.read_u16()
        dir = bs.read_norm_quat()
        pos = bs.read_vec3()
        velocity = bs.read_compressed_vec3()
        vehicle_health = bs.read_u16()

        health_armor_byte = bs.read_u8()
        driver_health = min(100, (health_armor_byte >> 4) * 7)
        driver_armor = min(100, (health_armor_byte & 0xf) * 7)

        driver_weapon_id = bs.read_bits_num(6)
        additional_key = bs.read_bits_num(2)
        siren = bs.read_bit()
        landing_gear = bs.read_bit()

        if has_extra := bs.read_bit():
            extra = bs.read_buffer(32)
        else:
            extra = None

        if has_trailer := bs.read_bit():
            trailer_id = bs.read_i16()
        else:
            trailer_id = None

        return DriverSync(driver_id, vehicle_id, lr_keys, ud_keys, keys, dir, pos, velocity, vehicle_health, driver_health, driver_armor, driver_weapon_id, additional_key, siren, landing_gear, trailer_id, extra)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        vehicle_id = bs.read_i16()
        lr_keys = bs.read_u16()
        ud_keys = bs.read_u16()
        keys = bs.read_u16()
        dir = bs.read_quat()
        pos = bs.read_vec3()
        velocity = bs.read_vec3()
        vehicle_health = bs.read_float()
        driver_health = bs.read_u8()
        driver_armor = bs.read_u8()
        driver_weapon_id = bs.read_bits_num(6)
        additional_key = bs.read_bits_num(2)
        siren = bs.read_u8()
        landing_gear = bs.read_u8()
        trailer_id = bs.read_i16()
        extra = bs.read_buffer(32)

        if trailer_id == -1:
            trailer_id = None

        return DriverSync(None, vehicle_id, lr_keys, ud_keys, keys, dir, pos, velocity, vehicle_health, driver_health, driver_armor, driver_weapon_id, additional_key, siren, landing_gear, trailer_id, extra)

class RconCommand(Message):
    def __init__(self, command):
        super().__init__(MSG.RCON_COMMAND)
        self.command = command

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_dynamic_buffer_u32(self.command.encode(SAMP_ENCODING))
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        command = bs.read_dynamic_buffer_u32().decode(SAMP_ENCODING)
        return RconCommand(command)

#class RconResponse(Message):
#    def __init__(self):
#        super().__init__(MSG.RCON_RESPONSE)
#
#    def encode_payload(self):
#        pass
#
#    @staticmethod
#    def decode_payload(data):
#        return RconResponse()

''' S2C and C2S
Client sends this message to sync its aim(e.g. where it's looking at)
'''
class AimSync(Message):
    def __init__(self, player_id, cam_mode, cam_dir, cam_pos, aim_z, weapon_state, cam_zoom, aspect_ratio):
        super().__init__(MSG.AIM_SYNC)
        self.player_id = player_id
        self.cam_mode = cam_mode
        self.cam_dir = cam_dir # camera direction as Vec3(euler angles)
        self.cam_pos = cam_pos # camera position as Vec3
        self.aim_z = aim_z
        self.weapon_state = weapon_state
        self.cam_zoom = cam_zoom
        self.aspect_ratio = aspect_ratio

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(self.player_id)
        bs.write_u8(self.mode)
        bs.write_vec3(self.cam_dir)
        bs.write_vec3(self.cam_pos)
        bs.write_float(self.aim_z)
        bs.write_bits_num(self.zoom, 6)
        bs.write_bits_num(self.weapon_state, 2)
        bs.write_u8(self.aspect_ratio)
        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u8(self.mode)
        bs.write_vec3(self.cam_dir)
        bs.write_vec3(self.cam_pos)
        bs.write_float(self.aim_z)
        bs.write_bits_num(self.zoom, 6)
        bs.write_bits_num(self.weapon_state, 2)
        bs.write_u8(self.aspect_ratio)
        return bs.data[:TO_BYTES(bs.len)]
        
    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_id = bs.read_u16()
        mode = bs.read_u8()
        cam_dir = bs.read_vec3()
        cam_pos = bs.read_vec3()
        aim_z = bs.read_float()
        zoom = bs.read_bits_num(6)
        weapon_state = bs.read_bits_num(2)
        aspect_ratio = bs.read_u8()
        return AimSync(player_id, mode, cam_dir, cam_pos, aim_z, weapon_state, zoom, aspect_ratio)
        
    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        mode = bs.read_u8()
        cam_dir = bs.read_vec3()
        cam_pos = bs.read_vec3()
        aim_z = bs.read_float()
        zoom = bs.read_bits_num(6)
        weapon_state = bs.read_bits_num(2)
        aspect_ratio = bs.read_u8()
        return AimSync(None, mode, cam_dir, cam_pos, aim_z, weapon_state, zoom, aspect_ratio)

''' C2S
The client sends this message to the server when:
 (1) The ammo of a weapon changes, e.g. when shooting so the ammo decreases
 (2) When starting/stopping to/from aiming at a player/actor
'''
class WeaponsUpdate(Message):
    def __init__(self, target_player_id=None, target_actor_id=None, weapons=[]):
        super().__init__(MSG.WEAPONS_UPDATE)
        self.target_player_id = target_player_id
        self.target_actor_id = target_actor_id
        self.weapons = weapons # [(slot, id, ammo), ...] ; up to 13 slots -> [0,12]

    def encode_client_payload(self):
        data = struct.pack('hh', -1 if self.target_player_id == None else self.target_player_id, -1 if self.target_actor_id == None else self.target_actor_id)
        for slot, id, ammo in self.weapons:
            data += struct.pack('BBH', slot, id, ammo)
        return data

    @staticmethod
    def decode_client_payload(data):
        target_player_id, target_actor_id = struct.unpack_from('hh', data)
        weapons = [weapon for weapon in struct.iter_unpack('BBH', data[4:])]
        return WeaponsUpdate(target_player_id, target_actor_id, weapons)

''' C2S
The client sends this message periodically to the server to inform the current money and drunk_level
'''
class StatsUpdate(Message):
    def __init__(self, money, drunk_level):
        super().__init__(MSG.STATS_UPDATE)
        self.money = money
        self.drunk_level = drunk_level

    def encode_server_payload(self):
        struct.pack('iI', self.money, self.drunk_level)

    @staticmethod
    def decode_client_payload(data):
        money, drunk_level = struct.unpack_from('iI', data)
        return StatsUpdate(money, drunk_level)

''' S2C and C2S
'''
class BulletSync(Message):
    def __init__(self, player_id, hit_type, hit_id, origin, hit_pos, offset, weapon_id):
        super().__init__(MSG.BULLET_SYNC)
        self.player_id = player_id
        self.hit_type = hit_type
        self.hit_id = hit_id
        self.origin = origin
        self.hit_pos = hit_pos
        self.offset = offset
        self.weapon_id = weapon_id

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(self.player_id)
        bs.write_u8(self.hit_type)
        bs.write_u16(self.hit_id)
        bs.write_vec3(self.origin)
        bs.write_vec3(self.hit_pos)
        bs.write_vec3(self.offset)
        bs.write_u8(self.weapon_id)
        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u8(self.hit_type)
        bs.write_u16(self.hit_id)
        bs.write_vec3(self.origin)
        bs.write_vec3(self.hit_pos)
        bs.write_vec3(self.offset)
        bs.write_u8(self.weapon_id)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_id = bs.read_u16()
        hit_type = bs.read_u8()
        hit_id = bs.read_u16()
        origin = bs.read_vec3()
        hit_pos = bs.read_vec3()
        offset = bs.read_vec3()
        weapon_id = bs.read_u8()
        return BulletSync(player_id, hit_type, hit_id, origin, hit_pos, offset, weapon_id)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        hit_type = bs.read_u8()
        hit_id = bs.read_u16()
        origin = bs.read_vec3()
        hit_pos = bs.read_vec3()
        offset = bs.read_vec3()
        weapon_id = bs.read_u8()
        return BulletSync(None, player_id, hit_type, hit_id, origin, hit_pos, offset, weapon_id)

''' S2C and S2C
'''
class PlayerSync(Message):
    def __init__(self, player_id, lr_keys=0, ud_keys=0, keys=0, pos=Vec3(0.0, 0.0, 2.0), dir=Vec3(0.0, 0.0, 0.0), health=0, armor=0, additional_key=0, weapon_id=0, special_action=0, vel=Vec3(0.0, 0.0, 0.0), surf_offset=None, surf_vehicle_id=None, animation_id=None, animation_flags=None):
        super().__init__(MSG.PLAYER_SYNC)
        self.player_id = player_id
        self.lr_keys = lr_keys
        self.ud_keys = ud_keys
        self.keys = keys
        self.pos = pos # Player position as Vec3
        self.dir = dir # Player direction as Quat
        self.health = health
        self.armor = armor
        self.additional_key = additional_key
        self.weapon_id = weapon_id
        self.special_action = special_action
        self.vel = vel # Player velocity as Vec3
        self.surf_offset = surf_offset
        self.surf_vehicle_id = surf_vehicle_id
        self.animation_id = animation_id
        self.animation_flags = animation_flags

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(self.player_id)

        if self.lr_keys != 0:
            bs.write_bit(1)
            bs.write_u16(self.lr_keys)
        else:
            bs.write_bit(0)

        if self.ud_keys != 0:
            bs.write_bit(1)
            bs.write_u16(self.ud_keys)
        else:
            bs.write_bit(0)

        bs.write_u16(self.keys)
        bs.write_vec3(self.pos)
        bs.write_norm_quat(self.dir)

        bs.write_u8(((int(self.health)&0xff)//7<<4) | ((int(self.armor)//7)&0x0f))

        bs.write_bits_num(self.weapon_id, 6)
        bs.write_bits_num(self.additional_key, 2)
        bs.write_u8(self.special_action)
        bs.write_compressed_vec3(self.vel)

        if self.surf_vehicle_id != None:
            bs.write_bit(1)
            bs.write_i16(self.surf_vehicle_id)
            bs.write_vec3(self.surf_offset)
        else:
            bs.write_bit(0)

        if self.animation_id != None:
            bs.write_bit(1)
            bs.write_i16(self.animation_id)
            bs.write_u16(self.animation_flags)
        else:
            bs.write_bit(0)

        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u16(self.lr_keys)
        bs.write_u16(self.ud_keys)
        bs.write_u16(self.keys)
        bs.write_vec3(self.pos)
        bs.write_quat(self.dir)
        bs.write_u8(self.health)
        bs.write_u8(self.armor)
        bs.write_bits_num(self.weapon_id, 6)
        bs.write_bits_num(self.additional_key, 2)
        bs.write_u8(self.special_action)
        bs.write_vec3(self.vel)
        bs.write_vec3(self.surf_offset)
        bs.write_i16(self.surf_vehicle_id)
        bs.write_i16(self.animation_id)
        bs.write_u16(self.animation_flags)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_id = bs.read_u16()

        if has_lr := bs.read_bit():
            lr_keys = bs.read_u16()
        else:
            lr_keys = 0

        if has_ud := bs.read_bit():
            ud_keys = bs.read_u16()
        else:
            ud_keys = 0

        keys = bs.read_u16()
        pos = bs.read_vec3()
        dir = bs.read_norm_quat()

        health_armor_byte = bs.read_u8()
        health = min(100, (health_armor_byte >> 4) * 7)
        armor = min(100, (health_armor_byte & 0xf) * 7)

        weapon_id = bs.read_bits_num(6)
        additional_key = bs.read_bits_num(2)
        special_action = bs.read_u8()
        vel = bs.read_compressed_vec3()

        if has_surf := bs.read_bit():
            surf_vehicle_id = bs.read_i16()
            surf_offset = bs.read_vec3()
        else:
            surf_vehicle_id = None
            surf_offset = None

        if has_animation := bs.read_bit():
            animation_id = bs.read_i16()
            animation_flags = bs.read_u16()
        else:
            animation_id = None
            animation_flags = None

        return PlayerSync(player_id, lr_keys, ud_keys, keys, pos, dir, health, armor, additional_key, weapon_id, special_action, vel, surf_offset, surf_vehicle_id, animation_id, animation_flags)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        lr_keys = bs.read_u16()
        ud_keys = bs.read_u16()
        keys = bs.read_u16()
        pos = bs.read_vec3()
        dir = bs.read_quat()
        health = bs.read_u8()
        armor = bs.read_u8()
        weapon_id = bs.read_bits_num(6)
        additional_key = bs.read_bits_num(2)
        special_action = bs.read_u8()
        vel = bs.read_vec3()
        surf_offset = bs.read_vec3()
        surf_vehicle_id = bs.read_i16()
        animation_id = bs.read_i16()
        animation_flags = bs.read_u16()

        if surf_vehicle_id == -1:
            surf_vehicle_id = None
            surf_offset = None

        if animation_id == -1:
            animation_id = None
            animation_flags = None

        return PlayerSync(None, lr_keys, ud_keys, keys, pos, dir, health, armor, additional_key, weapon_id, special_action, vel, surf_offset, surf_vehicle_id, animation_id, animation_flags)

''' S2C

'''
class MarkersSync(Message):
    def __init__(self, markers):
        super().__init__(MSG.MARKERS_SYNC)
        self.markers = [] # [(player_id, pos), ...]; pos may be None

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(len(self.markers))
        for player_id, pos in self.markers:
            bs.write_u16(player_id)
            if pos != None:
                bs.write_bit(1)
                bs.write_i16(int(pos.x))
                bs.write_i16(int(pos.y))
                bs.write_i16(int(pos.z))
            else:
                bs.write_bit(0)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_count = bs.read_u16()
        markers = [None] * player_count
        for i in range(player_count):
            player_id = bs.read_u16()
            if has_marker := bs.read_bit():
                pos = Vec3(bs.read_i16(), bs.read_i16(), bs.read_i16())
            else:
                pos = None
            markers[i] = (player_id, pos)
        return MarkersSync(markers)

''' S2C and C2S
Unoccupied means no one is in the vehicle
'''
class UnoccupiedVehicleSync(Message):
    def __init__(self, player_id, vehicle_id, seat_id, roll, rot, pos, vel, angular_vel, health):
        super().__init__(MSG.UNOCCUPIED_VEHICLE_SYNC)
        self.player_id = player_id
        self.vehicle_id = vehicle_id
        self.seat_id = seat_id
        self.roll = roll
        self.rot = rot
        self.pos = pos
        self.vel = vel
        self.angular_vel = angular_vel
        self.health = health

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(self.player_id)
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.seat_id)
        bs.write_vec3(self.roll)
        bs.write_vec3(self.rot)
        bs.write_vec3(self.pos)
        bs.write_vec3(self.vel)
        bs.write_vec3(self.angular_vel)
        bs.write_float(self.health)
        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.seat_id)
        bs.write_vec3(self.roll)
        bs.write_vec3(self.rot)
        bs.write_vec3(self.pos)
        bs.write_vec3(self.vel)
        bs.write_vec3(self.angular_vel)
        bs.write_float(self.health)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        seat_id = bs.read_u8()
        roll = bs.read_vec3()
        rot = bs.read_vec3()
        pos = bs.read_vec3()
        vel = bs.read_vec3()
        angular_vel = bs.read_vec3()
        health = bs.read_float()
        return UnoccupiedVehicleSync(player_id, vehicle_id, seat_id, roll, rot, pos, vel, angular_vel, health)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        vehicle_id = bs.read_u16()
        seat_id = bs.read_u8()
        roll = bs.read_vec3()
        rot = bs.read_vec3()
        pos = bs.read_vec3()
        vel = bs.read_vec3()
        angular_vel = bs.read_vec3()
        health = bs.read_float()
        return UnoccupiedVehicleSync(None, vehicle_id, seat_id, roll, rot, pos, vel, angular_vel, health)

''' S2C and C2S
'''
class TrailerSync(Message):
    def __init__(self, player_id, vehicle_id, pos, dir, vel, turn_vel):
        super().__init__(MSG.TRAILER_SYNC)
        self.player_id = player_id
        self.vehicle_id = vehicle_id
        self.pos = pos
        self.dir = dir
        self.vel = vel
        self.turn_vel = turn_vel

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(self.player_id)
        bs.write_u16(self.vehicle_id)
        bs.write_vec3(self.pos)
        bs.write_quat(self.dir)
        bs.write_vec3(self.vel)
        bs.write_vec3(self.turn_vel)
        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u16(self.vehicle_id)
        bs.write_vec3(self.pos)
        bs.write_quat(self.dir)
        bs.write_vec3(self.vel)
        bs.write_vec3(self.turn_vel)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        pos = bs.read_vec3()
        dir = bs.read_quat()
        vel = bs.read_vec3()
        turn_vel = bs.read_vec3()
        return TrailerSync(player_id, vehicle_id, pos, dir, vel, turn_vel)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        vehicle_id = bs.read_u16()
        pos = bs.read_vec3()
        dir = bs.read_quat()
        vel = bs.read_vec3()
        turn_vel = bs.read_vec3()
        return TrailerSync(None, vehicle_id, pos, dir, vel, turn_vel)

''' S2C and C2S
'''
class PassengerSync(Message):
    def __init__(self, passenger_id, vehicle_id, seat_id, drive_by, passenger_weapon_id, additional_key, passenger_health, passenger_armor, lr_keys, ud_keys, keys, pos):
        super().__init__(MSG.PASSENGER_SYNC)
        self.passenger_id = passenger_id
        self.vehicle_id = vehicle_id
        self.seat_id = seat_id
        self.drive_by = drive_by
        self.passenger_weapon_id = passenger_weapon_id
        self.additional_key = additional_key
        self.passenger_health = passenger_health
        self.passenger_armor = passenger_armor
        self.lr_keys = lr_keys
        self.ud_keys = ud_keys
        self.keys = keys
        self.pos = pos # passenger position; vec3

    def encode_server_payload(self):
        bs = Bitstream()
        bs.write_u16(self.passenger_id)
        bs.write_u16(self.vehicle_id)
        bs.write_bits_num(self.seat_id, 2)
        bs.write_bits_num(self.drive_by, 6)
        bs.write_bits_num(self.passenger_weapon_id, 6)
        bs.write_bits_num(self.additional_key, 2)
        bs.write_u8(self.passenger_health)
        bs.write_u8(self.passenger_armor)
        bs.write_u16(self.lr_keys)
        bs.write_u16(self.ud_keys)
        bs.write_u16(self.keys)
        bs.write_vec3(self.pos)
        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u16(self.vehicle_id)
        bs.write_bits_num(self.seat_id, 2)
        bs.write_bits_num(self.drive_by, 6)
        bs.write_bits_num(self.passenger_weapon_id, 6)
        bs.write_bits_num(self.additional_key, 2)
        bs.write_u8(self.passenger_health)
        bs.write_u8(self.passenger_armor)
        bs.write_u16(self.lr_keys)
        bs.write_u16(self.ud_keys)
        bs.write_u16(self.keys)
        bs.write_vec3(self.pos)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        passenger_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        seat_id = bs.read_bits_num(2)
        drive_by = bs.read_bits_num(6)
        passenger_weapon_id = bs.read_bits_num(6)
        additional_key = bs.read_bits_num(2)
        passenger_health = bs.read_u8()
        passenger_armor = bs.read_u8()
        lr_keys = bs.read_u16()
        ud_keys = bs.read_u16()
        keys = bs.read_u16()
        pos = bs.read_vec3()
        return PassengerSync(passenger_id, vehicle_id, seat_id, drive_by, passenger_weapon_id, additional_key, passenger_health, passenger_armor, lr_keys, ud_keys, keys, pos)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        vehicle_id = bs.read_u16()
        seat_id = bs.read_bits_num(2)
        drive_by = bs.read_bits_num(6)
        passenger_weapon_id = bs.read_bits_num(6)
        additional_key = bs.read_bits_num(2)
        passenger_health = bs.read_u8()
        passenger_armor = bs.read_u8()
        lr_keys = bs.read_u16()
        ud_keys = bs.read_u16()
        keys = bs.read_u16()
        pos = bs.read_vec3()
        return PassengerSync(None, vehicle_id, seat_id, drive_by, passenger_weapon_id, additional_key, passenger_health, passenger_armor, lr_keys, ud_keys, keys, pos)

''' S2C and C2S
'''
class SpectatorSync(Message):
    def __init__(self, lr_keys, ud_keys, keys, pos):
        super().__init__(MSG.SPECTATOR_SYNC)
        self.lr_keys = lr_keys
        self.ud_keys = ud_keys
        self.keys = keys
        self.pos = pos # player position as Vec3

    def encode_server_payload(self):
        bs = Bitstream()

        if self.lr_keys != 0:
            bs.write_bit(1)
            bs.write_u16(self.lr_keys)
        else:
            bs.write_bit(0)

        if self.ud_keys != 0:
            bs.write_bit(1)
            bs.write_u16(self.ud_keys)
        else:
            bs.write_bit(0)

        bs.write_u16(self.keys)
        bs.write_vec3(self.pos)

        return bs.data[:TO_BYTES(bs.len)]

    def encode_client_payload(self):
        bs = Bitstream()
        bs.write_u16(self.lr_keys)
        bs.write_u16(self.ud_keys)
        bs.write_u16(self.keys)
        bs.write_vec3(self.pos)
        return bs.data[:TO_BYTES(bs.len)]

    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)

        if has_lr := bs.read_bit():
            lr_keys = bs.read_u16()
        else:
            lr_keys = 0

        if has_ud := bs.read_bit():
            ud_keys = bs.read_u16()
        else:
            ud_keys = 0

        keys = bs.read_u16()
        pos = bs.read_vec3()
        return SpectatorSync(lr_keys, ud_keys, keys, pos)

    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        lr_keys = bs.read_u16()
        ud_keys = bs.read_u16()
        keys = bs.read_u16()
        pos = bs.read_vec3()
        return SpectatorSync(lr_keys, ud_keys, keys, pos)
