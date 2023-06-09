import enum

from .bitstream import *
from .common import *
from .huffman_encoding import default_huffman_tree
from sa import *

'''
Overview

When the RPC has no "target" in the name(e.g. SetPos, ) it likely refers to the character of the player the RPC is sent to.

e.g. SetHealth(50) sets the health of the character of the player you send to RPC to.
If there is 'Player' in the name, it likely refers to a specific player where you may need to specify the player id.


Related: list of words related to the RPC; useful for finding something with CTRL+F if you know an alternate name
'''

# samp rpc ids
class RPC(enum.IntEnum):
    SET_PLAYER_NAME             = 11  # SetPlayerName
    SET_POS                     = 12  # SetPos
    SET_POS_FIND_Z              = 13  # SetPosFindZ
    SET_HEALTH                  = 14  # SetHealth
    TOGGLE_CONTROLLABLE         = 15  # ToggleControllable
    PLAY_SOUND                  = 16  # PlaySound
    SET_WORLD_BOUNDS            = 17  # SetWorldBounds
    GIVE_MONEY                  = 18  # GiveMoney
    SET_DIR_Z                   = 19  # SetDirZ
    RESET_MONEY                 = 20  # ResetMoney
    REMOVE_ALL_WEAPONS          = 21  # RemoveAllWeapons
    GIVE_WEAPON                 = 22  # GiveWeapon
    CLICK_SCOREBOARD_PLAYER     = 23  # ClickScoreboardPlayer
    SET_VEHICLE_PARAMS_EX       = 24  # SetVehicleParamsEx
    CLIENT_JOIN                 = 25  # ClientJoin
    PLAYER_ENTER_VEHICLE        = 26  # PlayerEnterVehicle
    ENTER_VEHICLE               = 26  # EnterVehicle
    ENTER_EDIT_OBJECT           = 27  # EnterEditObject
    CANCEL_EDIT_OBJECT          = 28  # CancelEditObject
    SET_TIME                    = 29  # SetTime
    TOGGLE_CLOCK                = 30  # ToggleClock
    START_PLAYER_STREAM         = 32  # StartPlayerStream
    SET_SHOP_NAME               = 33  # SetShopName
    SET_PLAYER_SKILL_LEVEL      = 34  # SetPlayerSkillLevel
    SET_DRUNK_LEVEL             = 35  # SetDrunkLevel
    SHOW_3D_TEXT_LABEL          = 36  # Show3DTextLabel
    DISABLE_CHECKPOINT          = 37  # DisableCheckpoint
    SHOW_RACE_CHECKPOINT        = 38  # ShowRaceCheckpoint
    HIDE_RACE_CHECKPOINT        = 39  # HideRaceCheckpoint
    GAME_MODE_RESTART           = 40  # GameModeRestart
    PLAY_AUDIO_STREAM           = 41  # PlayAudioStream
    STOP_AUDIO_STREAM           = 42  # StopAudioStream
    REMOVE_BUILDING             = 43  # RemoveBuilding
    CREATE_OBJECT               = 44  # CreateObject
    SET_OBJECT_POS              = 45  # SetObjectPos
    SET_OBJECT_ROTATION         = 46  # SetObjectRotation
    DESTROY_OBJECT              = 47  # DestroyObject
    REQUEST_CHAT_COMMAND        = 50  # RequestChatCommand
    SEND_SPAWN                  = 52  # SendSpawn
    DEATH_NOTIFICATION          = 53  # DeathNotification
    NPC_JOIN                    = 54  # NpcJoin
    KILL_FEED_MESSAGE           = 55  # KillFeedMessage
    SET_MAP_ICON                = 56  # SetMapIcon
    REMOVE_VEHICLE_COMPONENT    = 57  # RemoveVehicleComponent
    HIDE_3D_TEXT_LABEL          = 58  # Hide3DTextLabel
    SET_PLAYER_CHAT_BUBBLE      = 59  # SetPlayerChatBubble
    SEND_GAME_TIME_UPDATE       = 60  # SendGameTimeUpdate
    SHOW_DIALOG                 = 61  # ShowDialog
    DIALOG_RESPONSE             = 62  # DialogResponse
    DESTROY_PICKUP              = 63  # DestroyPickup
    LINK_VEHICLE_TO_INTERIOR    = 65  # LinkVehicleToInterior
    SET_ARMOR                   = 66  # SetArmor
    SET_ARMED_WEAPON            = 67  # SetArmedWeapon
    SET_SPAWN_INFO              = 68  # SetSpawnInfo
    SET_PLAYER_TEAM             = 69  # SetPlayerTeam
    PUT_IN_VEHICLE              = 70  # PutInVehicle
    REMOVE_FROM_VEHICLE         = 71  # RemoveFromVehicle
    SET_PLAYER_COLOR            = 72  # SetPlayerColor
    SHOW_GAME_TEXT              = 73  # ShowGameText
    FORCE_CLASS_SELECTION       = 74  # ForceClassSelection
    ATTACH_OBJECT_TO_PLAYER     = 75  # AttachObjectToPlayer
    INIT_MENU                   = 76  # InitMenu
    SHOW_MENU                   = 77  # ShowMenu
    HIDE_MENU                   = 78  # HideMenu
    CREATE_EXPLOSION            = 79  # CreateExplosion
    TOGGLE_PLAYER_NAME_TAG      = 80  # TogglePlayerNameTag
    ATTACH_CAMERA_TO_OBJECT     = 81  # AttachCameraToObject
    INTERPOLATE_CAMERA          = 82  # InterpolateCamera
    CLICK_TEXTDRAW              = 83  # ClickTextdraw
    TOGGLE_TEXTDRAWS_CLICKABLE  = 83  # ToggleTextdrawsClickable
    SET_PLAYER_OBJECT_MATERIAL  = 84  # SetPlayerObjectMaterial
    STOP_FLASH_GANG_ZONE        = 85  # StopFlashGangZone
    APPLY_PLAYER_ANIMATION      = 86  # ApplyPlayerAnimation
    CLEAR_PLAYER_ANIMATION      = 87  # ClearPlayerAnimation
    SET_SPECIAL_ACTION          = 88  # SetSpecialAction
    SET_PLAYER_FIGHTING_STYLE   = 89  # SetPlayerFightingStyle
    SET_VELOCITY                = 90  # SetVelocity
    SET_VEHICLE_VELOCITY        = 91  # SetVehicleVelocity
    CHAT_MESSAGE                = 93  # ChatMessage
    SET_WORLD_TIME              = 94  # SetWorldTime
    CREATE_PICKUP               = 95  # CreatePickup
    SCM_EVENT                   = 96  # ScmEvent
    DESTROY_WEAPON_PICKUP       = 97  # DestroyWeaponPickup
    MOVE_OBJECT                 = 99  # MoveObject
    REQUEST_CHAT_MESSAGE        = 101 # RequestChatMessage
    PLAYER_CHAT_MESSAGE         = 101 # PlayerChatMessage
    SVR_STATS                   = 102 # SvrStats
    CLIENT_CHECK                = 103 # ClientCheck
    CLIENT_CHECK_RESPONSE       = 103 # ClientCheckResponse
    TOGGLE_STUNT_BONUS          = 104 # ToggleStuntBonus
    SET_TEXTDRAW_TEXT           = 105 # SetTextdrawText
    DAMAGE_VEHICLE              = 106 # DamageVehicle
    SET_CHECKPOINT              = 107 # SetCheckpoint
    ADD_GANG_ZONE               = 108 # AddGangZone
    PLAY_CRIME_REPORT           = 112 # PlayCrimeReport
    SET_PLAYER_ATTACHED_OBJECT  = 113 # SetPlayerAttachedObject
    GIVE_TAKE_DAMAGE            = 115 # GiveTakeDamage
    EDIT_ATTACHED_OBJECT        = 116 # EditAttachedObject
    EDIT_OBJECT                 = 117 # EditObject
    INTERIOR_CHANGE             = 118 # InteriorChange
    MAP_MARKER                  = 119 # MapMarker
    REMOVE_GANG_ZONE            = 120 # RemoveGangZone
    FLASH_GANG_ZONE             = 121 # FlashGangZone
    STOP_OBJECT                 = 122 # StopObject
    SET_VEHICLE_NUMBER_PLATE    = 123 # SetVehicleNumberPlate
    TOGGLE_SPECTATE             = 124 # ToggleSpectate
    SPECTATE_PLAYER             = 126 # SpectatePlayer
    SPECTATE_VEHICLE            = 127 # SpectateVehicle
    REQUEST_CLASS               = 128 # RequestClass
    REQUEST_CLASS_RESPONSE      = 128 # RequestClassResponse
    REQUEST_SPAWN               = 129 # RequestSpawn
    REQUEST_SPAWN_RESPONSE      = 129 # RequestSpawnResponse
    CONNECTION_REJECTED         = 130 # ConnectionRejected
    PICKED_UP_PICKUP            = 131 # PickedUpPickup
    MENU_SELECT                 = 132 # MenuSelect
    SET_WANTED_LEVEL            = 133 # SetWantedLevel
    SHOW_TEXTDRAW               = 134 # ShowTextdraw
    HIDE_TEXTDRAW               = 135 # HideTextdraw
    VEHICLE_DESTROYED           = 136 # VehicleDestroyed
    SERVER_JOIN                 = 137 # ServerJoin
    SERVER_QUIT                 = 138 # ServerQuit
    INIT_GAME                   = 139 # InitGame
    MENU_QUIT                   = 140 # MenuQuit
    REMOVE_MAP_ICON             = 144 # RemoveMapIcon
    SET_WEAPON_AMMO             = 145 # SetWeaponAmmo
    SET_GRAVITY                 = 146 # SetGravity
    SET_VEHICLE_HEALTH          = 147 # SetVehicleHealth
    ATTACH_TRAILER_TO_VEHICLE   = 148 # AttachTrailerToVehicle
    DETACH_TRAILER_FROM_VEHICLE = 149 # DetachTrailerFromVehicle
    SET_WEATHER                 = 152 # SetWeather
    SET_PLAYER_SKIN             = 153 # SetPlayerSkin
    PLAYER_EXIT_VEHICLE         = 154 # PlayerExitVehicle
    EXIT_VEHICLE                = 154 # ExitVehicle
    REQUEST_SCORES_AND_PINGS    = 155 # RequestScoresAndPings
    SET_INTERIOR                = 156 # SetInterior
    SET_CAMERA_POS              = 157 # SetCameraPos
    SET_CAMERA_LOOK_AT          = 158 # SetCameraLookAt
    SET_VEHICLE_POS             = 159 # SetVehiclePos
    SET_VEHICLE_DIR_Z           = 160 # SetVehicleDirZ
    SET_VEHICLE_PARAMS          = 161 # SetVehicleParams
    SET_CAMERA_BEHIND_PLAYER    = 162 # SetCameraBehindPlayer
    STOP_PLAYER_STREAM          = 163 # StopPlayerStream
    ADD_VEHICLE                 = 164 # AddVehicle
    REMOVE_VEHICLE              = 165 # RemoveVehicle
    DEATH_BROADCAST             = 166 # DeathBroadcast
    TOGGLE_VEHICLE_COLLISIONS   = 167 # ToggleVehicleCollisions
    CAMERA_TARGET               = 168 # CameraTarget
    TOGGLE_CAMERA_TARGET        = 170 # ToggleCameraTarget
    ADD_ACTOR                   = 171 # AddActor
    REMOVE_ACTOR                = 172 # RemoveActor
    APPLY_ACTOR_ANIMATION       = 173 # ApplyActorAnimation
    CLEAR_ACTOR_ANIMATION       = 174 # ClearActorAnimation
    SET_ACTOR_DIR_Z             = 175 # SetActorDirZ
    SET_ACTOR_POS               = 176 # SetActorPos
    SET_ACTOR_HEALTH            = 178 # SetActorHealth

from . import raknet
raknet.RPC = RPC
from .raknet import Rpc

# S2C means server to client
# C2S means client to server

''' S2C
player_id: id of the player to change the name
name: new name; length=[1,24]
success: should be 1?; if 0 also changes the name so idk what it means
'''
class SetPlayerName(Rpc):
    def __init__(self, player_id, name, success=1):
        super().__init__(RPC.SET_PLAYER_NAME)
        self.player_id = player_id
        self.name = name
        self.success = success

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_dynamic_str8(self.name)
        bs.write_u8(self.success)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        name = bs.read_dynamic_str8()
        success = bs.read_u8()
        return SetPlayerName(player_id, name, success)

''' S2C
Sets the positon.
pos: new position
e.g. SetPos(Vec3(0.0, 0.0, 3.0))
e.g. SetPos(SPOT.GROVE)
Related: SetPlayerPos
'''
class SetPos(Rpc):
    def __init__(self, pos):
        super().__init__(RPC.SET_POS)
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        return SetPos(pos)

''' S2C
Sets the position.
The final Z position may not be the value in the RPC, but rather the Z position of the closest solid object below Z(usually the ground)
e.g. SetPosFindZ(0, 0, 100) will set the position to Vec3(0, 0, 2) because Z=2 is the height of the floor below Z=100
'''
class SetPosFindZ(Rpc):
    def __init__(self, pos):
        super().__init__(RPC.SET_POS_FIND_Z)
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        return SetPosFindZ(pos)

''' S2C
Sets the health of the player this rpc is sent to.
health: new health value
e.g. SetHealth(50.0)
'''
class SetHealth(Rpc):
    def __init__(self, health):
        super().__init__(RPC.SET_HEALTH)
        self.health = health

    def encode_rpc_payload(self, bs):
        bs.write_float(self.health)

    @staticmethod
    def decode_rpc_payload(bs):
        health = bs.read_float()
        return SetHealth(health)

''' S2C
Freezes or unfreezes the player.
controllable: True or False
Note: The player cannot look nor move around when frozen.
Related: TogglePlayerControllable
e.g. ToggleControllable(False) # freezes the player
'''
class ToggleControllable(Rpc):
    def __init__(self, controllable):
        super().__init__(RPC.TOGGLE_CONTROLLABLE)
        self.controllable = bool(controllable)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.controllable)

    @staticmethod
    def decode_rpc_payload(bs):
        controllable = bs.read_u8()
        return ToggleControllable(controllable)

