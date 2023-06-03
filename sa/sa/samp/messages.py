import enum
import struct

from .raknet import *
from sa.weapon import WEAPON
from sa.skin import SKIN
from sa.vehicle import VEHICLE

class DriverSync(Message):
    def __init__(self, driver_id, vehicle_id, lr_keys, ud_keys, keys, dir, pos, velocity, vehicle_health, driver_health, driver_armor, driver_weapon_id, additional_key, siren, landing_gear, trailer_id, extra):
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
        self.trailer_id = trailer_id 
        self.extra = extra # extra(4 bytes): vehicle specific; may be train_speed(float), bike_inclination(float) or hydra_thrust_angle(uint32)
        if self.extra != None:
            self.train_speed = self.bike_inclination = struct.unpack('f', extra)[0]
            self.hydra_thrust_angle = struct.unpack('I', extra)[0]

    def __str__(self):
        return f'<DriverSync driver_id={self.driver_id} vehicle_id={self.vehicle_id} lr_keys={self.lr_keys} ud_keys={self.ud_keys} keys={self.keys} dir={self.dir} pos={self.pos} velocity={self.velocity} vehicle_health={self.vehicle_health:.02f} driver_health={self.driver_health:.2f} driver_armor={self.driver_armor:.02f} driver_weapon_id={self.driver_weapon_id} additional_key={self.additional_key} siren={self.siren} landing_gear={self.landing_gear} trailer_id={self.trailer_id}' + (f'extra(train_speed=bike_inclination={self.train_speed:.02f}; hydra_thrust_angle={self.hydra_thrust_angle})>' if (self.extra != None) else '')

    def __len__(self):
        return 0
    
    @staticmethod
    def decode_server_payload(data):
        driver_id = vehicle_id = lr_keys = ud_keys = keys = rot = pos = velocity = vehicle_health = driver_health = driver_armor = driver_weapon_id = additional_key = siren = landing_gear = hydra_thrust_angle = trailer_id = extra = None
        
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
        
        siren = bs.read_bool()
        landing_gear = bs.read_bool()
        
        if has_extra := bs.read_bool():
            extra = bs.read_buffer(32)
        
        has_trailer = bs.read_bool()
        if has_trailer:
            trailer_id = bs.read_u16()
        
        return DriverSync(driver_id, vehicle_id, lr_keys, ud_keys, keys, dir, pos, velocity, vehicle_health, driver_health, driver_armor, driver_weapon_id, additional_key, siren, landing_gear, trailer_id, extra)
    
    @staticmethod
    def decode_client_payload(data):
        driver_id = vehicle_id = lr_keys = ud_keys = keys = dir = pos = velocity = vehicle_health = driver_health = driver_armor = driver_weapon_id = additional_key = siren = landing_gear = hydra_thrust_angle = trailer_id = None
    
        bs = Bitstream(data)
        vehicle_id = bs.read_u16()
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
        trailer_id = bs.read_u16()
        extra = bs.read_buffer(32)
        return DriverSync(None, vehicle_id, lr_keys, ud_keys, keys, dir, pos, velocity, vehicle_health, driver_health, driver_armor, driver_weapon_id, additional_key, siren, landing_gear, trailer_id, extra)
MSG.DRIVER_SYNC.decode_server_payload = DriverSync.decode_server_payload
MSG.DRIVER_SYNC.decode_client_payload = DriverSync.decode_client_payload


class RconCommand(Message):
    def __init__(self):
        super().__init__(MSG.RCON_COMMAND)

    def __str__(self):
        return f'<RconCommand>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass

    @staticmethod
    def decode_payload(data):
        return RconCommand()
MSG.RCON_COMMAND.encode_payload = RconCommand.encode_payload
MSG.RCON_COMMAND.decode_payload = RconCommand.decode_payload


