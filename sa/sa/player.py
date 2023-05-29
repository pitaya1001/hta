class Player:
    def __init__(self):
        self.health = None
        self.armor = None
        self.money = None
        self.pos = None # player position as Vec3
        self.dir = None # player direction as Quat
        self.cam_pos = None # camera position as Vec3
        self.cam_dir = None # camera direction as Vec3(Euler angles)
        self.skin_id = None
        self.weapon_id = None
        self.fighting_style = None
        self.skill_level = None
        self.vehicle = None # the vehicle the player is inside(as driver or passenger), or None if not in a vehicle
        self.seat_id = None # the seat(0=driver, 1=front passenger, 2=back left passenger, 3=back right passenger, 4+=other seats(e.g. coach)) if in a vehicle, or None if not in a vehicle