''' S2C
Plays/Stops the specified sound for the player this rpc is sent to.
sound_id:
 - use 0 to stop the sound that is currently playing
 - see https://www.open.mp/docs/scripting/resources/sound-ids
 - see https://raw.githubusercontent.com/WoutProvost/samp-sound-array/master/sound.inc
pos: where the sound will played; use Vec3(0, 0, 0) for no position
'''
class PlaySound(Rpc):
    def __init__(self, sound_id, pos=Vec3(0,0,0)):
        super().__init__(RPC.PLAY_SOUND)
        self.sound_id = sound_id
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.sound_id)
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        sound_id = bs.read_u32()
        pos = bs.read_vec3()
        return PlaySound(sound_id, pos)

''' S2C
Sets the world boundaries for the player this rpc is sent to.
If the player tries to go out of the boundaries they will be pushed back in.
Default value: SetWorldBounds(20_000.0, -20_000.0, 20_000.0, -20_000.0)
                (North)
                 max_y
             ┌──────────┐
             │          │
(West) min_x │          │ max_x (East)
             │          │
             └──────────┘
                 min_y
                (South)
'''
class SetWorldBounds(Rpc):
    def __init__(self, max_x, min_x, max_y, min_y):
        super().__init__(RPC.SET_WORLD_BOUNDS)
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y

    def encode_rpc_payload(self, bs):
        bs.write_float(self.max_x)
        bs.write_float(self.min_x)
        bs.write_float(self.max_y)
        bs.write_float(self.min_y)

    @staticmethod
    def decode_rpc_payload(bs):
        max_x = bs.read_float()
        min_x = bs.read_float()
        max_y = bs.read_float()
        min_y = bs.read_float()
        return SetWorldBounds(max_x, min_x, max_y, min_y)

''' S2C
Give money to or take money from the player this rpc is sent to.
e.g. GiveMoney(123)
e.g. GiveMoney(-200)
e.g. GiveMoney(0) # nothing happens
Related: GivePlayerMoney
'''
class GiveMoney(Rpc):
    def __init__(self, amount):
        super().__init__(RPC.GIVE_MONEY)
        self.amount = amount

    def encode_rpc_payload(self, bs):
        bs.write_i32(self.amount)

    @staticmethod
    def decode_rpc_payload(bs):
        amount = bs.read_i32()
        return GiveMoney(amount)

''' S2C
Sets the Z component of the direction(orientation)
e.g. SetDirZ(0.0) # Player faces north

           (North)
              0°
              │
(West) 90° ──   ── 270° (East)
              │
             180°
           (South)
Related: SetPlayerFacingAngle
'''
class SetDirZ(Rpc):
    def __init__(self, angle):
        super().__init__(RPC.SET_DIR_Z)
        self.angle = angle

    def encode_rpc_payload(self, bs):
        bs.write_float(self.angle)

    @staticmethod
    def decode_rpc_payload(bs):
        angle = bs.read_float()
        return SetDirZ(angle)

''' S2C
Sets the money amount to zero of the player this rpc is sent to.
e.g. ResetMoney()
Related: ResetPlayerMoney
'''
class ResetMoney(Rpc):
    def __init__(self):
        super().__init__(RPC.RESET_MONEY)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ResetMoney()

''' S2C
Removes all weapons from the player this rpc is sent to.
Note: To remove specific weapons, set ammo to 0 using SetWeaponAmmo.
Related: ResetPlayerWeapons
'''
class RemoveAllWeapons(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_ALL_WEAPONS)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveAllWeapons()

''' S2C
Give a weapon with ammo to the player this rpc is sent to.
See weapons at sa/weapon.py
e.g. GiveWeapon(WEAPON.M4, 250)
Note: it accumulates, so giving it twice will double the ammo
Related: GivePlayerWeapon
'''
class GiveWeapon(Rpc):
    def __init__(self, weapon_id, ammo):
        super().__init__(RPC.GIVE_WEAPON)
        self.weapon_id = weapon_id
        self.ammo = ammo

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.weapon_id)
        bs.write_u32(self.ammo)

    @staticmethod
    def decode_rpc_payload(bs):
        weapon_id = bs.read_u32()
        ammo = bs.read_u32()
        return GiveWeapon(weapon_id, ammo)

''' C2S
Client sends this rpc when it clicks a player on the scoreboard(TAB)
player_id: the id of the player that has been clicked
source: seems to always be 0
Related: ClickPlayer, OnPlayerClickPlayer
'''
class ClickScoreboardPlayer(Rpc):
    def __init__(self, player_id, source):
        super().__init__(RPC.CLICK_SCOREBOARD_PLAYER)
        self.player_id = player_id
        self.source = source

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.source)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        source = bs.read_u8()
        return ClickScoreboardPlayer(player_id, source)

class SetVehicleParamsEx(Rpc):
    def __init__(self, vehicle_id, engine, lights=255, alarm=255, doors=255, bonnet=255, boot=255, objective=255, siren=255, door_driver=255, door_passenger=255, door_back_left=255, door_back_right=255, window_driver=255, window_passenger=255, window_back_left=255, window_back_right=255):
        super().__init__(RPC.SET_VEHICLE_PARAMS_EX)
        self.vehicle_id = vehicle_id
        self.engine = engine
        self.lights = lights
        self.alarm = alarm
        self.doors = doors
        self.bonnet = bonnet
        self.boot = boot
        self.objective = objective
        self.siren = siren
        self.door_driver = door_driver
        self.door_passenger = door_passenger
        self.door_back_left = door_back_left
        self.door_back_right = door_back_right
        self.window_driver = window_driver
        self.window_passenger = window_passenger
        self.window_back_left = window_back_left
        self.window_back_right = window_back_right

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.engine)
        bs.write_u8(self.lights)
        bs.write_u8(self.alarm)
        bs.write_u8(self.doors)
        bs.write_u8(self.bonnet)
        bs.write_u8(self.boot)
        bs.write_u8(self.objective)
        bs.write_u8(self.siren)
        bs.write_u8(self.door_driver)
        bs.write_u8(self.door_passenger)
        bs.write_u8(self.door_back_left)
        bs.write_u8(self.door_back_right)
        bs.write_u8(self.window_driver)
        bs.write_u8(self.window_passenger)
        bs.write_u8(self.window_back_left)
        bs.write_u8(self.window_back_right)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        engine = bs.read_u8()
        lights = bs.read_u8()
        alarm = bs.read_u8()
        doors = bs.read_u8()
        bonnet = bs.read_u8()
        boot = bs.read_u8()
        objective = bs.read_u8()
        siren = bs.read_u8()
        door_driver = bs.read_u8()
        door_passenger = bs.read_u8()
        door_back_left = bs.read_u8()
        door_back_right = bs.read_u8()
        window_driver = bs.read_u8()
        window_passenger = bs.read_u8()
        window_back_left = bs.read_u8()
        window_back_right = bs.read_u8()
        return SetVehicleParamsEx(vehicle_id, engine, lights, alarm, doors, bonnet, boot, objective, siren, door_driver, door_passenger, door_back_left, door_back_right, window_driver, window_passenger, window_back_left, window_back_right)

''' C2S
The client sends this RPC to the server in the connection process, after the server sends ConnectionRequestAccepted.
'''
class ClientJoin(Rpc):
    def __init__(self, version_code, mod, name, challenge_response, gpci, version):
        super().__init__(RPC.CLIENT_JOIN)
        self.version_code = version_code
        self.mod = mod
        self.name = name
        self.challenge_response = challenge_response
        self.gpci = gpci # "gpci"; (stands for get player client id)
        self.version = version

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.version_code)
        bs.write_u8(self.mod)
        bs.write_dynamic_str8(self.name)
        bs.write_u32(self.challenge_response)
        bs.write_dynamic_str8(self.gpci)
        bs.write_dynamic_str8(self.version)

    @staticmethod
    def decode_rpc_payload(bs):
        version_code = bs.read_u32()
        mod = bs.read_u8()
        name = bs.read_dynamic_str8()
        challenge_response = bs.read_u32()
        gpci = bs.read_dynamic_str8()
        version = bs.read_dynamic_str8()
        return ClientJoin(version_code, mod, name, challenge_response, gpci, version)

''' S2C
Makes the specified player do the animation of entering the specified vehicle for the player this RPC is sent to.
player_id: the id of the player entering the vehicle
vehicle_id: the id of the vehicle about to be entered
as_passenger: 0 if entering the driver seat; 1 if entering any passenger seat
'''
class PlayerEnterVehicle(Rpc):
    def __init__(self, player_id, vehicle_id, as_passenger):
        super().__init__(RPC.PLAYER_ENTER_VEHICLE)
        self.player_id = player_id
        self.vehicle_id = vehicle_id
        self.as_passenger = as_passenger

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.as_passenger)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        as_passenger = bs.read_u8()
        return PlayerEnterVehicle(player_id, vehicle_id, as_passenger)

''' C2S
Client sends when it enters a vehicle
vehicle_id: the id of the vehicle about to be entered
as_passenger: 0 if entering the driver seat; 1 if entering any passenger seat
'''
class EnterVehicle(Rpc):
    def __init__(self, vehicle_id, as_passenger):
        super().__init__(RPC.ENTER_VEHICLE)
        self.vehicle_id = vehicle_id
        self.as_passenger = as_passenger

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.as_passenger)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        as_passenger = bs.read_u8()
        return EnterVehicle(vehicle_id, as_passenger)
RPC.ENTER_VEHICLE.decode_client_rpc_payload = EnterVehicle.decode_rpc_payload

class EnterEditObject(Rpc):
    def __init__(self):
        super().__init__(RPC.ENTER_EDIT_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EnterEditObject()

class CancelEditObject(Rpc):
    def __init__(self):
        super().__init__(RPC.CANCEL_EDIT_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return CancelEditObject()

''' S2C
Sets the world time for the player this rpc is sent to.
e.g. SetTime(0, 0) # 00:00
e.g. SetTime(12, 30) # 12:30
Related: SetPlayerTime
'''
class SetTime(Rpc):
    def __init__(self, hour, minute=0):
        super().__init__(RPC.SET_TIME)
        self.hour = hour
        self.minute = minute

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.hour)
        bs.write_u8(self.minute)

    @staticmethod
    def decode_rpc_payload(bs):
        hour = bs.read_u8()
        minute = bs.read_u8()
        return SetTime(hour, minute)

''' S2C
Shows or hides the clock in the top right corner of the screen.
show: True or False
Note: The time of the clock may be modified by the SetTime RPC
Note: The time on the clock changes at a rate of one minute per one real world second, so one hour goes by every real world minute
e.g. ToggleClock(show=True)
'''
class ToggleClock(Rpc):
    def __init__(self, show):
        super().__init__(RPC.TOGGLE_CLOCK)
        self.show = bool(show)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.show)

    @staticmethod
    def decode_rpc_payload(bs):
        show = bs.read_u8()
        return ToggleClock(show)

''' S2C
Adds the specified player to the world.
If this rpc is sent twice(without a StopPlayerStream in between) it just overwrites the values.
team: valid team values are 0-254; None specifies the player is not in any team(internally it is defined as 255)
Note: The server MUST send the ServerJoin RPC before StartPlayerStream; i.e. logically a player has to first join the server, then be added to the world.
Related: WorldPlayerAdd, PlayerStreamIn
'''
class StartPlayerStream(Rpc):
    def __init__(self, player_id, team=None, skin_id=SKIN.CJ, pos=Vec3(0,0,3), dir_z=0.0, color=0xffffffff, fighting_style=0, skill_level=0):
        super().__init__(RPC.START_PLAYER_STREAM)
        self.player_id = player_id
        self.team = team
        self.skin_id = SKIN(skin_id)
        self.pos = pos
        self.dir_z = dir_z
        self.color = Color(color)
        self.fighting_style = fighting_style
        self.skill_level = skill_level

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(NO_TEAM_ID if self.team is None else self.team)
        bs.write_u32(self.skin_id)
        bs.write_vec3(self.pos)
        bs.write_float(self.dir_z)
        bs.write_u32(self.color)
        bs.write_u8(self.fighting_style)
        bs.write_u16(self.skill_level)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        team = bs.read_u8()
        if team == NO_TEAM_ID:
            team = None
        skin_id = bs.read_u32()
        pos = bs.read_vec3()
        dir_z = bs.read_float()
        color = bs.read_u32()
        fighting_style = bs.read_u8()
        skill_level = bs.read_u16()
        return StartPlayerStream(player_id, team, skin_id, pos, dir_z, color, fighting_style, skill_level)

class SetShopName(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_SHOP_NAME)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetShopName()

class WEAPON_SKILL(enum.IntEnum):
    PISTOL          = 0
    PISTOL_SILENCED = 1
    DESERT_EAGLE    = 2
    SHOTGUN         = 3
    SAWNOFF_SHOTGUN = 4
    SPAS12_SHOTGUN  = 5
    MICRO_UZI       = 6
    MP5             = 7
    AK47            = 8
    M4              = 9
    SNIPERRIFLE     = 10

''' S2C
Sets the skill level of the specified player.
player_id: id of the player to set the level of the specified weapon(skill_id)
skill_id: a member of WEAPON_SKILL
level: skill level

e.g. SetPlayerSkillLevel(244, WEAPON_SKILL.M4, 600)

There are 3 classes: Poor, Gangster and Hitman
This table shows the levels needed to advance to the next class

Weapon          Poor  Gangster  Hitman
Pistol          0     40        999
Slienced Pistol 0     500       999
Desert Eagle    0     200       999
Shotgun         0     200       999
Sawnoff         0     200       999
Combat          0     200       999
Micro Uzi       0     50        999
TEC-9           0     50        999
MP5             0     250       999
AK47            0     200       999
M4              0     200       999
Sniper Rifle    0     300       999
Country Rifle   0     300       999
'''
class SetPlayerSkillLevel(Rpc):
    def __init__(self, player_id, skill_id, level):
        super().__init__(RPC.SET_PLAYER_SKILL_LEVEL)
        self.player_id = player_id
        self.skill_id = skill_id
        self.level = level

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.skill_id)
        bs.write_u16(self.level)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        skill_id = bs.read_u32()
        level = bs.read_u16()
        return SetPlayerSkillLevel(player_id, skill_id, level)

