import enum
import struct

from .common import *

'''
number in parenthesis is how many bytes is requires

all values follow little endian byte order, except ip and port

query packet structure: b'SAMP'(4) + IPV4(4) + PORT(2) + ID(1) + payload(?)

the server should send back to the peer whatever is in IPV4 and PORT

CLIENT QUERIES:
 ID        NAME     PAYLOAD
 ord('p')  PING     timestamp(4)
 ord('i')  INFO     no payload
 ord('r')  RULES    no payload
 ord('c')  CLIENTS  no payload
 ord('x')  RCON     rcon_password_length(2) + rcon_password(rcon_password_length) + rcon_command_length(2) + rcon_command(rcon_command_length)
 
SERVER RESPONSES:
 ID        NAME     PAYLOAD
 ord('p')  PING     timestamp(4) ; just send back whatever was received from the client
 ord('i')  INFO     has_password(1) + player_count(2) + max_player_count(2) + hostname_length(32) + hostname(hostname_length) + gamemode_length(32) + gamemode(gamemode_length) + language_length(32) + language(language_length)
 ord('r')  RULES    rule_count(2) + [rule_length(1) + rule(rule_length) + value_length(1) + value(value_length)] * rule_count
 ord('c')  CLIENTS  client_count(2) + [player_name_length(1) + player_name(player_name_length) + score(4)] * client_count

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
    PING    = ord('p')
    INFO    = ord('i')
    RULES   = ord('r')
    CLIENTS = ord('c')
    RCON    = ord('x')

# fmt: B, H or I
def decode_query_string(data, offset, fmt):
    byte_width = struct.calcsize(fmt)
    length, = struct.unpack_from(fmt, data, offset)
    string = struct.unpack_from(f'{length}s', data, offset + byte_width)[0].decode(SAMP_ENCODING) 
    return string, offset + byte_width + length

class Query:
    def __init__(self, id=None, ip=None, port=None):
        self.id = id
        self.ip = ip
        self.port = port
    
    def __str__(self):
        return f'Query<{self.id}>'
    
    def encode_header(self):
        return b'SAMP' \
                + socket.inet_aton(self.ip) \
                + struct.pack('<HB', self.port, self.id)
    
    # return id, ip, port
    @staticmethod
    def decode_header(data):
        magic, ip, port, id = struct.unpack_from('<4s4sHB', data)
        return QUERY(id), socket.inet_ntoa(ip), port
    
    def encode_request(self):
        return self.encode_header() + self.encode_request_payload()
    
    @staticmethod
    def decode_request(data):
        id, ip, port = Query.decode_header(data)
        return id.decode_request_payload(data, ip, port)
    
    def encode_response(self):
        return self.encode_header() + self.encode_response_payload()
    
    @staticmethod
    def decode_response(data):
        id, ip, port = Query.decode_header(data)
        return id.decode_response_payload(data, ip, port)

class PingQuery(Query):
    def __init__(self, ip=None, port=None, time=None):
        super().__init__(QUERY.PING, ip, port)
        self.time = time # timestamp in ms; same as Raknet.get_time()
    
    def __str__(self):
        return f'PingQuery<{self.time}>'

    def encode_request_payload(self):
        return struct.pack('<I', self.time)
    
    @staticmethod
    def decode_request_payload(data, ip, port):
        ping_time, = struct.unpack_from('<I', data, QUERY_HEADER_SIZE)
        return PingQuery(ip, port, ping_time)
PingQuery.encode_response_payload = PingQuery.encode_request_payload
PingQuery.decode_response_payload = PingQuery.decode_request_payload
QUERY.PING.encode_request_payload = PingQuery.encode_request_payload
QUERY.PING.decode_request_payload = PingQuery.decode_request_payload
QUERY.PING.encode_response_payload = PingQuery.encode_response_payload
QUERY.PING.decode_response_payload = PingQuery.decode_response_payload

class InfoQuery(Query):
    def __init__(self, ip=None, port=None, has_password=None, player_count=None, max_player_count=None, hostname=None, gamemode=None, language=None):
        super().__init__(QUERY.INFO, ip, port)
        self.has_password = has_password
        self.player_count = player_count
        self.max_player_count = max_player_count
        self.hostname = hostname
        self.gamemode = gamemode
        self.language = language

    def __str__(self):
        return f'InfoQuery<{"PW " if self.has_password else ""}{self.player_count}/{self.max_player_count} | {self.hostname} | {self.gamemode} | {self.language}>'

    def encode_request_payload(self):
        return b''
    
    @staticmethod
    def decode_request_payload(data, ip, port):
        return InfoQuery(ip, port)

    def encode_response_payload(self):
        return struct.pack(f'<BHHI{len(self.hostname)}sI{len(self.gamemode)}sI{len(self.language)}s',
                        int(self.has_password), self.player_count, self.max_player_count, 
                        len(self.hostname), self.hostname.encode(SAMP_ENCODING), 
                        len(self.gamemode), self.gamemode.encode(SAMP_ENCODING), 
                        len(self.language), self.language.encode(SAMP_ENCODING))
    
    @staticmethod
    def decode_response_payload(data, ip, port):
        # decode has_password, player_count and max_player_count
        offset = QUERY_HEADER_SIZE
        has_password, player_count, max_player_count = struct.unpack_from('<BHH', data, offset)
        offset += struct.calcsize('<BHH')
        
        # decode hostname, gamemode and language
        hostname, offset = decode_query_string(data, offset, '<I')
        gamemode, offset = decode_query_string(data, offset, '<I')
        language, offset = decode_query_string(data, offset, '<I')
        
        return InfoQuery(ip, port, has_password, player_count, max_player_count, hostname, gamemode, language)
QUERY.INFO.encode_request_payload = InfoQuery.encode_request_payload
QUERY.INFO.encode_response_payload = InfoQuery.encode_response_payload
QUERY.INFO.decode_request_payload = InfoQuery.decode_request_payload
QUERY.INFO.decode_response_payload = InfoQuery.decode_response_payload

# rules; gravity, weather, website, ...
class RulesQuery(Query):
    def __init__(self, ip=None, port=None, rules=None):
        super().__init__(QUERY.RULES, ip, port)
        self.rules = rules # {rule: value, rule: value, ...}

    def __str__(self):
        return f'RulesQuery<{self.rules}>'

    def encode_request_payload(self):
        return b''
    
    @staticmethod
    def decode_request_payload(data, ip, port):
        return RulesQuery(ip, port)

    def encode_response_payload(self):
        data = b''
        data += struct.pack('<H', len(self.rules))
        for rule in self.rules:
            value = self.rules[rule]
            data += struct.pack(f'<B{len(rule)}sB{len(value)}s',
                                    len(rule), rule.encode(SAMP_ENCODING),
                                    len(value), value.encode(SAMP_ENCODING))
        return data
    
    @staticmethod
    def decode_response_payload(data, ip, port):
        offset = QUERY_HEADER_SIZE
        rules_length, = struct.unpack_from('<H', data, offset)
        offset += struct.calcsize('<H')
        
        # decode rules and values
        rules = {}
        for i in range(rules_length):
            rule, offset = decode_query_string(data, offset, 'B')
            value, offset = decode_query_string(data, offset, 'B')
            rules[rule] = value
        
        return RulesQuery(ip, port, rules)
QUERY.RULES.encode_request_payload = RulesQuery.encode_request_payload
QUERY.RULES.encode_response_payload = RulesQuery.encode_response_payload
QUERY.RULES.decode_request_payload = RulesQuery.decode_request_payload
QUERY.RULES.decode_response_payload = RulesQuery.decode_response_payload

class ClientsQuery(Query):
    def __init__(self, ip=None, port=None, clients=None):
        super().__init__(QUERY.CLIENTS, ip, port)
        self.clients = clients # {name: score, name: score, ...}

    def __str__(self):
        return f'ClientsQuery<{self.clients}>'

    def encode_request_payload(self):
        return b''

    @staticmethod
    def decode_request_payload(data, ip, port):
        return ClientsQuery(ip, port)

    def encode_response_payload(self):
        data = struct.pack('<H', len(self.clients))
        for name, score in self.clients.items():
            data += struct.pack(f'<B{len(name)}sI', len(name), name.encode(SAMP_ENCODING), score)
        return data
    
    @staticmethod
    def decode_response_payload(data, ip, port):
        offset = QUERY_HEADER_SIZE
        clients_length, = struct.unpack_from('<H', data, offset)
        offset += struct.calcsize('<H')
        
        # decode names and scores
        clients = {}
        for i in range(clients_length):
            name, offset = decode_query_string(data, offset, 'B')
            score, = struct.unpack_from('<I', data, offset)
            offset += 4
            
            clients[name] = score
        
        return ClientsQuery(ip, port, clients)
QUERY.CLIENTS.encode_request_payload = ClientsQuery.encode_request_payload
QUERY.CLIENTS.encode_response_payload = ClientsQuery.encode_response_payload
QUERY.CLIENTS.decode_request_payload = ClientsQuery.decode_request_payload
QUERY.CLIENTS.decode_response_payload = ClientsQuery.decode_response_payload

class RconQuery(Query):
    def __init__(self, ip=None, port=None, password=None, command=None):
        super().__init__(QUERY.RCON, ip, port)
        self.password = password
        self.command = command

    def __str__(self):
        return f'RconQuery<pw="{self.password}" cmd="{self.command}">'

    def encode_request_payload(self):
        return struct.pack(f'<H{len(self.password)}sH{len(self.command)}s',
                            len(self.password), self.password.encode(SAMP_ENCODING),
                            len(self.command), self.command.encode(SAMP_ENCODING))
    
    def decode_request_payload(self, data, ip, port):
        # decode password and command
        offset = QUERY_HEADER_SIZE
        password, offset = decode_query_string(data, offset, '<H')
        command, offset = decode_query_string(data, offset, '<H')
        return RconQuery(ip, port, password, command)
QUERY.RCON.encode_request_payload = RconQuery.encode_request_payload
QUERY.RCON.decode_request_payload = RconQuery.decode_request_payload