class RconResponse(Message):
    def __init__(self):
        super().__init__(MSG.RCON_RESPONSE)

    def __str__(self):
        return f'<RconResponse>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass

    @staticmethod
    def decode_payload(data):
        return RconResponse()
MSG.RCON_RESPONSE.encode_payload = RconResponse.encode_payload
MSG.RCON_RESPONSE.decode_payload = RconResponse.decode_payload


class AimSync(Message):
    def __init__(self, player_id, cam_mode, dir, pos, aim_z, weapon_state, cam_zoom, aspect_ratio):
        super().__init__(MSG.AIM_SYNC)
        self.player_id = player_id
        self.cam_mode = cam_mode
        self.dir = dir # camera direction; euler angles(x, y z)
        self.pos = pos # camera position
        self.aim_z = aim_z
        self.weapon_state = weapon_state
        self.cam_zoom = cam_zoom
        self.aspect_ratio = aspect_ratio

    def __str__(self):
        return f'<AimSync player_id={self.player_id} cam_mode={self.cam_mode} dir={self.dir} pos={self.pos} aim_z={self.aim_z} weapon_state={self.weapon_state} cam_zoom={self.cam_zoom} aspect_ratio={self.aspect_ratio}>'

    def __len__(self):
        return 0

    def encode_payload(self):
        return b''
    
    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        mode = bs.read_u8()
        dir = bs.read_vec3()
        pos = bs.read_vec3() 
        aim_z = bs.read_float()
        zoom = bs.read_bits_num(6)
        weapon_state = bs.read_bits_num(2)
        aspect_ratio = bs.read_u8()
        return AimSync(None, mode, dir, pos, aim_z, weapon_state, zoom, aspect_ratio)
    
    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        player_id = bs.read_u16()
        mode = bs.read_u8()
        dir = bs.read_vec3()
        pos = bs.read_vec3()
        aim_z = bs.read_float()
        zoom = bs.read_bits_num(6)
        weapon_state = bs.read_bits_num(2)
        aspect_ratio = bs.read_u8()
        return AimSync(player_id, mode, dir, pos, aim_z, weapon_state, zoom, aspect_ratio)
MSG.AIM_SYNC.decode_server_payload = AimSync.decode_server_payload
MSG.AIM_SYNC.decode_client_payload = AimSync.decode_client_payload

class WeaponsUpdate(Message):
    def __init__(self):
        super().__init__(MSG.WEAPONS_UPDATE)

    def __str__(self):
        return f'<WeaponsUpdate>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass

    @staticmethod
    def decode_payload(data):
        return WeaponsUpdate()
MSG.WEAPONS_UPDATE.encode_payload = WeaponsUpdate.encode_payload
MSG.WEAPONS_UPDATE.decode_payload = WeaponsUpdate.decode_payload


class StatsUpdate(Message):
    def __init__(self, money, drunk_level):
        super().__init__(MSG.STATS_UPDATE)
        self.money = money
        self.drunk_level = drunk_level

    def __str__(self):
        return f'<StatsUpdate money={self.money} drunk_level={self.drunk_level}>'

    def __len__(self):
        return 8

    def encode_payload(self):
        return struct.pack('<II', self.money, self.drunk_level)

    @staticmethod
    def decode_payload(data):
        money, drunk_level = struct.unpack_from('<II', data)
        return StatsUpdate(money, drunk_level)
MSG.STATS_UPDATE.encode_payload = StatsUpdate.encode_payload
MSG.STATS_UPDATE.decode_payload = StatsUpdate.decode_payload


class BulletSync(Message):
    def __init__(self):
        super().__init__(MSG.BULLET_SYNC)

    def __str__(self):
        return f'<BulletSync>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass

    @staticmethod
    def decode_payload(data):
        return BulletSync()
MSG.BULLET_SYNC.encode_payload = BulletSync.encode_payload
MSG.BULLET_SYNC.decode_payload = BulletSync.decode_payload