''' S2C
Sets the drunk level of the player this rpc is sent to.
e.g. SetDrunkLevel(2000+3*60) # camera sways for ~3 seconds and goes back to normal (assuming FPS=60)
The level automatically decreases over time
The rate of depends on the client FPS (i.e. FPS=X means it loses X levels per second), thus it is possible to estimate the FPS
In 0.3a the drunk level will decrement and stop at 2000. In 0.3b+ the drunk level decrements to zero.)
Max level: 50000
Level  Effect
<=2000 No effect
>2000  Camera swaying and hard to drive
>5000  Hidden HUD (i.e. radar, health/armor bar, ...)
Related: SetPlayerDrunkLevel
'''
class SetDrunkLevel(Rpc):
    def __init__(self, level):
        super().__init__(RPC.SET_DRUNK_LEVEL)
        self.level = level

    def encode_rpc_payload(self, bs):
        bs.write_i32(self.level)

    @staticmethod
    def decode_rpc_payload(bs):
        level = bs.read_i32()
        return SetDrunkLevel(level)

''' S2C
label_id: integer in the interval [0, 2047]; max id = MAX_3D_TEXT_LABEL_ID
text: text
color: color of the text
pos: position of the text as Vec3
draw_distance: maximum distance the text is still visible
test_los: 1 or 0; Test the line-of-sight(LOS) so the text can't be seen through objects
attached_player_id:nothing attached=None if it is the id of a player then the text is attached to the player; note: the player the 3d text is attached to cannot see it, only others
attached_vehicle_id:nothing attached=None; if it is the id of a vehicle then the text is attached to the player
note: if the text is attached to a player or vehicle, 'pos' becomes an offset relative to the player/vehicle.

Use the Hide3DTextLabel RPC to hide a 3d text label.
'''
class Show3DTextLabel(Rpc):
    def __init__(self, label_id, text, color, pos, draw_distance=50.0, test_los=1, attached_player_id=None, attached_vehicle_id=None):
        super().__init__(RPC.SHOW_3D_TEXT_LABEL)
        self.label_id = label_id
        self.color = Color(color)
        self.pos = pos
        self.draw_distance = draw_distance
        self.test_los = test_los
        self.attached_player_id = attached_player_id
        self.attached_vehicle_id = attached_vehicle_id
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.label_id)
        bs.write_u32(self.color)
        bs.write_vec3(self.pos)
        bs.write_float(self.draw_distance)
        bs.write_u8(self.test_los)
        bs.write_i16(-1 if self.attached_player_id is None else self.attached_player_id)
        bs.write_i16(-1 if self.attached_vehicle_id is None else self.attached_vehicle_id)
        bs.write_huffman_buffer(self.text.encode(SAMP_ENCODING), default_huffman_tree.encoding_table)

    @staticmethod
    def decode_rpc_payload(bs):
        label_id = bs.read_u16()
        color = bs.read_u32()
        pos = bs.read_vec3()
        draw_distance = bs.read_float()
        test_los = bs.read_u8()

        attached_player_id = bs.read_i16()
        if attached_player_id < 0:
            attached_player_id = None

        attached_vehicle_id = bs.read_i16()
        if attached_vehicle_id < 0:
            attached_vehicle_id = None

        text = bs.read_huffman_buffer(default_huffman_tree.root_node).decode(SAMP_ENCODING)
        return Show3DTextLabel(label_id, text, color, pos, draw_distance, test_los, attached_player_id, attached_vehicle_id)
RPC.SHOW_3D_TEXT_LABEL.decode_server_rpc_payload = Show3DTextLabel.decode_rpc_payload

class DisableCheckpoint(Rpc):
    def __init__(self):
        super().__init__(RPC.DISABLE_CHECKPOINT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DisableCheckpoint()

''' S2C
Shows a race checkpoint.
type: 0=Normal, 1=Finish, 2=Nothing(Only the checkpoint without anything in it), 3=Air normal(torus), 4=Air finish, 5=Air (rotates and stops), 6=Air (increases, decreases and disappears), 7=Air (swings down and up), 8=Air (swings up and down)
pos: position of the race checkpoint
next_pos: this vector is used to set the direction of the arrow of the checkpoint
diameter: race checkpoint diameter
Note: only one checkpoint is shown at a time
Related: SetPlayerRaceCheckpoint, SetRaceCheckpoint
'''
class ShowRaceCheckpoint(Rpc):
    def __init__(self, type, pos, next_pos, diameter):
        super().__init__(RPC.SHOW_RACE_CHECKPOINT)
        self.type = type
        self.pos = pos
        self.next_pos = next_pos
        self.diameter = diameter

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.type)
        bs.write_vec3(self.pos)
        bs.write_vec3(self.next_pos)
        bs.write_float(self.diameter)

    @staticmethod
    def decode_rpc_payload(bs):
        type = bs.read_u8()
        pos = bs.read_vec3()
        next_pos = bs.read_vec3()
        diameter = bs.read_float()
        return ShowRaceCheckpoint(type, pos, next_pos, diameter)

''' S2C
Hides the active race checkpoint(if any).
Related: DisablePlayerRaceCheckpoint, DisableRaceCheckpoint
'''
class HideRaceCheckpoint(Rpc):
    def __init__(self):
        super().__init__(RPC.HIDE_RACE_CHECKPOINT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return HideRaceCheckpoint()

class GameModeRestart(Rpc):
    def __init__(self):
        super().__init__(RPC.GAME_MODE_RESTART)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return GameModeRestart()

''' S2C
Plays an audio stream.
url: address of the stream
use_pos: True or False; If false, the audio is played no matter where the player is(i.e. pos and radius are unused).
pos and radius: specify a sphere; audio is only played this sphere.
e.g. PlayAudioStream('https://upload.wikimedia.org/wikipedia/commons/a/ac/Pig_grunt_-_Erdie.ogg') makes player hear a pig oinking .
'''
class PlayAudioStream(Rpc):
    def __init__(self, url, use_pos=False, pos=Vec3(0.0, 0.0, 0.0), radius=0.0):
        super().__init__(RPC.PLAY_AUDIO_STREAM)
        self.url = url
        self.use_pos = use_pos
        self.pos = pos
        self.radius = radius

    def encode_rpc_payload(self, bs):
        bs.write_dynamic_str8(self.url)
        bs.write_vec3(self.pos)
        bs.write_float(self.radius)
        bs.write_u8(self.use_pos)

    @staticmethod
    def decode_rpc_payload(bs):
        url = bs.read_dynamic_str8()
        pos = bs.read_vec3()
        radius = bs.read_float()
        use_pos = bs.read_u8()
        return PlayAudioStream(url, use_pos, pos, radius)

''' S2C
Stops an audio stream.
e.g. StopAudioStream() makes the currently playing stream(if any) stop.
'''
class StopAudioStream(Rpc):
    def __init__(self):
        super().__init__(RPC.STOP_AUDIO_STREAM)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return StopAudioStream()

''' S2C
Removes zero or more objects.
model_id: a specific model id, or None(matches all model ids)
pos and radius are used to specify a sphere; objects are only removed if they are inside this imaginary sphere
'''
class RemoveBuilding(Rpc):
    def __init__(self, model_id, pos, radius):
        super().__init__(RPC.REMOVE_BUILDING)
        self.model_id = model_id
        self.pos = pos
        self.radius = radius

    def encode_rpc_payload(self, bs):
        bs.write_i32(-1 if self.model_id == None else self.model_id)
        bs.write_vec3(self.pos)
        bs.write_float(self.radius)

    @staticmethod
    def decode_rpc_payload(bs):
        model_id = bs.read_i32()
        if model_id == -1:
            model_id = None
        pos = bs.read_vec3()
        radius = bs.read_float()
        return RemoveBuilding(model_id, pos, radius)

class CreateObject(Rpc):
    def __init__(self, object_id, model_id, pos, dir=Vec3(0.0, 0.0, 0.0), draw_distance=100.0, no_camera_col=True, attached_object_id=None, attached_vehicle_id=None, attach_offset=None, attach_dir=None, sync_rotation=None):
        super().__init__(RPC.CREATE_OBJECT)
        self.object_id = object_id
        self.model_id = model_id
        self.pos = pos # Object position as Vec3
        self.dir = dir # Object direction as Vec3
        self.draw_distance = float(draw_distance)
        self.no_camera_col = no_camera_col
        self.attached_object_id = attached_object_id
        self.attached_vehicle_id = attached_vehicle_id
        self.attach_offset = attach_offset
        self.attach_dir = attach_dir
        self.sync_rotation = sync_rotation

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.object_id)
        bs.write_u32(self.model_id)
        bs.write_vec3(self.pos)
        bs.write_vec3(self.dir)
        bs.write_float(self.draw_distance)
        bs.write_u8(self.no_camera_col)
        bs.write_i16(-1 if self.attached_object_id is None else self.attached_object_id)
        bs.write_i16(-1 if self.attached_vehicle_id is None else self.attached_vehicle_id)
        if self.attached_object_id is not None or self.attached_vehicle_id is not None:
            bs.write_vec3(self.attach_offset)
            bs.write_vec3(self.attach_dir)
            bs.write_u8(self.sync_rotation)

    @staticmethod
    def decode_rpc_payload(bs):
        object_id = bs.read_u16()
        model_id = bs.read_u32()
        pos = bs.read_vec3()
        dir = bs.read_vec3()
        draw_distance = bs.read_float()
        no_camera_col = bs.read_u8()
        attached_object_id = bs.read_i16()
        if attached_object_id == -1:
            attached_object_id = None
        attached_vehicle_id = bs.read_i16()
        if attached_vehicle_id == -1:
            attached_vehicle_id = None
        if attached_object_id is not None or attached_vehicle_id is not None:
            attach_offset = bs.read_vec3()
            attach_dir = bs.read_vec3()
            sync_rotation = bs.read_u8()
        else:
            attach_offset = None
            attach_dir = None
            sync_rotation = None
        return CreateObject(object_id, model_id, pos, dir, draw_distance, no_camera_col, attached_object_id, attached_vehicle_id, attach_offset, attach_dir, sync_rotation)

class SetObjectPos(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_OBJECT_POS)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetObjectPos()

class SetObjectRotation(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_OBJECT_ROTATION)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetObjectRotation()

class DestroyObject(Rpc):
    def __init__(self, object_id):
        super().__init__(RPC.DESTROY_OBJECT)
        self.object_id = object_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.object_id)

    @staticmethod
    def decode_rpc_payload(bs):
        object_id = bs.read_u16()
        return DestroyObject(object_id)

''' C2S
Client sends a command to the server, e.g. "/help"
command: command.
Related: PlayerRequestCommandMessage, SendCommand 
'''
class RequestChatCommand(Rpc):
    def __init__(self, command):
        super().__init__(RPC.REQUEST_CHAT_COMMAND)
        self.command = command

    def encode_rpc_payload(self, bs):
        bs.write_dynamic_str32(self.command)

    @staticmethod
    def decode_rpc_payload(bs):
        command = bs.read_dynamic_str32()
        return RequestChatCommand(command)

''' C2S
Clients notifies the server when it has spawned
'''
class SendSpawn(Rpc):
    def __init__(self):
        super().__init__(RPC.SEND_SPAWN)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SendSpawn()

class DeathNotification(Rpc):
    def __init__(self, reason, killer_id):
        super().__init__(RPC.DEATH_NOTIFICATION)
        self.reason = reason
        self.killer_id = killer_id

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.reason)
        bs.write_u16(self.killer_id)

    @staticmethod
    def decode_rpc_payload(bs):
        reason = bs.read_u8()
        killer_id = bs.read_u16()
        return DeathNotification(reason, killer_id)

class NpcJoin(Rpc):
    def __init__(self):
        super().__init__(RPC.NPC_JOIN)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return NpcJoin()

''' S2C
Adds a message to the kill feed.
A kill feed message has the following format: KILLER REASON VICTIM
killer_id: player id of the killer; this value should be None if there is no killer(e.g. suicide)
victim_id: player id of the victim
reason: a weapon id; see sa/weapon.py
Note: kill feed(or death chat/window) is the area on the screen on the right(F9)
'''
class KillFeedMessage(Rpc):
    def __init__(self, killer_id, victim_id, reason):
        super().__init__(RPC.KILL_FEED_MESSAGE)
        self.killer_id = killer_id
        self.victim_id = victim_id
        self.reason = WEAPON(reason)

    def encode_rpc_payload(self, bs):
        bs.write_i16(self.killer_id)
        bs.write_i16(-1 if self.victim_id == None else self.victim_id)
        bs.write_u8(self.reason)

    @staticmethod
    def decode_rpc_payload(bs):
        killer_id = bs.read_i16()
        if killer_id == -1:
            killer_id = None
        victim_id = bs.read_i16()
        reason = bs.read_u8()
        return KillFeedMessage(killer_id, victim_id, reason)

class SetMapIcon(Rpc):
    def __init__(self, icon_id, pos, type, color, style):
        super().__init__(RPC.SET_MAP_ICON)
        self.icon_id = icon_id
        self.pos = pos
        self.type = type
        self.color = Color(color)
        self.style = style

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.icon_id)
        bs.write_vec3(self.pos)
        bs.write_u8(self.type)
        bs.write_u32(self.color)
        bs.write_u8(self.style)

    @staticmethod
    def decode_rpc_payload(bs):
        icon_id = bs.read_u8()
        pos = bs.read_vec3()
        type_ = bs.read_u8()
        color = bs.read_u32()
        style = bs.read_u8()
        return SetMapIcon(icon_id, pos, type_, color, style)

class RemoveVehicleComponent(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_VEHICLE_COMPONENT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveVehicleComponent()

''' S2C
Hides a 3D Text Label.
'''
class Hide3DTextLabel(Rpc):
    def __init__(self, label_id):
        super().__init__(RPC.HIDE_3D_TEXT_LABEL)
        self.label_id = label_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.label_id)

    @staticmethod
    def decode_rpc_payload(bs):
        label_id = bs.read_u16()
        return Hide3DTextLabel(label_id)
RPC.HIDE_3D_TEXT_LABEL.decode_server_rpc_payload = Hide3DTextLabel.decode_rpc_payload

