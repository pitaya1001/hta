import logging
import enum
import random
import asyncio

SAMP_ENCODING = 'latin1' # iso-8859-1
#SAMP_ENCODING = 'cp1251' # Windows-1251

DEFAULT_GRAVITY = 0.008

''' This constant is used for:
(1) Initial cookie the client sends to server
(2) The value that shoud be xored with the server cookie to calculate the secret cookie
'''
MAGIC_COOKIE = 0x6969

MAX_PLAYER_ID = 1000 - 1 # [0,999] ; Note: 0 is a valid player id
MAX_VEHICLE_ID = 2000 - 1 # [1,1999] ; Note: 0 is NOT a valid vehicle id
MAX_OBJECT_ID = 1000 - 1
MAX_PLAYER_NAME_LENGTH = 24
MAX_DIALOG_ID = 32768 - 1

MAX_TEXTDRAW_TEXT_LENGTH = 1024
MAX_TEXTDRAW_ID = 2048 + 256 - 1

MAX_3D_TEXT_LABEL_ID = 2048 - 1

CLIENT_VERSION_37 = 4057

# team id when player is not in any team
NO_TEAM_ID = 255

INVALID_ID = 0xffff # 2**16-1

INVALID_WEAPON_ID = 0xffffffff

class Weapon:
    def __init__(self, id=INVALID_WEAPON_ID, ammo=0):
        self.id = id
        self.ammo = ammo

    def __str__(self):
        return f'<Weapon {self.id} - {self.ammo}>'

class Color:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value:08x}'

# TODO: fix tables
# https://gtamods.com/wiki/GXT

gxt_table_1 = ' '*32 + '''
 !"#$%&'()*+,-./
0123456789:;�=�?
™ABCDEFGHIJKLMNO
PQRSTUVWXYZ[\\]¡ 
`abcdefghijklmno
pqrstuvwxyz�|$~)
ÀÁÂÄÆÇÈÉÊËÌÍÎÏÒÓ
ÔÖÙÚÛÜßàáâäæçèéê
ëìíîïòóôöùúûüÑñ¿
0123456789:a
'''.replace('\n','')

gxt_table_2 = ' '*32 + '''
 !"#$%&'()*+,-./
0123456789:;�=�?
™ABCDEFGHIJKLMNO
PQRSTUVWXYZ \\*¡ 
`abcdefghijklmno
pqrstuvwxyz�|$~)
ÀÁÂÄÆÇÈÉÊËÌÍÎÏÒÓ
ÔÖÙÚÛÜßàáâäæçèéê
ëìíîïòóôöùúûüÑñ¿
0123456789:a
'''.replace('\n','')

def decode_gxt(data): return ''.join(map(lambda b: gxt_table_1[b], data))

