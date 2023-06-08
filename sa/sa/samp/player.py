from sa.player import Player as SaPlayer
from .keys import KeyData
from .anim import AnimData
from .surf import SurfData

from .common import pretty_format

class Player(SaPlayer):
    def __init__(self, id, name='', color=0xffffffff):
        super().__init__()
        self.peer = None
        self.id = id
        self.name = name
        self.color = color
        self.score = 0
        self.ping = 0
        self.in_world = False
        self.in_fov = False
        self.team = None
        self.key_data = KeyData(0, 0, 0)
        self.surf_data = None
        self.anim_data = None
        self.player_pool = None # reference to player pool; it is probably a shared pool
        self.vehicle_pool = None # reference to vehicle pool; it is probably a shared pool
        self.logged_in_rcon = False
    
    def __str__(self):
        return pretty_format(self, 0)