''' S2C
Shows a text above the name tag of the specified player.
player_id: id of the player to create the chat bubble for.
text: text inside the bubble
color: The text color
draw_distance: distance that players are able to see the bubble
expire_time: time in miliseconds the bubble should be displayed for.
Note: You can't see your own text bubble. The same applies to attached 3D text labels.
'''
class SetPlayerChatBubble(Rpc):
    def __init__(self, player_id, text, color=0xffffffff, draw_distance=100.0, expire_time=1000):
        super().__init__(RPC.SET_PLAYER_CHAT_BUBBLE)
        self.player_id = player_id
        self.color = Color(color)
        self.draw_distance = draw_distance
        self.expire_time = expire_time
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.color)
        bs.write_float(self.draw_distance)
        bs.write_u32(self.expire_time)
        bs.write_dynamic_str8(self.text)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        color = bs.read_u32()
        draw_distance = bs.read_float()
        expire_time = bs.read_u32()
        text = bs.read_dynamic_str8()
        return SetPlayerChatBubble(player_id, text, color, draw_distance, expire_time)

class SendGameTimeUpdate(Rpc):
    def __init__(self, time):
        super().__init__(RPC.SEND_GAME_TIME_UPDATE)
        self.time = time

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.time)

    @staticmethod
    def decode_rpc_payload(bs):
        time = bs.read_u32()
        return SendGameTimeUpdate(time)

class DIALOG_STYLE(enum.IntEnum):
    MESSAGE            = 0
    INPUT              = 1
    LIST               = 2
    PASSWORD           = 3
    TABLE              = 4
    TABLE_WITH_HEADERS = 5

''' S2C
Max dialog id = 32767 = 2^15-1 = 0x7fff
A negative id closes any open dialog
e.g. ShowDialog(-1, 0, '', '', '', '') ; -1 closes any open dialog
'''
class ShowDialog(Rpc):
    def __init__(self, dialog_id, style, title, button1, button2, text):
        super().__init__(RPC.SHOW_DIALOG)
        self.dialog_id = dialog_id
        self.style = DIALOG_STYLE(style)
        self.title = title
        self.button1 = button1
        self.button2 = button2
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_i16(self.dialog_id)
        bs.write_u8(self.style)
        bs.write_dynamic_str8(self.title)
        bs.write_dynamic_str8(self.button1)
        bs.write_dynamic_str8(self.button2)
        bs.write_huffman_buffer(self.text.encode(SAMP_ENCODING), default_huffman_tree.encoding_table)

    @staticmethod
    def decode_rpc_payload(bs):
        dialog_id = bs.read_i16()
        style = DIALOG_STYLE(bs.read_u8())
        title = bs.read_dynamic_str8()
        button1 = bs.read_dynamic_str8()
        button2 = bs.read_dynamic_str8()
        text = bs.read_huffman_buffer(default_huffman_tree.root_node).decode(SAMP_ENCODING)
        return ShowDialog(dialog_id, style, title, button1, button2, text)

class DIALOG_BUTTON(enum.IntEnum):
    LEFT  = 1
    RIGHT = 0

'''
Respond to the current dialog on the screen
dialog_id:  id of the dialog on the screen
button: the button selected; DIALOG_BUTTON.LEFT(selected when ENTER is pressed) or DIALOG_BUTTON.RIGHT
list_index: the index of the row if LIST/TABLE/TABLE_WITH_HEADERS style, otherwise None
text: depends on the dialog style; textbox input value(INPUT/PASSWORD styles), row text(LIST/TABLE/TABLE_WITH_HEADERS styles), empty string(MESSAGE style)
'''
class DialogResponse(Rpc):
    def __init__(self, dialog_id, button=DIALOG_BUTTON.LEFT, list_index=None, text=''):
        super().__init__(RPC.DIALOG_RESPONSE)
        self.dialog_id = dialog_id
        self.button = button
        self.list_index = list_index
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.dialog_id)
        bs.write_u8(self.button)
        bs.write_i16(-1 if self.list_index is None else self.list_index)
        bs.write_dynamic_str8(self.text)

    @staticmethod
    def decode_rpc_payload(bs):
        dialog_id = bs.read_u16()
        button = bs.read_u8()
        list_index = bs.read_i16()
        if list_index == -1:
            list_index = None
        text = bs.read_dynamic_str8()
        return DialogResponse(dialog_id, button, list_index, text)

''' S2C
Server sends to destroy a pickup created with CreatePickup
pickup_id: id of the pickup to destroy
'''
class DestroyPickup(Rpc):
    def __init__(self, pickup_id):
        super().__init__(RPC.DESTROY_PICKUP)
        self.pickup_id = pickup_id

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.pickup_id)

    @staticmethod
    def decode_rpc_payload(bs):
        pickup_id = bs.read_u32()
        return DestroyPickup(pickup_id)

class LinkVehicleToInterior(Rpc):
    def __init__(self):
        super().__init__(RPC.LINK_VEHICLE_TO_INTERIOR)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return LinkVehicleToInterior()

class SetArmor(Rpc):
    def __init__(self, armor):
        super().__init__(RPC.SET_ARMOR)
        self.armor = float(armor)

    def encode_rpc_payload(self, bs):
        bs.write_float(self.armor)

    @staticmethod
    def decode_rpc_payload(bs):
        armor = bs.read_float()
        return SetArmor(armor)

class SetArmedWeapon(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_ARMED_WEAPON)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetArmedWeapon()

''' S2C
Sets spawn info.
team: valid team values are 0-254; None specifies the player is not in any team(internally it is defined as 255)
pos: coordinate where client will spawn
dir_z: Z component of the direction(orientation) of the player's character and camera(because they are the same value when the player spawns); 0.0 is North
Note: The client is only able to spawn(even if the server tries to force a spawn) after the server sends SetSpawnInfo
Note: To make a client spawn after connection, you may send SetSpawnInfo, followed by RequestSpawnResponse(REQUEST_SPAWN.FORCE)
'''
class SetSpawnInfo(Rpc):
    def __init__(self, team=None, skin=SKIN.CJ, pos=Vec3(0.0, 0.0, 3.0), dir_z=0.0, weapon1=Weapon(), weapon2=Weapon(), weapon3=Weapon()):
        super().__init__(RPC.SET_SPAWN_INFO)
        self.team = team
        self.skin = SKIN(skin)
        self.pos = pos
        self.dir_z = float(dir_z)
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.weapon3 = weapon3

    def encode_rpc_payload(self, bs):
        bs.write_u8(NO_TEAM_ID if self.team is None else self.team)
        bs.write_u32(self.skin)
        bs.write_u8(0) # unknown
        bs.write_vec3(self.pos)
        bs.write_float(self.dir_z)
        bs.write_u32(self.weapon1.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon1.ammo)
        bs.write_u32(self.weapon2.ammo)
        bs.write_u32(self.weapon3.ammo)

    @staticmethod
    def decode_rpc_payload(bs):
        team = bs.read_u8()
        if team == NO_TEAM_ID:
            team = None
        skin = bs.read_u32()
        bs.skip_bits(8) # unused
        pos = bs.read_vec3()
        dir_z = bs.read_float()
        weapon1_id = bs.read_u32()
        weapon2_id = bs.read_u32()
        weapon3_id = bs.read_u32()
        weapon1_ammo = bs.read_u32()
        weapon2_ammo = bs.read_u32()
        weapon3_ammo = bs.read_u32()
        weapon1 = Weapon(weapon1_id, weapon1_ammo)
        weapon2 = Weapon(weapon2_id, weapon2_ammo)
        weapon3 = Weapon(weapon3_id, weapon3_ammo)
        return SetSpawnInfo(team, skin, pos, dir_z, weapon1, weapon2, weapon3)

''' S2C
Sets the team of the specified player.
player_id: id of the player to change the team
team: new team; valid team values are 0-254; None specifies the player is not in any team(internally it is defined as 255)
'''
class SetPlayerTeam(Rpc):
    def __init__(self, player_id, team=None):
        super().__init__(RPC.SET_PLAYER_TEAM)
        self.player_id = player_id
        self.team = team

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(NO_TEAM_ID if self.team is None else self.team)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        team = bs.read_u8()
        if team == NO_TEAM_ID:
            team = None
        return SetPlayerTeam(player_id, team)

''' S2C
Puts(i.e. instantly teleports) the player inside the specified vehicle at the specified seat
vehicle_id: id of the vehicle to put the player in
seat_id: 0=driver, 1=front passenger, 2=back left passenger, 3=back right passenger, 4+=other seats(e.g. coach)
Note: The player does not seem to crash if the seat is invalid.
e.g. PutInVehicle(100, 0) # puts the player as driver
'''
class PutInVehicle(Rpc):
    def __init__(self, vehicle_id, seat_id):
        super().__init__(RPC.PUT_IN_VEHICLE)
        self.vehicle_id = vehicle_id
        self.seat_id = seat_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.seat_id)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        seat_id = bs.read_u8()
        return PutInVehicle(vehicle_id, seat_id)

''' S2C
Plays the animation of exiting the vehicle.
Note: Depending on the vehicle velocity the animation may not play, causing the player not to exit.
e.g. RemoveFromVehicle() # If the player is a driver in a car, they'll open the door and step out of the car.
'''
class RemoveFromVehicle(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_FROM_VEHICLE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveFromVehicle()

''' S2C
Sets the color of the specified player.
player_id: id of the player to change the color
color: new color as RRGGBBAA
'''
class SetPlayerColor(Rpc):
    def __init__(self, player_id, color):
        super().__init__(RPC.SET_PLAYER_COLOR)
        self.player_id = player_id
        self.color = Color(color)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.color)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        color = bs.read_u32()
        return SetPlayerColor(player_id, color)

''' S2C
Makes 'text' appear in 'style' for 'duration' milliseconds on the screen of
the client.
- style: integer in the range [0,15]
- duration: duration in milliseconds
- text: text
'''
class ShowGameText(Rpc):
    def __init__(self, style, duration, text):
        super().__init__(RPC.SHOW_GAME_TEXT)
        self.style = style
        self.duration = duration
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.style)
        bs.write_u32(self.duration)
        bs.write_dynamic_str32(self.text)

    @staticmethod
    def decode_rpc_payload(bs):
        style = bs.read_u32()
        duration = bs.read_u32()
        text = bs.read_dynamic_str32()
        return ShowGameText(style, duration, text)

class ForceClassSelection(Rpc):
    def __init__(self):
        super().__init__(RPC.FORCE_CLASS_SELECTION)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ForceClassSelection()

class AttachObjectToPlayer(Rpc):
    def __init__(self):
        super().__init__(RPC.ATTACH_OBJECT_TO_PLAYER)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AttachObjectToPlayer()

class InitMenu(Rpc):
    def __init__(self):
        super().__init__(RPC.INIT_MENU)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return InitMenu()

class ShowMenu(Rpc):
    def __init__(self):
        super().__init__(RPC.SHOW_MENU)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ShowMenu()

class HideMenu(Rpc):
    def __init__(self):
        super().__init__(RPC.HIDE_MENU)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return HideMenu()

'''
Type  Visible  Splits  Creates Fire  Physical Blast  Audible Sound       Range  Special
   0      Yes       -             -             Yes            Yes       Large   Normal
   1      Yes       -           Yes               -            Yes      Normal   Normal
   2      Yes       -           Yes             Yes            Yes       Large   Normal
   3      Yes       -    Sometimes?             Yes            Yes       Large   Normal
   4      Yes     Yes             -             Yes              -      Normal   Unusual explosion, produces just special blast burn FX effects and blasts things away, NO SOUND EFFECTS.
   5      Yes     Yes             -             Yes              -      Normal   Unusual explosion, produces just special blast burn FX effects and blasts things away, NO SOUND EFFECTS.
   6      Yes       -             -             Yes            Yes  Very Large   Additional reddish explosion after-glow
   7      Yes       -             -             Yes            Yes        Huge   Additional reddish explosion after-glow
   8        -       -             -             Yes            Yes      Normal   Invisible
   9        -       -           Yes             Yes            Yes      Normal   Creates fires at ground level, otherwise explosion is heard but invisible.
  10      Yes       -             -             Yes            Yes       Large   Normal
  11      Yes       -             -             Yes            Yes       Small   Normal
  12      Yes       -             -             Yes            Yes  Very Small   Really Small
  13        -       -             -                -             -       Large   roduces no special effects other than black burn effects on the ground, does no damage either.
'''
class CreateExplosion(Rpc):
    def __init__(self, pos, type, radius):
        super().__init__(RPC.CREATE_EXPLOSION)
        self.pos = pos
        self.type = type
        self.radius = radius

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)
        bs.write_u32(self.type)
        bs.write_float(self.radius)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        type = bs.read_u32()
        radius = bs.read_float()
        return CreateExplosion(pos, type, radius)

''' S2C
Shows or hides the name tag of the specified player.
show: True or False
'''
class TogglePlayerNameTag(Rpc):
    def __init__(self, player_id, show):
        super().__init__(RPC.TOGGLE_PLAYER_NAME_TAG)
        self.player_id = player_id
        self.show = bool(show)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.show)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        show = bs.read_u8()
        return TogglePlayerNameTag(player_id, show)

class AttachCameraToObject(Rpc):
    def __init__(self):
        super().__init__(RPC.ATTACH_CAMERA_TO_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AttachCameraToObject()

'''
pos_set:
from_pos: start position
to_pos: end position
time: duration in milliseconds of the interpolation
cut_type: CUT_TYPE.MOVE or CUT_TYPE.CUT
'''
class InterpolateCamera(Rpc):
    def __init__(self, pos_set, from_pos, to_pos, time, cut_type):
        super().__init__(RPC.INTERPOLATE_CAMERA)
        self.pos_set = pos_set
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.time = time
        self.cut_type = cut_type

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.pos_set)
        self.from_pos.encode(bs)
        self.to_pos.encode(bs)
        bs.write_u32(self.time)
        bs.write_u8(self.cut_type)

    @staticmethod
    def decode_rpc_payload(bs):
        pos_set = bs.read_bit()
        from_pos = bs.read_vec3()
        to_pos = bs.read_vec3()
        time = bs.read_u32()
        cut_type = bs.read_u8()
        return InterpolateCamera(pos_set, from_pos, to_pos, time, cut_type)

