import socket
import asyncio
import traceback
import enum
import random
import string

from .rpcs import *
from .player import Player
from .encryption import encrypt_buffer
from .raknet import *
from .gpci import generate_random_gpci
from .common import *
from .auth_keys import auth_keys
from .vehicle import *

class CLIENT_STATE(enum.IntEnum):
    UNCONNECTED = enum.auto()
    COOKIE = enum.auto(),
    REQUEST = enum.auto(),
    CONNECTED = enum.auto(),

class Client(Player):
    def __init__(self, server_addr=None, name=''.join(random.choices(string.ascii_uppercase, k=MAX_PLAYER_NAME_LENGTH)), gpci=generate_random_gpci(), version='0.3.7-R5', server_password=''):
        super().__init__(id=None, name=name)
        self.server_addr = server_addr
        self.gpci = gpci
        self.version = version
        self.server_password = server_password

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0)) # bind to all interfaces on a OS assigned port

        self.server_peer = Peer(server_addr, is_server_peer=True, sendto=self.sendto_encrypted)
        self.server_peer.connected_message_callbacks.append(self.on_connected_message)
        self.server_peer.unconnected_message_callbacks.append(self.on_unconnected_message)

        self.message_callbacks = [] # callback(message, internal_packet, peer, client)

        self.connected = False
        self.state = CLIENT_STATE.UNCONNECTED

        self.server_cookie = MAGIC_COOKIE
        self.connection_cookie_task = None

        self.recv_loop_task = asyncio.get_running_loop().create_task(self.recv_loop())

        # attributes
        self.player_pool = [None] * (MAX_PLAYER_ID + 1) # useful for lookup(O(1) time) by player id
        self.players = [] # useful for quickly iterating connected players
        self.players_in_fov = [] # useful for quickly iterating over players in our field of view

        self.vehicle_pool = [None] * (MAX_VEHICLE_ID + 1) # useful for lookup(O(1) time) by vehicle id
        self.vehicles_in_fov = [] # useful for quickly iterating over vehicles in our field of view

        self.dialog = None # the dialog visible on the screen, or None if there is no dialog

        self.textdraw_pool = [None] * (MAX_TEXTDRAW_ID + 1) # useful for lookup(O(1) time) by textdraw id
        self.textdraws = [] # useful for quickly iterating over present textdraws

    def sendto_encrypted(self, buffer):
        buffer = encrypt_buffer(buffer, self.server_addr[1])
        self.socket.sendto(buffer, self.server_addr)

    async def start(self):
        if self.state != CLIENT_STATE.UNCONNECTED:
            return

        self.connection_cookie_task = asyncio.get_running_loop().create_task(self.retry_connection_cookie(delay=0))

    def update(self):
        self.server_peer.update()

    async def recv_loop(self):
        try:
            loop = asyncio.get_running_loop()
            while True: # receive UDP packet
                data, addr = await loop.sock_recvfrom(self.socket, 2**16)
                if addr == self.server_addr: # make sure the packet came from the server
                    self.server_peer.handle_packet(data)
        except asyncio.exceptions.CancelledError:
            pass
        except:
            log(traceback.format_exc())

    def on_connected_message(self, message, internal_packet, peer):
        for callback in self.message_callbacks:
            if callback(message, internal_packet, peer, self) is True:
                break

        if message.id == MSG.PLAYER_SYNC:
            player_id = message.player_id
            
            if player_id > MAX_PLAYER_ID:
                return
                
            player = self.player_pool[player_id]
            
            if not player:
                return
                
            # update attributes
            player.pos = message.pos
            player.health = message.health
            player.armor = message.armor
            player.weapon_id = message.weapon_id
            #player.vehicle = player.seat_id = None
        elif message.id == MSG.DRIVER_SYNC:
            vehicle_id = message.vehicle_id
            driver_id = message.driver_id

            if (
                vehicle_id > MAX_VEHICLE_ID
                or driver_id > MAX_PLAYER_ID
            ):
                return

            vehicle = self.vehicle_pool[vehicle_id]
            driver = self.player_pool[driver_id]
        
            if not vehicle or not driver:
                return
            
            # update driver attributes
            driver.pos = message.pos
            driver.vehicle = vehicle
            driver.seat_id = 0 # driver seat
            driver.health = message.driver_health
            driver.armor = message.driver_armor
            driver.weapon_id = message.driver_weapon_id
            # update vehicle attributes
            vehicle.driver_id = message.driver_id
            vehicle.pos = message.pos
            vehicle.health = message.vehicle_health
        elif message.id == MSG.PASSENGER_SYNC:
            passenger_id = message.vehicle_id
            vehicle_id = message.vehicle_id
            
            if (
                passenger_id > MAX_PLAYER_ID
                or vehicle_id > MAX_VEHICLE_ID
            ):
                return
            
            passenger = self.player_pool[passenger_id]
            vehicle = self.vehicle_pool[vehicle_id]
            
            if not passener or not vehicle:
                return
                
            # update passenger attributes
            passenger.pos = message.pos
            passenger.vehicle = vehicle
            passenger.seat_id = message.seat_id
            passenger.health = message.passenger_health
            passenger.armor = message.passenger_armor
        elif message.id == MSG.RPC:
            rpc = message
            if rpc.rpc_id == RPC.SERVER_JOIN:
                if rpc.player_id > MAX_PLAYER_ID:
                    return
                
                if self.player_pool[rpc.player_id]: # player with the same id already connected
                    log(f'warning: ServerJoin called twice without ServerQuit in between; player_id={rpc.player_id}')
                    return
                
                player = Player(rpc.player_id, rpc.player_name, rpc.color)
                
                self.player_pool[rpc.player_id] = player
                
                player.players_in_fov_index = None  # used for later removing from 'players_in_fov' list in O(1) time
                
                player.players_index = len(self.players) # used for later removing from 'players' list in O(1) time
                self.players.append(player)
            elif rpc.rpc_id == RPC.SERVER_QUIT:
                if rpc.player_id > MAX_PLAYER_ID:
                    return
                
                player = self.player_pool[rpc.player_id]
                
                if not player:
                    return
                
                self.player_pool[rpc.player_id] = None
                
                # remove from 'players' list in O(1) time
                self.players[-1].players_index = player.players_index # update index
                self.players[player.players_index] = self.players[-1]
                self.players.pop(-1)
                
                # remove from 'players_in_fov' list in O(1) time
                if player.players_in_fov_index: # if present in 'players_in_fov' list
                    self.players_in_fov[-1].players_in_fov_index = player.players_in_fov_index # update index
                    self.players_in_fov[player.players_in_fov_index] = self.players_in_fov[-1]
                    self.players_in_fov.pop(-1)
            elif rpc.rpc_id == RPC.ADD_PLAYER:
                if rpc.player_id > MAX_PLAYER_ID:
                    return
                    
                player = self.player_pool[rpc.player_id]
                
                if not player:
                    return 
                    
                # update attributes
                player.in_fov = True
                player.team = rpc.team
                player.skin_id = rpc.skin_id
                player.pos = rpc.pos
                player.color = rpc.color
                player.fighting_style = rpc.fighting_style
                player.skill_level = rpc.skill_level
                player.players_in_fov_index = len(self.players_in_fov) # used for later removing from 'players_in_fov' list in O(1) time
                self.players_in_fov.append(player)
            elif rpc.rpc_id == RPC.REMOVE_PLAYER:
                if rpc.player_id > MAX_PLAYER_ID:
                    return
                    
                player = self.player_pool[rpc.player_id]
                
                if (
                    not player
                    or player.players_in_fov_index is None
                ):
                    return
                
                player.in_fov = False
                
                # remove 'player' from 'players_in_fov' list in O(1) time
                self.players_in_fov[-1].players_in_fov_index = player.players_in_fov_index # update index
                self.players_in_fov[player.players_in_fov_index] = self.players_in_fov[-1]
                self.players_in_fov.pop(-1)
                player.players_in_fov_index = None
            elif rpc.rpc_id == RPC.ADD_VEHICLE:
                if rpc.vehicle_id > MAX_VEHICLE_ID:
                    return
                    
                vehicle = self.vehicle_pool[rpc.vehicle_id]
                
                if vehicle:
                    return
                 
                try:
                    vehicle = Vehicle(rpc.vehicle_id, rpc.model_id)
                except IndexError: # bad model id
                    return
                
                self.vehicle_pool[rpc.vehicle_id] = vehicle
                
                vehicle.vehicles_in_fov_index = len(self.vehicles_in_fov) # used for later removing from 'vehicles_in_fov' list in O(1) time
                self.vehicles_in_fov.append(vehicle)
            elif rpc.rpc_id == RPC.REMOVE_VEHICLE:
                if rpc.vehicle_id > MAX_VEHICLE_ID:
                    return
                    
                vehicle = self.vehicle_pool[rpc.vehicle_id]
                
                if not vehicle:
                    return
                    
                self.vehicle_pool[rpc.vehicle_id] = None
                
                # remove 'vehicle' from 'vehicles_in_fov' in O(1) time
                self.vehicles_in_fov[-1].vehicles_in_fov_index = vehicle.vehicles_in_fov_index # update index
                self.vehicles_in_fov[vehicle.vehicles_in_fov_index] = self.vehicles_in_fov[-1]
                self.vehicles_in_fov.pop(-1)
            elif rpc.rpc_id == RPC.SHOW_DIALOG:
                if rpc.dialog_id <= MAX_DIALOG_ID: # show dialog
                    self.dialog = rpc
                else: # close dialog
                    self.dialog = None
            elif rpc.rpc_id == RPC.SHOW_TEXTDRAW:
                if rpc.textdraw_id > MAX_TEXTDRAW_ID:
                    return
                    
                textdraw = self.textdraw_pool[rpc.textdraw_id]
                
                if not textdraw:
                    return
                
                self.textdraw_pool[rpc.textdraw_id] = rpc
                
                rpc.textdraws_index = len(self.textdraws) # used for later removing from 'textdraws' list in O(1) time
                self.textdraws.append(rpc)
            elif rpc.rpc_id == RPC.HIDE_TEXTDRAW:
                if rpc.textdraw_id > MAX_TEXTDRAW_ID:
                    return
                    
                textdraw = self.textdraw_pool[rpc.textdraw_id]
                
                if not textdraw:
                    return
                
                self.textdraw_pool[rpc.textdraw_id] = None
                
                # remove from 'textdraws' list in O(1) time
                self.textdraws[-1].textdraws_index = textdraw.textdraws_index # update index
                self.textdraws[textdraw.textdraws_index] = self.textdraws[-1]
                self.textdraws.pop(-1)  
        elif message.id == MSG.CONNECTION_REQUEST_ACCEPTED:
            self.id = message.player_id # save the id the server assigned to us
            peer.push_message(ClientJoin(CLIENT_VERSION_37, 1, self.name, (message.cookie ^ CLIENT_VERSION_37), self.gpci, self.version))
            peer.push_message(NewIncomingConnection(ip=peer.addr[0], port=peer.addr[1]))
        elif message.id == MSG.AUTH_KEY:
            server_key = bytes(message.key[:-1])
            client_key = auth_keys[server_key]
            peer.push_message(AuthKey(client_key))

    async def retry_connection_cookie(self, delay):
        await asyncio.sleep(delay)
        self.server_peer.send_unconnected_message(OpenConnectionRequest(self.server_cookie))
        self.connection_cookie_task = asyncio.get_running_loop().create_task(self.retry_connection_cookie(random.uniform(1.0, 3.0)))

    def on_unconnected_message(self, message, peer):
        if message.id == MSG.OPEN_CONNECTION_COOKIE: # server sent us the encoded server cookie
            # calculate the secret cookie from it
            self.server_cookie = message.cookie ^ MAGIC_COOKIE

            if self.connection_cookie_task:
                self.connection_cookie_task.cancel()
            self.connection_cookie_task = asyncio.get_running_loop().create_task(self.retry_connection_cookie(delay=0))
        elif message.id == MSG.CONNECTION_BANNED:
            # oh no :(
            pass
        elif message.id == MSG.OPEN_CONNECTION_REPLY:
            if self.connection_cookie_task:
                self.connection_cookie_task.cancel()
                self.connection_cookie_task = None
            # nice, server granted us access
            # we are now a connected peer
            # Send connection request
            peer.push_message(ConnectionRequest(self.server_password))
