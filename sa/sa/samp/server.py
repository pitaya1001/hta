'''
There is one player pool, one vehicle pool.
Stream distance is the same for everyone
'''

import socket
import asyncio
import os # urandom
import traceback
import time
import threading

from .raknet import *
from .rpcs import *
from .common import *
from .player import *
from .gpci import validate_gpci
from .auth_keys import auth_keys
from .encryption import decrypt_buffer
from .query import *

from .spots import *

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

        self.rcon_password = 'changeme'

        # actual max player count used to limit how many players may join
        self.max_player_count = (MAX_PLAYER_ID + 1)
        
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
        # None = do NOT fake it; not None = do fake it
        # e.g. server.fake_player_list = {'alice': 100, 'zebra':999}
        self.fake_player_list = None
        
        # fake detailed player list(overrides real variable in query requests)
        # None = do NOT fake it; not None = do fake it 
        # e.g. server.fake_detailed_player_list = {0: ('alice', 100, 12), 1: ('zebra', 999, 15)}
        self.fake_detailed_player_list = None

        self.message_callbacks = [] # callback(message, internal_packet, peer, server)
        self.post_message_callbacks = [] # callback(message, internal_packet, peer, server)

        self.cached_info_query_payload = None
        self.cached_rules_query_payload = None
        self.cached_clients_query_payload = None
        self.cached_detailed_query_payload = None
        self.cached_bad_rcon_password_query_payload = RconQueryResponse(None, None, 'Invalid RCON password.').encode_payload()
        self.query_cache_ttl = 15 # in seconds
        self.cache_query_payloads()

        self.player_stream_distance = 200.0

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

    def update_player_streams_naive(self):
        '''
        naive implementation
        iterate all players and calculate the distance to all other players.
        '''
        for peer in self.peers.values():
            player = peer.player
            updated_players_in_fov = [other_peer.player for other_peer in self.peers.values() if other_peer != peer and player.pos.distance2d(other_peer.player.pos) <= self.player_stream_distance]
            for new_player in [p for p in updated_players_in_fov if p not in player.players_in_fov]:
                peer.push_message(StartPlayerStream(new_player.id, team=new_player.team, pos=new_player.pos, color=new_player.color))
            for old_player in [p for p in player.players_in_fov if p not in updated_players_in_fov]:
                peer.push_message(StopPlayerStream(old_player.id))
            player.players_in_fov = updated_players_in_fov
    
    #def update_player_streams_grid(self):
    #    '''
    #    grid implementation
    #    cell size is at least the stream distance
    #    First, iterate all players putting them into cells on the grid
    #    Then, iterate again, and calculate the distance to players only in
    #    the current and adjacent cells.
    #    '''
    #    for peer in self.peers.values():
    #        player = peer.player

    def stream_thread(self):
        '''
        determine if a player should start/stop being streamed to other players
        i.e. this functions sends the StartPlayerStream and StopPlayerStream rpcs
        A good analogy is the following: imagine a 2D plane full of moving circles,
        whenever two circles overlap, both receive a StartPlayerStream RPC saying that
        a new circle is overlapping them. When the opposite occurs(i.e. they are
        no longer overlapping), both receive a StopPlayerStream RPC.
        '''
        try:
            while True:
                time.sleep(1)
                self.update_player_streams_naive()
        except:
            log(traceback.format_exc())

    def logic_thread(self):
        try:
            while True:
                time.sleep(0.1)
                for peer in self.peers.values():
                    player = peer.player
                    #if player.pos is not None:
                    #    player.pos.x+=0.1
                    #    print(player.pos)
                    for near_player in player.players_in_fov:
                        vehicle = near_player.vehicle
                        if vehicle: # in vehicle
                            if near_player.seat_id == 0: # driver
                                peer.push_message(DriverSync(vehicle.id, near_player.id, pos=vehicle.pos, dir=vehicle.dir, vehicle_health=vehicle.health, driver_health=near_player.health, driver_armor=near_player.armor))
                            else: # passenger
                                peer.push_message(PassengerSync(vehicle.id, near_player.id, pos=near_player.pos, health=near_player.health, armor=near_player.armor, seat_id=near_player.seat_id))
                        else: # on foot
                            peer.push_message(PlayerSync(near_player.id, pos=near_player.pos, dir=near_player.dir, health=near_player.health, armor=near_player.armor))
        except:
            log(traceback.format_exc())

    def get_lowest_unused_id(self):
        return next(id for id, player in enumerate(self.player_pool) if player is None)

    def get_highest_unused_id(self):
        return next(id for id, player in enumerate(reversed(self.player_pool)) if player is None)

    def get_random_unused_id(self):
        return random.choice(id for id, player in enumerate(self.player_pool) if player is None)

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

        threading.Thread(target=self.logic_thread, daemon=True).start()
        threading.Thread(target=self.stream_thread, daemon=True).start()

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
        q = InfoQueryResponse(None, None, has_password,
                    self.get_query_player_count(),
                    self.get_query_max_player_count(),
                    self.hostname, self.gamemode, self.language)
        self.cached_info_query_payload = q.encode_payload()

    def cache_rules_query_payload(self):
        q = RulesQueryResponse(None, None, self.rules)
        self.cached_rules_query_payload = q.encode_payload()

    def cache_clients_query_payload(self):
        if self.fake_player_list is not None:
            clients = self.fake_player_list
        else:
            clients = [(peer.player.name, peer.player.score) for peer in self.peers.values()]
        q = ClientsQueryResponse(None, None, clients)
        self.cached_clients_query_payload = q.encode_payload()

    def cache_detailed_query_payload(self):
        if self.fake_detailed_player_list is not None:
            players = self.fake_detailed_player_list
        else:
            players = [(peer.player.id, peer.player.name, peer.player.score, peer.player.ping) for peer in self.peers.values()]
        q = DetailedQueryResponse(None, None, players)
        self.cached_detailed_query_payload = q.encode_payload()

    def cache_query_payloads(self):
        self.cache_info_query_payload()
        self.cache_rules_query_payload()
        self.cache_clients_query_payload()
        self.cache_detailed_query_payload()

    async def cache_query_payloads_loop(self):
        try:
            while True:
                await asyncio.sleep(self.query_cache_ttl)
                self.cache_query_payloads()
        except asyncio.exceptions.CancelledError: pass
        except: log(traceback.format_exc())

    def handle_rcon_command(self, command):
        cmd = command.split()[0]
        arg = command[len(cmd):].strip()
        match cmd:
            case 'hostname':
                self.hostname = arg
                self.cache_info_query_payload()
            case 'gamemodetext':
                self.gamemode = arg
                self.cache_info_query_payload()
            case 'language':
                self.language = arg
                self.cache_info_query_payload()
            case 'say':
                self.push_message_to_all(ChatMessage(f'* Admin: {arg}', color=0x2587ceaa))
            case 'echo':
                print(arg)
            case 'gravity':
                try:
                    gravity = float(arg)
                except ValueError:
                    return
                self.push_message_to_all(SetGravity(gravity))
            case 'weather':
                try:
                    weather = int(arg)
                except ValueError:
                    return
                if 0 <= weather <= 0xff:
                    self.push_message_to_all(SetWeather(weather))
            case 'weburl':
                self.rules['weburl'] = arg
                self.cache_rules_query_payload()
            case 'password':
                self.password = arg
                self.cache_info_query_payload()
            case 'rcon_password':
                self.rcon_password = arg
            case 'players':
                lines = ['ID\tName\tPing\tIP']
                for (ip, port), peer in self.peers.items():
                    player = peer.player
                    lines.append(f'{player.id}\t{player.name}\t{player.ping}\t{ip}')
                return lines
            case 'cmdlist':
                cmdlist = ['echo', 'exec', 'cmdlist', 'varlist', 'exit', 'kick', 'ban', 'gmx', 'changemode', 'say', 'reloadbans', 'reloadlog', 'players', 'banip', 'unbanip', 'gravity', 'weather', 'loadfs', 'unloadfs', 'reloadfs']
                lines = ['Console commands'] + [cmd for cmd in cmdlist] + ['']
                return lines
            case 'varlist':
                return [
                    'Console Variables:',
                    f'  language\t= "{self.language}"  (string)',
                    f'  hostname\t= "{self.hostname}"  (string)',
                    f'  maxplayers\t= {self.max_player_count}  (int) (read-only)',
                    f'  password\t= "{self.password}"  (string)',
                    f'  port\t\t= {self.addr[1]}  (int) (read-only)',
                    f'  rcon_password\t= "{self.rcon_password}"  (string)',
                    '',
                ]

    def handle_query(self, data, addr):
        match data[QUERY_ID_OFFSET]: # query id
            case QUERY.PING: output = data[:QUERY_HEADER_SIZE+4] # just send back whatever ping time we received
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
            case QUERY.DETAILED: output = data[:QUERY_HEADER_SIZE] + self.cached_detailed_query_payload
            case QUERY.RCON:
                try:
                    q = RconQueryRequest.decode(data)
                except: # bad query
                    return
                if q.password != self.rcon_password:
                    output = data[:QUERY_HEADER_SIZE] + self.cached_bad_rcon_password_query_payload
                else:
                    if (lines := self.handle_rcon_command(q.command)) is not None:
                        for line in lines:
                            q = RconQueryResponse(q.ip, q.port, line)
                            self.socket.sendto(q.encode(), addr)
                    return
        self.socket.sendto(output, addr)

    def add_peer(self, addr, addrs):
        peer = Peer(addr, is_server_peer=False, sendto=lambda buffer: self.socket.sendto(buffer, addr))
        peer.connected = True
        peer.expected_client_key = None
        peer.connected_message_callbacks.append(self.on_connected_message)

        player = Player()
        player.id = self.get_unused_id(self)
        player.player_pool = self.player_pool
        player.vehicle_pool = self.vehicle_pool
        player.peer = peer
        self.player_pool[player.id] = player
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
            allow_weapons = True,
            limit_global_chat_radius = False,
            global_chat_radius = 0,
            stunt_bonus = True,
            name_tag_draw_distance = 200.0,
            disable_enter_exits = True,
            name_tag_los = True,
            manual_vehicle_engine_and_light = 0,
            spawns_available = 0,
            player_id = peer.player.id,
            show_player_tags = True,
            show_player_markers = True,
            world_time = 12,
            weather = 0,
            gravity = DEFAULT_GRAVITY,
            lan_mode = False,
            death_drop_money = False,
            instagib = False,
            onfoot_rate = 40,
            incar_rate = 40,
            weapon_rate = 40,
            multiplier = 10,
            lag_comp = True,
            hostname = self.hostname,
            vehicle_models = [0] * 212,
            vehicle_friendly_fire = True
        )
        peer.push_message(rpc)

    def on_connected_message(self, message, internal_packet, peer):
        for callback in self.message_callbacks:
            if callback(message, internal_packet, peer, self) is True:
                return

        if message.id == MSG.PLAYER_SYNC:
            player = peer.player
            player.vehicle = None
            player.seat_id = None
            player.pos = message.pos
            player.dir = message.dir
            player.health = message.health
            player.armor = message.armor
            player.weapon_id = message.weapon_id
            player.key_data = message.key_data
            player.anim_data = message.anim_data
        elif message.id == MSG.DRIVER_SYNC:
            player = peer.player
            vehicle_id = message.vehicle_id
            
            if vehicle_id > MAX_VEHICLE_ID:
                return
            
            vehicle = player.vehicle_pool[vehicle_id]
            
            if not vehicle:
                return
            
            vehicle.pos = message.pos
            vehicle.dir = message.dir
            vehicle.health = message.vehicle_health
            
            player.vehicle = vehicle
            player.seat_id = 0
            player.pos = message.pos
            player.dir = message.dir
            player.health = message.driver_health
            player.armor = message.driver_armor
            player.weapon_id = message.driver_weapon_id
            player.key_data = message.key_data
        elif message.id == MSG.PASSENGER_SYNC:
            player = peer.player
            vehicle_id = message.vehicle_id
            
            if vehicle_id > MAX_VEHICLE_ID:
                return
            
            vehicle = player.vehicle_pool[vehicle_id]
            
            if not vehicle:
                return
            
            vehicle.pos = message.pos
            
            player.vehicle = vehicle
            player.seat_id = message.seat_id
            player.pos = message.pos
            player.health = message.passenger_health
            player.armor = message.passenger_armor
            player.weapon_id = message.passenger_weapon_id
            player.key_data = message.key_data
        elif message.id == MSG.SPECTATOR_SYNC:
            ss = message
            player = peer.player
            player.pos = ss.pos
            player.key_data = ss.key_data
        elif message.id == MSG.RPC:
            rpc = message
            id = rpc.rpc_id
            if id == RPC.PLAYER_CHAT_MESSAGE:
                self.push_message_to_all(PlayerChatMessage(peer.player.id, rpc.message))
            elif id == RPC.REQUEST_SPAWN:
                peer.player.waiting_request_spawn_response = True
                peer.push_message(RequestSpawnResponse(REQUEST_SPAWN.ACCEPT))
                peer.player.waiting_request_spawn_response = False
            elif id == RPC.CLIENT_JOIN:
                if validate_gpci(rpc.gpci):
                    player = peer.player
                    player.name = rpc.name

                    self.init_game_for_player(peer)
                    peer.push_message(SetSpawnInfo(pos=SPOT.GROVE))
                    peer.push_message(RequestSpawnResponse(REQUEST_SPAWN.FORCE))
                    player.pos = SPOT.GROVE

                    # tell this peer about connected players
                    for other_peer in self.peers.values():
                        if other_peer == peer:
                            continue
                        peer.push_message(ServerJoin(other_peer.player.id, other_peer.player.name, other_peer.player.color))

                    # tell other peers this peer connected
                    self.push_message_to_others(peer, ServerJoin(player.id, peer.player.name, peer.player.color))
                    #self.push_message_to_others(peer, StartPlayerStream(player.id,pos=player.pos))
                else:
                    # todo: kick player?
                    pass
                    del self.peers[peer.addr]
                    return
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
        elif message.id == MSG.RCON_COMMAND:
            if peer.player.logged_in_rcon:
                lines = self.handle_rcon_command(message.command)
                
                if not lines:
                    return
                
                for line in lines: # rcon response
                    peer.push_message(ChatMessage(line, color=0xffffffff))
            else:
                cmd = message.command.split()[0]
                arg = message.command[len(cmd):].strip()
                
                if cmd.lower() != 'login':
                    return
                
                if arg != self.rcon_password:
                    peer.push_message(ChatMessage('SERVER: Bad admin password. Repeated attempts will get you banned.', color=0xffffffff))
                else:
                    peer.player.logged_in_rcon = True
                    peer.push_message(ChatMessage('SERVER: You are logged in as admin.', color=0xffffffff))
        
        for callback in self.post_message_callbacks:
            if callback(message, internal_packet, peer, self) is True:
                return