class PlayerSync(Message):
    def __init__(self, player_id=None, lr_keys=None, ud_keys=None, keys=None, pos=None, dir=None, health=None, armor=None, additional_key=None, weapon_id=None, special_action=None, speed=None, surf_offset=None, surf_vehicle_id=None, animation_id=None, animation_flags=None):
        super().__init__(MSG.PLAYER_SYNC)
        self.player_id = player_id
        self.lr_keys = lr_keys
        self.ud_keys = ud_keys
        self.keys = keys
        self.pos = pos # player position; vec3
        self.dir = dir # player direction; quaternion
        self.health = health
        self.armor = armor
        self.additional_key = additional_key
        self.weapon_id = weapon_id
        self.special_action = special_action
        self.speed = speed
        self.surf_offset = surf_offset
        self.surf_vehicle_id = surf_vehicle_id
        self.animation_id = animation_id
        self.animation_flags = animation_flags

    def __str__(self):
        return f'<PlayerSync player_id={self.player_id} pos={self.pos} weapon_id={self.weapon_id} health={self.health} armor={self.armor} special_action={self.special_action} dir={self.dir} speed={self.speed} surf_offset={self.surf_offset} surf_vehicle_id={self.surf_vehicle_id} animation_id={self.animation_id} animation_flags={self.animation_flags} lr_keys={self.lr_keys} ud_keys={self.ud_keys} keys={self.keys} additional_key={self.additional_key}>'

    def __len__(self):
        return None

    def encode_payload(self):
        pass
        #additional_key_and_weapon_id = self.weapon_id | (self.additional_key << 6)
        #return struct.pack('<HHHfffffffBBBBffffffHHH', self.lr_keys, self.ud_keys, self.keys, self.pos.x, self.pos.y, self.pos.z, self.quat.w, self.quat.x, self.quat.y, self.quat.z, self.health, self.armor, additional_key_and_weapon_id, self.special_action, self.speed.x, self.speed.y, self.speed.z, self.surf_offset.x, self.surf_offset.y, self.surf_offset.z, self.surf_vehicle_id, self.animation_id, self.animation_flags)
        
    @staticmethod
    def decode_server_payload(data):
        lr_keys = ud_keys = keys = pos = rot = health = armor = additional_key = weapon_id = special_action = velocity = surf_offset = surf_vehicle_id = animation_id = animation_flags = None
    
        bs = Bitstream(data)
        player_id = bs.read_u16()
        
        if has_lr := bs.read_bool():
            lr_keys = bs.read_u16()
        else:
            lr_keys = 0
        
        if has_ud := bs.read_bool():
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
        velocity = bs.read_compressed_vec3()
        
        if has_surf := bs.read_bool():
            surf_vehicle_id = bs.read_u16()
            surf_offset = bs.read_vec3()
        
        if has_animation := bs.read_bool():
            animation_id = bs.read_u16()
            animation_flags = bs.read_u16()
        
        return PlayerSync(player_id, lr_keys, ud_keys, keys, pos, dir, health, armor, additional_key, weapon_id, special_action, velocity, surf_offset, surf_vehicle_id, animation_id, animation_flags)
    
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
        velocity = bs.read_vec3()
        surf_offset = bs.read_vec3()
        surf_vehicle_id = bs.read_u16()
        animation_id = bs.read_u16()
        animation_flags = bs.read_u16()
        return PlayerSync(None, lr_keys, ud_keys, keys, pos, dir, health, armor, additional_key, weapon_id, special_action, velocity, surf_offset, surf_vehicle_id, animation_id, animation_flags)
MSG.PLAYER_SYNC.decode_server_payload = PlayerSync.decode_server_payload   
MSG.PLAYER_SYNC.decode_client_payload = PlayerSync.decode_client_payload


class MarkersSync(Message):
    def __init__(self):
        super().__init__(MSG.MARKERS_SYNC)

    def __str__(self):
        return f'<MarkersSync>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass

    @staticmethod
    def decode_payload(data):
        return MarkersSync()
