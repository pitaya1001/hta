import enum
from .bitstream import *
from .common import *
from .huffman_encoding import default_huffman_tree
from sa import *

# samp rpc ids
class RPC(enum.IntEnum):
    SET_PLAYER_NAME             = 11  # SetPlayerName
    SET_PLAYER_POS              = 12  # SetPlayerPos
    SET_PLAYER_POS_FIND_Z       = 13  # SetPlayerPosFindZ
    SET_PLAYER_HEALTH           = 14  # SetPlayerHealth
    TOGGLE_PLAYER_CONTROLLABLE  = 15  # TogglePlayerControllable
    PLAY_SOUND                  = 16  # PlaySound
    SET_WORLD_BOUNDS            = 17  # SetWorldBounds
    GIVE_PLAYER_MONEY           = 18  # GivePlayerMoney
    SET_PLAYER_FACING_ANGLE     = 19  # SetPlayerFacingAngle
    RESET_PLAYER_MONEY          = 20  # ResetPlayerMoney
    RESET_PLAYER_WEAPONS        = 21  # ResetPlayerWeapons
    GIVE_PLAYER_WEAPON          = 22  # GivePlayerWeapon
    CLICK_SCOREBOARD_PLAYER     = 23  # ClickScoreboardPlayer
    SET_VEHICLE_PARAMS_EX       = 24  # SetVehicleParamsEx
    CLIENT_JOIN                 = 25  # ClientJoin
    PLAYER_ENTER_VEHICLE        = 26  # PlayerEnterVehicle
    ENTER_EDIT_OBJECT           = 27  # EnterEditObject
    CANCEL_EDIT_OBJECT          = 28  # CancelEditObject
    SET_PLAYER_TIME             = 29  # SetPlayerTime
    TOGGLE_CLOCK                = 30  # ToggleClock
    WORLD_PLAYER_ADD            = 32  # WorldPlayerAdd
    SET_SHOP_NAME               = 33  # SetShopName
    SET_SKILL_LEVEL             = 34  # SetSkillLevel
    SET_PLAYER_DRUNK_LEVEL      = 35  # SetPlayerDrunkLevel
    CREATE_3D_TEXT_LABEL        = 36  # Create3DTextLabel
    DISABLE_CHECKPOINT          = 37  # DisableCheckpoint
    SET_RACE_CHECKPOINT         = 38  # SetRaceCheckpoint
    DISABLE_RACE_CHECKPOINT     = 39  # DisableRaceCheckpoint
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
    UPDATE_3D_TEXT_LABEL        = 58  # Update3DTextLabel
    PLAYER_BUBBLE               = 59  # PlayerBubble
    SEND_GAME_TIME_UPDATE       = 60  # SendGameTimeUpdate
    SHOW_DIALOG                 = 61  # ShowDialog
    DIALOG_RESPONSE             = 62  # DialogResponse
    DESTROY_PICKUP              = 63  # DestroyPickup
    LINK_VEHICLE_TO_INTERIOR    = 65  # LinkVehicleToInterior
    SET_PLAYER_ARMOR            = 66  # SetPlayerArmor
    SET_ARMED_WEAPON            = 67  # SetArmedWeapon
    SET_SPAWN_INFO              = 68  # SetSpawnInfo
    SET_PLAYER_TEAM             = 69  # SetPlayerTeam
    PUT_PLAYER_IN_VEHICLE       = 70  # PutPlayerInVehicle
    REMOVE_PLAYER_FROM_VEHICLE  = 71  # RemovePlayerFromVehicle
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
    CLEAR_PLAYER_ANIMATIONS     = 87  # ClearPlayerAnimations
    SET_PLAYER_SPECIAL_ACTION   = 88  # SetPlayerSpecialAction
    SET_PLAYER_FIGHTING_STYLE   = 89  # SetPlayerFightingStyle
    SET_PLAYER_VELOCITY         = 90  # SetPlayerVelocity
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
    TOGGLE_PLAYER_SPECTATING    = 124 # TogglePlayerSpectating
    SPECTATE_PLAYER             = 126 # SpectatePlayer
    SPECTATE_VEHICLE            = 127 # SpectateVehicle
    REQUEST_CLASS               = 128 # RequestClass
    REQUEST_CLASS_RESPONSE      = 128 # RequestClassResponse
    REQUEST_SPAWN               = 129 # RequestSpawn
    REQUEST_SPAWN_RESPONSE      = 129 # RequestSpawnResponse
    CONNECTION_REJECTED         = 130 # ConnectionRejected
    PICKED_UP_PICKUP            = 131 # PickedUpPickup
    MENU_SELECT                 = 132 # MenuSelect
    SET_PLAYER_WANTED_LEVEL     = 133 # SetPlayerWantedLevel
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
    REQUEST_SCORES_AND_PINGS    = 155 # RequestScoresAndPings
    SET_PLAYER_INTERIOR         = 156 # SetPlayerInterior
    SET_CAMERA_POS              = 157 # SetCameraPos
    SET_CAMERA_LOOK_AT          = 158 # SetCameraLookAt
    SET_VEHICLE_POS             = 159 # SetVehiclePos
    SET_VEHICLE_Z_ANGLE         = 160 # SetVehicleZAngle
    SET_VEHICLE_PARAMS          = 161 # SetVehicleParams
    SET_CAMERA_BEHIND_PLAYER    = 162 # SetCameraBehindPlayer
    WORLD_PLAYER_REMOVE         = 163 # WorldPlayerRemove
    WORLD_VEHICLE_ADD           = 164 # WorldVehicleAdd
    WORLD_VEHICLE_REMOVE        = 165 # WorldVehicleRemove
    DEATH_BROADCAST             = 166 # DeathBroadcast
    TOGGLE_VEHICLE_COLLISIONS   = 167 # ToggleVehicleCollisions
    CAMERA_TARGET               = 168 # CameraTarget
    ENABLE_PLAYER_CAMERA_TARGET = 170 # EnablePlayerCameraTarget
    SHOW_ACTOR                  = 171 # ShowActor
    HIDE_ACTOR                  = 172 # HideActor
    APPLY_ACTOR_ANIMATION       = 173 # ApplyActorAnimation
    CLEAR_ACTOR_ANIMATION       = 174 # ClearActorAnimation
    SET_ACTOR_FACING_ANGLE      = 175 # SetActorFacingAngle
    SET_ACTOR_POS               = 176 # SetActorPos
    SET_ACTOR_HEALTH            = 178 # SetActorHealth
    BEGIN = SET_PLAYER_NAME
    END = SET_ACTOR_HEALTH

from . import raknet
raknet.RPC = RPC
from .raknet import Rpc

class SetPlayerName(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_NAME)

    def __str__(self):
        return f'<SetPlayerName>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerName()
RPC.SET_PLAYER_NAME.decode_rpc_payload = SetPlayerName.decode_rpc_payload


class SetPlayerPos(Rpc):
    def __init__(self, pos):
        super().__init__(RPC.SET_PLAYER_POS)
        self.pos = pos

    def __str__(self):
        return f'<SetPlayerPos {self.pos}>'

    def __len__(self):
        return TO_BITS(12)

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        return SetPlayerPos(pos)
RPC.SET_PLAYER_POS.decode_rpc_payload = SetPlayerPos.decode_rpc_payload


class SetPlayerPosFindZ(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_POS_FIND_Z)

    def __str__(self):
        return f'<SetPlayerPosFindZ>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerPosFindZ()
RPC.SET_PLAYER_POS_FIND_Z.decode_rpc_payload = SetPlayerPosFindZ.decode_rpc_payload


class SetPlayerHealth(Rpc):
    def __init__(self, health):
        super().__init__(RPC.SET_PLAYER_HEALTH)
        self.health = health

    def __str__(self):
        return f'<SetPlayerHealth health={self.health:.02f}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_float(self.health)

    @staticmethod
    def decode_rpc_payload(bs):
        health = bs.read_float()
        return SetPlayerHealth(health)
RPC.SET_PLAYER_HEALTH.decode_rpc_payload = SetPlayerHealth.decode_rpc_payload


class TogglePlayerControllable(Rpc):
    def __init__(self, movable):
        super().__init__(RPC.TOGGLE_PLAYER_CONTROLLABLE)
        self.movable = movable

    def __str__(self):
        return f'<TogglePlayerControllable movable={self.movable}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.movable)

    @staticmethod
    def decode_rpc_payload(bs):
        movable = bs.read_u8()
        return TogglePlayerControllable(movable)
RPC.TOGGLE_PLAYER_CONTROLLABLE.decode_rpc_payload = TogglePlayerControllable.decode_rpc_payload


class PlaySound(Rpc):
    def __init__(self):
        super().__init__(RPC.PLAY_SOUND)

    def __str__(self):
        return f'<PlaySound>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return PlaySound()
RPC.PLAY_SOUND.decode_rpc_payload = PlaySound.decode_rpc_payload


class SetWorldBounds(Rpc):
    def __init__(self, min_x, max_x, min_y, max_y):
        super().__init__(RPC.SET_WORLD_BOUNDS)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def __str__(self):
        return f'<SetWorldBounds x=[{self.min_x:.02f}, {self.max_x:.02f}] y=[{self.min_y:.02f}, {self.max_y:.02f}]>'

    def __len__(self):
        return TO_BITS(16)

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
        return SetWorldBounds(min_x, max_x, min_y, max_y)
RPC.SET_WORLD_BOUNDS.decode_rpc_payload = SetWorldBounds.decode_rpc_payload


class GivePlayerMoney(Rpc):
    def __init__(self, money):
        super().__init__(RPC.GIVE_PLAYER_MONEY)
        self.money = money

    def __str__(self):
        return f'<GivePlayerMoney money={self.money}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.money)

    @staticmethod
    def decode_rpc_payload(bs):
        money = bs.read_u32()
        return GivePlayerMoney(money)
RPC.GIVE_PLAYER_MONEY.decode_rpc_payload = GivePlayerMoney.decode_rpc_payload


class SetPlayerFacingAngle(Rpc):
    def __init__(self, angle):
        super().__init__(RPC.SET_PLAYER_FACING_ANGLE)
        self.angle = angle

    def __str__(self):
        return f'<SetPlayerFacingAngle angle={self.angle:.02f}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_float(angle)

    @staticmethod
    def decode_rpc_payload(bs):
        angle = bs.read_float()
        return SetPlayerFacingAngle(angle)
RPC.SET_PLAYER_FACING_ANGLE.decode_rpc_payload = SetPlayerFacingAngle.decode_rpc_payload


class ResetPlayerMoney(Rpc):
    def __init__(self):
        super().__init__(RPC.RESET_PLAYER_MONEY)

    def __str__(self):
        return f'<ResetPlayerMoney>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ResetPlayerMoney()
RPC.RESET_PLAYER_MONEY.decode_rpc_payload = ResetPlayerMoney.decode_rpc_payload


class ResetPlayerWeapons(Rpc):
    def __init__(self):
        super().__init__(RPC.RESET_PLAYER_WEAPONS)

    def __str__(self):
        return f'<ResetPlayerWeapons>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ResetPlayerWeapons()
RPC.RESET_PLAYER_WEAPONS.decode_rpc_payload = ResetPlayerWeapons.decode_rpc_payload


class GivePlayerWeapon(Rpc):
    def __init__(self):
        super().__init__(RPC.GIVE_PLAYER_WEAPON)

    def __str__(self):
        return f'<GivePlayerWeapon>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return GivePlayerWeapon()
RPC.GIVE_PLAYER_WEAPON.decode_rpc_payload = GivePlayerWeapon.decode_rpc_payload


class ClickScoreboardPlayer(Rpc):
    def __init__(self, player_id, source):
        super().__init__(RPC.CLICK_SCOREBOARD_PLAYER)
        self.player_id = player_id
        self.source = source

    def __str__(self):
        return f'<ClickScoreboardPlayer player_id={self.player_id} source={self.source}>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.source)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        source = bs.read_u8()
        return ClickScoreboardPlayer(player_id, source)
RPC.CLICK_SCOREBOARD_PLAYER.decode_rpc_payload = ClickScoreboardPlayer.decode_rpc_payload

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

    def __str__(self):
        return f'<SetVehicleParamsEx vehicle_id={self.vehicle_id} engine={self.engine} lights={self.lights} alarm={self.alarm} doors={self.doors} bonnet={self.bonnet} boot={self.boot} objective={self.objective} siren={self.siren} door_driver={self.door_driver} door_passenger={self.door_passenger} door_back_left={self.door_back_left} door_back_right={self.door_back_right} window_driver={self.window_driver} window_passenger={self.window_passenger} window_back_left={self.window_back_left} window_back_right={self.window_back_right}>'

    def __len__(self):
        return TO_BITS(18)

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
RPC.SET_VEHICLE_PARAMS_EX.decode_rpc_payload = SetVehicleParamsEx.decode_rpc_payload


