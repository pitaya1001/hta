import enum

# https://team.sa-mp.com/wiki/Weapons.html
# https://www.open.mp/docs/scripting/resources/weaponids

class WEAPON(enum.IntEnum):
    FIST              = 0
    BRASS_KNUCKLE     = 1
    GOLF_CLUB         = 2
    NITE_STICK        = 3
    KNIFE             = 4
    BASEBALL_BAT      = 5
    SHOVEL            = 6
    POOL_STICK        = 7
    KATANA            = 8
    CHAINSAW          = 9
    DILDO             = 10
    DILDO2            = 11
    VIBRATOR          = 12
    VIBRATOR2         = 13
    FLOWERS           = 14
    CANE              = 15
    GRENADE           = 16
    TEAR_GAS          = 17
    MOLOTOV           = 18
    COLT45            = 22
    SILENCED_PISTOL   = 23
    DESERT_EAGLE      = 24
    SHOTGUN           = 25
    SAWEDOFF_SHOTGUN  = 26
    COMBAT_SHOTGUN    = 27
    UZI               = 28
    MP5               = 29
    AK47              = 30
    M4                = 31
    TEC9              = 32
    RIFLE             = 33
    SNIPER            = 34
    RPG               = 35
    HEAT_SEEKING_RPG  = 36
    FLAMETHROWER      = 37
    MINIGUN           = 38
    SATCHEL           = 39
    BOMB              = 40
    SPRAY_CAN         = 41
    FIRE_EXTINGUISHER = 42
    CAMERA            = 43
    NIGHT_VISION      = 44
    THERMAL_GOGGLES   = 45
    PARACHUTE         = 46
    FAKE_PISTOL       = 47
    VEHICLE           = 49
    HELICOPTER_BLADES = 50
    EXPLOSION         = 51
    DROWNED           = 53
    SPLAT             = 54
    CONNECT           = 200
    DISCONNECT        = 201
    SUICIDE           = 255