MSG.MARKERS_SYNC.encode_payload = MarkersSync.encode_payload
MSG.MARKERS_SYNC.decode_payload = MarkersSync.decode_payload


class UnoccupiedSync(Message):
    def __init__(self):
        super().__init__(MSG.UNOCCUPIED_SYNC)

    def __str__(self):
        return f'<UnoccupiedSync>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass
    
    @staticmethod
    def decode_payload(data):
        return UnoccupiedSync()
MSG.UNOCCUPIED_SYNC.encode_payload = UnoccupiedSync.encode_payload
MSG.UNOCCUPIED_SYNC.decode_payload = UnoccupiedSync.decode_payload


class TrailerSync(Message):
    def __init__(self):
        super().__init__(MSG.TRAILER_SYNC)

    def __str__(self):
        return f'<TrailerSync>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass

    @staticmethod
    def decode_payload(data):
        return TrailerSync()
MSG.TRAILER_SYNC.encode_payload = TrailerSync.encode_payload
MSG.TRAILER_SYNC.decode_payload = TrailerSync.decode_payload


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

    def __str__(self):
        return f'<PassengerSync passenger_id={self.passenger_id} vehicle_id={self.vehicle_id} seat_id={self.seat_id} drive_by={self.drive_by} passenger_weapon_id={self.passenger_weapon_id} additional_key={self.additional_key} passenger_health={self.passenger_health:.02f} passenger_armor={self.passenger_armor:.02f} lr_keys={self.lr_keys} ud_keys={self.ud_keys} keys={self.keys} pos={self.pos}>'

    def __len__(self):
        return 0

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
MSG.PASSENGER_SYNC.decode_server_payload = PassengerSync.decode_server_payload
MSG.PASSENGER_SYNC.decode_client_payload = PassengerSync.decode_client_payload


class SpectatorSync(Message):
    def __init__(self, lr_keys, ud_keys, keys, pos):
        super().__init__(MSG.SPECTATOR_SYNC)
        self.lr_keys = lr_keys
        self.ud_keys = ud_keys
        self.keys = keys
        self.pos = pos # player position as Vec3

    def __str__(self):
        return f'<SpectatorSync lr_keys={self.lr_keys} ud_keys={self.ud_keys} keys={self.keys} pos={self.pos}>'

    def __len__(self):
        return 0

    def encode_payload(self):
        pass
    
    @staticmethod
    def decode_client_payload(data):
        bs = Bitstream(data)
        lr_keys = bs.read_u16()
        ud_leys = bs.read_u16()
        keys = bs.read_u16()
        pos = bs.read_vec3()
        return SpectatorSync(lr_keys, ud_keys, keys, pos)
    
    @staticmethod
    def decode_server_payload(data):
        bs = Bitstream(data)
        
        has_lr = bs.read_bool()
        if has_lr:
            lr_keys = bs.read_u16()
        else:
            lr_keys = 0
        
        has_ud = bs.read_bool()
        if has_ud:
            ud_keys = bs.read_u16()
        else:
            ud_keys = 0
        
        keys = bs.read_u16()
        pos = bs.read_vec3()
        return SpectatorSync(lr_keys, ud_keys, keys, pos)
MSG.SPECTATOR_SYNC.encode_payload = SpectatorSync.encode_payload
MSG.SPECTATOR_SYNC.decode_server_payload = SpectatorSync.decode_server_payload
MSG.SPECTATOR_SYNC.decode_client_payload = SpectatorSync.decode_client_payload

for message in MSG:
    try:
        message.encode_client_payload = message.encode_payload
        message.encode_server_payload = message.encode_payload
    except AttributeError:
        pass
    try:
        message.decode_client_payload = message.decode_payload
        message.decode_server_payload = message.decode_payload
    except AttributeError:
        pass
