import socket
import asyncio
import os # urandom
import traceback
import time

from .raknet import *
from .rpcs import *
from .common import *
from .player import *
from .gpci import validate_gpci
from .auth_keys import auth_keys
from .encryption import decrypt_buffer
from .query import *

class Server:
    def __init__(self, addr=None):
        self.addr = addr
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.addr)
        
        self.max_connections_per_ip = 5
        self.ips = {}
        self.peers = {} # {addr: Peer, ...}
        
        self.query = True # If true, the server answers queries, otherwise it doesn't
        
        self.player_pool = [None] * (MAX_PLAYER_ID + 1) # useful for lookup(O(1) time) by player id
        
        self.vehicle_pool = [None] * (MAX_VEHICLE_ID + 1) # useful for lookup(O(1) time) by vehicle id
                
        # {rule: var, rule: var, ...} ; both are strings
        self.rules = {
            'lagcomp': 'On',
            'mapname': 'San Andreas',
            'version': '0.3.7',
            'weather': '11',
            'weburl': 'www.sa-mp.com',
            'worldtime': '08:00',
        }
        
        self.hostname = 'SA-MP 0.3 Server'
        self.gamemode = 'None'
        self.language = 'English'
        self.password = '' # if empty, server has no password
        self.max_player_count = (MAX_PLAYER_ID + 1) # actual max player count used to limit how many players may join
        
        self.rcon_password_bytes = b''
        
        # fake player count(overrides real value in query requests)
        # None = do NOT fake it ; answer queries with real value -> len(self.peers)
        # integer = do fake it
        # e.g. server.fake_player_count = 123
        self.fake_player_count = None
        
        # fake max player count(overrides real value in query requests)
        # None = do NOT fake it; anwer queries with real value -> self.max_player_count 
        # integer = do fake it
        # e.g. server_fake_max_player_count = 456
        self.fake_max_player_count = None
        
        # fake player list(overrides real variable in query requests)
        # None = do NOT fake it; answers quries with real variable -> self.cached_clients_query_payload
        # {name: score, name: score, ... } = do fake it ; name is string, score is int
        # e.g. server.fake_player_list = {'alice': 100, 'zebra': 999}
        self.fake_player_list = None
        
        # callbacks
        self.bad_rcon_password_callbacks = []
        
        self.message_callbacks = [] # callback(message, internal_packet, peer, server)
        
        self.cached_info_query_payload = None
        self.cached_rules_query_payload = None
        self.cached_clients_query_payload = None
        self.query_cache_ttl = 15 # in seconds
        self.cache_query_payloads()
        
        self.send_rate = 40
        self.logic_callbacks = []
        
        self.loop = asyncio.get_running_loop()
        
        self.raknet_cookie = None
        self.expected_raknet_cookie = None
        self.raknet_cookie_ttl = 60 # in seconds
        self.cached_open_connection_cookie = None
        self.cached_open_connection_reply = OpenConnectionReply().encode()
        self.generate_raknet_cookie()
        self.generate_raknet_cookie_loop_task = None
        
        self.token = int.from_bytes(os.urandom(4), 'little')
        
        self.ping_interval = 5 # in seconds
        self.ping_loop_task = None
        self.last_ping_t = time.time()
        
        # Default algorithms: Server.get_lowest_unused_id, Server.get_highest_unused_id, Server.get_random_unused_id
        # Alternatively you may asign your own function; it should return an integer and have only the self parameter.
        self.get_unused_id = Server.get_lowest_unused_id
        
        self.running = False
        
        self.last_logic_t = time.time()
        
        self.cached_scores_and_pings = None
        self.cached_scores_and_pings_ttl = 5 # in seconds
        self.cache_scores_and_pings()
    
    # push message to all peers
    def push_message_to_all(self, message, reliability=RELIABILITY.RELIABLE, priority=PRIORITY.HIGH, ordering_channel=None):
        for _, peer in self.peers.items():
            peer.push_message(message, reliability, priority, ordering_channel)
    
    # push message to all peers expect one(the excluded_peer)
    def push_message_to_others(self, excluded_peer, message, reliability=RELIABILITY.RELIABLE, priority=PRIORITY.HIGH, ordering_channel=None):
        for _, peer in self.peers.items():
            if peer != excluded_peer:
                peer.push_message(message, reliability, priority, ordering_channel)
    
    async def recv_loop(self):
        try:
            loop = asyncio.get_running_loop()
            while True: # receive UDP packet
                data, addr = await loop.sock_recvfrom(self.socket, 2**16)
                self.handle_packet(data, addr)
        except asyncio.exceptions.CancelledError: pass
        except: log(traceback.format_exc())
    
    def cache_scores_and_pings(self):
        players = []
        for peer in self.peers.values():
            player = peer.player
            players.append((player.id, player.score, player.ping))
        self.cached_scores_and_pings = RequestScoresAndPingsResponse(players).encode()
    
    async def cache_scores_and_pings_loop(self):
        try:
            while True:
                await asyncio.sleep(self.cached_scores_and_pings_ttl)
                self.cache_scores_and_pings()
        except asyncio.exceptions.CancelledError: pass
        except: log(traceback.format_exc())
    
    async def ping_loop(self):
        try:
            while True:
                await asyncio.sleep(self.ping_interval)
                self.last_ping_t = time.time()
                self.push_message_to_all(InternalPing(time=get_time()))
        except asyncio.exceptions.CancelledError: pass
        except: log(traceback.format_exc())
    
    def generate_raknet_cookie(self):
        self.raknet_cookie = int.from_bytes(os.urandom(2), 'little')
        self.expected_raknet_cookie = (self.raknet_cookie ^ MAGIC_COOKIE).to_bytes(2, 'little')
        self.cached_open_connection_cookie = OpenConnectionCookie(self.raknet_cookie).encode()
    
    async def generate_raknet_cookie_loop(self):
        try:
            while True:
                await asyncio.sleep(self.raknet_cookie_ttl)
                self.generate_raknet_cookie()
        except asyncio.exceptions.CancelledError: pass
        except: log(traceback.format_exc())
    
    def set_rcon_password(self, password):
        if type(password) == str:
            self.rcon_password_bytes = password.encode(SAMP_ENCODING)
        elif type(password) == bytes:
            self.rcon_password_bytes = password
        else:
            raise ValueError
    
    def update_logic(self):
        now = time.time()
        dt = now - self.last_logic_t
        self.last_logic_t = now
        
        #for callback in self.logic_callbacks:
        #    callback(dt)
        #
        #for peer in self.peers:
        #    player = peer.player
        #    if player.in_world:
        #        for player_in_fov in player.players_in_fov:
        #            #peer.push_message(OnFootSync(player_in_fov...))
    
    def get_lowest_unused_id(self):
        for i, player in enumerate(self.player_pool):
            if player == None:
                return i
    
    def get_highest_unused_id(self):
        for i, player in enumerate(reversed(self.player_pool)):
            if player == None:
                return i
    
    def get_random_unused_id(self):
        unused_ids = []
        for i, player in enumerate(self.player_pool):
            if player == None:
                unused_ids.append(i)
        random_index = random.randint(0,len(unused_id)-1)
        return unused_id[random_index]
    
    def kick_non_whitelisted_players(self):
        pass
    
    def update(self):
        #print(len(self.peers))
        for _,peer in self.peers.items():
            peer.update()
        
        #self.update_logic()
    
    
    async def start(self):
        if self.running:
            return
        
        self.recv_task = self.loop.create_task(self.recv_loop())
        
        self.generate_raknet_cookie_task = self.loop.create_task(self.generate_raknet_cookie_loop())
        
        self.cache_query_payloads_task = self.loop.create_task(self.cache_query_payloads_loop())
        
        self.ping_task = self.loop.create_task(self.ping_loop())
        
        self.cache_scores_and_pings_task = self.loop.create_task(self.cache_scores_and_pings_loop())
    
        self.running = True
    
    async def stop(self):
        if not self.running:
            return
        
        #self.clients.clear()
        
        #self.transport.close()
        
        self.socket.close()
        await self.recv_loop()
        
        self.generate_raknet_cookie_task.cancel()
        await self.generate_raknet_cookie_task
        
        self.cache_query_payloads_task.cancel()
        await self.cache_query_payloads_task
        
        self.ping_task.cancel()
        await self.ping_task
        
        self.cache_scores_and_pings_task.cancel()
        await self.cache_scores_and_pings_task
        
        self.running = False
        #self.logic_task.cancel()
        #await self.logic_task
    
    def get_query_player_count(self):
        return len(self.peers) if (self.fake_player_count is None) \
            else self.fake_player_count
    
    def get_query_max_player_count(self):
        return self.max_player_count if (self.fake_max_player_count is None) \
            else self.fake_max_player_count
    
    def cache_info_query_payload(self):
        has_password = len(self.password) > 0
        q = InfoQuery(None, None, has_password,
                    self.get_query_player_count(),
                    self.get_query_max_player_count(),
                    self.hostname, self.gamemode, self.language)
        self.cached_info_query_payload = q.encode_response_payload()
    
    def cache_rules_query_payload(self):
        q = RulesQuery(None, None, self.rules)
        self.cached_rules_query_payload = q.encode_response_payload()
    
    def cache_clients_query_payload(self):
        q = ClientsQuery(None, None)
        if self.fake_player_list:
            q.clients = self.fake_player_list
        else:
            q.clients = {}
            for _, peer in self.peers.items():
                player = peer.player
                q.clients[player.name] = player.score
        self.cached_clients_query_payload = q.encode_response_payload()
    
    def cache_query_payloads(self):
        self.cache_info_query_payload()
        self.cache_rules_query_payload()
        self.cache_clients_query_payload()
    
    async def cache_query_payloads_loop(self):
        try:
            while True:
                await asyncio.sleep(self.query_cache_ttl)
                self.cache_query_payloads()
        except asyncio.exceptions.CancelledError: pass
        except: log(traceback.format_exc())
    
    def handle_query(self, data, addr):
        match data[QUERY_ID_OFFSET]: # query id
            case QUERY.PING: output = data[:QUERY_HEADER_SIZE+4] # just send whatever ping time we received back
            case QUERY.INFO: output = data[:QUERY_HEADER_SIZE] + self.cached_info_query_payload
            case QUERY.RULES: output = data[:QUERY_HEADER_SIZE] + self.cached_rules_query_payload
            case QUERY.CLIENTS:
                # if we want to set a fake player count we cannot send the
                # player list because if we did the player count would be
                # the number of players in the list (this is the default
                # behavior in the samp server browser)
                if self.fake_player_count:
                    return
                output = data[:QUERY_HEADER_SIZE] + self.cached_clients_query_payload
        self.socket.sendto(output, addr)
    
    def add_peer(self, addr, addrs):
        peer = Peer(addr, is_server_peer=False, sendto=lambda buffer: self.socket.sendto(buffer, addr))
        peer.connected = True
        peer.expected_client_key = None
        peer.connected_message_callbacks.append(self.on_connected_message)
        
        id = self.get_unused_id(self)
        player = Player(id)
        player.peer = peer
        self.player_pool[id] = player
        peer.player = player
        
        self.peers[addr] = peer
        
        if addrs:
            addrs.append(addr)
        else:
            addrs = [addr]
        self.ips[addr[0]] = addrs
                    
    def handle_packet(self, data, addr):
        # if query packet, reply with cached response
        if data[:4] == b'SAMP' and self.query and len(data) >= QUERY_HEADER_SIZE:
            self.handle_query(data, addr)
            return
        
        data = decrypt_buffer(data, self.addr[1])
        
        # check addr
        try: # packet from connected peer
            peer = self.peers[addr]
            peer.handle_connected_packet(data)
        except KeyError: # packet from unconnected peer
            # check if server is full
            if len(self.peers) >= self.max_player_count:
                return
        
            # check if the same ip is trying to make multiple connection over the limit
            try:
                addrs = self.ips[addr[0]]
                if len(addrs) >= self.max_connections_per_ip:
                    return
            except:
                addrs = None
            
            # handle initial raknet open connection request using cached response
            if data[0] == MSG.OPEN_CONNECTION_REQUEST:
                if data[1:3] == self.expected_raknet_cookie: # challenge passed; grant access
                    output = self.cached_open_connection_reply
                    self.add_peer(addr, addrs)
                else: # wrong answer; try again
                    output = self.cached_open_connection_cookie
                self.socket.sendto(output, addr)
    
    def init_game_for_player(self, peer):
        rpc = InitGame(
            zone_names = 1,
            use_cj_walk = 0,
            allow_weapons = 1,
            limit_global_chat_radius = 0,
            global_chat_radius = 1000.0,
            stunt_bonus = 0,
            name_tag_draw_distance = 200.0,
            disable_enter_exits = 0,
            name_tag_los = 1,
            manual_vehicle_engine_and_light = 0,
            spawns_available = 0,
            player_id = peer.player.id,
            show_player_tags = 1,
            show_player_markers = 1,
            world_time = 12,
            weather = 0,
            gravity = DEFAULT_GRAVITY,
            lan_mode = 0,
            death_drop_money = 0,
            instagib = 0,
            onfoot_rate = 40,
            incar_rate = 40,
            weapon_rate = 40,
            multiplier = 10,
            lag_comp = 1,
            hostname = self.hostname,
            vehicle_models = [0] * 212,
            vehicle_friendly_fire = 1
        )
        peer.push_message(rpc)
    
    def on_connected_message(self, message, internal_packet, peer):
        for callback in self.message_callbacks:
            if callback(message, internal_packet, peer, self) == True:
                return
    
        if message.id == MSG.RPC:
            rpc = message
            id = rpc.rpc_id
            if id == RPC.PLAYER_CHAT_MESSAGE:
                self.push_message_to_all(PlayerChatMessage(peer.player.id, rpc.message))
            elif id == RPC.CLIENT_JOIN:
                if validate_gpci(rpc.gpci):
                    peer.player.name = rpc.name
                    
                    self.init_game_for_player(peer)
                    peer.push_message(SetSpawnInfo(pos=Vec3(0, 0, 2)))
                    peer.push_message(RequestSpawnResponse(REQUEST_SPAWN.FORCE))
                    
                    # tell this peer which players are connected
                    for _, p in self.peers.items():
                        if p != peer:
                            peer.push_message(ServerJoin(p.player.id, p.player.color, is_npc=False, player_name=p.player.name))
                    
                    # tell all peers a new player connected
                    self.push_message_to_others(peer, ServerJoin(peer.player.id, peer.player.name, peer.player.color, is_npc=False,))
                else:
                    # todo: kick player?
                    pass
            elif id == RPC.REQUEST_SCORES_AND_PINGS:
                peer.push_encoded_message(self.cached_scores_and_pings)
        elif message.id == MSG.CONNECTION_REQUEST:
            if self.password == message.password:
                random_index = random.randint(0, len(auth_keys)-1)
                server_key = list(auth_keys)[random_index]
                peer.expected_client_key = auth_keys[server_key]
                message = AuthKey(server_key + b'\0')
                peer.push_message(message)
            else:
                # bad password
                pass
        elif message.id == MSG.AUTH_KEY:
            if message.key == peer.expected_client_key:
                player = peer.player
                msg = ConnectionRequestAccepted(ip=peer.addr[0], port=peer.addr[1], player_id=player.id, cookie=self.token)
                peer.push_message(msg, RELIABILITY.RELIABLE, PRIORITY.SYSTEM)
        elif message.id == MSG.CONNECTED_PONG:
            ping = int((time.time() - self.last_ping_t) * 1000)
            if ping >= peer.player.ping:
                peer.player.ping = ping
    