''' C2S
Client sends when it clicks a textdraw
textdraw_id: id of the textdraw that was clicked
'''
class ClickTextdraw(Rpc):
    def __init__(self, textdraw_id):
        super().__init__(RPC.CLICK_TEXTDRAW)
        self.textdraw_id = textdraw_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        return ClickTextdraw(textdraw_id)

''' S2C
Determines whether or not the player may click textdraws.
clickable: True or False
color: hover color?
'''
class ToggleTextdrawsClickable(Rpc):
    def __init__(self, clickable, color):
        super().__init__(RPC.TOGGLE_TEXTDRAWS_CLICKABLE)
        self.clickable = bool(clickable)
        self.color = Color(color)

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.clickable)
        bs.write_u32(self.color)

    @staticmethod
    def decode_rpc_payload(bs):
        clickable = bs.read_bit()
        color = bs.read_u32()
        return ToggleTextdrawsClickable(clickable, color)

class SetPlayerObjectMaterial(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_OBJECT_MATERIAL)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerObjectMaterial()

class StopFlashGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.STOP_FLASH_GANG_ZONE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return StopFlashGangZone()

class ApplyPlayerAnimation(Rpc):
    def __init__(self, player_id, anim_lib, anim_name, delta, loop, lockx, locky, freeze, time):
        super().__init__(RPC.APPLY_PLAYER_ANIMATION)
        self.player_id = player_id
        self.anim_lib = anim_lib
        self.anim_name = anim_name
        self.delta = float(delta)
        self.loop = loop
        self.lockx = lockx
        self.locky = locky
        self.freeze = freeze
        self.time = time

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_dynamic_str8(self.anim_lib)
        bs.write_dynamic_str8(self.anim_name)
        bs.write_float(self.delta)
        bs.write_bit(self.loop)
        bs.write_bit(self.lockx)
        bs.write_bit(self.locky)
        bs.write_bit(self.freeze)
        bs.write_u32(self.time)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        anim_lib = bs.read_dynamic_str8()
        anim_name = bs.read_dynamic_str8()
        delta = bs.read_float()
        loop = bs.read_bit()
        lockx = bs.read_bit()
        locky = bs.read_bit()
        freeze = bs.read_bit()
        time = bs.read_u32()
        return ApplyPlayerAnimation(player_id, anim_lib, anim_name, delta, loop, lockx, locky, freeze, time)

class ClearPlayerAnimation(Rpc):
    def __init__(self, player_id):
        super().__init__(RPC.CLEAR_PLAYER_ANIMATION)
        self.player_id = player_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        return ClearPlayerAnimation(player_id)

''' S2C
Sets the special action.
action_id: see the SPECIAL_ACTION enum class
BUG: Removing jetpacks from players by setting their special action to 0 causes the sound to stay until death.
'''
class SetSpecialAction(Rpc):
    def __init__(self, action_id):
        super().__init__(RPC.SET_SPECIAL_ACTION)
        self.action_id = action_id

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.action_id)

    @staticmethod
    def decode_rpc_payload(bs):
        action_id = bs.read_u8()
        return SetSpecialAction(action_id)

''' S2C
Sets the fighting style of the specified player.
player_id: id of the player to set the fighting style
fighting_style: value to set; see the FIGHTING_STYLE class enum
'''
class SetPlayerFightingStyle(Rpc):
    def __init__(self, player_id, fighting_style):
        super().__init__(RPC.SET_PLAYER_FIGHTING_STYLE)
        self.player_id = player_id
        self.fighting_style = fighting_style

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.fighting_style)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        fighting_style = bs.read_u8()
        return SetPlayerFightingStyle(player_id, fighting_style)

''' S2C
Sets the velocity of the player this RPC is sent to.
vel: velocity to set (Vec3)
Related: SetPlayerVelocity
'''
class SetVelocity(Rpc):
    def __init__(self, vel):
        super().__init__(RPC.SET_VELOCITY)
        self.vel = vel # new player velocity as Vec3

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.vel)

    @staticmethod
    def decode_rpc_payload(bs):
        vel = bs.read_vec3()
        return SetVelocity(vel)

class VEHICLE_VELOCITY(enum.IntEnum):
    LINEAR  = 0
    ANGULAR = 1

''' S2C
Sets the (linear or angular)velocity of the vehicle the player is in.
This RPC has no affect on un-occupied vehicles and does not affect trains.
type: either VEHICLE_VELOCITY.LINEAR or VEHICLE_VELOCITY.ANGULAR
'''
class SetVehicleVelocity(Rpc):
    def __init__(self, type, vel):
        super().__init__(RPC.SET_VEHICLE_VELOCITY)
        self.type = VEHICLE_VELOCITY(type)
        self.vel = vel

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.type)
        bs.write_vec3(self.vel)

    @staticmethod
    def decode_rpc_payload(bs):
        type = bs.read_u8()
        vel = bs.read_vec3()
        return SetVehicleVelocity(type, vel)

''' S2C
Sends a chat message.
message: message
color: color as RRGGBBAA
e.g. ChatMessage('Invalid command', 0xdd0000ff) shows as 'Invalid command' (in red)
Related: SendClientMessage
'''
class ChatMessage(Rpc):
    def __init__(self, message, color=0xffffffff):
        super().__init__(RPC.CHAT_MESSAGE)
        self.message = message
        self.color = Color(color)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.color)
        bs.write_dynamic_str32(self.message)

    @staticmethod
    def decode_rpc_payload(bs):
        color = bs.read_u32()
        message = bs.read_dynamic_str32()
        return ChatMessage(message, color)

class SetWorldTime(Rpc):
    def __init__(self, hour):
        super().__init__(RPC.SET_WORLD_TIME)
        self.hour = hour

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.hour)

    @staticmethod
    def decode_rpc_payload(bs):
        hour = bs.read_u8()
        return SetWorldTime(hour)

''' S2C
Type Description
0    It has no special attributes and cannot be picked up. It also does not trigger OnPlayerPickUpPickup, and is not removed when closing the server
1    Exists always. Disables pickup scripts such as horseshoes and oysters to allow for scripted actions ONLY. Will trigger OnPlayerPickUpPickup every few seconds. This is likely a SA-MP bug
2    Disappears after pickup, respawns after 30 seconds if the player is at a distance of at least 15 meters (used for money pickups)
3    Disappears after pickup, respawns after death
4    Disappears after 20 seconds. Respawns after death
5    Disappears after 120 seconds. Respawns after death
8    Disappears after pickup, but has no effect (used for money pickups)
9    Explodes on contact with any ground vehicle in 10 seconds after creation (used for land mines)
10   Explodes on contact with any ground vehicle (used for land mines)
11   Explodes on contact with any vessel in 10 seconds after creation (used for nautical/sea mines)
12   Explodes on contact with any vessel (used for nautical/sea mines)
13   Invisible. Triggers checkpoint sound when picked up with a vehicle, but doesn't trigger OnPlayerPickUpPickup (floating pickup)
14   Disappears after pickup, can only be picked up with a vehicle. Triggers checkpoint sound (floating pickup)
15   Same as type 2, however the pickup will respawn after 12 minutes. If the model ID is a bribe, it will respawn after just 5 minutes.
18   Similar to type 1. Pressing Tab (KEY_ACTION) makes it disappear but the key press doesn't trigger OnPlayerPickUpPickup (used for properties)
19   Disappears after pickup, but doesn't respawn. Makes "cash pickup" sound if picked up
20   Similar to type 1. Disappears when you take a picture of it with the Camera weapon, which triggers "Snapshot # out of 0" message. Taking a picture doesn't trigger OnPlayerPickUpPickup (used for snapshot locations)
22   Same as type 3 (used for missions)
'''
class CreatePickup(Rpc):
    def __init__(self, pickup_id, model_id, type, pos):
        super().__init__(RPC.CREATE_PICKUP)
        self.pickup_id = pickup_id
        self.model_id = model_id
        self.type = type
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.pickup_id)
        bs.write_u32(self.model_id)
        bs.write_u32(self.type)
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        pickup_id = bs.read_u32()
        model_id = bs.read_u32()
        type = bs.read_u32()
        pos = bs.read_vec3()
        return CreatePickup(pickup_id, model_id, type, pos)

class ScmEvent(Rpc):
    def __init__(self):
        super().__init__(RPC.SCM_EVENT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ScmEvent()

class DestroyWeaponPickup(Rpc):
    def __init__(self):
        super().__init__(RPC.DESTROY_WEAPON_PICKUP)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DestroyWeaponPickup()

class MoveObject(Rpc):
    def __init__(self, object_id, pos, target, speed, target_r):
        super().__init__(RPC.MOVE_OBJECT)
        self.object_id = object_id
        self.pos = pos
        self.target = target
        self.speed = speed
        self.target_r = target_r

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.object_id)
        bs.write_vec3(self.pos)
        self.target.encode(bs)
        bs.write_float(self.speed)
        self.target_r.encode(bs)

    @staticmethod
    def decode_rpc_payload(bs):
        object_id = bs.read_u16()
        pos = bs.read_vec3()
        target = bs.read_vec3()
        speed = bs.read_float()
        target_r = bs.read_vec3()
        return MoveObject(object_id, pos, target, speed, target_r)

''' C2S
Sent when something is typed in chat that doesn't start with '/'(because it would then be a RequestChatCommand RPC).
Note: Ideally the server processes the request and sends a PlayerChatMessage RPC to whoever should get our message
e.g. RequestChatMessage('Hello, I am a player!')
Related: PlayerRequestChatMessage, ChatMessage 
'''
class RequestChatMessage(Rpc):
    def __init__(self, message):
        super().__init__(RPC.REQUEST_CHAT_MESSAGE)
        self.message = message

    def encode_rpc_payload(self, bs):
        bs.write_dynamic_str8(self.message)

    @staticmethod
    def decode_rpc_payload(bs):
        message = bs.read_dynamic_str8()
        return RequestChatMessage(message)
RPC.REQUEST_CHAT_MESSAGE.decode_client_rpc_payload = RequestChatMessage.decode_rpc_payload

''' S2C
Sends a player chat message
e.g. assuming 'Bob' has id 123, then PlayerChatMessage(123, 'Hello, I am bob!') shows in chat as 'Bob: Hello I am bob'.
Related: PlayerChatMessage, ChatMessage
'''
class PlayerChatMessage(Rpc):
    def __init__(self, player_id, message):
        super().__init__(RPC.PLAYER_CHAT_MESSAGE)
        self.player_id = player_id
        self.message = message

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_dynamic_str8(self.message)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        message = bs.read_dynamic_str8()
        return PlayerChatMessage(player_id, message)
RPC.PLAYER_CHAT_MESSAGE.decode_server_rpc_payload = PlayerChatMessage.decode_rpc_payload

class SvrStats(Rpc):
    def __init__(self):
        super().__init__(RPC.SVR_STATS)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SvrStats()

# https://www.blast.hk/threads/11140/
#unknown types? (5, 69)
class CLIENT_CHECK(enum.IntEnum):
    # server sends ClientCheck(arg=0, offset=0, size=2)
    # clients answers ClientCheckResponse(arg=flags, checksum=?)
    # returns 32 flags from the CPhysicalSA structure
    # flags include: if in vehicle, on foot, in water, vulnerable to damage...
    FLAGS = 2

    # server sends ClientCheck(arg=model id, offset=0, size=size)
    # client answers ClientCheckResponse(arg=model id in request, checksum=checksum)
    # reads the data of the specified model's CBaseModelInfoSA structure and returns a one-byte checksum
    BASE_MODEL_CHECKSUM = 70

    # server sends ClientCheck(arg=model id, offset=0, size=size)
    # client answers ClientCheckResponse(arg=model id in request, checksum=checksum)
    # reads the data of the specified model's CColModelSA structure and returns a one-byte checksum
    COLLISION_MODEL_CHECKSUM = 71

    # server sends ClientCheck(arg=0, offset=0, size=2)
    # client answers ClientCheckResponse(arg=boot time in ms, checksum=0)
    # may be used to detect PC/Android, because apparently android clients do not respond to it
    BOOT_TIME = 72

''' S2C
Perform a memory check on the client
type: see the CLIENT_CHECK enum
arg: depends on type
offset: depends on type
size: 2 or greater
'''
class ClientCheck(Rpc):
    def __init__(self, type, arg, offset, size):
        super().__init__(RPC.CLIENT_CHECK)
        self.type = type
        self.arg = arg
        self.offset = offset
        self.size = size

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.type)
        bs.write_u32(self.arg)
        bs.write_u16(self.offset)
        bs.write_u16(self.size)

    @staticmethod
    def decode_rpc_payload(bs):
        type = bs.read_u8()
        arg = bs.read_u32()
        offset = bs.read_u16()
        size = bs.read_u16()
        return ClientCheck(type, arg, offset, size)
CLIENT_CHECK.decode_server_rpc_payload = ClientCheck.decode_rpc_payload

''' C2S
Responds to a server ClientCheck
type: see the CLIENT_CHECK enum
arg: depends on type
checksum: depends on type
'''
class ClientCheckResponse(Rpc):
    def __init__(self, type, arg, checksum):
        super().__init__(RPC.CLIENT_CHECK_RESPONSE)
        self.type = type
        self.arg = arg
        self.checksum = checksum

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.type)
        bs.write_u32(self.arg)
        bs.write_u8(self.checksum)

    @staticmethod
    def decode_rpc_payload(bs):
        type = bs.read_u8()
        arg = bs.read_u32()
        checksum = bs.read_u8()
        return ClientCheckResponse(type, arg, checksum)
RPC.CLIENT_CHECK_RESPONSE.decode_client_rpc_payload = ClientCheckResponse.decode_rpc_payload

''' S2C
Enables or disables stunt bonuses.
enable: True or False
'''
class ToggleStuntBonus(Rpc):
    def __init__(self, enable):
        super().__init__(RPC.TOGGLE_STUNT_BONUS)
        self.enable = bool(enable)

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.enable)

    @staticmethod
    def decode_rpc_payload(bs):
        enable = bs.read_bit()
        return ToggleStuntBonus(enable)

class SetTextdrawText(Rpc):
    def __init__(self, textdraw_id, text):
        super().__init__(RPC.SET_TEXTDRAW_TEXT)
        self.textdraw_id = textdraw_id
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)
        bs.write_dynamic_str16(self.text)

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        text = bs.read_dynamic_str16()
        return SetTextdrawText(textdraw_id, text)