class ClientJoin(Rpc):
    def __init__(self, version_code, mod, name, challenge_response, gpci, version):
        super().__init__(RPC.CLIENT_JOIN)
        self.version_code = version_code
        self.mod = mod
        self.name = name
        self.challenge_response = challenge_response
        self.gpci = gpci # "gpci"; (stands for get player client id)
        self.version = version

    def __str__(self):
        return f"<ClientJoin version_code={self.version_code} mod={self.mod} name='{self.name}' challenge_response={self.challenge_response:x} gpci='{self.gpci}' version='{self.version}'>"

    def __len__(self):
        return TO_BITS(4 + 1 + 1 + len(self.name.encode(SAMP_ENCODING)) + 4 + 1 + len(self.gpci) + 1 + len(self.version.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.version_code)
        bs.write_u8(self.mod)
        bs.write_dynamic_buffer_u8(self.name.encode(SAMP_ENCODING))
        bs.write_u32(self.challenge_response)
        bs.write_dynamic_buffer_u8(self.gpci.encode())
        bs.write_dynamic_buffer_u8(self.version.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        version_code = bs.read_u32()
        mod = bs.read_u8()
        name = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        challenge_response = bs.read_u32()
        gpci = bs.read_dynamic_buffer_u8().decode()
        version = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        return ClientJoin(version_code, mod, name, challenge_response, gpci, version)
RPC.CLIENT_JOIN.decode_rpc_payload = ClientJoin.decode_rpc_payload


''' S2C
Server sends when a player enters a vehicle
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

    def __str__(self):
        return f'<PlayerEnterVehicle player_id={self.player_id} vehicle_id={self.vehicle_id} as_passenger={self.as_passenger}>'

    def __len__(self):
        return TO_BITS(5)

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
RPC.PLAYER_ENTER_VEHICLE.decode_server_rpc_payload = PlayerEnterVehicle.decode_rpc_payload


''' C2S
Client sends when it enters a vehicle
vehicle_id: the id of the vehicle about to be entered
as_passenger: 0 if entering the driver seat; 1 if entering any passenger seat
'''
class EnterVehicle(Rpc):
    def __init__(self, vehicle_id, as_passenger):
        super().__init__(RPC.PLAYER_ENTER_VEHICLE)
        self.vehicle_id = vehicle_id
        self.as_passenger = as_passenger

    def __str__(self):
        return f'<EnterVehicle vehicle_id={self.vehicle_id} as_passenger={self.as_passenger}>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.as_passenger)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        as_passenger = bs.read_u8()
        return EnterVehicle(vehicle_id, as_passenger)
RPC.PLAYER_ENTER_VEHICLE.decode_client_rpc_payload = EnterVehicle.decode_rpc_payload


class EnterEditObject(Rpc):
    def __init__(self):
        super().__init__(RPC.ENTER_EDIT_OBJECT)

    def __str__(self):
        return f'<EnterEditObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EnterEditObject()
RPC.ENTER_EDIT_OBJECT.decode_rpc_payload = EnterEditObject.decode_rpc_payload


class CancelEditObject(Rpc):
    def __init__(self):
        super().__init__(RPC.CANCEL_EDIT_OBJECT)

    def __str__(self):
        return f'<CancelEditObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return CancelEditObject()
RPC.CANCEL_EDIT_OBJECT.decode_rpc_payload = CancelEditObject.decode_rpc_payload


class SetPlayerTime(Rpc):
    def __init__(self, hour, minute):
        super().__init__(RPC.SET_PLAYER_TIME)
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f'<SetPlayerTime {self.hour:02}:{self.minute:02}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.hour)
        bs.write_u8(self.minute)

    @staticmethod
    def decode_rpc_payload(bs):
        hour = bs.read_u8()
        minute = bs.read_u8()
        return SetPlayerTime(hour, minute)
RPC.SET_PLAYER_TIME.decode_rpc_payload = SetPlayerTime.decode_rpc_payload


class ToggleClock(Rpc):
    def __init__(self):
        super().__init__(RPC.TOGGLE_CLOCK)

    def __str__(self):
        return f'<ToggleClock>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ToggleClock()
RPC.TOGGLE_CLOCK.decode_rpc_payload = ToggleClock.decode_rpc_payload


class WorldPlayerAdd(Rpc):
    def __init__(self, player_id, team, skin_id, pos, facing_angle, color, fighting_style, skill_level):
        super().__init__(RPC.WORLD_PLAYER_ADD)
        self.player_id = player_id
        self.team = team
        self.skin_id = SKIN(skin_id)
        self.pos = pos
        self.facing_angle = facing_angle
        self.color = color
        self.fighting_style = fighting_style
        self.skill_level = skill_level

    def __str__(self):
        return f'<WorldPlayerAdd player_id={self.player_id} team={self.team} skin_id={self.skin_id.name}({self.skin_id.value}) pos={self.pos} facing_angle={self.facing_angle:.02f} color={self.color:08x} fighting_style={self.fighting_style} skill_level={self.skill_level}>'

    def __len__(self):
        return TO_BITS(30)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.team)
        bs.write_u32(self.skin_id)
        bs.write_vec3(self.pos)
        bs.write_float(self.facing_angle)
        bs.write_u32(self.color)
        bs.write_u8(self.fighting_style)
        bs.write_u16(self.skill_level)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        team = bs.read_u8()
        skin_id = SKIN(bs.read_u32())
        pos = bs.read_vec3()
        facing_angle = bs.read_float()
        color = bs.read_u32()
        fighting_style = bs.read_u8()
        skill_level = bs.read_u16()
        return WorldPlayerAdd(player_id, team, skin_id, pos, facing_angle, color, fighting_style, skill_level)
RPC.WORLD_PLAYER_ADD.decode_rpc_payload = WorldPlayerAdd.decode_rpc_payload


class SetShopName(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_SHOP_NAME)

    def __str__(self):
        return f'<SetShopName>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetShopName()
RPC.SET_SHOP_NAME.decode_rpc_payload = SetShopName.decode_rpc_payload


class SetSkillLevel(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_SKILL_LEVEL)

    def __str__(self):
        return f'<SetSkillLevel>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetSkillLevel()
RPC.SET_SKILL_LEVEL.decode_rpc_payload = SetSkillLevel.decode_rpc_payload


class SetPlayerDrunkLevel(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_DRUNK_LEVEL)

    def __str__(self):
        return f'<SetPlayerDrunkLevel>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerDrunkLevel()
RPC.SET_PLAYER_DRUNK_LEVEL.decode_rpc_payload = SetPlayerDrunkLevel.decode_rpc_payload


class Create3DTextLabel(Rpc):
    def __init__(self, label_id, color, pos, draw_distance, test_los, attached_player_id, attached_vehicle_id, text):
        super().__init__(RPC.CREATE_3D_TEXT_LABEL)
        self.label_id = label_id
        self.color = color
        self.pos = pos
        self.draw_distance = draw_distance
        self.test_los = test_los
        self.attached_player_id = attached_player_id
        self.attached_vehicle_id = attached_vehicle_id
        self.text = text

    def __str__(self):
        return f'<Create3DTextLabel label_id={self.label_id} color={self.color:08x} pos={self.pos} draw_distance={self.draw_distance:.02f} test_los={self.test_los} attached_player_id={self.attached_player_id} attached_vehicle_id={self.attached_vehicle_id} text={repr(self.text)}>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        label_id = bs.read_u16()
        color = bs.read_u32()
        pos = bs.read_vec3()
        draw_distance = bs.read_float()
        test_los = bs.read_u8()
        attached_player_id = bs.read_u16()
        attached_vehicle_id = bs.read_u16()
        text = bs.read_huffman_buffer(default_huffman_tree.root_node).decode(SAMP_ENCODING)
        return Create3DTextLabel(label_id, color, pos, draw_distance, test_los, attached_player_id, attached_vehicle_id, text)
RPC.CREATE_3D_TEXT_LABEL.decode_rpc_payload = Create3DTextLabel.decode_rpc_payload


class DisableCheckpoint(Rpc):
    def __init__(self):
        super().__init__(RPC.DISABLE_CHECKPOINT)

    def __str__(self):
        return f'<DisableCheckpoint>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DisableCheckpoint()
RPC.DISABLE_CHECKPOINT.decode_rpc_payload = DisableCheckpoint.decode_rpc_payload


class SetRaceCheckpoint(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_RACE_CHECKPOINT)

    def __str__(self):
        return f'<SetRaceCheckpoint>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetRaceCheckpoint()
RPC.SET_RACE_CHECKPOINT.decode_rpc_payload = SetRaceCheckpoint.decode_rpc_payload


class DisableRaceCheckpoint(Rpc):
    def __init__(self):
        super().__init__(RPC.DISABLE_RACE_CHECKPOINT)

    def __str__(self):
        return f'<DisableRaceCheckpoint>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DisableRaceCheckpoint()
RPC.DISABLE_RACE_CHECKPOINT.decode_rpc_payload = DisableRaceCheckpoint.decode_rpc_payload


class GameModeRestart(Rpc):
    def __init__(self):
        super().__init__(RPC.GAME_MODE_RESTART)

    def __str__(self):
        return f'<GameModeRestart>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return GameModeRestart()
RPC.GAME_MODE_RESTART.decode_rpc_payload = GameModeRestart.decode_rpc_payload


class RpcPlayAudioStream(Rpc):
    def __init__(self, url, pos, radius, use_pos):
        super().__init__(RPC.PLAY_AUDIO_STREAM)
        self.url = url
        self.pos = pos
        self.radius = float(radius)
        self.use_pos = use_pos

    def __str__(self):
        return f"<RpcPlayAudioStream url='{self.url}' pos={self.pos} radius={self.radius:.02f} use_pos={self.use_pos}>"

    def __len__(self):
        return TO_BITS(1 + len(self.url.encode(SAMP_ENCODING)) + 12 + 4 + 1)

    def encode_rpc_payload(self, bs):
        bs.write_dynamic_buffer_u8(self.url.encode(SAMP_ENCODING))
        bs.write_vec3(self.pos)
        bs.write_float(self.radius)
        bs.write_u8(self.use_pos)

    @staticmethod
    def decode_rpc_payload(bs):
        url = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        pos = bs.read_vec3()
        radius = bs.read_float()
        use_pos = bs.read_u8()
        return RpcPlayAudioStream(url, pos, radius, use_pos)
RPC.PLAY_AUDIO_STREAM.decode_rpc_payload = RpcPlayAudioStream.decode_rpc_payload


class StopAudioStream(Rpc):
    def __init__(self):
        super().__init__(RPC.STOP_AUDIO_STREAM)

    def __str__(self):
        return f'<StopAudioStream>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return StopAudioStream()
RPC.STOP_AUDIO_STREAM.decode_rpc_payload = StopAudioStream.decode_rpc_payload


class RemoveBuilding(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_BUILDING)

    def __str__(self):
        return f'<RemoveBuilding>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveBuilding()
RPC.REMOVE_BUILDING.decode_rpc_payload = RemoveBuilding.decode_rpc_payload


class RemoveBuilding(Rpc):
    def __init__(self, object_model, pos, radius):
        super().__init__(RPC.REMOVE_BUILDING)
        self.object_model = object_model
        self.pos = pos
        self.radius = float(radius)

    def __str__(self):
        return f'<RemoveBuilding model={self.object_model} pos={self.pos} radius={self.radius:.02f}>'

    def __len__(self):
        return TO_BITS(20)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.object_model)
        bs.write_vec3(self.pos)
        bs.write_float(self.radius)

    @staticmethod
    def decode_rpc_payload(bs):
        object_model = bs.read_u32()
        pos = bs.read_vec3()
        radius = bs.read_float()
        return RemoveBuilding(object_model, pos, radius)
RPC.REMOVE_BUILDING.decode_rpc_payload = RemoveBuilding.decode_rpc_payload


class CreateObject(Rpc):
    def __init__(self, object_id, model_id, pos, dir, draw_distance, no_camera_col, attached_object=INVALID_ID, attached_vehicle=INVALID_ID, attach_offset=None, attach_dir=None, sync_rotation=None):
        super().__init__(RPC.CREATE_OBJECT)
        self.object_id = object_id
        self.model_id = model_id
        self.pos = pos # Object position as Vec3
        self.dir = dir # Object direction as Vec3
        self.draw_distance = float(draw_distance)
        self.no_camera_col = no_camera_col
        self.attached_object = attached_object
        self.attached_vehicle = attached_vehicle
        self.attach_offset = attach_offset
        self.attach_dir = attach_dir
        self.sync_rotation = sync_rotation

    def __str__(self):
        return f'<CreateObject object_id={self.object_id} model_id={self.model_id} pos={self.pos} dir={self.dir} draw_distance={self.draw_distance} no_camera_col={self.no_camera_col} attached_object={self.attached_object} attached_vehicle={self.attached_vehicle} attach_offset={self.attach_offset} attach_dir={self.attach_dir} sync_rotation={self.sync_rotation}>'

    def __len__(self):
        return 64 if (self.attached_object != INVALID_ID or self.attached_vehicle != INVALID_ID) else 39

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.object_id)
        bs.write_u32(self.model_id)
        bs.write_vec3(self.pos)
        bs.write_vec3(self.dir)
        bs.write_float(self.draw_distance)
        bs.write_u8(self.no_camera_col)
        bs.write_u16(self.attached_object)
        bs.write_u16(self.attached_vehicle)
        if self.attached_object != INVALID_ID or self.attached_vehicle != INVALID_ID:
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
        attached_object = bs.read_u16()
        attached_vehicle = bs.read_u16()
        if attached_object != INVALID_ID or attached_vehicle != INVALID_ID:
            attach_offset = bs.read_vec3()
            attach_dir = bs.read_vec3()
            sync_rotation = bs.read_u8()
        else:
            attach_offset = None
            attach_dir = None
            sync_rotation = None
        return CreateObject(object_id, model_id, pos, dir, draw_distance, no_camera_col, attached_object, attached_vehicle, attach_offset, attach_rot, sync_rotation)
RPC.CREATE_OBJECT.decode_rpc_payload = CreateObject.decode_rpc_payload


class SetObjectPos(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_OBJECT_POS)

    def __str__(self):
        return f'<SetObjectPos>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetObjectPos()
RPC.SET_OBJECT_POS.decode_rpc_payload = SetObjectPos.decode_rpc_payload


class SetObjectRotation(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_OBJECT_ROTATION)

    def __str__(self):
        return f'<SetObjectRotation>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetObjectRotation()
RPC.SET_OBJECT_ROTATION.decode_rpc_payload = SetObjectRotation.decode_rpc_payload


class DestroyObject(Rpc):
    def __init__(self, object_id):
        super().__init__(RPC.DESTROY_OBJECT)
        self.object_id = object_id

    def __str__(self):
        return f'<DestroyObject object_id={self.object_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.object_id)

    @staticmethod
    def decode_rpc_payload(bs):
        object_id = bs.read_u16()
        return DestroyObject(object_id)
RPC.DESTROY_OBJECT.decode_rpc_payload = DestroyObject.decode_rpc_payload

''' C2S
Client sends a command to the server, e.g. "/help"
'''
class RequestChatCommand(Rpc):
    def __init__(self, command):
        super().__init__(RPC.REQUEST_CHAT_COMMAND)
        self.command = command

    def __str__(self):
        return f"<RequestChatCommand '{self.command}'>"

    def __len__(self):
        return TO_BITS(4 + len(self.command.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_dynamic_buffer_u32(self.command.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        command = bs.read_dynamic_buffer_u32().decode(SAMP_ENCODING)
        return RequestChatCommand(command)
RPC.REQUEST_CHAT_COMMAND.decode_rpc_payload = RequestChatCommand.decode_rpc_payload


class SendSpawn(Rpc):
    def __init__(self):
        super().__init__(RPC.SEND_SPAWN)

    def __str__(self):
        return f'<SendSpawn>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SendSpawn()
RPC.SEND_SPAWN.decode_rpc_payload = SendSpawn.decode_rpc_payload


class DeathNotification(Rpc):
    def __init__(self, reason, killer_id):
        super().__init__(RPC.DEATH_NOTIFICATION)
        self.reason = reason
        self.killer_id = killer_id

    def __str__(self):
        return f'<DeathNotification reason={self.reason} killer_id={self.killer_id}>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.reason)
        bs.write_u16(self.killer_id)

    @staticmethod
    def decode_rpc_payload(bs):
        reason = bs.read_u8()
        killer_id = bs.read_u16()
        return DeathNotification(reason, killer_id)
RPC.DEATH_NOTIFICATION.decode_rpc_payload = DeathNotification.decode_rpc_payload


class NpcJoin(Rpc):
    def __init__(self):
        super().__init__(RPC.NPC_JOIN)

    def __str__(self):
        return f'<NpcJoin>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return NpcJoin()
RPC.NPC_JOIN.decode_rpc_payload = NpcJoin.decode_rpc_payload


class KillFeedMessage(Rpc):
    def __init__(self, killer_id, victim_id, reason):
        super().__init__(RPC.KILL_FEED_MESSAGE)
        self.killer_id = killer_id
        self.victim_id = victim_id
        self.reason = reason

    def __str__(self):
        return f'<KillFeedMessage killer_id={self.killer_id} victim_id={self.victim_id} reason={self.reason.name}({self.reason.value})>'

    def __len__(self):
        return TO_BITS(5)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.killer_id)
        bs.write_u16(self.victim_id)
        bs.write_u8(self.reason)

    @staticmethod
    def decode_rpc_payload(bs):
        killer_id = bs.read_u16()
        victim_id = bs.read_u16()
        reason = bs.read_u8()
        return KillFeedMessage(killer_id, victim_id, reason)
RPC.KILL_FEED_MESSAGE.decode_rpc_payload = KillFeedMessage.decode_rpc_payload


class SetMapIcon(Rpc):
    def __init__(self, icon_id, pos, type, color, style):
        super().__init__(RPC.SET_MAP_ICON)
        self.icon_id = icon_id
        self.pos = pos
        self.type = type
        self.color = color
        self.style = style

    def __str__(self):
        return f'<SetMapIcon icon_id={self.icon_id} pos={self.pos} type={self.type} color={self.color:08x} style={self.style}>'

    def __len__(self):
        return TO_BITS(19)

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
RPC.SET_MAP_ICON.decode_rpc_payload = SetMapIcon.decode_rpc_payload


class RemoveVehicleComponent(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_VEHICLE_COMPONENT)

    def __str__(self):
        return f'<RemoveVehicleComponent>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveVehicleComponent()
RPC.REMOVE_VEHICLE_COMPONENT.decode_rpc_payload = RemoveVehicleComponent.decode_rpc_payload


class Update3DTextLabel(Rpc):
    def __init__(self, label_id):
        super().__init__(RPC.UPDATE_3D_TEXT_LABEL)
        self.label_id = label_id

    def __str__(self):
        return f'<Update3DTextLabel label_id={self.label_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.label_id)

    @staticmethod
    def decode_rpc_payload(bs):
        label_id = bs.read_u16()
        return Update3DTextLabel(label_id)
RPC.UPDATE_3D_TEXT_LABEL.decode_rpc_payload = Update3DTextLabel.decode_rpc_payload

'''
Text above a player's name tag.
'''
class PlayerBubble(Rpc):
    def __init__(self, player_id, color, draw_distance, expire_time, text):
        super().__init__(RPC.PLAYER_BUBBLE)
        self.player_id = player_id
        self.color = color
        self.draw_distance = draw_distance
        self.expire_time = expire_time
        self.text = text

    def __str__(self):
        return f"<PlayerBubble player_id={self.player_id} color={self.color:08x} draw_distance={self.draw_distance:.02f} expire_time={self.expire_time} text='{self.text}'>"

    def __len__(self):
        return TO_BITS(2 + 4 + 4 + 4 + 1 + len(self.text.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.color)
        bs.write_float(self.draw_distance)
        bs.write_u32(self.expire_time)
        bs.write_dynamic_buffer_u8(self.text.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        color = bs.read_u32()
        draw_distance = bs.read_float()
        expire_time = bs.read_u32()
        #text = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        text=''
        return PlayerBubble(player_id, color, draw_distance, expire_time, text)
RPC.PLAYER_BUBBLE.decode_rpc_payload = PlayerBubble.decode_rpc_payload


class SendGameTimeUpdate(Rpc):
    def __init__(self, time):
        super().__init__(RPC.SEND_GAME_TIME_UPDATE)
        self.time = time

    def __str__(self):
        return f'<SendGameTimeUpdate time={self.time:x}>'

    def __len__(self):
        return 4

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.time)

    @staticmethod
    def decode_rpc_payload(bs):
        time = bs.read_u32()
        return SendGameTimeUpdate(time)
RPC.SEND_GAME_TIME_UPDATE.decode_rpc_payload = SendGameTimeUpdate.decode_rpc_payload


class DIALOG_STYLE(enum.IntEnum):
    MESSAGE            = 0
    INPUT              = 1
    LIST               = 2
    PASSWORD           = 3
    TABLE              = 4
    TABLE_WITH_HEADERS = 5

'''
Max dialog id = 32767 = 2^15-1 = 0x7fff
A negative id[0x8000, 0xffff] closes any open dialog; use INVALID_ID
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

    def __str__(self):
        return f"<ShowDialog dialog_id={self.dialog_id} style={self.style.name}({self.style.value}) title='{self.title}' button1='{self.button1}' button2='{self.button2}' text={repr(self.text)}>"

    def __len__(self):
        bs = Bitstream(2+len(self.text))
        bs.write_huffman_buffer(self.text.encode(SAMP_ENCODING), default_huffman_tree.root_node)
        huffman_buffer_size = TO_BYTES(bs.len)
        return TO_BITS(3 + (1+len(self.title.encode(SAMP_ENCODING))) \
            + (1+len(self.button1.encode(SAMP_ENCODING))) \
            + (1+len(self.title.encode(SAMP_ENCODING))) \
            + huffman_buffer_size)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.dialog_id)
        bs.write_u8(self.style)
        bs.write_dynamic_buffer_u8(self.title.encode(SAMP_ENCODING))
        bs.write_dynamic_buffer_u8(self.button1.encode(SAMP_ENCODING))
        bs.write_dynamic_buffer_u8(self.button2.encode(SAMP_ENCODING))
        bs.write_huffman_buffer(self.text.encode(SAMP_ENCODING), default_huffman_tree.root_node)

    @staticmethod
    def decode_rpc_payload(bs):
        dialog_id = bs.read_u16()
        style = DIALOG_STYLE(bs.read_u8())
        title = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        button1 = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        button2 = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        text = bs.read_huffman_buffer(default_huffman_tree.root_node).decode(SAMP_ENCODING)
        return ShowDialog(dialog_id, style, title, button1, button2, text)
RPC.SHOW_DIALOG.decode_rpc_payload = ShowDialog.decode_rpc_payload


'''
Respond to the current dialog on the screen
dialog_id:  id of the dialog on the screen
button: the button selected; DIALOG_BUTTON.LEFT(selected when ENTER is pressed) or DIALOG_BUTTON.RIGHT
list_index: the index of the row if LIST/TABLE/TABLE_WITH_HEADERS style, otherwise INVALID_ID
text: depends on the dialog style; textbox input value(INPUT/PASSWORD styles), row text(LIST/TABLE/TABLE_WITH_HEADERS styles), empty string(MESSAGE style)
'''
class DIALOG_BUTTON(enum.IntEnum):
    LEFT  = 1
    RIGHT = 0

class DialogResponse(Rpc):
    def __init__(self, dialog_id, button=DIALOG_BUTTON.LEFT, list_index=INVALID_ID, text=''):
        super().__init__(RPC.DIALOG_RESPONSE)
        self.dialog_id = dialog_id
        self.button = button
        self.list_index = list_index
        self.text = text

    def __str__(self):
        return f'<DialogResponse dialog_id={self.dialog_id} button={self.button.name}({self.button.value}) list_index={self.list_index} text={repr(self.text)}>'

    def __len__(self):
        return TO_BITS(2 + 1 + 2 + 1 + len(self.text.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.dialog_id)
        bs.write_u8(self.button)
        bs.write_u16(self.list_index)
        bs.write_dynamic_buffer_u8(self.text.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        dialog_id = bs.read_u16()
        button = bs.read_u8()
        list_index = bs.read_u16()
        text = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        return DialogResponse(dialog_id, button, list_index, text)
RPC.DIALOG_RESPONSE.decode_rpc_payload = DialogResponse.decode_rpc_payload

''' S2C
Server sends to destroy a pickup created with CreatePickup
pickup_id: id of the pickup to destroy
'''
class DestroyPickup(Rpc):
    def __init__(self, pickup_id):
        super().__init__(RPC.DESTROY_PICKUP)
        self.pickup_id = pickup_id

    def __str__(self):
        return f'<DestroyPickup pickup_id={self.pickup_id}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.pickup_id)

    @staticmethod
    def decode_rpc_payload(bs):
        pickup_id = bs.read_u32()
        return DestroyPickup(pickup_id)
RPC.DESTROY_PICKUP.decode_rpc_payload = DestroyPickup.decode_rpc_payload


class LinkVehicleToInterior(Rpc):
    def __init__(self):
        super().__init__(RPC.LINK_VEHICLE_TO_INTERIOR)

    def __str__(self):
        return f'<LinkVehicleToInterior>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return LinkVehicleToInterior()
RPC.LINK_VEHICLE_TO_INTERIOR.decode_rpc_payload = LinkVehicleToInterior.decode_rpc_payload


class SetPlayerArmor(Rpc):
    def __init__(self, armor):
        super().__init__(RPC.SET_PLAYER_ARMOR)
        self.armor = float(armor)

    def __str__(self):
        return f'<SetPlayerArmor armor={self.armor:.02f}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_float(self.armor)

    @staticmethod
    def decode_rpc_payload(bs):
        armor = bs.read_float()
        return SetPlayerArmor(armor)
RPC.SET_PLAYER_ARMOR.decode_rpc_payload = SetPlayerArmor.decode_rpc_payload


class SetArmedWeapon(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_ARMED_WEAPON)

    def __str__(self):
        return f'<SetArmedWeapon>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetArmedWeapon()
RPC.SET_ARMED_WEAPON.decode_rpc_payload = SetArmedWeapon.decode_rpc_payload


class SetSpawnInfo(Rpc):
    def __init__(self, team=0, skin=SKIN.CJ, pos=Vec3(0.0, 0.0, 0.0), rotation=0.0, weapon1=Weapon(), weapon2=Weapon(), weapon3=Weapon()):
        super().__init__(RPC.SET_SPAWN_INFO)
        self.team = team
        self.skin = SKIN(skin)
        self.pos = pos
        self.rotation = float(rotation)
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.weapon3 = weapon3

    def __str__(self):
        return f'<SetSpawnInfo team={self.team} skin={self.skin.name}({self.skin.value}) pos={self.pos} rotation={self.rotation:.2f} weapon1={self.weapon1} weapon2={self.weapon2} weapon3={self.weapon3}'

    def __len__(self):
        return TO_BITS(46)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.team)
        bs.write_u32(self.skin)
        bs.write_u8(0) # unused
        bs.write_vec3(self.pos)
        bs.write_float(self.rotation)
        bs.write_u32(self.weapon1.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon1.ammo)
        bs.write_u32(self.weapon2.ammo)
        bs.write_u32(self.weapon3.ammo)

    @staticmethod
    def decode_rpc_payload(bs):
        team = bs.read_u8()
        skin = bs.read_u32()
        bs.skip_bits(8) # unused
        pos = bs.read_vec3()
        rotation = bs.read_float()
        weapon1_id = bs.read_u32()
        weapon2_id = bs.read_u32()
        weapon3_id = bs.read_u32()
        weapon1_ammo = bs.read_u32()
        weapon2_ammo = bs.read_u32()
        weapon3_ammo = bs.read_u32()
        weapon1 = Weapon(weapon1_id, weapon1_ammo)
        weapon2 = Weapon(weapon2_id, weapon2_ammo)
        weapon3 = Weapon(weapon3_id, weapon3_ammo)
        return SetSpawnInfo(team, skin, pos, rotation, weapon1, weapon2, weapon3)
RPC.SET_SPAWN_INFO.decode_server_rpc_payload = SetSpawnInfo.decode_rpc_payload


class SetPlayerTeam(Rpc):
    def __init__(self, player_id, team):
        super().__init__(RPC.SET_PLAYER_TEAM)
        self.player_id = player_id
        self.team = team

    def __str__(self):
        return f'<SetPlayerTeam player_id={self.player_id} team={self.team}>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.team)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        team = bs.read_u8()
        return SetPlayerTeam(player_id, team)
RPC.SET_PLAYER_TEAM.decode_rpc_payload = SetPlayerTeam.decode_rpc_payload


''' S2C
Puts a player in a vehicle
vehicle_id: id of the vehicle to put the player in
seat_id: 0=driver, 1=front passenger, 2=back left passenger, 3=back right passenger, 4+=other seats(e.g. coach)
WARNING: If the seat is invalid or taken, the player will crash when exiting the vehicle
'''
class PutPlayerInVehicle(Rpc):
    def __init__(self, vehicle_id, seat_id):
        super().__init__(RPC.PUT_PLAYER_IN_VEHICLE)
        self.vehicle_id = vehicle_id
        self.seat_id = seat_id

    def __str__(self):
        return f'<PutPlayerInVehicle vehicle_id={self.vehicle_id} seat_id={self.seat_id}>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.seat_id)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        seat_id = bs.read_u8()
        return PutPlayerInVehicle(vehicle_id, seat_id)
RPC.PUT_PLAYER_IN_VEHICLE.decode_rpc_payload = PutPlayerInVehicle.decode_rpc_payload


''' S2C
Removes a player from the vehicle they are currently in
'''
class RemovePlayerFromVehicle(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_PLAYER_FROM_VEHICLE)

    def __str__(self):
        return f'<RemovePlayerFromVehicle>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemovePlayerFromVehicle()
RPC.REMOVE_PLAYER_FROM_VEHICLE.decode_rpc_payload = RemovePlayerFromVehicle.decode_rpc_payload


class SetPlayerColor(Rpc):
    def __init__(self, player_id, color):
        super().__init__(RPC.SET_PLAYER_COLOR)
        self.player_id = player_id
        self.color = color

    def __str__(self):
        return f'<SetPlayerColor id={self.player_id} color={self.color:08x}>'

    def __len__(self):
        return TO_BITS(6)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.color)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        color = bs.read_u32()
        return SetPlayerColor(player_id, color)
RPC.SET_PLAYER_COLOR.decode_rpc_payload = SetPlayerColor.decode_rpc_payload

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

    def __str__(self):
        return f"<ShowGameText style={self.style} duration={self.duration} text='{self.text}'>"

    def __len__(self):
        return TO_BITS(12 + len(self.text.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.style)
        bs.write_u32(self.duration)
        bs.write_dynamic_buffer_u32(self.text.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        style = bs.read_u32()
        duration = bs.read_u32()
        text = bs.read_dynamic_buffer_u32().decode(SAMP_ENCODING)
        return ShowGameText(style, duration, text)
RPC.SHOW_GAME_TEXT.decode_rpc_payload = ShowGameText.decode_rpc_payload


class ForceClassSelection(Rpc):
    def __init__(self):
        super().__init__(RPC.FORCE_CLASS_SELECTION)

    def __str__(self):
        return f'<ForceClassSelection>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ForceClassSelection()
RPC.FORCE_CLASS_SELECTION.decode_rpc_payload = ForceClassSelection.decode_rpc_payload


class AttachObjectToPlayer(Rpc):
    def __init__(self):
        super().__init__(RPC.ATTACH_OBJECT_TO_PLAYER)

    def __str__(self):
        return f'<AttachObjectToPlayer>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AttachObjectToPlayer()
RPC.ATTACH_OBJECT_TO_PLAYER.decode_rpc_payload = AttachObjectToPlayer.decode_rpc_payload


class InitMenu(Rpc):
    def __init__(self):
        super().__init__(RPC.INIT_MENU)

    def __str__(self):
        return f'<InitMenu>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return InitMenu()
RPC.INIT_MENU.decode_rpc_payload = InitMenu.decode_rpc_payload


class ShowMenu(Rpc):
    def __init__(self):
        super().__init__(RPC.SHOW_MENU)

    def __str__(self):
        return f'<ShowMenu>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ShowMenu()
RPC.SHOW_MENU.decode_rpc_payload = ShowMenu.decode_rpc_payload


class HideMenu(Rpc):
    def __init__(self):
        super().__init__(RPC.HIDE_MENU)

    def __str__(self):
        return f'<HideMenu>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return HideMenu()
RPC.HIDE_MENU.decode_rpc_payload = HideMenu.decode_rpc_payload

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

    def __str__(self):
        return f'<CreateExplosion pos={self.pos} type={self.type} radius={self.radius:.02f}>'

    def __len__(self):
        return TO_BITS(12+4+4)

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
RPC.CREATE_EXPLOSION.decode_rpc_payload = CreateExplosion.decode_rpc_payload


class TogglePlayerNameTag(Rpc):
    def __init__(self, player_id, show):
        super().__init__(RPC.TOGGLE_PLAYER_NAME_TAG)
        self.player_id = player_id
        self.show = show

    def __str__(self):
        return f'<TogglePlayerNameTag player_id={self.player_id} show={self.show}>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.show)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        show = bs.read_u8()
        return TogglePlayerNameTag(player_id, show)
RPC.TOGGLE_PLAYER_NAME_TAG.decode_rpc_payload = TogglePlayerNameTag.decode_rpc_payload


class AttachCameraToObject(Rpc):
    def __init__(self):
        super().__init__(RPC.ATTACH_CAMERA_TO_OBJECT)

    def __str__(self):
        return f'<AttachCameraToObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AttachCameraToObject()
RPC.ATTACH_CAMERA_TO_OBJECT.decode_rpc_payload = AttachCameraToObject.decode_rpc_payload

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

    def __str__(self):
        return f'<InterpolateCamera pos_set={self.pos_set} from_pos={self.from_pos} to_pos={self.to_pos} time={self.time} cut_type={self.cut_type}>'

    def __len__(self):
        return 1 + TO_BITS(29)

    def encode_rpc_payload(self, bs):
        bs.write_bool(self.pos_set)
        self.from_pos.encode(bs)
        self.to_pos.encode(bs)
        bs.write_u32(self.time)
        bs.write_u8(self.cut_type)

    @staticmethod
    def decode_rpc_payload(bs):
        pos_set = bs.read_bool()
        from_pos = bs.read_vec3()
        to_pos = bs.read_vec3()
        time = bs.read_u32()
        cut_type = bs.read_u8()
        return InterpolateCamera(pos_set, from_pos, to_pos, time, cut_type)
RPC.INTERPOLATE_CAMERA.decode_rpc_payload = InterpolateCamera.decode_rpc_payload


class ClickTextdraw(Rpc):
    def __init__(self, textdraw_id):
        super().__init__(RPC.CLICK_TEXTDRAW)
        self.textdraw_id = textdraw_id

    def __str__(self):
        return f'<ClickTextdraw textdraw_id={self.textdraw_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        return ClickTextdraw(textdraw_id)
RPC.CLICK_TEXTDRAW.decode_client_rpc_payload = ClickTextdraw.decode_rpc_payload

'''
Set whether or not textdraw selection is enabled or disabled
'''
class ToggleTextdrawsClickable(Rpc):
    def __init__(self, clickable, color):
        super().__init__(RPC.TOGGLE_TEXTDRAWS_CLICKABLE)
        self.clickable = clickable
        self.color = color

    def __str__(self):
        return f'<ToggleTextdrawsClickable clickable={self.clickable} color={self.color:08x}>'

    def __len__(self):
        return 1 + TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_bool(self.clickable)
        bs.write_u32(self.color)

    @staticmethod
    def decode_rpc_payload(bs):
        clickable = bs.read_bool()
        color = bs.read_u32()
        return ToggleTextdrawsClickable(clickable, color)
RPC.TOGGLE_TEXTDRAWS_CLICKABLE.decode_server_rpc_payload = ToggleTextdrawsClickable.decode_rpc_payload

class SetPlayerObjectMaterial(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_OBJECT_MATERIAL)

    def __str__(self):
        return f'<SetPlayerObjectMaterial>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerObjectMaterial()
RPC.SET_PLAYER_OBJECT_MATERIAL.decode_rpc_payload = SetPlayerObjectMaterial.decode_rpc_payload


class StopFlashGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.STOP_FLASH_GANG_ZONE)

    def __str__(self):
        return f'<StopFlashGangZone>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return StopFlashGangZone()
RPC.STOP_FLASH_GANG_ZONE.decode_rpc_payload = StopFlashGangZone.decode_rpc_payload


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

    def __str__(self):
        return f"<ApplyPlayerAnimation player_id={self.player_id} anim_lib='{self.anim_lib}' anim_name='{self.anim_name}' delta={self.delta:.02f} loop={self.loop} lockx={self.lockx} locky={self.locky} freeze={self.freeze} time={self.time}>"

    def __len__(self):
        return TO_BITS(2 + 1 + len(self.anim_lib.encode(SAMP_ENCODING)) + 1 + len(self.anim_name.encode(SAMP_ENCODING)) + 4 + 1*4 + 4)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_dynamic_buffer_u8(self.anim_lib.encode(SAMP_ENCODING))
        bs.write_dynamic_buffer_u8(self.anim_name.encode(SAMP_ENCODING))
        bs.write_float(self.delta)
        bs.write_bit(self.loop)
        bs.write_bit(self.lockx)
        bs.write_bit(self.locky)
        bs.write_bit(self.freeze)
        bs.write_u32(self.time)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        anim_lib = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        anim_name = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        delta = bs.read_float()
        loop = bs.read_bit()
        lockx = bs.read_bit()
        locky = bs.read_bit()
        freeze = bs.read_bit()
        time = bs.read_u32()
        return ApplyPlayerAnimation(player_id, anim_lib, anim_name, delta, loop, lockx, locky, freeze, time)
RPC.APPLY_PLAYER_ANIMATION.decode_rpc_payload = ApplyPlayerAnimation.decode_rpc_payload


class ClearPlayerAnimations(Rpc):
    def __init__(self, player_id):
        super().__init__(RPC.CLEAR_PLAYER_ANIMATIONS)
        self.player_id = player_id

    def __str__(self):
        return f'<ClearPlayerAnimations player_id={self.player_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        return ClearPlayerAnimations(player_id)
RPC.CLEAR_PLAYER_ANIMATIONS.decode_rpc_payload = ClearPlayerAnimations.decode_rpc_payload


class SetPlayerSpecialAction(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_SPECIAL_ACTION)

    def __str__(self):
        return f'<SetPlayerSpecialAction>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerSpecialAction()
RPC.SET_PLAYER_SPECIAL_ACTION.decode_rpc_payload = SetPlayerSpecialAction.decode_rpc_payload


class SetPlayerFightingStyle(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_FIGHTING_STYLE)

    def __str__(self):
        return f'<SetPlayerFightingStyle>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerFightingStyle()
RPC.SET_PLAYER_FIGHTING_STYLE.decode_rpc_payload = SetPlayerFightingStyle.decode_rpc_payload


class SetPlayerVelocity(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_VELOCITY)

    def __str__(self):
        return f'<SetPlayerVelocity>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerVelocity()
RPC.SET_PLAYER_VELOCITY.decode_rpc_payload = SetPlayerVelocity.decode_rpc_payload


class SetVehicleVelocity(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_VEHICLE_VELOCITY)

    def __str__(self):
        return f'<SetVehicleVelocity>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetVehicleVelocity()
RPC.SET_VEHICLE_VELOCITY.decode_rpc_payload = SetVehicleVelocity.decode_rpc_payload


class ChatMessage(Rpc):
    def __init__(self, message, color):
        super().__init__(RPC.CHAT_MESSAGE)
        self.message = message
        self.color = color

    def __str__(self):
        return f"<ChatMessage color={self.color:08x} '{self.message}'>"
    
    def __len__(self):
        return TO_BITS(4 + 4 + len(self.message.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.color)
        bs.write_dynamic_buffer_u32(self.message.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        color = bs.read_u32()
        message = bs.read_dynamic_buffer_u32().decode(SAMP_ENCODING)
        return ChatMessage(message, color)
RPC.CHAT_MESSAGE.decode_rpc_payload = ChatMessage.decode_rpc_payload


class SetWorldTime(Rpc):
    def __init__(self, hour):
        super().__init__(RPC.SET_WORLD_TIME)
        self.hour = hour

    def __str__(self):
        return f'<SetWorldTime hour={self.hour}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.hour)

    @staticmethod
    def decode_rpc_payload(bs):
        hour = bs.read_u8()
        return SetWorldTime(hour)
RPC.SET_WORLD_TIME.decode_rpc_payload = SetWorldTime.decode_rpc_payload


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

    def __str__(self):
        return f'<CreatePickup pickup_id={self.pickup_id} model_id={self.model_id} type={self.type} pos={self.pos}>'

    def __len__(self):
        return TO_BITS(4+4+4+12)

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
RPC.CREATE_PICKUP.decode_rpc_payload = CreatePickup.decode_rpc_payload


class ScmEvent(Rpc):
    def __init__(self):
        super().__init__(RPC.SCM_EVENT)

    def __str__(self):
        return f'<ScmEvent>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ScmEvent()
RPC.SCM_EVENT.decode_rpc_payload = ScmEvent.decode_rpc_payload


class DestroyWeaponPickup(Rpc):
    def __init__(self):
        super().__init__(RPC.DESTROY_WEAPON_PICKUP)

    def __str__(self):
        return f'<DestroyWeaponPickup>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DestroyWeaponPickup()
RPC.DESTROY_WEAPON_PICKUP.decode_rpc_payload = DestroyWeaponPickup.decode_rpc_payload


class MoveObject(Rpc):
    def __init__(self, object_id, pos, target, speed, target_r):
        super().__init__(RPC.MOVE_OBJECT)
        self.object_id = object_id
        self.pos = pos
        self.target = target
        self.speed = speed
        self.target_r = target_r

    def __str__(self):
        return f'<MoveObject object_id={self.object_id} pos={self.pos} target={self.target} speed={self.speed:.02f} target_r={self.target_r}>'

    def __len__(self):
        return TO_BITS(42)

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
RPC.MOVE_OBJECT.decode_rpc_payload = MoveObject.decode_rpc_payload


class RequestChatMessage(Rpc):
    def __init__(self, message):
        super().__init__(RPC.REQUEST_CHAT_MESSAGE)
        self.message = message
    
    def __str__(self):
        return f"<RequestChatMessage '{self.message}'>"

    def __len__(self):
        return TO_BITS(1 + len(self.message.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_dynamic_buffer_u8(self.message.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        message = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        return RequestChatMessage(message)
RPC.REQUEST_CHAT_MESSAGE.decode_client_rpc_payload = RequestChatMessage.decode_rpc_payload


class PlayerChatMessage(Rpc):
    def __init__(self, player_id, message):
        super().__init__(RPC.PLAYER_CHAT_MESSAGE)
        self.player_id = player_id
        self.message = message
    
    def __str__(self):
        return f"<PlayerChatMessage player_id={self.player_id} '{self.message}'>"

    def __len__(self):
        return TO_BITS(2 + 1 + len(self.message.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_dynamic_buffer_u8(self.message.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        message = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        return PlayerChatMessage(player_id, message)
RPC.PLAYER_CHAT_MESSAGE.decode_server_rpc_payload = PlayerChatMessage.decode_rpc_payload

class SvrStats(Rpc):
    def __init__(self):
        super().__init__(RPC.SVR_STATS)

    def __str__(self):
        return f'<SvrStats>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SvrStats()
RPC.SVR_STATS.decode_rpc_payload = SvrStats.decode_rpc_payload

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

    def __str__(self):
        return f'<ClientCheck type={self.type} arg={self.arg:08x} offset={self.offset} size={self.size}>'

    def __len__(self):
        return TO_BITS(9)

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
RPC.CLIENT_CHECK.decode_server_rpc_payload = ClientCheck.decode_rpc_payload

''' C2S
Responds to a server ClientCheck
type: see the CLIENT_CHECK enum
arg: depends on type
checksum: depends on type
'''
class ClientCheckResponse(Rpc):
    def __init__(self, type, arg, checksum):
        super().__init__(RPC.CLIENT_CHECK)
        self.type = type
        self.arg = arg
        self.checksum = checksum

    def __str__(self):
        return f'<ClientCheckResponse type={self.type} arg={self.arg:08x} checksum={self.checksum}>'

    def __len__(self):
        return TO_BITS(6)

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
RPC.CLIENT_CHECK.decode_client_rpc_payload = ClientCheckResponse.decode_rpc_payload


class ToggleStuntBonus(Rpc):
    def __init__(self, enable):
        super().__init__(RPC.TOGGLE_STUNT_BONUS)
        self.enable = enable

    def __str__(self):
        return f'<ToggleStuntBonus enable={self.enable}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.enable)

    @staticmethod
    def decode_rpc_payload(bs):
        enable = bs.read_u8()
        return ToggleStuntBonus(enable)
RPC.TOGGLE_STUNT_BONUS.decode_rpc_payload = ToggleStuntBonus.decode_rpc_payload


class SetTextdrawText(Rpc):
    def __init__(self, textdraw_id, text):
        super().__init__(RPC.SET_TEXTDRAW_TEXT)
        self.textdraw_id = textdraw_id
        self.text = text

    def __str__(self):
        return f"<SetTextdrawText textdraw_id={self.textdraw_id} text='{self.text}'>" 

    def __len__(self):
        return TO_BITS(4 + 2 + len(self.text.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)
        bs.write_dynamic_buffer_u16(self.text.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        text = bs.read_dynamic_buffer_u16().decode(SAMP_ENCODING)
        return SetTextdrawText(textdraw_id, text)
RPC.SET_TEXTDRAW_TEXT.decode_rpc_payload = SetTextdrawText.decode_rpc_payload


class DamageVehicle(Rpc):
    def __init__(self, vehicle_id, panels, doors, lights, tires):
        super().__init__(RPC.DAMAGE_VEHICLE)
        self.vehicle_id = vehicle_id
        self.panels = panels
        self.doors = doors
        self.lights = lights
        self.tires = tires

    def __str__(self):
        return f'<DamageVehicle vehicle_id={self.vehicle_id} panels={self.panels} doors={self.doors} lights={self.lights} tires={self.tires}>'

    def __len__(self):
        return TO_BITS(12)

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
RPC.DAMAGE_VEHICLE.decode_rpc_payload = DamageVehicle.decode_rpc_payload


class SetCheckpoint(Rpc):
    def __init__(self, pos, radius):
        super().__init__(RPC.SET_CHECKPOINT)
        self.pos = pos
        self.radius = radius

    def __str__(self):
        return f'<SetCheckpoint pos={self.pos} radius={self.radius}>'

    def __len__(self):
        return TO_BITS(12+4)

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)
        bs.write_float(self.radius)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        radius = bs.read_float()
        return SetCheckpoint(pos, radius)
RPC.SET_CHECKPOINT.decode_rpc_payload = SetCheckpoint.decode_rpc_payload


class AddGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.ADD_GANG_ZONE)

    def __str__(self):
        return f'<AddGangZone>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AddGangZone()
RPC.ADD_GANG_ZONE.decode_rpc_payload = AddGangZone.decode_rpc_payload


class PlayCrimeReport(Rpc):
    def __init__(self):
        super().__init__(RPC.PLAY_CRIME_REPORT)

    def __str__(self):
        return f'<PlayCrimeReport>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return PlayCrimeReport()
RPC.PLAY_CRIME_REPORT.decode_rpc_payload = PlayCrimeReport.decode_rpc_payload


class SetPlayerAttachedObject(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_ATTACHED_OBJECT)

    def __str__(self):
        return f'<SetPlayerAttachedObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerAttachedObject()
RPC.SET_PLAYER_ATTACHED_OBJECT.decode_rpc_payload = SetPlayerAttachedObject.decode_rpc_payload

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
take: 1 if client took damage; 0 if client gave damage
player_id: id of the player the client damaged; only used if take is 0
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

    def __str__(self):
        return f'<GiveTakeDamage take={self.take} player_id={self.player_id} amount={self.amount:.02f} weapon_id={self.weapon_id.name}({self.weapon_id.value}) body_part={self.body_part.name}({self.body_part.value})>'

    def __len__(self):
        return 1 + TO_BITS(14)

    def encode_rpc_payload(self, bs):
        bs.write_bool(self.take)
        bs.write_u16(self.player_id)
        bs.write_float(self.amount)
        bs.write_u32(self.weapon_id)
        bs.write_u32(self.body_part)

    @staticmethod
    def decode_rpc_payload(bs):
        take = bs.read_bool()
        player_id = bs.read_u16()
        amount = bs.read_float()
        weapon_id = bs.read_u32()
        body_part = bs.read_u32()
        return GiveTakeDamage(take, player_id, amount, weapon_id, body_part)
RPC.GIVE_TAKE_DAMAGE.decode_rpc_payload = GiveTakeDamage.decode_rpc_payload


class EditAttachedObject(Rpc):
    def __init__(self):
        super().__init__(RPC.EDIT_ATTACHED_OBJECT)

    def __str__(self):
        return f'<EditAttachedObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EditAttachedObject()
RPC.EDIT_ATTACHED_OBJECT.decode_rpc_payload = EditAttachedObject.decode_rpc_payload


class EditObject(Rpc):
    def __init__(self):
        super().__init__(RPC.EDIT_OBJECT)

    def __str__(self):
        return f'<EditObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EditObject()
RPC.EDIT_OBJECT.decode_rpc_payload = EditObject.decode_rpc_payload


''' C2S
Client sends when the interior changes
'''
class InteriorChange(Rpc):
    def __init__(self, interior_id):
        super().__init__(RPC.INTERIOR_CHANGE)
        self.interior_id = interior_id

    def __str__(self):
        return f'<InteriorChange interior_id={self.interior_id}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.interior_id)

    @staticmethod
    def decode_rpc_payload(bs):
        interior_id = bs.read_u8()
        return InteriorChange(interior_id)
RPC.INTERIOR_CHANGE.decode_rpc_payload = InteriorChange.decode_rpc_payload


class MapMarker(Rpc):
    def __init__(self):
        super().__init__(RPC.MAP_MARKER)

    def __str__(self):
        return f'<MapMarker>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return MapMarker()
RPC.MAP_MARKER.decode_rpc_payload = MapMarker.decode_rpc_payload


class RemoveGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.REMOVE_GANG_ZONE)

    def __str__(self):
        return f'<RemoveGangZone>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RemoveGangZone()
RPC.REMOVE_GANG_ZONE.decode_rpc_payload = RemoveGangZone.decode_rpc_payload


class FlashGangZone(Rpc):
    def __init__(self):
        super().__init__(RPC.FLASH_GANG_ZONE)

    def __str__(self):
        return f'<FlashGangZone>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return FlashGangZone()
RPC.FLASH_GANG_ZONE.decode_rpc_payload = FlashGangZone.decode_rpc_payload


class StopObject(Rpc):
    def __init__(self):
        super().__init__(RPC.STOP_OBJECT)

    def __str__(self):
        return f'<StopObject>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return StopObject()
RPC.STOP_OBJECT.decode_rpc_payload = StopObject.decode_rpc_payload


class SetVehicleNumberPlate(Rpc):
    def __init__(self, vehicle_id, text):
        super().__init__(RPC.SET_VEHICLE_NUMBER_PLATE)
        self.vehicle_id = vehicle_id
        self.text = text

    def __str__(self):
        return f"<SetVehicleNumberPlate vehicle_id={self.vehicle_id} text='{self.text}'>"

    def __len__(self):
        return TO_BITS(2 + 1 + len(self.text.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_dynamic_buffer_u8(self.text.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        text = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        return SetVehicleNumberPlate(vehicle_id, text)
RPC.SET_VEHICLE_NUMBER_PLATE.decode_rpc_payload = SetVehicleNumberPlate.decode_rpc_payload


class TogglePlayerSpectating(Rpc):
    def __init__(self, spectating):
        super().__init__(RPC.TOGGLE_PLAYER_SPECTATING)
        self.spectating = spectating

    def __str__(self):
        return f'<TogglePlayerSpectating spectating={self.spectating}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.spectating)

    @staticmethod
    def decode_rpc_payload(bs):
        spectating = bs.read_u32()
        return TogglePlayerSpectating(spectating)
RPC.TOGGLE_PLAYER_SPECTATING.decode_rpc_payload = TogglePlayerSpectating.decode_rpc_payload

class SPECTATE_MODE(enum.IntEnum):
    NORMAL = 1 # Normal spectate mode (third person point of view). Camera can not be changed
    FIXED = 2 # Use SetPlayerCameraPos after this to position the player's camera, and it will track the player/vehicle set with PlayerSpectatePlayer/PlayerSpectateVehicle
    SIDE = 3 # The camera will be attached to the side of the player/vehicle (like when you're in first-person camera on a bike and you do a wheelie)

class SpectatePlayer(Rpc):
    def __init__(self, player_id, mode):
        super().__init__(RPC.SPECTATE_PLAYER)
        self.player_id = player_id
        self.mode = SPECTATE_MODE(mode)

    def __str__(self):
        return f'<SpectatePlayer player_id={self.player_id} mode={self.mode.name}({self.mode.value})>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.mode)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        mode = bs.read_u8()
        return SpectatePlayer(player_id, mode)
RPC.SPECTATE_PLAYER.decode_rpc_payload = SpectatePlayer.decode_rpc_payload


class SpectateVehicle(Rpc):
    def __init__(self, vehicle_id, mode):
        super().__init__(RPC.SPECTATE_VEHICLE)
        self.vehicle_id = vehicle_id
        self.mode = SPECTATE_MODE(mode)

    def __str__(self):
        return f'<SpectateVehicle vehicle_id={self.vehicle_id} mode={self.mode.name}({self.mode.value})>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u8(self.mode)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        mode = bs.read_u8()
        return SpectateVehicle(vehicle_id, mode)
RPC.SPECTATE_VEHICLE.decode_rpc_payload = SpectateVehicle.decode_rpc_payload

class RequestClass(Rpc):
    def __init__(self, class_id=None):
        super().__init__(RPC.REQUEST_CLASS)
        self.class_id = class_id
    
    def __str__(self):
        return f'<RequestClass class_id={self.class_id}>'
    
    def __len__(self):
        return TO_BITS(4)
    
    def encode_rpc_payload(self, bs):
        bs.write_u32(self.class_id)
    
    @staticmethod
    def decode_rpc_payload(bs):
        class_id = bs.read_u32()
        return RequestClass(class_id)
RPC.REQUEST_CLASS.decode_client_rpc_payload = RequestClass.decode_rpc_payload


'''
if response is 0 then all other parameters will be ignored
response: either 1 or 0
'''
class RequestClassResponse(Rpc):
    def __init__(self, response, team=None, skin=None, pos=None, rotation=None, weapon1=None, weapon2=None, weapon3=None):
        super().__init__(RPC.REQUEST_CLASS)
        self.response = response
        self.team = team
        self.skin = None if (skin == None) else SKIN(skin)
        self.pos = pos
        self.rotation = None if (rotation == None) else float(rotation)
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.weapon3 = weapon3

    def __str__(self):
        return f'<RequestClassResponse response={self.response} team={self.team} skin={self.skin.name}({self.skin.value}) pos={self.pos} rotation={self.rotation:.02f} weapon1={self.weapon1} weapon2={self.weapon2} weapon3={self.weapon3}'

    def __len__(self):
        return TO_BITS(1 if self.response == 0 else 48)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.response)
        if self.response == 0:
            return
        bs.write_u8(self.team)
        bs.write_u32(self.skin)
        bs.write_u8(0) # unused
        bs.write_vec3(self.pos)
        bs.write_float(self.rotation)
        bs.write_u32(self.weapon1.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon2.id)
        bs.write_u32(self.weapon1.ammo)
        bs.write_u32(self.weapon2.ammo)
        bs.write_u32(self.weapon3.ammo)

    @staticmethod
    def decode_rpc_payload(bs):
        team = skin = pos = rotation = weapon1 = weapon2 = weapon3 = None
        response = bs.read_u8()
        if response == 1:
            team = bs.read_u8()
            skin = bs.read_u32()
            bs.skip_bits(8) # unused
            pos = bs.read_vec3()
            rotation = bs.read_float()
            weapon1_id = bs.read_u32()
            weapon2_id = bs.read_u32()
            weapon3_id = bs.read_u32()
            weapon1_ammo = bs.read_u32()
            weapon2_ammo = bs.read_u32()
            weapon3_ammo = bs.read_u32()
            weapon1 = Weapon(weapon1_id, weapon1_ammo)
            weapon2 = Weapon(weapon2_id, weapon2_ammo)
            weapon3 = Weapon(weapon3_id, weapon3_ammo)
        return RequestClassResponse(response, team, skin, pos, rotation, weapon1, weapon2, weapon3)
RPC.REQUEST_CLASS.decode_server_rpc_payload = RequestClassResponse.decode_rpc_payload

class RequestSpawn(Rpc):
    def __init__(self):
        super().__init__(RPC.REQUEST_SPAWN)

    def __str__(self):
            return f'<RequestSpawn>'

    def __len__(self):
        return 0

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

class RequestSpawnResponse(Rpc):
    def __init__(self, response):
        super().__init__(RPC.REQUEST_SPAWN_RESPONSE)
        self.response = response

    def __str__(self):
        return f'<RequestSpawnResponse response={self.response}>'

    def __len__(self):
        return TO_BITS(1)

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

    def __str__(self):
        return f'<ConnectionRejected reason={self.reason.name}({self.reason.value})>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.reason)

    @staticmethod
    def decode_rpc_payload(bs):
        reason = bs.read_u8()
        return ConnectionRejected(reason)
RPC.CONNECTION_REJECTED.decode_rpc_payload = ConnectionRejected.decode_rpc_payload


class PickedUpPickup(Rpc):
    def __init__(self, pickup_id):
        super().__init__(RPC.PICKED_UP_PICKUP)
        self.pickup_id = pickup_id

    def __str__(self):
        return f'<PickedUpPickup pickup_id={self.pickup_id}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.pickup_id)

    @staticmethod
    def decode_rpc_payload(bs):
        pickup_id = bs.read_u32()
        return PickedUpPickup(pickup_id)
RPC.PICKED_UP_PICKUP.decode_rpc_payload = PickedUpPickup.decode_rpc_payload


class MenuSelect(Rpc):
    def __init__(self):
        super().__init__(RPC.MENU_SELECT)

    def __str__(self):
        return f'<MenuSelect>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return MenuSelect()
RPC.MENU_SELECT.decode_rpc_payload = MenuSelect.decode_rpc_payload


class SetPlayerWantedLevel(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_PLAYER_WANTED_LEVEL)

    def __str__(self):
        return f'<SetPlayerWantedLevel>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetPlayerWantedLevel()
RPC.SET_PLAYER_WANTED_LEVEL.decode_rpc_payload = SetPlayerWantedLevel.decode_rpc_payload

'''
The x,y coordinate is the top left coordinate for the text draw area based on a 640x480 "canvas" (irrespective of screen resolution).
'''
class ShowTextdraw(Rpc):
    def __init__(self, textdraw_id, flags, letter_size, letter_color, line_size, box_color, shadow, outline, background_color, style, clickable, pos, model_id, rot, zoom, color1, color2, text):
        super().__init__(RPC.SHOW_TEXTDRAW)
        self.textdraw_id = textdraw_id
        self.flags = flags
        self.letter_size = letter_size
        self.letter_color = letter_color
        self.line_size = line_size
        self.box_color = box_color
        self.shadow = shadow
        self.outline = outline
        self.background_color = background_color
        self.style = style
        self.clickable = clickable
        self.pos = pos
        self.model_id = model_id
        self.rot = rot
        self.zoom = zoom
        self.color1 = color1
        self.color2 = color2
        self.text = text

    def __str__(self):
        return f"<ShowTextdraw textdraw_id={self.textdraw_id} text='{self.text}' pos={self.pos} rot={self.rot} color1={self.color1:08x} color2={self.color2:08x} flags={self.flags} letter_size={self.letter_size} letter_color={self.letter_color:08x} line_size={self.line_size} box_color={self.box_color:08x} shadow={self.shadow} outline={self.outline} background_color={self.background_color:08x} style={self.style} clickable={self.clickable} model_id={self.model_id} zoom={self.zoom:.02f}>"

    def __len__(self):
        return TO_BITS(67 + len(self.text))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)
        bs.write_u8(self.flags)
        self.letter_size.encode(bs)
        bs.write_u32(self.letter_color)
        self.line_size.encode(bs)
        bs.write_u32(self.box_color)
        bs.write_u8(self.shadow)
        bs.write_u8(self.outline)
        bs.write_u32(self.background_color)
        bs.write_u8(self.style)
        bs.write_u8(self.clickable)
        bs.write_vec3(self.pos)
        bs.write_u16(self.model_id)
        self.rot.encode(bs)
        bs.write_float(self.zoom)
        bs.write_u16(self.color1)
        bs.write_u16(self.color2)
        try:
            bs.write_dynamic_buffer_u16(encode_gxt(self.text))
        except:
            log(f'ShowTextdraw.encode_rpc_payload: failed to encode "{self.text}"')
            bs.write_dynamic_buffer_u16('')
    
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
        rot = bs.read_vec3()
        zoom = bs.read_float()
        color1 = bs.read_u16()
        color2 = bs.read_u16()
        try:
            text = decode_gxt(bs.read_dynamic_buffer_u16())
        except Exception as e:
            log('ShowTextdraw.decode_rpc_payload; failed to decode; bs={bs.data.hex(" ")}')
            text = ''
        return ShowTextdraw(textdraw_id, flags, letter_size, letter_color, line_size, box_color, shadow, outline, background_color, style, clickable, pos, model_id, rot, zoom, color1, color2, text)
RPC.SHOW_TEXTDRAW.decode_rpc_payload = ShowTextdraw.decode_rpc_payload


class HideTextdraw(Rpc):
    def __init__(self, textdraw_id):
        super().__init__(RPC.HIDE_TEXTDRAW)
        self.textdraw_id = textdraw_id

    def __str__(self):
        return f'<HideTextdraw textdraw_id={self.textdraw_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.textdraw_id)

    @staticmethod
    def decode_rpc_payload(bs):
        textdraw_id = bs.read_u16()
        return HideTextdraw(textdraw_id)
RPC.HIDE_TEXTDRAW.decode_rpc_payload = HideTextdraw.decode_rpc_payload


class VehicleDestroyed(Rpc):
    def __init__(self):
        super().__init__(RPC.VEHICLE_DESTROYED)

    def __str__(self):
        return f'<VehicleDestroyed>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return VehicleDestroyed()
RPC.VEHICLE_DESTROYED.decode_rpc_payload = VehicleDestroyed.decode_rpc_payload


class ServerJoin(Rpc):
    def __init__(self, player_id, color, is_npc, player_name):
        super().__init__(RPC.SERVER_JOIN)
        self.player_id = player_id
        self.color = color
        self.is_npc = is_npc
        self.player_name = player_name

    def __str__(self):
        return f"<ServerJoin player_id={self.player_id} player_name='{self.player_name}' color={self.color:08x} is_npc={self.is_npc}>"

    def __len__(self):
        return TO_BITS(7 + len(self.player_name.encode(SAMP_ENCODING)))

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u32(self.color)
        bs.write_u8(self.is_npc)
        bs.write_dynamic_buffer_u8(self.player_name.encode(SAMP_ENCODING))

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        color = bs.read_u32()
        is_npc = bs.read_u8()
        player_name = bs.read_dynamic_buffer_u8().decode(SAMP_ENCODING)
        return ServerJoin(player_id, color, is_npc, player_name)
RPC.SERVER_JOIN.decode_rpc_payload = ServerJoin.decode_rpc_payload


class QUIT_REASON(enum.IntEnum):
    TIMEOUT  = 0
    QUIT     = 1
    KICK_BAN = 2

class ServerQuit(Rpc):
    def __init__(self, player_id, reason=QUIT_REASON.QUIT):
        super().__init__(RPC.SERVER_QUIT)
        self.player_id = player_id
        self.reason = QUIT_REASON(reason)

    def __str__(self):
        return f'<ServerQuit player_id={self.player_id} reason={self.reason.name}({self.reason.value})>'

    def __len__(self):
        return TO_BITS(3)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u8(self.reason)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        reason = QUIT_REASON(bs.read_u8())
        return ServerQuit(player_id, reason)
RPC.SERVER_QUIT.decode_rpc_payload = ServerQuit.decode_rpc_payload


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
    
    def __str__(self):
        return f"<InitGame zone_names={self.zone_names} use_cj_walk={self.use_cj_walk} allow_weapons={self.allow_weapons} limit_global_chat_radius={self.limit_global_chat_radius} global_chat_radius={self.global_chat_radius:.2f} stunt_bonus={self.stunt_bonus} name_tag_draw_distance={self.name_tag_draw_distance:.2f} disable_enter_exits={self.disable_enter_exits} name_tag_los={self.name_tag_los} manual_vehicle_engine_and_light={self.manual_vehicle_engine_and_light} spawns_available={self.spawns_available} player_id={self.player_id} show_player_tags={self.show_player_tags} show_player_markers={self.show_player_markers} world_time={self.world_time} weather={self.weather} gravity={self.gravity:.5f} lan_mode={self.lan_mode} death_drop_money={self.death_drop_money} instagib={self.instagib} onfoot_rate={self.onfoot_rate} incar_rate={self.incar_rate} weapon_rate={self.weapon_rate} multiplier={self.multiplier} lag_comp={self.lag_comp} hostname='{self.hostname}' vehicle_friendly_fire={self.vehicle_friendly_fire}>"

    def __len__(self):
        return 395 + TO_BITS(1 + len(self.hostname.encode(SAMP_ENCODING)) + 212) + 32

    def encode_rpc_payload(self, bs):
        bs.write_bool(self.zone_names)
        bs.write_bool(self.use_cj_walk)
        bs.write_bool(self.allow_weapons)
        bs.write_bool(self.limit_global_chat_radius)
        bs.write_float(self.global_chat_radius)
        bs.write_bool(self.stunt_bonus)
        bs.write_float(self.name_tag_draw_distance)
        bs.write_bool(self.disable_enter_exits)
        bs.write_bool(self.name_tag_los)
        bs.write_bool(self.manual_vehicle_engine_and_light)
        bs.write_u32(self.spawns_available)
        bs.write_u16(self.player_id)
        bs.write_bool(self.show_player_tags)
        bs.write_u32(self.show_player_markers)
        bs.write_u8(self.world_time)
        bs.write_u8(self.weather)
        bs.write_float(self.gravity)
        bs.write_bool(self.lan_mode)
        bs.write_u32(self.death_drop_money)
        bs.write_bool(self.instagib)
        bs.write_u32(self.onfoot_rate)
        bs.write_u32(self.incar_rate)
        bs.write_u32(self.weapon_rate)
        bs.write_u32(self.multiplier)
        bs.write_u32(self.lag_comp)
        bs.write_dynamic_buffer_u8(self.hostname.encode(SAMP_ENCODING))
        bs.write_bits(bytearray(self.vehicle_models), TO_BITS(212))
        bs.write_u32(self.vehicle_friendly_fire)

    @staticmethod
    def decode_rpc_payload(bs):
        zone_names                       = bs.read_bool()
        use_cj_walk                      = bs.read_bool()
        allow_weapons                    = bs.read_bool()
        limit_global_chat_radius         = bs.read_bool()
        global_chat_radius               = bs.read_float()
        stunt_bonus                      = bs.read_bool()
        name_tag_draw_distance           = bs.read_float()
        disable_enter_exits              = bs.read_bool()
        name_tag_los                     = bs.read_bool()
        manual_vehicle_engine_and_light  = bs.read_bool()
        spawns_available                 = bs.read_u32()
        player_id                        = bs.read_u16()
        show_player_tags                 = bs.read_bool()
        show_player_markers              = bs.read_u32()
        world_time                       = bs.read_u8()
        weather                          = bs.read_u8()
        gravity                          = bs.read_float()
        lan_mode                         = bs.read_bool()
        death_drop_money                 = bs.read_u32()
        instagib                         = bs.read_bool()
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
RPC.INIT_GAME.decode_rpc_payload = InitGame.decode_rpc_payload


class MenuQuit(Rpc):
    def __init__(self):
        super().__init__(RPC.MENU_QUIT)

    def __str__(self):
        return f'<MenuQuit>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return MenuQuit()
RPC.MENU_QUIT.decode_rpc_payload = MenuQuit.decode_rpc_payload


class RemoveMapIcon(Rpc):
    def __init__(self, icon_id):
        super().__init__(RPC.REMOVE_MAP_ICON)
        self.icon_id = icon_id

    def __str__(self):
        return f'<RemoveMapIcon icon_id={self.icon_id}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.icon_id)

    @staticmethod
    def decode_rpc_payload(bs):
        icon_id = bs.read_u8()
        return RemoveMapIcon(icon_id)
RPC.REMOVE_MAP_ICON.decode_rpc_payload = RemoveMapIcon.decode_rpc_payload


class SetWeaponAmmo(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_WEAPON_AMMO)

    def __str__(self):
        return f'<SetWeaponAmmo>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetWeaponAmmo()
RPC.SET_WEAPON_AMMO.decode_rpc_payload = SetWeaponAmmo.decode_rpc_payload


class SetGravity(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_GRAVITY)

    def __str__(self):
        return f'<SetGravity>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetGravity()
RPC.SET_GRAVITY.decode_rpc_payload = SetGravity.decode_rpc_payload


class SetVehicleHealth(Rpc):
    def __init__(self, vehicle_id, health):
        super().__init__(RPC.SET_VEHICLE_HEALTH)
        self.vehicle_id = vehicle_id
        self.health = health

    def __str__(self):
        return f'<SetVehicleHealth vehicle_id={self.vehicle_id} health={self.health:.02f}>'

    def __len__(self):
        return TO_BITS(6)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_float(self.health)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        health = bs.read_float()
        return SetVehicleHealth(vehicle_id, health)
RPC.SET_VEHICLE_HEALTH.decode_rpc_payload = SetVehicleHealth.decode_rpc_payload


class AttachTrailerToVehicle(Rpc):
    def __init__(self):
        super().__init__(RPC.ATTACH_TRAILER_TO_VEHICLE)

    def __str__(self):
        return f'<AttachTrailerToVehicle>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return AttachTrailerToVehicle()
RPC.ATTACH_TRAILER_TO_VEHICLE.decode_rpc_payload = AttachTrailerToVehicle.decode_rpc_payload


class DetachTrailerFromVehicle(Rpc):
    def __init__(self):
        super().__init__(RPC.DETACH_TRAILER_FROM_VEHICLE)

    def __str__(self):
        return f'<DetachTrailerFromVehicle>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return DetachTrailerFromVehicle()
RPC.DETACH_TRAILER_FROM_VEHICLE.decode_rpc_payload = DetachTrailerFromVehicle.decode_rpc_payload


'''
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

    def __str__(self):
        return f'<SetWeather weather_id={self.weather_id}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.weather_id)

    @staticmethod
    def decode_rpc_payload(bs):
        weather_id = bs.read_u8()
        return SetWeather(weather_id)
RPC.SET_WEATHER.decode_rpc_payload = SetWeather.decode_rpc_payload


class SetPlayerSkin(Rpc):
    def __init__(self, player_id, skin_id):
        super().__init__(RPC.SET_PLAYER_SKIN)
        self.player_id = player_id
        self.skin_id = skin_id

    def __str__(self):
        return f'<SetPlayerSkin player_id={self.player_id} skin_id={self.skin_id}>'

    def __len__(self):
        return TO_BITS(8)

    def encode_rpc_payload(self, bs):
        bs.write_u32(self.player_id)
        bs.write_u32(self.skin_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u32()
        skin_id = bs.read_u32()
        return SetPlayerSkin(player_id, skin_id)
RPC.SET_PLAYER_SKIN.decode_rpc_payload = SetPlayerSkin.decode_rpc_payload

''' S2C
Server sends when a player exits a vehicle
player_id: the id of the player exiting the vehicle
vehicle_id: the id of the vehicle about to be exited
'''
class PlayerExitVehicle(Rpc):
    def __init__(self, player_id, vehicle_id):
        super().__init__(RPC.PLAYER_EXIT_VEHICLE)
        self.player_id = player_id
        self.vehicle_id = vehicle_id

    def __str__(self):
        return f'<PlayerExitVehicle player_id={self.player_id} vehicle_id={self.vehicle_id}>'

    def __len__(self):
        return TO_BITS(4)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)
        bs.write_u16(self.vehicle_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        vehicle_id = bs.read_u16()
        return PlayerExitVehicle(player_id, vehicle_id)
RPC.PLAYER_EXIT_VEHICLE.decode_server_rpc_payload = PlayerExitVehicle.decode_rpc_payload


''' C2S
Client sends when it exits a vehicle
vehicle_id: the id of the vehicle about to be exited
'''
class ExitVehicle(Rpc):
    def __init__(self, vehicle_id):
        super().__init__(RPC.PLAYER_EXIT_VEHICLE)
        self.vehicle_id = vehicle_id

    def __str__(self):
        return f'<ExitVehicle vehicle_id={self.vehicle_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        return ExitVehicle(vehicle_id)
RPC.PLAYER_EXIT_VEHICLE.decode_client_rpc_payload = ExitVehicle.decode_rpc_payload


class RequestScoresAndPings(Rpc):
    def __init__(self):
        super().__init__(RPC.REQUEST_SCORES_AND_PINGS)

    def __str__(self):
        return f'<RequestScoresAndPings>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return RequestScoresAndPings()
RPC.REQUEST_SCORES_AND_PINGS.decode_client_rpc_payload = RequestScoresAndPings.decode_rpc_payload

''' S2C
Response for the RequestScoresAndPings client message.
Provides scoreboard data(score and pings) for ids
players = [[id, score, ping], [id, score, ping], ...]
'''
class RequestScoresAndPingsResponse(Rpc):
    def __init__(self, players):
        super().__init__(RPC.REQUEST_SCORES_AND_PINGS)
        self.players = players

    def __str__(self):
        s = ''
        for player in self.players:
            s += f'({player[0]} {player[1]} {player[2]}), '
        return f'<RequestScoresAndPingsResponse {s}>'

    def __len__(self):
        return TO_BITS(10 * len(self.players))

    def encode_rpc_payload(self, bs):
        for player in self.players:
            bs.write_u16(player[0])
            bs.write_u32(player[1])
            bs.write_u32(player[2])

    @staticmethod
    def decode_rpc_payload(bs):
        player_count = TO_BYTES(bs.unread_bits_count()) // 10
        players = [None] * player_count
        for i in range(player_count):
            id = bs.read_u16()
            score = bs.read_u32()
            ping = bs.read_u32()
            players[i] = [id, score, ping]
        return RequestScoresAndPingsResponse(players)
RPC.REQUEST_SCORES_AND_PINGS.decode_server_rpc_payload = RequestScoresAndPingsResponse.decode_rpc_payload


class SetPlayerInterior(Rpc):
    def __init__(self, interior_id):
        super().__init__(RPC.SET_PLAYER_INTERIOR)
        self.interior_id = interior_id

    def __str__(self):
        return f'<SetPlayerInterior interior_id={self.interior_id}>'

    def __len__(self):
        return TO_BITS(1)

    def encode_rpc_payload(self, bs):
        bs.write_u8(self.interior_id)

    @staticmethod
    def decode_rpc_payload(bs):
        interior_id = bs.read_u8()
        return SetPlayerInterior(interior_id)
RPC.SET_PLAYER_INTERIOR.decode_rpc_payload = SetPlayerInterior.decode_rpc_payload


class SetCameraPos(Rpc):
    def __init__(self, pos):
        super().__init__(RPC.SET_CAMERA_POS)
        self.pos = pos

    def __str__(self):
        return f'<SetCameraPos {self.pos}>'

    def __len__(self):
        return TO_BITS(12)

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        return SetCameraPos(pos)
RPC.SET_CAMERA_POS.decode_rpc_payload = SetCameraPos.decode_rpc_payload


class CAMERA_CUT(enum.IntEnum):
    MOVE = 1 # The camera position and/or target will move to its new value over time.
    CUT = 2 # The camera position and/or target will move to its new value instantly.

class SetCameraLookAt(Rpc):
    def __init__(self, pos, cut_type):
        super().__init__(RPC.SET_CAMERA_LOOK_AT)
        self.pos = pos
        self.cut_type = CAMERA_CUT(cut_type)

    def __str__(self):
        return f'<SetCameraLookAt {self.pos} cut_type={self.cut_type.name}({self.cut_type.value})>'

    def __len__(self):
        return TO_BITS(13)

    def encode_rpc_payload(self, bs):
        bs.write_vec3(self.pos)
        bs.write_u8(self.cut_type)

    @staticmethod
    def decode_rpc_payload(bs):
        pos = bs.read_vec3()
        cut_type = bs.read_u8()
        return SetCameraLookAt(pos, cut_type)
RPC.SET_CAMERA_LOOK_AT.decode_rpc_payload = SetCameraLookAt.decode_rpc_payload


class SetVehiclePos(Rpc):
    def __init__(self, vehicle_id, pos):
        super().__init__(RPC.SET_VEHICLE_POS)
        self.vehicle_id = vehicle_id
        self.pos = pos

    def __str__(self):
        return f'<SetVehiclePos vehicle_id={self.vehicle_id} pos={self.pos}>'

    def __len__(self):
        return TO_BITS(14)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_vec3(self.pos)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        pos = bs.read_vec3()
        return SetVehiclePos(vehicle_id, pos)
RPC.SET_VEHICLE_POS.decode_rpc_payload = SetVehiclePos.decode_rpc_payload


class SetVehicleZAngle(Rpc):
    def __init__(self, vehicle_id, angle):
        super().__init__(RPC.SET_VEHICLE_Z_ANGLE)
        self.vehicle_id = vehicle_id
        self.angle = angle

    def __str__(self):
        return f'<SetVehicleZAngle vehicle_id={self.vehicle_id} angle={self.angle:.02f}>'

    def __len__(self):
        return TO_BITS(6)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_float(self.angle)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        angle = bs.read_float()
        return SetVehicleZAngle(vehicle_id, angle)
RPC.SET_VEHICLE_Z_ANGLE.decode_rpc_payload = SetVehicleZAngle.decode_rpc_payload


class SetVehicleParams(Rpc):
    def __init__(self, vehicle_id, objective, doors_locked):
        super().__init__(RPC.SET_VEHICLE_PARAMS)
        self.vehicle_id = vehicle_id
        self.objective = objective
        self.doors_locked = doors_locked

    def __str__(self):
        return f'<SetVehicleParams vehicle_id={self.vehicle_id} objective={self.objective} doors_locked={self.doors_locked}>'

    def __len__(self):
        return TO_BITS(4)

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
RPC.SET_VEHICLE_PARAMS.decode_rpc_payload = SetVehicleParams.decode_rpc_payload


class SetCameraBehindPlayer(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_CAMERA_BEHIND_PLAYER)

    def __str__(self):
        return f'<SetCameraBehindPlayer>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetCameraBehindPlayer()
RPC.SET_CAMERA_BEHIND_PLAYER.decode_rpc_payload = SetCameraBehindPlayer.decode_rpc_payload


class WorldPlayerRemove(Rpc):
    def __init__(self, player_id):
        super().__init__(RPC.WORLD_PLAYER_REMOVE)
        self.player_id = player_id

    def __str__(self):
        return f'<WorldPlayerRemove player_id={self.player_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(player_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        return WorldPlayerRemove(player_id)
RPC.WORLD_PLAYER_REMOVE.decode_rpc_payload = WorldPlayerRemove.decode_rpc_payload


class WorldVehicleAdd(Rpc):
    def __init__(self, vehicle_id, model_id, pos, angle, interior_color1, interior_color2, health, interior, door_damage_status, panel_damage_status, light_damage_status, tire_damage_status, add_siren, mods, paint_job, body_color1, body_color2):
        super().__init__(RPC.WORLD_VEHICLE_ADD)
        self.vehicle_id = vehicle_id
        self.model_id = model_id
        self.pos = pos
        self.angle = angle
        self.interior_color1 = interior_color1
        self.interior_color2 = interior_color2
        self.health = health
        self.interior = interior
        self.door_damage_status = door_damage_status
        self.panel_damage_status = panel_damage_status
        self.light_damage_status = light_damage_status
        self.tire_damage_status = tire_damage_status
        self.add_siren = add_siren
        self.mods = mods
        self.paint_job = paint_job
        self.body_color1 = body_color1
        self.body_color2 = body_color2

    def __str__(self):
        return f'<WorldVehicleAdd vehicle_id={self.vehicle_id} model_id={self.model_id} pos={self.pos} angle={self.angle:.02f} interior_color1={self.interior_color1:08x} interior_color2={self.interior_color2:08x} health={self.health} interior={self.interior} door_damage_status={self.door_damage_status} panel_damage_status={self.panel_damage_status} light_damage_status={self.light_damage_status} tire_damage_status={self.tire_damage_status} add_siren={self.add_siren} mods={self.mods} paint_job={self.paint_job} body_color1={self.body_color1:08x} body_color2={self.body_color2:08x}>'

    def __len__(self):
        return TO_BITS(63)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)
        bs.write_u32(self.model_id)
        bs.write_vec3(self.pos)
        bs.write_float(self.angle)
        bs.write_u8(self.interior_color1)
        bs.write_u8(self.interior_color2)
        bs.write_float(self.health)
        bs.write_u8(self.interior)
        bs.write_u32(self.door_damage_status)
        bs.write_u32(self.panel_damage_status)
        bs.write_u8(self.light_damage_status)
        bs.write_u8(self.tire_damage_status)
        bs.write_u8(self.add_siren)
        for mod in self.mods:
            bs.write_u8(mod)
        bs.write_u8(self.paint_job)
        bs.write_u32(self.body_color1)
        bs.write_u32(self.body_color2)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        model_id = bs.read_u32()
        pos = bs.read_vec3()
        angle = bs.read_float()
        interior_color1 = bs.read_u8()
        interior_color2 = bs.read_u8()
        health = bs.read_float()
        interior = bs.read_u8()
        door_damage_status = bs.read_u32()
        panel_damage_status = bs.read_u32()
        light_damage_status = bs.read_u8()
        tire_damage_status = bs.read_u8()
        add_siren = bs.read_u8()
        mods = [bs.read_u8() for i in range(14)]
        paint_job = bs.read_u8()
        body_color1 = bs.read_u32()
        body_color2 = bs.read_u32()
        return WorldVehicleAdd(vehicle_id, model_id, pos, angle, interior_color1, interior_color2, health, interior, door_damage_status, panel_damage_status, light_damage_status, tire_damage_status, add_siren, mods, paint_job, body_color1, body_color2)
RPC.WORLD_VEHICLE_ADD.decode_rpc_payload = WorldVehicleAdd.decode_rpc_payload


class WorldVehicleRemove(Rpc):
    def __init__(self, vehicle_id):
        super().__init__(RPC.WORLD_VEHICLE_REMOVE)
        self.vehicle_id = vehicle_id

    def __str__(self):
        return f'<WorldVehicleRemove vehicle_id={self.vehicle_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.vehicle_id)

    @staticmethod
    def decode_rpc_payload(bs):
        vehicle_id = bs.read_u16()
        return WorldVehicleRemove(vehicle_id)
RPC.WORLD_VEHICLE_REMOVE.decode_rpc_payload = WorldVehicleRemove.decode_rpc_payload


class DeathBroadcast(Rpc):
    def __init__(self, player_id):
        super().__init__(RPC.DEATH_BROADCAST)
        self.player_id = player_id

    def __str__(self):
        return f'<DeathBroadcast player_id={self.player_id}>'

    def __len__(self):
        return TO_BITS(2)

    def encode_rpc_payload(self, bs):
        bs.write_u16(self.player_id)

    @staticmethod
    def decode_rpc_payload(bs):
        player_id = bs.read_u16()
        return DeathBroadcast(player_id)
RPC.DEATH_BROADCAST.decode_rpc_payload = DeathBroadcast.decode_rpc_payload


class ToggleVehicleCollisions(Rpc):
    def __init__(self, enable):
        super().__init__(RPC.TOGGLE_VEHICLE_COLLISIONS)
        self.enable = enable
    
    def __str__(self):
        return f'<ToggleVehicleCollisions enable={self.enable}>'

    def __len__(self):
        return 1

    def encode_rpc_payload(self, bs):
        bs.write_bool(self.enable)

    @staticmethod
    def decode_rpc_payload(bs):
        enable = bs.read_bool()
        return ToggleVehicleCollisions(enable)
RPC.TOGGLE_VEHICLE_COLLISIONS.decode_rpc_payload = ToggleVehicleCollisions.decode_rpc_payload


class CameraTarget(Rpc):
    def __init__(self):
        super().__init__(RPC.CAMERA_TARGET)

    def __str__(self):
        return f'<CameraTarget>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return CameraTarget()
RPC.CAMERA_TARGET.decode_rpc_payload = CameraTarget.decode_rpc_payload


class ShowActor(Rpc):
    def __init__(self):
        super().__init__(RPC.SHOW_ACTOR)

    def __str__(self):
        return f'<ShowActor>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ShowActor()
RPC.SHOW_ACTOR.decode_rpc_payload = ShowActor.decode_rpc_payload


class HideActor(Rpc):
    def __init__(self):
        super().__init__(RPC.HIDE_ACTOR)

    def __str__(self):
        return f'<HideActor>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return HideActor()
RPC.HIDE_ACTOR.decode_rpc_payload = HideActor.decode_rpc_payload


class ApplyActorAnimation(Rpc):
    def __init__(self):
        super().__init__(RPC.APPLY_ACTOR_ANIMATION)

    def __str__(self):
        return f'<ApplyActorAnimation>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ApplyActorAnimation()
RPC.APPLY_ACTOR_ANIMATION.decode_rpc_payload = ApplyActorAnimation.decode_rpc_payload


class ClearActorAnimation(Rpc):
    def __init__(self):
        super().__init__(RPC.CLEAR_ACTOR_ANIMATION)

    def __str__(self):
        return f'<ClearActorAnimation>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return ClearActorAnimation()
RPC.CLEAR_ACTOR_ANIMATION.decode_rpc_payload = ClearActorAnimation.decode_rpc_payload


class SetActorFacingAngle(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_ACTOR_FACING_ANGLE)

    def __str__(self):
        return f'<SetActorFacingAngle>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetActorFacingAngle()
RPC.SET_ACTOR_FACING_ANGLE.decode_rpc_payload = SetActorFacingAngle.decode_rpc_payload


class SetActorPos(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_ACTOR_POS)

    def __str__(self):
        return f'<SetActorPos>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetActorPos()
RPC.SET_ACTOR_POS.decode_rpc_payload = SetActorPos.decode_rpc_payload


class SetActorHealth(Rpc):
    def __init__(self):
        super().__init__(RPC.SET_ACTOR_HEALTH)

    def __str__(self):
        return f'<SetActorHealth>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return SetActorHealth()
RPC.SET_ACTOR_HEALTH.decode_rpc_payload = SetActorHealth.decode_rpc_payload


class EnablePlayerCameraTarget(Rpc):
    def __init__(self):
        super().__init__(RPC.ENABLE_PLAYER_CAMERA_TARGET)

    def __str__(self):
        return f'<EnablePlayerCameraTarget>'

    def __len__(self):
        return 0

    def encode_rpc_payload(self, bs):
        pass

    @staticmethod
    def decode_rpc_payload(bs):
        return EnablePlayerCameraTarget()
RPC.ENABLE_PLAYER_CAMERA_TARGET.decode_rpc_payload = EnablePlayerCameraTarget.decode_rpc_payload


'''
Usually most RPCs are only sent by either the client or server. And when it is
sent by both the RPC may have the same payload structure. In these cases we
define only "RPC.[RPC_NAME].decode_rpc_payload" to the static decoder function
of the specific Rpc class. However raknet.Rpc doesn't call
"RPC.[RPC_NAME].decode_rpc_payload", it only calls decode_client_rpc_payload or
decode_server_rpc_payload; so in this for loop we set both these members to 
decode_rpc_payload.
'''
for rpc in RPC:
    try:
        rpc.decode_client_rpc_payload = rpc.decode_rpc_payload
        rpc.decode_server_rpc_payload = rpc.decode_rpc_payload
    except AttributeError:
        pass