gxt_dict = {
          '!':0x21, '"':0x22, '#':0x23, '$':0x24, '%':0x25, '&':0x26, "'":0x27, '(':0x28, ')':0x29, '*':0x2a, '+':0x2b,  ',':0x2c, '-':0x2d, '.':0x2e, '/':0x2f,
'0':0x30, '1':0x31, '2':0x32, '3':0x33, '4':0x34, '5':0x35, '6':0x36, '7':0x37, '8':0x38, '9':0x39, ':':0x3a, ';':0x3b,            '=':0x3d,           '?':0x3f,
'™':0x40, 'A':0x41, 'B':0x42, 'C':0x43, 'D':0x44, 'E':0x45, 'F':0x46, 'G':0x47, 'H':0x48, 'I':0x49, 'J':0x4a, 'K':0x4b,  'L':0x4c, 'M':0x4d, 'N':0x4e, 'O':0x4f,
'P':0x50, 'Q':0x51, 'R':0x52, 'S':0x53, 'T':0x54, 'U':0x55, 'V':0x56, 'W':0x57, 'X':0x58, 'Y':0x59, 'Z':0x5a, '[':0x5b, '\\':0x5c, ']':0x5d, '¡':0x5e, ' ':0x5f,
'`':0x60, 'a':0x61, 'b':0x62, 'c':0x63, 'd':0x64, 'e':0x65, 'f':0x66, 'g':0x67, 'h':0x68, 'i':0x69, 'j':0x6a, 'k':0x6b,  'l':0x6c, 'm':0x6d, 'n':0x6e, 'o':0x6f,
'p':0x70, 'q':0x71, 'r':0x72, 's':0x73, 't':0x74, 'u':0x75, 'v':0x76, 'w':0x77, 'x':0x78, 'y':0x79, 'z':0x7a, '�':0x7b,  '|':0x7c, '$':0x7d, '~':0x7e, ')':0x7f,
'À':0x80, 'Á':0x81, 'Â':0x82, 'Ä':0x83, 'Æ':0x84, 'Ç':0x85, 'È':0x86, 'É':0x87, 'Ê':0x88, 'Ë':0x89, 'Ì':0x8a, 'Í':0x8b,  'Î':0x8c, 'Ï':0x8d, 'Ò':0x8e, 'Ó':0x8f,
'Ô':0x90, 'Ö':0x91, 'Ù':0x92, 'Ú':0x93, 'Û':0x94, 'Ü':0x95, 'ß':0x96, 'à':0x97, 'á':0x98, 'â':0x99, 'ä':0x9a, 'æ':0x9b,  'ç':0x9c, 'è':0x9d, 'é':0x9e, 'ê':0x9f,
'ë':0xa0, 'ì':0xa1, 'í':0xa2, 'î':0xa3, 'ï':0xa4, 'ò':0xa5, 'ó':0xa6, 'ô':0xa7, 'ö':0xa8, 'ù':0xa9, 'ú':0xaa, 'û':0xab,  'ü':0xac, 'Ñ':0xad, 'ñ':0xae, '¿':0xaf,
'0':0xb0, '1':0xb1, '2':0xb2, '3':0xb3, '4':0xb4, '5':0xb5, '6':0xb6, '7':0xb7, '8':0xb8, '9':0xb9, ':':0xba, 'a':0xbb,
}
def encode_gxt(s): return str(map(lambda c:gxt_dict[c], s))


class SPECIAL_ACTION(enum.IntEnum):
    NONE          = 0
    DUCK          = 1
    JETPACK       = 2
    ENTER_VEHICLE = 3
    EXIT_VEHICLE  = 4
    DANCE1        = 5
    DANCE2        = 6
    DANCE3        = 7
    DANCE4        = 8
    HANDSUP       = 10
    CELLPHONE     = 11
    SITTING       = 12
    STOPCELLPHONE = 13
    BEER          = 20
    SMOKE         = 21
    WINE          = 22
    SPRUNK        = 23
    CUFFED        = 24
    CARRY         = 25
    PISSING       = 68

# Used in two RPCs: SetPlayerFightingStyle and WorldPlayerAdd
class FIGHTING_STYLE(enum.IntEnum):
    NORMAL   = 4
    BOXING   = 5
    KUNGFU   = 6
    KNEEHEAD = 7
    GRABKICK = 15
    ELBOW    = 16

#logging.basicConfig(filename='samp.log',filemode='a',format='%(asctime)s.%(msecs)03d %(message)s',datefmt='%d%m%y-%H%M%S',level=logging.INFO)

def setup_logger(logger_name, file_name):
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(message)s','%d%m%y-%H%M%S')
    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

main_logger = setup_logger('main', 'samp.log')

def log(s):
    #logging.info(s)
    main_logger.info(s)

def pretty_format(self, skip_n):
    s = f'<{self.__class__.__name__}'
    for var, value in list(self.__dict__.items())[skip_n:]:
        if type(value) == float:
            s += f' {var}={value:.2f}'
        elif type(value) == str:
            s += f' {var}={repr(value)}'
        elif type(value) == bytearray or type(var) == bytes:
            s += f' {var}=[{value.hex(" ")}]'
        elif isinstance(value, enum.Enum):
            s += f' {var}={value.name}({value.value})'
        else:
            s += f' {var}={value}'
    s += '>'
    return s