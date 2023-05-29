import socket
import asyncio
import struct
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
        #print('Client.on_connected_message', message, peer)
        if message.id == MSG.CONNECTION_REQUEST_ACCEPTED:
            self.id = message.player_id # save the id the server assigned to us
            peer.push_message(ClientJoin(CLIENT_VERSION_37, 1, self.name, (message.cookie ^ CLIENT_VERSION_37), self.gpci, self.version))
            #if not self.connected:
            peer.push_message(NewIncomingConnection(ip=peer.addr[0], port=peer.addr[1]))
                #self.connected = True
        if message.id == MSG.AUTH_KEY:
            server_key = bytes(message.key[:-1])
            client_key = auth_keys[server_key]
            peer.push_message(AuthKey(client_key))
    
    async def retry_connection_cookie(self, delay):
        await asyncio.sleep(delay)
        self.server_peer.send_unconnected_message(OpenConnectionRequest(self.server_cookie))
        self.connection_cookie_task = asyncio.get_running_loop().create_task(self.retry_connection_cookie(random.uniform(1.0, 3.0)))
    
    def on_unconnected_message(self, message, peer):
        #print('Client.on_unconnected_message', message, peer)
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
