from sa.player import Player as SaPlayer

class Player(SaPlayer):
    def __init__(self, id, name=None, color=0xffffffff):
        super().__init__()
        self.id = id
        self.name = name
        self.color = color
        self.score = 0
        self.ping = 0
        self.in_world = False
        self.in_fov = False
        self.team = None
