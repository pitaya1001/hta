import enum
import struct
import socket

from .bitstream import *
from .common import *

'''
See /examples/query.py

Examples:

q = Query.decode_request(data) ; decodes any query request packet(e.g. request packets sent from the client)
q = Query.decode_response(data) ; decode any query response packet(e.g. response packets sent from the server)

# Sending request queries as a client
SERVER_ADDR = ('127.0.0.1', 7777)
client_socket.sendto(PingQueryRequest(SERVER_ADDR[0], SERVER_ADDR[1], 12345).encode(), SERVER_ADDR)
client_socket.sendto(InfoQueryRequest(SERVER_ADDR[0], SERVER_ADDR[1]).encode(), SERVER_ADDR)
client_socket.sendto(RulesQueryRequest(SERVER_ADDR[0], SERVER_ADDR[1]).encode(), SERVER_ADDR)
client_socket.sendto(ClientsQueryRequest(SERVER_ADDR[0], SERVER_ADDR[1]).encode(), SERVER_ADDR)
client_socket.sendto(DetailedQueryRequest(SERVER_ADDR[0], SERVER_ADDR[1]).encode(), SERVER_ADDR)
client_socket.sendto(RconQueryRequest(SERVER_ADDR[0], SERVER_ADDR[1], password='changeme', command='varlist').encode(), SERVER_ADDR)

# Decoding query responses from the server
while True:
    data, addr = client_socket.recvfrom(4096)
    print(Query.decode_response(data))


number in parenthesis is how many bytes it uses

all values follow little endian byte order, except ip and port

query packet structure: b'SAMP'(4) + IPV4(4) + PORT(2) + ID(1) + payload(varies)
Note: the PORT does not need to be the port of the server nor the client's. It may be any 16-bit value
the server should send back to the peer whatever is in IPV4 and PORT


CLIENT QUERY REQUESTS
 ID        NAME     PAYLOAD
 ord('p')  PING     timestamp(4)
 ord('i')  INFO     no payload
 ord('r')  RULES    no payload
 ord('c')  CLIENTS  no payload
 ord('d')  DETAILED no payload
 ord('x')  RCON     rcon_password_length(2) + rcon_password(rcon_password_length) + rcon_command_length(2) + rcon_command(rcon_command_length)

SERVER QUERY RESPONSES
 ID        NAME     PAYLOAD
 ord('p')  PING     timestamp(4) ; just send back whatever was received from the client
 ord('i')  INFO     has_password(1) + player_count(2) + max_player_count(2) + hostname_length(32) + hostname(hostname_length) + gamemode_length(32) + gamemode(gamemode_length) + language_length(32) + language(language_length)
 ord('r')  RULES    rule_count(2) + [rule_length(1) + rule(rule_length) + value_length(1) + value(value_length)] * rule_count
 ord('c')  CLIENTS  client_count(2) + [player_name_length(1) + player_name(player_name_length) + score(4)] * client_count
 ord('d')  DETAILED player_count(2) + [player_id(1) + player_name_length(1) + player_name(player_name_length) + score(4) + ping(4)] * player_count
 ord('x')  RCON     rcon_response_length(2) + rcon_response(rcon_response_length)

NOTES
a query packet must contain b"SAMP" at the start, otherwise it is ignored.
additional bytes at the end of a query packet are ignored. The packet is processed as usual.
if too many query response packets are sent to the samp server browser it crashes after a few seconds.
the server may take as much time as it likes to send the query response back to the client, it will hapily receive it even after minutes.
if a ping with a timestamp in the future is sent to the samp server browser, it shows an integer overflow exception in a message dialog
'''

QUERY_HEADER_SIZE = 4 + 4 + 2 + 1 # b'SAMP'(4) + ipv4(4) + port(2) + id(1)
QUERY_ID_OFFSET = 10 # 4 + 4 + 2

class QUERY(enum.IntEnum):
    PING     = ord('p')
    INFO     = ord('i')
    RULES    = ord('r')
    CLIENTS  = ord('c')
    DETAILED = ord('d')
    RCON     = ord('x')