class DamageVehicle(Rpc):
    def __init__(self, vehicle_id, panels, doors, lights, tires):
        super().__init__(RPC.DAMAGE_VEHICLE)
        self.vehicle_id = vehicle_id
        self.panels = panels
        self.doors = doors
        self.lights = lights
        self.tires = tires

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u32(self.panels)
        bs.write_u32(self.doors)
        bs.write_u8(self.lights)
        bs.write_u8(self.tires)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        panels = bs.read_u32()
        doors = bs.read_u32()
        lights = bs.read_u8()
        tires = bs.read_u8()
        return DamageVehicle(vehicle_id, panels, doors, lights, tires)

class SetCheckpoint(Rpc):
    def __init__(self, pos, radius):
        super().__init__(RPC.SET_CHECKPOINT)
        self.pos = pos
        self.radius = radius

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)
        bs.write_float(self.radius)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        radius = bs.read_float()
        return SetCheckpoint(pos, radius)

class AddGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.ADD_GANG_ZONE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AddGangZone()

class PlayCrimeReport(Rpc):
    def __init__(self):
        super().__init__(RPC.PLAY_CRIME_REPORT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return PlayCrimeReport()

class SetPlayerAttachedObject(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_ATTACHED_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerAttachedObject()

# Used by GiveTakeDamage and GiveActorDamage
class BODY_PART(enum.IntEnum):
    TORSO     = 3
    GROIN     = 4
    LEFT_ARM  = 5
    RIGHT_ARM = 6
    LEFT_LEG  = 7
    RIGHT_LEG = 8
    HEAD      = 9

''' C2S
Client sends when takes or gives damage
take: 1=took damage; 0=gave damage
player_id: id of the player the client damaged; only used if take is 0(i.e. client damaged someone)
amount: amount of damage given or taken
weapon_id: weapon used to inflict damage; see WEAPON enum
body_part: body part where damage was applied to; see BODY_PART enum
'''
class GiveTakeDamage(Rpc):
    def __init__(self, take, player_id, amount, weapon_id, body_part):
        super().__init__(RPC.GIVE_TAKE_DAMAGE)
        self.take = take
        self.player_id = player_id
        self.amount = amount
        self.weapon_id = weapon_id
        self.body_part = body_part

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.take)
        bs.write_u16(self.player_id)
        bs.write_float(self.amount)
        bs.write_u32(self.weapon_id)
        bs.write_u32(self.body_part)

    @staticmethod
    def decode_rpc_payload(bs):
        take = bs.read_bit()
        player_id = bs.read_u16()
        amount = bs.read_float()
        weapon_id = bs.read_u32()
        body_part = bs.read_u32()
        return GiveTakeDamage(take, player_id, amount, weapon_id, body_part)

class EditAttachedObject(Rpc):
    def __init__(self):
        super().__init__(RPC.EDIT_ATTACHED_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EditAttachedObject()

class EditObject(Rpc):
    def __init__(self):
        super().__init__(RPC.EDIT_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EditObject()

''' C2S
Client sends when the interior changes
'''
class InteriorChange(Rpc):
    def __init__(self, interior_id):
        super().__init__(RPC.INTERIOR_CHANGE)
        self.interior_id = interior_id

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.interior_id)

    @staticmethod
    def decode_rpc_payload(bs):
        interior_id = bs.read_u8()
        return InteriorChange(interior_id)

class MapMarker(Rpc):
    def __init__(self):
        super().__init__(RPC.MAP_MARKER)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return MapMarker()

class RemoveGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_GANG_ZONE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveGangZone()

class FlashGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.FLASH_GANG_ZONE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return FlashGangZone()

class StopObject(Rpc):
    def __init__(self):
        super().__init__(RPC.STOP_OBJECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return StopObject()

class SetVehicleNumberPlate(Rpc):
    def __init__(self, vehicle_id, text):
        super().__init__(RPC.SET_VEHICLE_NUMBER_PLATE)
        self.vehicle_id = vehicle_id
        self.text = text

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_dynamic_str8(self.text)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        text = bs.read_dynamic_str8()
        return SetVehicleNumberPlate(vehicle_id, text)

''' S2C
Enables or disables spectator mode.
enable: True or False
Note: The server should send SpectatePlayer or SpectateVehicle after sending this RPC
'''
class ToggleSpectate(Rpc):
    def __init__(self, enable):
        super().__init__(RPC.TOGGLE_SPECTATE)
        self.enable = bool(enable)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.enable)

    @staticmethod
    def decode_rpc_payload(bs):
        enable = bs.read_u32()
        return ToggleSpectate(enable)

class SPECTATE_MODE(enum.IntEnum):
    NORMAL = 1 # Normal spectate mode (third person point of view). Camera can not be changed
    FIXED = 2 # Use SetPlayerCameraPos after this to position the player's camera, and it will track the player/vehicle set with PlayerSpectatePlayer/PlayerSpectateVehicle
    SIDE = 3 # The camera will be attached to the side of the player/vehicle (like when you're in first-person camera on a bike and you do a wheelie)

''' S2C
'''
class SpectatePlayer(Rpc):
    def __init__(self, player_id, mode):
        super().__init__(RPC.SPECTATE_PLAYER)
        self.player_id = player_id
        self.mode = SPECTATE_MODE(mode)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.mode)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        mode = bs.read_u8()
        return SpectatePlayer(player_id, mode)

''' S2C
'''
class SpectateVehicle(Rpc):
    def __init__(self, vehicle_id, mode):
        super().__init__(RPC.SPECTATE_VEHICLE)
        self.vehicle_id = vehicle_id
        self.mode = SPECTATE_MODE(mode)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.mode)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        mode = bs.read_u8()
        return SpectateVehicle(vehicle_id, mode)

''' C2S
'''
class RequestClass(Rpc):
    def __init__(self, class_id=None):
        super().__init__(RPC.REQUEST_CLASS)
        self.class_id = class_id

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.class_id)

    @staticmethod
    def decode_rpc_payload(bs):
        class_id = bs.read_u32()
        return RequestClass(class_id)

''' S2C
if response is 0 then all other parameters will be ignored
response: either 1 or 0
team: new team; valid team values are 0-254; None specifies the player is not in any team(internally it is defined as 255)
dir_z: Z component of the direction(orientation) of the player's character and camera(because they are the same value when the player spawns); 0.0 is North
'''
class RequestClassResponse(Rpc):
    def __init__(self, response, team=None, skin=None, pos=None, dir_z=None, weapon1=None, weapon2=None, weapon3=None):
        super().__init__(RPC.REQUEST_CLASS_RESPONSE)
        self.response = response
        self.team = team
        self.skin = None if skin is None else SKIN(skin)
        self.pos = pos
        self.dir_z = dir_z
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.weapon3 = weapon3

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.response)
        if self.response == 0:
            return
        bs.write_u8(NO_TEAM_ID if self.team is None else self.team)
        bs.write_u32(self.skin)
        bs.write_u8(0) # unused
        bs.write_vec3(self.pos)
        bs.write_float(self.dir_z)
        bs.write_u32(self.weapon1.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon1.ammo)
        bs.write_u32(self.weapon2.ammo)
        bs.write_u32(self.weapon3.ammo)

    @staticmethod
    def decode_rpc_payload(bs):
        team = skin = pos = dir_z = weapon1 = weapon2 = weapon3 = None
        if (response := bool(bs.read_u8())) is True:
            team = bs.read_u8()
            skin = bs.read_u32()
            bs.skip_bits(8) # unused
            pos = bs.read_vec3()
            dir_z = bs.read_float()
            weapon1_id = bs.read_u32()
            weapon2_id = bs.read_u32()
            weapon3_id = bs.read_u32()
            weapon1_ammo = bs.read_u32()
            weapon2_ammo = bs.read_u32()
            weapon3_ammo = bs.read_u32()
            weapon1 = Weapon(weapon1_id, weapon1_ammo)
            weapon2 = Weapon(weapon2_id, weapon2_ammo)
            weapon3 = Weapon(weapon3_id, weapon3_ammo)
        return RequestClassResponse(response, team, skin, pos, dir_z, weapon1, weapon2, weapon3)
RPC.REQUEST_CLASS_RESPONSE.decode_server_rpc_payload = RequestClassResponse.decode_rpc_payload

''' C2S
Sent when the client clicks the SPAWN button.
'''
class RequestSpawn(Rpc):
    def __init__(self):
        super().__init__(RPC.REQUEST_SPAWN)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RequestSpawn()
RPC.REQUEST_SPAWN.decode_client_rpc_payload = RequestSpawn.decode_rpc_payload

class REQUEST_SPAWN(enum.IntEnum):
    REJECT = 0
    ACCEPT = 1
    FORCE  = 2

''' S2C
When the client sends a RequestSpawn RPC, the server should respond with this RPC.
Note: The server may send this RPC at any point with the REQUEST_SPAWN.FORCE response to make the client spawn or respawn(if already spawned)
Note: Make sure to send SetSpawnInfo before attempting to make the client spawn(otherwise it won't spawn)
'''
class RequestSpawnResponse(Rpc):
    def __init__(self, response):
        super().__init__(RPC.REQUEST_SPAWN_RESPONSE)
        self.response = REQUEST_SPAWN(response)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.response)

    @staticmethod
    def decode_rpc_payload(bs):
        response = bs.read_u8()
        return RequestSpawnResponse(response)
RPC.REQUEST_SPAWN_RESPONSE.decode_server_rpc_payload = RequestSpawnResponse.decode_rpc_payload

class REJECT_REASON(enum.IntEnum):
    BAD_VERSION  = 1
    BAD_NICKNAME = 2
    BAD_MOD      = 3
    BAD_PLAYERID = 4

class ConnectionRejected(Rpc):
    def __init__(self, reason):
        super().__init__(RPC.CONNECTION_REJECTED)
        self.reason = REJECT_REASON(reason)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.reason)

    @staticmethod
    def decode_rpc_payload(bs):
        reason = bs.read_u8()
        return ConnectionRejected(reason)

class PickedUpPickup(Rpc):
    def __init__(self, pickup_id):
        super().__init__(RPC.PICKED_UP_PICKUP)
        self.pickup_id = pickup_id

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.pickup_id)

    @staticmethod
    def decode_rpc_payload(bs):
        pickup_id = bs.read_u32()
        return PickedUpPickup(pickup_id)

class MenuSelect(Rpc):
    def __init__(self):
        super().__init__(RPC.MENU_SELECT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return MenuSelect()

''' S2C
Set the wanted level.
level: new wanted value.
Related: SetPlayerWantedLevel
'''
class SetWantedLevel(Rpc):
    def __init__(self, level):
        super().__init__(RPC.SET_WANTED_LEVEL)
        self.level = level

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.level)

    @staticmethod
    def decode_rpc_payload(bs):
        level = bs.read_u8()
        return SetWantedLevel(level)

# resources
# https://www.mixmods.com.br/2013/07/fontes-das-letras-do-gta-sa/
# https://team.sa-mp.com/wiki/PlayerTextDrawFont.html
# https://www.open.mp/docs/scripting/functions/PlayerTextDrawFont

class TEXTDRAW_FLAG(enum.IntEnum):
    BOX = (1 << 7),
    LEFT = (1 << 6),
    RIGHT = (1 << 5),
    CENTER = (1 << 4),
    PROPORTIONAL = (1 << 3),

class TEXTDRAW_STYLE(enum.IntEnum):
	FONT_BECKETT_REGULAR = 0 # Font
	FONT_AHARONI_BOLD    = 1 # Font
	FONT_BANK_GOTHIC     = 2 # Font
	FONT_PRICEDOWN       = 3 # Font
	SPRITE               = 4 # TXD sprite
	MODEL                = 5 # Model

''' S2C
Shows a textdraw.
textdraw_id: [0, 2303]
pos: screen coordinate; Vec2(x, y) based on a 640x480 "imaginary canvas" (irrespective of screen resolution).
leter_size: Vec2(character_width, character_height); Recommended: height to width ratio of 4 to 1 (e.g. if x is 0.5 then y should be 2).
flags: a member of TEXTDRAW_FLAG
style: a member of TEXTDRAW_STYLE
'''
class ShowTextdraw(Rpc):
    def __init__(self, textdraw_id, text, pos, flags=0, letter_size=Vec2(1,1), letter_color=0xffffffff, line_size=Vec2(0,0), box_color=0, shadow=0, outline=0, background_color=0x00000000, style=TEXTDRAW_STYLE.FONT_BECKETT_REGULAR, clickable=False, model_id=None, model_dir=None, model_zoom=None, model_color1=None, model_color2=None):
        super().__init__(RPC.SHOW_TEXTDRAW)
        self.textdraw_id = textdraw_id
        self.text = text
        self.pos = pos
        self.flags = flags
        self.letter_size = letter_size
        self.letter_color = Color(letter_color)
        self.line_size = line_size
        self.box_color = Color(box_color)
        self.shadow = shadow
        self.outline = outline
        self.background_color = Color(background_color)
        self.style = TEXTDRAW_STYLE(style)
        self.clickable = bool(clickable)
        self.model_id = model_id
        self.model_dir = model_dir
        self.model_zoom = model_zoom
        self.model_color1 = model_color1
        self.model_color2 = model_color2

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)
        bs.write_u8(self.flags)
        bs.write_vec2(self.letter_size)
        bs.write_u32(self.letter_color)
        bs.write_vec2(self.line_size)
        bs.write_u32(self.box_color)
        bs.write_u8(self.shadow)
        bs.write_u8(self.outline)
        bs.write_u32(self.background_color)
        bs.write_u8(self.style)
        bs.write_u8(self.clickable)
        bs.write_vec2(self.pos)
        bs.write_u16(0 if self.model_id is None else self.model_id)
        bs.write_vec3(Vec3(0.0, 0.0, 0.0) if self.model_dir is None else self.model_dir)
        bs.write_float(1.0 if self.model_zoom is None else self.model_zoom)
        bs.write_i16(-1 if self.model_color1 is None else self.model_color1)
        bs.write_i16(-1 if self.model_color2 is None else self.model_color2)
        bs.write_dynamic_str16(self.text)

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        flags = bs.read_u8()
        letter_size = bs.read_vec2()
        letter_color = bs.read_u32()
        line_size = bs.read_vec2()
        box_color = bs.read_u32()
        shadow = bs.read_u8()
        outline = bs.read_u8()
        background_color = bs.read_u32()
        style = bs.read_u8()
        clickable = bs.read_u8()
        pos = bs.read_vec2()
        model_id = bs.read_u16()
        model_dir = bs.read_vec3()
        model_zoom = bs.read_float()
        model_color1 = bs.read_u16()
        model_color2 = bs.read_u16()
        if style != TEXTDRAW_STYLE.MODEL:
            model_id = model_dir = model_zoom = model_color1 = model_color2 = None
        text = bs.read_dynamic_str16()
        return ShowTextdraw(textdraw_id, text, pos, flags, letter_size, letter_color, line_size, box_color, shadow, outline, background_color, style, clickable, model_id, model_dir, model_zoom, model_color1, model_color2)

