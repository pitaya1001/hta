import enum

# https://team.sa-mp.com/wiki/Keys.html
# https://www.open.mp/docs/scripting/resources/keys

from .bitstream import *

class PLAYER_KEY(enum.IntEnum):
    ACTION           = 1 << 0  # TAB           ~k~~PED_ANSWER_PHONE~
    CROUCH           = 1 << 1  # C             ~k~~PED_DUCK~
    FIRE             = 1 << 2  # LCTRL/LMB     ~k~~PED_FIREWEAPON~
    SPRINT           = 1 << 3  # SPACE         ~k~~PED_SPRINT~
    SECONDARY_ATTACK = 1 << 4  # ENTER         ~k~~VEHICLE_ENTER_EXIT~
    JUMP             = 1 << 5  # LSHIFT        ~k~~PED_JUMPING~
    LOOK_RIGHT       = 1 << 6  # -             -
    AIM              = 1 << 7  # RMB           ~k~~PED_LOCK_TARGET~
    LOOK_LEFT        = 1 << 8  # -             -
    LOOK_BEHIND      = 1 << 9  # NUM1/MMB      ~k~~PED_LOOKBEHIND~
    WALK             = 1 << 10 # LALT          ~k~~SNEAK_ABOUT~
    ANALOG_UP        = 1 << 11 # NUM8          -
    ANALOG_DOWN      = 1 << 12 # NUM2          -
    ANALOG_LEFT      = 1 << 13 # NUM4          ~k~~VEHICLE_LOOKLEFT~
    ANALOG_RIGHT     = 1 << 14 # NUM6          ~k~~VEHICLE_LOOKRIGHT~
    YES              = 1 << 16 # Y             ~k~~CONVERSATION_YES~
    NO               = 1 << 17 # N             ~k~~CONVERSATION_NO~
    CTRL_BACK        = 1 << 18 # H             ~k~~GROUP_CONTROL_BWD~
    #                          # G             ~k~~GROUP_CONTROL_FWD~ ; cannot be detected in SA-MP, as it used internally to enter vehicles as passenger. However, the gametext definition still exists.

class VEHICLE_KEY(enum.IntEnum):
    ACTION            = 1 << 0  # LCTRL/NUM0    ~k~~VEHICLE_FIREWEAPON_ALT~
    HORN              = 1 << 1  # H/CAPSLOCK    ~k~~VEHICLE_HORN~
    FIRE              = 1 << 2  # LALT          ~k~~VEHICLE_FIREWEAPON~
    ACCELERATE        = 1 << 3  # W             ~k~~VEHICLE_ACCELERATE~
    SECONDARY_ATTACK  = 1 << 4  # ENTER         ~k~~VEHICLE_ENTER_EXIT~
    BRAKE             = 1 << 5  # S             ~k~~VEHICLE_BRAKE~
    LOOK_RIGHT        = 1 << 6  # E             ~k~~VEHICLE_LOOKRIGHT~
    HANDBRAKE         = 1 << 7  # SPACE         ~k~~VEHICLE_HANDBRAKE~
    LOOK_LEFT         = 1 << 8  # Q             ~k~~VEHICLE_LOOKLEFT~
    TOGGLE_SUBMISSION = 1 << 9  # 2             ~k~~TOGGLE_SUBMISSIONS~
    #                 = 1 << 10 # -             -
    ANALOG_UP         = 1 << 11 # NUM8          ~k~~VEHICLE_TURRETUP~
    ANALOG_DOWN       = 1 << 12 # NUM2          ~k~~VEHICLE_TURRETDOWN~
    ANALOG_LEFT       = 1 << 13 # NUM4          ~k~~VEHICLE_TURRETLEFT~
    ANALOG_RIGHT      = 1 << 14 # NUM6          ~k~~VEHICLE_TURRETRIGHT~
    YES               = 1 << 16 # Y             ~k~~CONVERSATION_YES~
    NO                = 1 << 17 # N             ~k~~CONVERSATION_NO~
    CTRL_BACK         = 1 << 18 # H             ~k~~GROUP_CONTROL_BWD~

class LR_KEY(enum.IntEnum):
    NONE  = 0
    LEFT  = -128 # LEFT     ~k~~GO_LEFT~     ~k~~VEHICLE_STEERLEFT~
    RIGHT = 128 # RIGHT    ~k~~GO_RIGHT~    ~k~~VEHICLE_STEERRIGHT~

class UD_KEY(enum.IntEnum):
    NONE = 0
    UP   = -128 # UP      ~k~~GO_FORWARD~    ~k~~VEHICLE_STEERUP~
    DOWN = 128  # DOWN    ~k~~GO_BACK~       ~k~~VEHICLE_STEERDOWN~

# lr_keys and ud_keys are just for animation, they do not actually make the player move, 'vel' does
class KeyData:
    def __init__(self, lr_keys, ud_keys, keys):
        self.lr_keys = lr_keys #LR_KEY(lr_keys) # i16; LR_KEY.LEFT, LR_KEY.RIGHT or 0(neither)
        self.ud_keys = ud_keys #UD_KEY(ud_keys) # i16; UD_KEY.UP, UD_KEY.DOWN or 0(neither)
        self.keys = keys # u32; bitmask of constants in PLAYER_KEY(if on foot) or VEHICLE_KEY(if in vehicle)

    def __str__(self):
        bitmask = ''
        for constants in PLAYER_KEY, VEHICLE_KEY:
            bitmask += '('
            count = 0
            x = self.keys
            while constant := next((c for c in constants if x & c), 0):
                bitmask += f'{constant.name} '
                x = x & ~constant
                count += 1
            if count == 0:
                bitmask += 'NONE) '
            else:
                bitmask = bitmask[:-1] + ') '
        #return f'<KeyData lr_keys={self.lr_keys.name} ud_keys={self.ud_keys.name} keys={bitmask[:-1]}>'
        return f'<KeyData lr_keys={self.lr_keys} ud_keys={self.ud_keys} keys={bitmask[:-1]}>'

def read_key_data(self):
    lr_keys = self.read_i16()
    ud_keys = self.read_i16()
    keys = self.read_u16()
    return KeyData(lr_keys, ud_keys, keys)

def write_key_data(self, key_data):
    self.write_i16(key_data.lr_keys)
    self.write_i16(key_data.ud_keys)
    self.write_u16(key_data.keys)

def read_compressed_key_data(self):
    if has_lr := self.read_bit():
        lr_keys = self.read_i16()
    else:
        lr_keys = 0

    if has_ud := self.read_bit():
        ud_keys = self.read_i16()
    else:
        ud_keys = 0

    keys = self.read_u16()

    return KeyData(lr_keys, ud_keys, keys)

def write_compressed_key_data(self, key_data):
    if key_data.lr_keys != 0:
        self.write_bit(1)
        self.write_i16(key_data.lr_keys)
    else:
        self.write_bit(0)

    if key_data.ud_keys != 0:
        self.write_bit(1)
        self.write_i16(key_data.ud_keys)
    else:
        self.write_bit(0)

    self.write_u16(key_data.keys)

Bitstream.read_key_data = read_key_data
Bitstream.write_key_data = write_key_data
Bitstream.read_compressed_key_data = read_compressed_key_data
Bitstream.write_compressed_key_data = write_compressed_key_data