class Query:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        
    def __str__(self):
        return pretty_format(self, skip_n=1)

    def encode_header(self):
        return b'SAMP' + socket.inet_aton(self.ip) \
                       + struct.pack('HB', self.port, self.id)

    # return id, ip, port
    @staticmethod
    def decode_header(data):
        magic, ip, port, id = struct.unpack_from('4s4sHB', data)
        return QUERY(id), socket.inet_ntoa(ip), port

    def encode(self):
        return self.encode_header() + self.encode_payload()
    
    '''
    Decodes any query request.
    e.g. q = Query.decode_request(data)
    '''
    @staticmethod
    def decode_request(data):
        id, ip, port = Query.decode_header(data)
        return id.decode_request_payload(data[QUERY_HEADER_SIZE:], ip, port)

    '''
    Decodes any query response.
    e.g. q = Query.decode_response(data)
    '''
    @staticmethod
    def decode_response(data):
        id, ip, port = Query.decode_header(data)
        return id.decode_response_payload(data[QUERY_HEADER_SIZE:], ip, port)

class PingQueryRequest(Query):
    def __init__(self, ip, port, time):
        super().__init__(QUERY.PING, ip, port)
        self.time = time # timestamp in ms; same as raknet.get_time()
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return PingQueryRequest.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        return struct.pack('I', self.time)

    @staticmethod
    def decode_payload(data, ip, port):
        ping_time, = struct.unpack_from('I', data)
        return PingQueryRequest(ip, port, ping_time)
QUERY.PING.decode_request_payload = PingQueryRequest.decode_payload

class PingQueryResponse(Query):
    def __init__(self, ip, port, time):
        super().__init__(QUERY.PING, ip, port)
        self.time = time # timestamp in ms; same as raknet.get_time()
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return PingQueryResponse.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        return struct.pack('I', self.time)

    @staticmethod
    def decode_payload(data, ip, port):
        ping_time, = struct.unpack_from('I', data)
        return PingQueryResponse(ip, port, ping_time)
QUERY.PING.decode_response_payload = PingQueryResponse.decode_payload

class InfoQueryRequest(Query):
    def __init__(self, ip, port):
        super().__init__(QUERY.INFO, ip, port)
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return InfoQueryRequest.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data, ip, port):
        return InfoQueryRequest(ip, port)
QUERY.INFO.decode_request_payload = InfoQueryRequest.decode_payload

class InfoQueryResponse(Query):
    def __init__(self, ip, port, has_password, player_count, max_player_count, hostname, gamemode, language):
        super().__init__(QUERY.INFO, ip, port)
        self.has_password = bool(has_password)
        self.player_count = player_count
        self.max_player_count = max_player_count
        self.hostname = hostname
        self.gamemode = gamemode
        self.language = language
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return InfoQueryResponse.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        bs = Bitstream(capacity=128)
        bs.write_u8(self.has_password)
        bs.write_u16(self.player_count)
        bs.write_u16(self.max_player_count)
        bs.write_dynamic_str32(self.hostname)
        bs.write_dynamic_str32(self.gamemode)
        bs.write_dynamic_str32(self.language)
        return bs.to_bytes()

    @staticmethod
    def decode_payload(data, ip, port):
        bs = Bitstream(data)
        has_password = bs.read_u8()
        player_count = bs.read_u16()
        max_player_count = bs.read_u16()
        hostname = bs.read_dynamic_str32()
        gamemode = bs.read_dynamic_str32()
        language = bs.read_dynamic_str32()
        return InfoQueryResponse(ip, port, has_password, player_count, max_player_count, hostname, gamemode, language)
QUERY.INFO.decode_response_payload = InfoQueryResponse.decode_payload

class RulesQueryRequest(Query):
    def __init__(self, ip, port):
        super().__init__(QUERY.RULES, ip, port)
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return RulesQueryRequest.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data, ip, port):
        return RulesQueryRequest(ip, port)
QUERY.RULES.decode_request_payload = RulesQueryRequest.decode_payload

class RulesQueryResponse(Query):
    def __init__(self, ip, port, rules):
        super().__init__(QUERY.RULES, ip, port)
        self.rules = rules # {rule: value, ...} or [(rule, value), ...]
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return RulesQueryResponse.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        bs = Bitstream(capacity=256)
        bs.write_u16(len(self.rules))
        if isinstance(self.rules, dict):
            for rule, value in self.rules.items():
                bs.write_dynamic_str8(rule)
                bs.write_dynamic_str8(value)
        if isinstance(self.rules, list):
            for rule, value in self.rules:
                bs.write_dynamic_str8(rule)
                bs.write_dynamic_str8(value)
        
        return bs.to_bytes()

    @staticmethod
    def decode_payload(data, ip, port):
        bs = Bitstream(data)
        rule_count = bs.read_u16()
        rules = [(bs.read_dynamic_str8(), bs.read_dynamic_str8()) for _ in range(rule_count)]
        return RulesQueryResponse(ip, port, rules)