class HideTextdraw(Rpc):
    def __init__(self, textdraw_id):
        super().__init__(RPC.HIDE_TEXTDRAW)
        self.textdraw_id = textdraw_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        return HideTextdraw(textdraw_id)

class VehicleDestroyed(Rpc):
    def __init__(self):
        super().__init__(RPC.VEHICLE_DESTROYED)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return VehicleDestroyed()

''' S2C
Notifies that the specified player has connected to the server.
player_id: id(index) of the player in the player pool to be added
color: color as RRGGBBAA; shows in the scoreboard and ingame as the tag color
is_npc: True or False
player_name: name
'''
class ServerJoin(Rpc):
    def __init__(self, player_id, player_name, color=0xffffffff, is_npc=False):
        super().__init__(RPC.SERVER_JOIN)
        self.player_id = player_id
        self.color = Color(color)
        self.is_npc = bool(is_npc)
        self.player_name = player_name

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.color)
        bs.write_u8(self.is_npc)
        bs.write_dynamic_str8(self.player_name)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        color = bs.read_u32()
        is_npc = bs.read_u8()
        player_name = bs.read_dynamic_str8()
        return ServerJoin(player_id, player_name, color, is_npc)

class QUIT_REASON(enum.IntEnum):
    TIMEOUT  = 0
    QUIT     = 1
    KICK_BAN = 2

''' S2C
Notifies that the specified player has disconnected from the server.
reason: a member of QUIT_REASON
'''
class ServerQuit(Rpc):
    def __init__(self, player_id, reason=QUIT_REASON.QUIT):
        super().__init__(RPC.SERVER_QUIT)
        self.player_id = player_id
        self.reason = QUIT_REASON(reason)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.reason)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        reason = bs.read_u8()
        return ServerQuit(player_id, reason)

''' S2C
Usually sent to a client after it sends a ClientJoin RPC.
'''
class InitGame(Rpc):
    def __init__(self, zone_names, use_cj_walk, allow_weapons, limit_global_chat_radius, global_chat_radius, stunt_bonus, name_tag_draw_distance, disable_enter_exits, name_tag_los, manual_vehicle_engine_and_light, spawns_available, player_id, show_player_tags, show_player_markers, world_time, weather, gravity, lan_mode, death_drop_money, instagib, onfoot_rate, incar_rate, weapon_rate, multiplier, lag_comp, hostname, vehicle_models, vehicle_friendly_fire):
        super().__init__(RPC.INIT_GAME)
        self.zone_names = zone_names
        self.use_cj_walk = use_cj_walk
        self.allow_weapons = allow_weapons
        self.limit_global_chat_radius = limit_global_chat_radius
        self.global_chat_radius = global_chat_radius
        self.stunt_bonus = stunt_bonus
        self.name_tag_draw_distance = name_tag_draw_distance
        self.disable_enter_exits = disable_enter_exits
        self.name_tag_los = name_tag_los
        self.manual_vehicle_engine_and_light = manual_vehicle_engine_and_light
        self.spawns_available = spawns_available
        self.player_id = player_id
        self.show_player_tags = show_player_tags
        self.show_player_markers = show_player_markers
        self.world_time = world_time
        self.weather = weather
        self.gravity = float(gravity)
        self.lan_mode = lan_mode
        self.death_drop_money = death_drop_money
        self.instagib = instagib
        self.onfoot_rate = onfoot_rate
        self.incar_rate = incar_rate
        self.weapon_rate = weapon_rate
        self.multiplier = multiplier
        self.lag_comp = lag_comp
        self.hostname = hostname
        self.vehicle_models = vehicle_models
        self.vehicle_friendly_fire = vehicle_friendly_fire

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.zone_names)
        bs.write_bit(self.use_cj_walk)
        bs.write_bit(self.allow_weapons)
        bs.write_bit(self.limit_global_chat_radius)
        bs.write_float(self.global_chat_radius)
        bs.write_bit(self.stunt_bonus)
        bs.write_float(self.name_tag_draw_distance)
        bs.write_bit(self.disable_enter_exits)
        bs.write_bit(self.name_tag_los)
        bs.write_bit(self.manual_vehicle_engine_and_light)
        bs.write_u32(self.spawns_available)
        bs.write_u16(self.player_id)
        bs.write_bit(self.show_player_tags)
        bs.write_u32(self.show_player_markers)
        bs.write_u8(self.world_time)
        bs.write_u8(self.weather)
        bs.write_float(self.gravity)
        bs.write_bit(self.lan_mode)
        bs.write_u32(self.death_drop_money)
        bs.write_bit(self.instagib)
        bs.write_u32(self.onfoot_rate)
        bs.write_u32(self.incar_rate)
        bs.write_u32(self.weapon_rate)
        bs.write_u32(self.multiplier)
        bs.write_u32(self.lag_comp)
        bs.write_dynamic_str8(self.hostname)
        bs.write_bits(bytearray(self.vehicle_models), TO_BITS(212))
        bs.write_u32(self.vehicle_friendly_fire)

    @staticmethod
    def decode_rpc_payload(bs):
        zone_names                       = bs.read_bit()
        use_cj_walk                      = bs.read_bit()
        allow_weapons                    = bs.read_bit()
        limit_global_chat_radius         = bs.read_bit()
        global_chat_radius               = bs.read_float()
        stunt_bonus                      = bs.read_bit()
        name_tag_draw_distance           = bs.read_float()
        disable_enter_exits              = bs.read_bit()
        name_tag_los                     = bs.read_bit()
        manual_vehicle_engine_and_light  = bs.read_bit()
        spawns_available                 = bs.read_u32()
        player_id                        = bs.read_u16()
        show_player_tags                 = bs.read_bit()
        show_player_markers              = bs.read_u32()
        world_time                       = bs.read_u8()
        weather                          = bs.read_u8()
        gravity                          = bs.read_float()
        lan_mode                         = bs.read_bit()
        death_drop_money                 = bs.read_u32()
        instagib                         = bs.read_bit()
        onfoot_rate                      = bs.read_u32()
        incar_rate                       = bs.read_u32()
        weapon_rate                      = bs.read_u32()
        multiplier                       = bs.read_u32()
        lag_comp                         = bs.read_u32()

        hostname_size = bs.read_u8()
        hostname = bytearray(hostname_size)
        bs.read_bits(hostname, TO_BITS(hostname_size))
        hostname = hostname.decode(SAMP_ENCODING)

        vehicle_models = bytearray(212)
        bs.read_bits(vehicle_models, TO_BITS(212))

        vehicle_friendly_fire = bs.read_u32()

        return InitGame(zone_names, use_cj_walk, allow_weapons, limit_global_chat_radius, global_chat_radius, stunt_bonus, name_tag_draw_distance, disable_enter_exits, name_tag_los, manual_vehicle_engine_and_light, spawns_available, player_id, show_player_tags, show_player_markers, world_time, weather, gravity, lan_mode, death_drop_money, instagib, onfoot_rate, incar_rate, weapon_rate, multiplier, lag_comp, hostname, vehicle_models, vehicle_friendly_fire)

class MenuQuit(Rpc):
    def __init__(self):
        super().__init__(RPC.MENU_QUIT)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return MenuQuit()

class RemoveMapIcon(Rpc):
    def __init__(self, icon_id):
        super().__init__(RPC.REMOVE_MAP_ICON)
        self.icon_id = icon_id

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.icon_id)

    @staticmethod
    def decode_rpc_payload(bs):
        icon_id = bs.read_u8()
        return RemoveMapIcon(icon_id)

''' S2C
Sets the ammo of the specified weapon.
e.g. SetWeaponAmmo(WEAPON.MP5, 30) ; Set MP5 ammo to 30; it gives an MP5 if the player did not have one(will not be selected weapon, use GiveWeapon for that)
e.g. SetWeaponAmmo(WEAPON.MP5, 0) ; Removes MP5
Related: SetPlayerAmmo
'''
class SetWeaponAmmo(Rpc):
    def __init__(self, weapon_id, ammo):
        super().__init__(RPC.SET_WEAPON_AMMO)
        self.weapon_id = weapon_id
        self.ammo = ammo

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.weapon_id)
        bs.write_u16(self.ammo)

    @staticmethod
    def decode_rpc_payload(bs):
        weapon_id = bs.read_u8()
        ammo = bs.read_u16()
        return SetWeaponAmmo(weapon_id, ammo)

''' S2C
Sets the gravity value.
gravity: new gravity value; default value is 0.008
e.g. SetGravity(0.008) # resets gravity
Related: SetPlayerGravity
'''
class SetGravity(Rpc):
    def __init__(self, gravity):
        super().__init__(RPC.SET_GRAVITY)
        self.gravity = gravity
    
    def __str__(self): # because of precision
        return f'<SetGravity gravity={self.gravity:.5f}'

    def encode_rpc_payload(self, bs):
        bs.write_float(self.gravity)

    @staticmethod
    def decode_rpc_payload(bs):
        gravity = bs.read_float()
        return SetGravity(gravity)

''' S2C
Sets the health of the specified vehicle.
vehicle_id: id of the vehicle to set the health
health: new health value
Note: A value less than 250.0(represents 25% in a 1000 hp vehicle) makes the vehicle catch on fire and after a few seconds explode.
Note: If the vehicle is on fire(i.e. hp < 250) and the health is set to a value greater or equal to 250 the fire will disappear and the vehicle won't explode.
e.g. SetVehicleHealth(53, 2500) # sets the hp of the vehicle with id 53 to 2500
'''
class SetVehicleHealth(Rpc):
    def __init__(self, vehicle_id, health):
        super().__init__(RPC.SET_VEHICLE_HEALTH)
        self.vehicle_id = vehicle_id
        self.health = health

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_float(self.health)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        health = bs.read_float()
        return SetVehicleHealth(vehicle_id, health)

class AttachTrailerToVehicle(Rpc):
    def __init__(self):
        super().__init__(RPC.ATTACH_TRAILER_TO_VEHICLE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AttachTrailerToVehicle()

class DetachTrailerFromVehicle(Rpc):
    def __init__(self):
        super().__init__(RPC.DETACH_TRAILER_FROM_VEHICLE)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DetachTrailerFromVehicle()

''' S2C
ID  Name                    Type                                   Description (in singleplayer)
0   EXTRASUNNY_LA           Blue skies                             Los Santos specific weather
1   SUNNY_LA                Blue skies                             Los Santos specific weather
2   EXTRASUNNY_SMOG_LA      Blue skies                             Los Santos specific weather
3   SUNNY_SMOG_LA           Blue skies                             Los Santos specific weather
4   CLOUDY_LA               Blue skies                             Los Santos specific weather
5   SUNNY_SF                Blue skies                             San Fierro specific weather
6   EXTRASUNNY_SF           Blue skies                             San Fierro specific weather
7   CLOUDY_SF               Blue skies                             San Fierro specific weather
8   RAINY_SF                Stormy                                 San Fierro specific weather
9   FOGGY_SF                Cloudy and foggy                       San Fierro specific weather
10  SUNNY_VEGAS             Clear blue sky                         Las Venturas specific weather
11  EXTRASUNNY_VEGAS        Heat waves                             Las Venturas specific weather
12  CLOUDY_VEGAS            Dull, colourless                       Las Venturas specific weather
13  EXTRASUNNY_COUNTRYSIDE  Dull, colourless                       Countryside specific weather
14  SUNNY_COUNTRYSIDE       Dull, colourless                       Countryside specific weather
15  CLOUDY_COUNTRYSIDE      Dull, colourless                       Countryside specific weather
16  RAINY_COUNTRYSIDE       Dull, cloudy, rainy                    Countryside specific weather
17  EXTRASUNNY_DESERT       Heat waves                             Bone County specific weather
18  SUNNY_DESERT            Heat waves                             Bone County specific weather
19  SANDSTORM_DESERT        Sandstorm                              Bone County specific weather
20  UNDERWATER              Greenish, foggy                        Used internally when camera is underwater
21  EXTRACOLOURS_1          Very dark, gradiented skyline, purple  Weather used in interiors
22  EXTRACOLOURS_2          Very dark, gradiented skyline, purple  Weather used in interiors
'''
class SetWeather(Rpc):
    def __init__(self, weather_id):
        super().__init__(RPC.SET_WEATHER)
        self.weather_id = weather_id

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.weather_id)

    @staticmethod
    def decode_rpc_payload(bs):
        weather_id = bs.read_u8()
        return SetWeather(weather_id)

''' S2C
Sets the skin of the specified player.
player_id: id of the player to set the skin
skin_id: id of the skin to set; see the SKIN enumeration
'''
class SetPlayerSkin(Rpc):
    def __init__(self, player_id, skin_id):
        super().__init__(RPC.SET_PLAYER_SKIN)
        self.player_id = player_id # id of the player to change the skin
        self.skin_id = skin_id # skin to change to

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.player_id)
        bs.write_u32(self.skin_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u32()
        skin_id = bs.read_u32()
        return SetPlayerSkin(player_id, skin_id)

''' S2C
Makes the specified player do the animation of exiting the specified vehicle.
player_id: id of the player that will do the animation
vehicle_id: the id of the vehicle about to be exited
'''
class PlayerExitVehicle(Rpc):
    def __init__(self, player_id, vehicle_id):
        super().__init__(RPC.PLAYER_EXIT_VEHICLE)
        self.player_id = player_id
        self.vehicle_id = vehicle_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u16(self.vehicle_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        return PlayerExitVehicle(player_id, vehicle_id)

''' C2S
Client sends when it exits a vehicle
vehicle_id: the id of the vehicle about to be exited
'''
class ExitVehicle(Rpc):
    def __init__(self, vehicle_id):
        super().__init__(RPC.EXIT_VEHICLE)
        self.vehicle_id = vehicle_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        return ExitVehicle(vehicle_id)
RPC.EXIT_VEHICLE.decode_client_rpc_payload = ExitVehicle.decode_rpc_payload

''' C2S
Client sends when the scoreboard is opened.
Related: OnPlayerRequestScoresAndPings, UpdateScoresAndPings 
'''
class RequestScoresAndPings(Rpc):
    def __init__(self):
        super().__init__(RPC.REQUEST_SCORES_AND_PINGS)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RequestScoresAndPings()

''' S2C
Response for the RequestScoresAndPings RPC
Provides scoreboard data(score and pings) for ids
players = [(id, score, ping), ...]
Related: SendPlayerScoresAndPings, UpdateScoresAndPings
'''
class RequestScoresAndPingsResponse(Rpc):
    def __init__(self, players):
        super().__init__(RPC.REQUEST_SCORES_AND_PINGS)
        self.players = players

    def encode_rpc_payload(self, bs):
        for id, score, ping in self.players:
            bs.write_u16(id)
            bs.write_u32(score)
            bs.write_u32(ping)

    @staticmethod
    def decode_rpc_payload(bs):
        player_count = TO_BYTES(bs.unread_bits_count()) // 10
        players = [None] * player_count
        for i in range(player_count):
            id = bs.read_u16()
            score = bs.read_u32()
            ping = bs.read_u32()
            players[i] = (id, score, ping)
        return RequestScoresAndPingsResponse(players)
RPC.REQUEST_SCORES_AND_PINGS.decode_server_rpc_payload = RequestScoresAndPingsResponse.decode_rpc_payload

class SetInterior(Rpc):
    def __init__(self, interior_id):
        super().__init__(RPC.SET_INTERIOR)
        self.interior_id = interior_id

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.interior_id)

    @staticmethod
    def decode_rpc_payload(bs):
        interior_id = bs.read_u8()
        return SetInterior(interior_id)

class SetCameraPos(Rpc):
    def __init__(self, pos):
        super().__init__(RPC.SET_CAMERA_POS)
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        return SetCameraPos(pos)

class CAMERA_CUT(enum.IntEnum):
    MOVE = 1 # The camera position and/or target will move to its new value over time.
    CUT = 2 # The camera position and/or target will move to its new value instantly.

class SetCameraLookAt(Rpc):
    def __init__(self, pos, cut_type):
        super().__init__(RPC.SET_CAMERA_LOOK_AT)
        self.pos = pos
        self.cut_type = CAMERA_CUT(cut_type)

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)
        bs.write_u8(self.cut_type)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        cut_type = bs.read_u8()
        return SetCameraLookAt(pos, cut_type)

class SetVehiclePos(Rpc):
    def __init__(self, vehicle_id, pos):
        super().__init__(RPC.SET_VEHICLE_POS)
        self.vehicle_id = vehicle_id
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        pos = bs.read_vec3()
        return SetVehiclePos(vehicle_id, pos)

''' S2C
Sets the Z component of the vehicle's direction(orientation).
angle: new Z value.
Related: SetVehicleZAngle
'''
class SetVehicleDirZ(Rpc):
    def __init__(self, vehicle_id, angle):
        super().__init__(RPC.SET_VEHICLE_DIR_Z)
        self.vehicle_id = vehicle_id
        self.angle = angle

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_float(self.angle)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        angle = bs.read_float()
        return SetVehicleDirZ(vehicle_id, angle)

class SetVehicleParams(Rpc):
    def __init__(self, vehicle_id, objective, doors_locked):
        super().__init__(RPC.SET_VEHICLE_PARAMS)
        self.vehicle_id = vehicle_id
        self.objective = objective
        self.doors_locked = doors_locked

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.objective)
        bs.write_u8(self.doors_locked)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        objective = bs.read_u8()
        doors_locked = bs.read_u8()
        return SetVehicleParams(vehicle_id, objective, doors_locked)

class SetCameraBehindPlayer(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_CAMERA_BEHIND_PLAYER)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetCameraBehindPlayer()

''' S2C
Removes the specified player from the world.
Related: WorldPlayerRemove, PlayerStreamOut
'''
class StopPlayerStream(Rpc):
    def __init__(self, player_id):
        super().__init__(RPC.STOP_PLAYER_STREAM)
        self.player_id = player_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        return StopPlayerStream(player_id)

''' S2C
Adds a vehicle to the world.
vehicle_id: [1, 1999] ; 0 is an invalid id
Note: If the RPC is sent twice(without RemoveVehicle in between) the vehicle respawns and a warning message is shown in the chat
Related: WorldVehicleAdd, StreamInVehicle
e.g. AddVehicle(1, VEHICLE.RHINO, Vec3(0, 0, 3))
'''
class AddVehicle(Rpc):
    def __init__(self, vehicle_id, model_id, pos, health=1000.0, dir_z=0.0, interior_color1=0, interior_color2=0, interior=0, door_damage_status=0, panel_damage_status=0, light_damage_status=0, tire_damage_status=0, add_siren=False, mods=[0]*14, paint_job=0, body_color1=0, body_color2=0):
        super().__init__(RPC.ADD_VEHICLE)
        self.vehicle_id = vehicle_id
        self.model_id = VEHICLE(model_id) # model id of the vehicle; see sa/vehicle.py
        self.pos = pos # position of the vehicle
        self.health = health
        self.dir_z = dir_z # Z component of the vehicle's direction; a.k.a. "yaw"
        self.interior_color1 = interior_color1
        self.interior_color2 = interior_color2
        self.interior = interior
        self.door_damage_status = door_damage_status
        self.panel_damage_status = panel_damage_status
        self.light_damage_status = light_damage_status
        self.tire_damage_status = tire_damage_status
        self.add_siren = add_siren
        self.mods = mods
        self.paint_job = paint_job
        self.body_color1 = Color(body_color1)
        self.body_color2 = Color(body_color2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u32(self.model_id)
        bs.write_vec3(self.pos)
        bs.write_float(self.dir_z)
        bs.write_u8(self.interior_color1)
        bs.write_u8(self.interior_color2)
        bs.write_float(self.health)
        bs.write_u8(self.interior)
        bs.write_u32(self.door_damage_status)
        bs.write_u32(self.panel_damage_status)
        bs.write_u8(self.light_damage_status)
        bs.write_u8(self.tire_damage_status)
        bs.write_u8(self.add_siren)
        for i in range(14): # 14 mods
            bs.write_u8(self.mods[i])
        bs.write_u8(self.paint_job)
        bs.write_u32(self.body_color1)
        bs.write_u32(self.body_color2)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        model_id = bs.read_u32()
        pos = bs.read_vec3()
        dir_z = bs.read_float()
        interior_color1 = bs.read_u8()
        interior_color2 = bs.read_u8()
        health = bs.read_float()
        interior = bs.read_u8()
        door_damage_status = bs.read_u32()
        panel_damage_status = bs.read_u32()
        light_damage_status = bs.read_u8()
        tire_damage_status = bs.read_u8()
        add_siren = bs.read_u8()
        mods = [bs.read_u8() for _ in range(14)]
        paint_job = bs.read_u8()
        body_color1 = bs.read_u32()
        body_color2 = bs.read_u32()
        return AddVehicle(vehicle_id, model_id, pos, health, dir_z, interior_color1, interior_color2, interior, door_damage_status, panel_damage_status, light_damage_status, tire_damage_status, add_siren, mods, paint_job, body_color1, body_color2)

''' S2C
Removes the specified vehicle from the world.
Note: if the id is invalid, the client ignores the RPC.
Related: WorldVehicleRemove, StreamOutVehicle
'''
class RemoveVehicle(Rpc):
    def __init__(self, vehicle_id):
        super().__init__(RPC.REMOVE_VEHICLE)
        self.vehicle_id = vehicle_id # id of the vehicle to remove

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        return RemoveVehicle(vehicle_id)

class DeathBroadcast(Rpc):
    def __init__(self, player_id):
        super().__init__(RPC.DEATH_BROADCAST)
        self.player_id = player_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        return DeathBroadcast(player_id)

''' S2C
Enables or disables vehicle collisions.
enable: True or False
'''
class ToggleVehicleCollisions(Rpc):
    def __init__(self, enable):
        super().__init__(RPC.TOGGLE_VEHICLE_COLLISIONS)
        self.enable = bool(enable)

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.enable)

    @staticmethod
    def decode_rpc_payload(bs):
        enable = bs.read_bit()
        return ToggleVehicleCollisions(enable)

''' C2S
'''
class CameraTarget(Rpc):
    def __init__(self):
        super().__init__(RPC.CAMERA_TARGET)

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return CameraTarget()

''' S2C
Enable or disables camera targeting functions to the specified.
'''
class ToggleCameraTarget(Rpc):
    def __init__(self, enable):
        super().__init__(RPC.TOGGLE_CAMERA_TARGET)
        self.enable = bool(enable)

    def encode_rpc_payload(self, bs):
        bs.write_bit(self.enable)

    @staticmethod
    def decode_rpc_payload(bs):
        enable = bs.read_bit()
        return ToggleCameraTarget(enable)

''' S2C
Adds an actor to the world.
actor_id: id of the actor; [0, 999]
Related: CreateActor, ShowActor, ShowActorForPlayer
'''
class AddActor(Rpc):
    def __init__(self, actor_id, pos, skin_id=SKIN.CJ, dir_z=0.0, health=100.0, invulnerable=True):
        super().__init__(RPC.ADD_ACTOR)
        self.actor_id = actor_id
        self.pos = pos
        self.skin_id = skin_id
        self.dir_z = dir_z
        self.health = health
        self.invulnerable = invulnerable

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)
        bs.write_u32(self.skin_id)
        bs.write_vec3(self.pos)
        bs.write_float(self.dir_z)
        bs.write_float(self.health)
        bs.write_u8(self.invulnerable)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        skin_id = bs.read_u32()
        pos = bs.read_vec3()
        dir_z = bs.read_float()
        health = bs.read_float()
        invulnerable = bs.read_u8()
        return AddActor(actor_id, pos, skin_id, dir_z, health, invulnerable)

''' S2C
Removes the specified actor from the world.
actor_id: id of the actor to hide
Related: DestroyActor, HideActor, HideActorForPlayer
'''
class RemoveActor(Rpc):
    def __init__(self, actor_id):
        super().__init__(RPC.REMOVE_ACTOR)
        self.actor_id = actor_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        return RemoveActor(actor_id)

''' S2C
Makes the actor play an animation.
actor_id: id of the actor.

'''
class ApplyActorAnimation(Rpc):
    def __init__(self, actor_id, anim_lib, anim_name, delta, loop, lock_x, lock_y, freeze, time):
        super().__init__(RPC.APPLY_ACTOR_ANIMATION)
        self.actor_id = actor_id
        self.anim_lib = anim_lib
        self.anim_name = anim_name
        self.delta = delta
        self.loop = loop
        self.lock_x = lock_x
        self.lock_y = lock_y
        self.freeze = freeze
        self.time = time

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)
        bs.write_dynamic_str8(self.anim_lib)
        bs.write_dynamic_str8(self.anim_name)
        bs.write_float(self.delta)
        bs.write_bit(self.loop)
        bs.write_bit(self.lock_x)
        bs.write_bit(self.lock_y)
        bs.write_bit(self.freeze)
        bs.write_float(self.time)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        anim_lib = bs.read_dynamic_str8()
        anim_name = bs.read_dynamic_str8()
        delta = bs.read_float()
        loop = bs.read_bit()
        lock_x = bs.read_bit()
        lock_y = bs.read_bit()
        freeze = bs.read_bit()
        time = bs.read_float()
        return ApplyActorAnimation(actor_id, anim_lib, anim_name, delta, loop, lock_x, lock_y, freeze, time)

''' S2C
Stop any animation the actor is playing.
actor_id: id of the actor
'''
class ClearActorAnimation(Rpc):
    def __init__(self, actor_id):
        super().__init__(RPC.CLEAR_ACTOR_ANIMATION)
        self.actor_id = actor_id

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        return ClearActorAnimation(actor_id)

''' S2C
Sets the Z component of the actor's direction(orientation)
actor_id: id of the actor
angle: new value for Z
Related: SetActorFacingAngle
'''
class SetActorDirZ(Rpc):
    def __init__(self, actor_id, angle):
        super().__init__(RPC.SET_ACTOR_DIR_Z)
        self.actor_id = actor_id
        self.angle = angle

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)
        bs.write_float(self.angle)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        angle = bs.read_float()
        return SetActorDirZ(actor_id, angle)

''' S2C
Sets the position of the actor.
actor_id: id of the actor.
pos: new position value
'''
class SetActorPos(Rpc):
    def __init__(self, actor_id, pos):
        super().__init__(RPC.SET_ACTOR_POS)
        self.actor_id = actor_id
        self.pos = pos

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        pos = bs.read_vec3()
        return SetActorPos(actor_id, pos)

''' S2C
Sets the health of the actor.
actor_id: id of the actor.
health: new health value.
'''
class SetActorHealth(Rpc):
    def __init__(self, actor_id, health):
        super().__init__(RPC.SET_ACTOR_HEALTH)
        self.actor_id = actor_id
        self.health = health

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.actor_id)
        bs.write_float(self.health)

    @staticmethod
    def decode_rpc_payload(bs):
        actor_id = bs.read_u16()
        health = bs.read_float()
        return SetActorHealth(actor_id, health)

import inspect
module = inspect.getmodule(inspect.currentframe())
for rpc in RPC:
    # get SomeSampRpc class from RPC.SOME_SAMP_RPC
    class_name = ''.join(w.capitalize() for w in rpc.name.split('_'))
    try:
        rpc_class = getattr(module, class_name)
        if rpc.__dict__.get('decode_client_rpc_payload') is None:
            rpc.decode_client_rpc_payload = rpc_class.decode_rpc_payload
        if rpc.__dict__.get('decode_server_rpc_payload') is None:
            rpc.decode_server_rpc_payload = rpc_class.decode_rpc_payload
    except AttributeError:
        continue