QUERY.RULES.decode_response_payload = RulesQueryResponse.decode_payload

class ClientsQueryRequest(Query):
    def __init__(self, ip, port):
        super().__init__(QUERY.CLIENTS, ip, port)
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return ClientsQueryRequest.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data, ip, port):
        return ClientsQueryRequest(ip, port)
QUERY.CLIENTS.decode_request_payload = ClientsQueryRequest.decode_payload

class ClientsQueryResponse(Query):
    def __init__(self, ip, port, clients):
        super().__init__(QUERY.CLIENTS, ip, port)
        self.clients = clients # {name: score, ...} or [(name, score), ...]
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return ClientsQueryResponse.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        bs = Bitstream(capacity=512)
        bs.write_u16(len(self.clients))
        if isinstance(self.clients, dict):
            for name, score in self.clients.items():
                bs.write_dynamic_str8(name)
                bs.write_u32(score)
        elif isinstance(self.clients, list):
            for name, score in self.clients:
                bs.write_dynamic_str8(name)
                bs.write_u32(score)
        return bs.to_bytes()

    @staticmethod
    def decode_payload(data, ip, port):
        bs = Bitstream(data)
        client_count = bs.read_u16()
        clients = [(bs.read_dynamic_str8(), bs.read_u32()) for _ in range(client_count)]
        return ClientsQueryResponse(ip, port, clients)
QUERY.CLIENTS.decode_response_payload = ClientsQueryResponse.decode_payload

class DetailedQueryRequest(Query):
    def __init__(self, ip, port):
        super().__init__(QUERY.DETAILED, ip, port)
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return DetailedQueryRequest.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data, ip, port):
        return DetailedQueryRequest(ip, port)
QUERY.DETAILED.decode_request_payload = DetailedQueryRequest.decode_payload

class DetailedQueryResponse(Query):
    def __init__(self, ip, port, players):
        super().__init__(QUERY.DETAILED, ip, port)
        self.players = players # {id: (name, score, ping), ...} or [(id, name, score, ping), ...]
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return DetailedQueryResponse.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        bs = Bitstream(capacity=512)
        bs.write_u16(len(self.players))
        if isinstance(self.players, dict):
            for id, (name, score, ping) in self.players.items():
                bs.write_u8(id)
                bs.write_dynamic_str8(name)
                bs.write_u32(score)
                bs.write_u32(ping)
        elif isinstance(self.players, list):
            for id, name, score, ping in self.players:
                bs.write_u8(id)
                bs.write_dynamic_str8(name)
                bs.write_u32(score)
                bs.write_u32(ping)
        return bs.to_bytes()

    @staticmethod
    def decode_payload(data, ip, port):
        bs = Bitstream(data)
        player_count = bs.read_u16()
        players = [(bs.read_u8(), bs.read_dynamic_str8(), bs.read_u32(), bs.read_u32()) for _ in range(player_count)]
        return DetailedQueryResponse(ip, port, players)
QUERY.DETAILED.decode_response_payload = DetailedQueryResponse.decode_payload

class RconQueryRequest(Query):
    def __init__(self, ip, port, password, command):
        super().__init__(QUERY.RCON, ip, port)
        self.password = password
        self.command = command
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return RconQueryRequest.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        bs = Bitstream(capacity=128)
        bs.write_dynamic_str16(self.password)
        bs.write_dynamic_str16(self.command)
        return bs.to_bytes()

    @staticmethod
    def decode_payload(data, ip, port):
        bs = Bitstream(data)
        password = bs.read_dynamic_str16()
        command = bs.read_dynamic_str16()
        return RconQueryRequest(ip, port, password, command)
QUERY.RCON.decode_request_payload = RconQueryRequest.decode_payload

class RconQueryResponse(Query):
    def __init__(self, ip, port, response):
        super().__init__(QUERY.RCON, ip, port)
        self.response = response
        
    @staticmethod
    def decode(data):
        id, ip, port = Query.decode_header(data)
        return RconQueryResponse.decode_payload(data[QUERY_HEADER_SIZE:], ip, port)

    def encode_payload(self):
        bs = Bitstream(capacity=128)
        bs.write_dynamic_str16(self.response)
        return bs.to_bytes()

    @staticmethod
    def decode_payload(data, ip, port):
        bs = Bitstream(data)
        response = bs.read_dynamic_str16()
        return RconQueryResponse(ip, port, response)
QUERY.RCON.decode_response_payload = RconQueryResponse.decode_payload
