import queue # Queue
import socket # inet_aton
import enum
import ctypes # QueryPerformanceFrequency, QueryPerformanceCounter
import ctypes.wintypes # LARGE_INTEGER
import time
import traceback

'''
RAKNET ARCHITECTURE:
We always use UDP in this raknet implementation

by default a peer is unconnected

All raknet packets(from unconnected peers) have exactly one message at the start.
 A peer becomes connected after the server send an OpenConnectionReply message

All raknet packets(from connected peers) have two parts(in this order):
 1. reliable message acknowlegements(see Acknowledgments)
 2. zero or more internal packets(see InternalPacket)

An internal packet has a whole message or part of a split message

SA-MP protocol
(Client.OpenConnectionRequest + Server.OpenConnectionCookie) * n ; until the client sends the correct cookie
Server.OpenConnectionReply
Client.ConnectionRequest
Server.AuthKey
Client.AuthKey
Server.ConnectionRequestAccepted
Client.NewIncomingConnection
Client.ClientJoin

Client.DisconnectNotification when disconnecting from a server

TODO:
 check if acknowledgments will fit before encoding all of them
 implement resend reliable messages
'''

from .bitstream import *

from .common import *

# raknet internal message identifiers
class MSG(enum.IntEnum):
    INTERNAL_PING                     = 6   # 0x06
    #PING                              = 7   # 0x07
    #PING_OPEN_CONNECTIONS             = 8   # 0x08
    CONNECTED_PONG                    = 9   # 0x09
    #REQUEST_STATIC_DATA               = 10  # 0x0a
    CONNECTION_REQUEST                = 11  # 0x0b
    AUTH_KEY                          = 12  # 0x0c ; used in the connection process; see auth_keys.py
    #BROADCAST_PINGS                   = 14  # 0x0e
    #SECURED_CONNECTION_RESPONSE       = 15  # 0x0f
    #SECURED_CONNECTION_CONFIRMATION   = 16  # 0x10
    #RPC_MAPPING                       = 17  # 0x11
    #SET_RANDOM_NUMBER_SEED            = 19  # 0x13
    RPC                               = 20  # 0x14
    #RPC_REPLY                         = 21  # 0x15
    DETECT_LOST_CONNECTIONS           = 23  # 0x16
    OPEN_CONNECTION_REQUEST           = 24  # 0x18  ; cookie challenge
    OPEN_CONNECTION_REPLY             = 25  # 0x19  ; cookie challenge
    OPEN_CONNECTION_COOKIE            = 26  # 0x1a  ; cookie challenge
    #RSA_PUBLIC_KEY_MISMATCH           = 28  # 0x1c
    #CONNECTION_ATTEMPT_FAILED         = 29  # 0x1d
    NEW_INCOMING_CONNECTION           = 30  # 0x1e
    #NO_FREE_INCOMING_CONNECTIONS      = 31  # 0x1f
    DISCONNECTION_NOTIFICATION	      = 32  # 0x20
    #CONNECTION_LOST                   = 33  # 0x21
    CONNECTION_REQUEST_ACCEPTED       = 34  # 0x22
    CONNECTION_BANNED                 = 36  # 0x24
    #INVALID_PASSWORD                  = 37  # 0x25
    #MODIFIED_PACKET                   = 38  # 0x26
    #PONG                              = 39  # 0x27
    TIMESTAMP                         = 40  # 0x28
    RECEIVED_STATIC_DATA              = 41  # 0x29
    #REMOTE_DISCONNECTION_NOTIFICATION = 42  # 0x2a
    #REMOTE_CONNECTION_LOST            = 43  # 0x2b
    REMOTE_NEW_INCOMING_CONNECTION    = 44  # 0x2c
    REMOTE_EXISTING_CONNECTION        = 45  # 0x2d
    #REMOTE_STATIC_DATA                = 46  # 0x2e
    #ADVERTISE_SYSTEM                  = 55  # 0x37

    # samp message identifiers
    DRIVER_SYNC     = 200  # 0xc8
    RCON_COMMAND    = 201  # 0xc9
    RCON_RESPONSE   = 202  # 0xca
    AIM_SYNC        = 203  # 0xcb
    WEAPONS_UPDATE  = 204  # 0xcc
    STATS_UPDATE    = 205  # 0xcd
    BULLET_SYNC     = 206  # 0xce
    PLAYER_SYNC     = 207  # 0xcf
    MARKERS_SYNC    = 208  # 0xd0
    UNOCCUPIED_SYNC = 209  # 0xd1
    TRAILER_SYNC    = 210  # 0xd2
    PASSENGER_SYNC  = 211  # 0xd3
    SPECTATOR_SYNC  = 212  # 0xd4
    
    def is_samp(self):
        return self.value >= MSG.DRIVER_SYNC

class PRIORITY(enum.IntEnum):
    SYSTEM = 0
    HIGH   = 1
    MEDIUM = 2
    LOW    = 3
NUMBER_OF_PRIORITIES = len(PRIORITY)

''' raknet reliability constants
RELIABLE: messages require the remote peer to acknowledge that it was received; if they do not the message is sent again
UNRELIABLE: messages do not use acknowledgments
SEQUENCED: messages use an ordering index; if we receive a message with ordering index X and later receive a message with ordering index X-1 we drop it because we only care about the most recent sequenced message
ORDERED: messages are delivered in the exact same order as they were pushed
'''
class RELIABILITY(enum.IntEnum):
    UNRELIABLE           = 6
    UNRELIABLE_SEQUENCED = 7
    RELIABLE             = 8
    RELIABLE_ORDERED     = 9
    RELIABLE_SEQUENCED   = 10
    BEGIN                = UNRELIABLE
    END                  = RELIABLE_SEQUENCED
    
    def reliable(self):
        return self.value == RELIABILITY.RELIABLE or self.value == RELIABILITY.RELIABLE_ORDERED or self.value == RELIABILITY.RELIABLE_SEQUENCED

    def ordered(self):
        return self.value == RELIABILITY.RELIABLE_ORDERED

    def sequenced(self):
        return self.value == RELIABILITY.UNRELIABLE_SEQUENCED or self.value == RELIABILITY.RELIABLE_SEQUENCED

class RPC(enum.IntEnum):
    pass

ORDERED_STREAMS_COUNT = 32

MTU_SIZE = 576 # 1500
IPV4_HEADER_SIZE = 20
UDP_HEADER_SIZE = 8
MAX_UDP_PACKET_PAYLOAD_SIZE = MTU_SIZE - IPV4_HEADER_SIZE - UDP_HEADER_SIZE

MIN_ACKS_SIZE = 1

MAX_INTERNAL_PACKET_HEADER_SIZE = 19

# MAX_MESSAGE_SIZE in other words is the maximum internal packet payload size
MAX_MESSAGE_SIZE = MAX_UDP_PACKET_PAYLOAD_SIZE - MIN_ACKS_SIZE - MAX_INTERNAL_PACKET_HEADER_SIZE

kernel32 = ctypes.windll.kernel32
perf_frequency = ctypes.wintypes.LARGE_INTEGER()
kernel32.QueryPerformanceFrequency(ctypes.byref(perf_frequency))

# return in ms
def get_time():
    timestamp = ctypes.wintypes.LARGE_INTEGER()
    kernel32.QueryPerformanceCounter(ctypes.byref(timestamp))
    return int(timestamp.value * 1000 / perf_frequency.value)

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

class InternalPacket:
    def __init__(self, sequence_number, reliability, ordering_channel, ordering_index, split_id=None, split_index=None, split_count=None, payload=b''):
        self.sequence_number = sequence_number
        self.reliability = reliability
        self.ordering_channel = ordering_channel
        self.ordering_index = ordering_index
        self.split_id = split_id
        self.split_index = split_index
        self.split_count = split_count
        self.payload = payload
    
    def __str__(self):
        return pretty_format(self, 0)
    
    def encode(self, bs):
        # encode sequence number
        bs.write_u16(self.sequence_number)
        
        # encode reliability
        bs.write_bits_num(self.reliability, 4)
        if self.reliability.sequenced() or self.reliability.ordered():
            bs.write_bits_num(self.ordering_channel, 5)
            bs.write_u16(self.ordering_index)
        
        # encode split packet attributes
        is_split_message = self.split_id != None
        bs.write_bit(is_split_message)
        if is_split_message:
            bs.write_u16(self.split_id)
            bs.write_compressed_u32(self.split_index)
            bs.write_compressed_u32(self.split_count)
        
        # encode payload size
        bs.write_compressed_u16(TO_BITS(len(self.payload)))
        
        # copy payload
        bs.write_aligned(self.payload)
    
    @staticmethod
    def decode(bs):
        # decode sequence number
        sequence_number = bs.read_u16()
        
        # decode reliability
        reliability = RELIABILITY(bs.read_bits_num(4)) # the enum should raise an exception if the reliability is invalid
        if reliability.sequenced() or reliability.ordered():
            ordering_channel = bs.read_bits_num(5)
            ordering_index = bs.read_u16()
        else:
            ordering_channel = None
            ordering_index = None
        
        # decode split packet attributes 
        is_split = bs.read_bit()
        if is_split:
            split_id = bs.read_u16()
            split_index = bs.read_compressed_u32()
            split_count = bs.read_compressed_u32()
            # do some sanity checks; change it if you need it...
            if split_index >= split_count or split_count >= 100:
                raise Exception('bad split packet')
        else:
            split_id = None
            split_index = None
            split_count = None
        
        # decode payload size
        payload_size = TO_BYTES(bs.read_compressed_u16())
        if payload_size > 1500:
            raise Exception('packet payload too big')
        
        # copy payload
        payload = bytearray(payload_size)
        bs.read_aligned(payload, payload_size)
        
        return InternalPacket(sequence_number, reliability, ordering_channel, ordering_index, split_id, split_index, split_count, payload)

class Message:
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return pretty_format(self, 1)
    
    def encode_header(self):
        return self.id.to_bytes(1, 'little')
    
    @staticmethod
    def decode_header(data):
        try:
            id = MSG(data[0])
            # skip timestamp if present
            if id == MSG.TIMESTAMP:
                # data[1:4] # skip timestamp
                id = MSG(data[5]) # decode real id
                return id, data[6:]
            else:
                return id, data[1:]
        except Exception as e:
            e.add_note(f'id=0x{id:x} data={data.hex(" ")}')
            raise e
    
    # in case they are the same
    # note: derived Rpc classes override this
    def encode(self):
        return self.encode_header() + self.encode_payload()
    
    def encode_from_client(self):
        return self.encode_header() + self.id.encode_client_payload(self)
    
    def encode_from_server(self):
        return self.encode_header() + self.id.encode_server_payload(self)
    
    @staticmethod
    def decode_from_client(data):
        id, data = Message.decode_header(data)
        try:
            return id.decode_client_payload(data)
        except Exception as e:
            e.add_note(f'id=0x{id:x} data=[{data.hex(" ")}]')
            raise e

    @staticmethod
    def decode_from_server(data):
        id, data = Message.decode_header(data)
        try:
            return id.decode_server_payload(data)
        except Exception as e:
            e.add_note(f'id=0x{id:x}; data=[{data.hex(" ")}]')
            raise e

class Rpc(Message):
    def __init__(self, rpc_id):
        super().__init__(MSG.RPC)
        self.rpc_id = rpc_id
    
    def __str__(self):
        return pretty_format(self, 2)

    # encode message payload
    def encode_payload(self):
        # encode rpc payload
        payload_bs = Bitstream(capacity=64)
        self.encode_rpc_payload(payload_bs)
        # encode rpc header
        bs = Bitstream(capacity=64)
        bs.write_u8(self.rpc_id)
        bs.write_compressed_u32(payload_bs.len)
        # copy rpc payload
        bs.write_bits(payload_bs.data, payload_bs.len)
        return bs.data[:TO_BYTES(bs.len)]
    
    # decode message payload
    @staticmethod
    def decode_client_payload(data):
        rpc_id, bs = Rpc.decode_payload_header(data)
        return rpc_id.decode_client_rpc_payload(bs)
    
    # decode message payload
    @staticmethod
    def decode_server_payload(data):
        rpc_id, bs = Rpc.decode_payload_header(data)
        return rpc_id.decode_server_rpc_payload(bs)
    
    @staticmethod
    def decode_payload_header(data):
        bs = Bitstream(data)
        
        # decode rpc id
        rpc_id = bs.read_u8()
        rpc_id = RPC(rpc_id)
        
        # decode rpc payload size
        rpc_payload_size_in_bits = bs.read_compressed_u32()
        if rpc_payload_size_in_bits > TO_BITS(len(data) + 16):
            raise Exception('bad rpc: invalid size')
        
        return rpc_id, bs
MSG.RPC.decode_client_payload = Rpc.decode_client_payload
MSG.RPC.decode_server_payload = Rpc.decode_server_payload

class OpenConnectionRequest(Message):
    def __init__(self, cookie):
        super().__init__(MSG.OPEN_CONNECTION_REQUEST)
        self.cookie = cookie
    
    def encode_payload(self):
        return struct.pack('<H', self.cookie)
    
    @staticmethod
    def decode_payload(data):
        cookie, = struct.unpack('<H', data)
        return OpenConnectionRequest(cookie)

class OpenConnectionCookie(Message):
    def __init__(self, cookie):
        super().__init__(MSG.OPEN_CONNECTION_COOKIE)
        self.cookie = cookie
    
    def encode_payload(self):
        return struct.pack('<H', self.cookie)
    
    @staticmethod
    def decode_payload(data):
        cookie, = struct.unpack('<H', data)
        return OpenConnectionCookie(cookie)

class OpenConnectionReply(Message):
    def __init__(self):
        super().__init__(MSG.OPEN_CONNECTION_REPLY)
    
    def encode_payload(self):
        return b'\x00'
    
    @staticmethod
    def decode_payload(data):
        return OpenConnectionReply()

class NewIncomingConnection(Message):
    def __init__(self, ip, port):
        super().__init__(MSG.NEW_INCOMING_CONNECTION)
        self.ip = ip
        self.port = port
    
    def encode_payload(self):
        return socket.inet_aton(self.ip) + self.port.to_bytes(2, 'little')
    
    @staticmethod
    def decode_payload(data):
        ip = socket.inet_ntoa(data[:4])
        port, = struct.unpack_from('<H', data, 4)
        return NewIncomingConnection(ip, port)

class ConnectionRequest(Message):
    def __init__(self, password):
        super().__init__(MSG.CONNECTION_REQUEST)
        self.password = password
    
    def encode_payload(self):
        return self.password.encode(SAMP_ENCODING)
    
    @staticmethod
    def decode_payload(data):
        password = data.decode(SAMP_ENCODING)
        return ConnectionRequest(password)

class ConnectionRequestAccepted(Message):
    def __init__(self, ip, port, player_id, cookie):
        super().__init__(MSG.CONNECTION_REQUEST_ACCEPTED)
        self.ip = ip
        self.port = port
        self.player_id = player_id
        self.cookie = cookie
    
    def encode_payload(self):
        return socket.inet_aton(self.ip) + struct.pack('HHI', self.port, self.player_id, self.cookie)

    @staticmethod
    def decode_payload(data):
        ip = socket.inet_ntoa(data[:4])
        port, player_id, cookie = struct.unpack_from('<HHI', data, 4)
        return ConnectionRequestAccepted(ip, port, player_id, cookie)

class InternalPing(Message):
    def __init__(self, time):
        super().__init__(MSG.INTERNAL_PING)
        self.time = time
    
    def encode_payload(self):
        return struct.pack('<I', self.time)

    @staticmethod
    def decode_payload(data):
        ping_time, = struct.unpack_from('<I', data)
        return InternalPing(ping_time)

class ConnectedPong(Message):
    def __init__(self, ping_time, pong_time):
        super().__init__(MSG.CONNECTED_PONG)
        self.ping_time = ping_time
        self.pong_time = pong_time
    
    def encode_payload(self):
        return struct.pack('<II', self.ping_time, self.pong_time)

    @staticmethod
    def decode_payload(data):
        ping_time, pong_time = struct.unpack_from('<II', data)
        return ConnectedPong(ping_time, pong_time)

class Timestamp(Message):
    def __init__(self):
        super().__init__(MSG.TIMESTAMP)
    
    @staticmethod
    def decode_payload(data):
        return Timestamp()

class ReceivedStaticData(Message):
    def __init__(self, local_static_data):
        super().__init__(MSG.RECEIVED_STATIC_DATA)
        self.local_static_data = local_static_data
    
    def encode_payload(self):
        return self.local_static_data

    @staticmethod
    def decode_payload(data):
        local_static_data = data
        return ReceivedStaticData(local_static_data)

class DetectLostConnections(Message):
    def __init__(self):
        super().__init__(MSG.DETECT_LOST_CONNECTIONS)
    
    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data):
        return DetectLostConnections()

class AuthKey(Message):
    def __init__(self, key):
        super().__init__(MSG.AUTH_KEY)
        self.key = key
    
    def encode_payload(self):
        return len(self.key).to_bytes(1, 'little') + self.key

    @staticmethod
    def decode_payload(data):
        key_size = data[0]
        key = data[1:1+key_size]
        return AuthKey(key)

'''
The client sees the message "Server closed the connection." when the server sends
'''
class DisconnectionNotification(Message):
    def __init__(self):
        super().__init__(MSG.DISCONNECTION_NOTIFICATION)
    
    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data):
        return DisconnectionNotification()

class RemoteNewIncomingConnection(Message):
    def __init__(self, ip, port, player_id):
        super().__init__(MSG.REMOTE_NEW_INCOMING_CONNECTION)
        self.ip = ip
        self.port = port
        self.player_id = player_id
    
    def encode_payload(self):
        return socket.inet_aton(self.ip) + struct.pack('HH', self.port, self.player_id)

    @staticmethod
    def decode_payload(data):
        ip = socket.inet_ntoa(data[:4])
        port, player_id = struct.unpack_from('<HH', data, 4)
        return RemoteNewIncomingConnection(ip, port, player_id)

class RemoteExistingConnection(Message):
    def __init__(self, ip, port, player_id):
        super().__init__(MSG.REMOTE_EXISTING_CONNECTION)
        self.ip = ip
        self.port = port
        self.player_id = player_id
    
    def encode_payload(self):
        return socket.inet_aton(self.ip) + struct.pack('HH', self.port, self.player_id)

    @staticmethod
    def decode_payload(data):
        ip = socket.inet_ntoa(data[:4])
        port, player_id = struct.unpack_from('<HH', data, 4)
        return RemoteExistingConnection(ip, port, player_id)

class ConnectionBanned(Message):
    def __init__(self):
        super().__init__(MSG.CONNECTION_BANNED)
    
    def encode_payload(self):
        return b''

    @staticmethod
    def decode_payload(data):
        return ConnectionBanned()

from .messages import *
import inspect
module = inspect.getmodule(inspect.currentframe())
for msg in MSG:
    # get SomeRaknetMessage class from MSG.SOME_RAKNET_MESSAGE
    class_name = ''.join(w.capitalize() for w in msg.name.split('_'))
    try:
        msg_class = getattr(module, class_name)
        
        if msg_class.__dict__.get('encode_payload') != None:
            msg.encode_client_payload = msg_class.encode_payload
            msg.encode_server_payload = msg_class.encode_payload
        
        if msg_class.__dict__.get('decode_payload') != None:
            msg.decode_client_payload = msg_class.decode_payload
            msg.decode_server_payload = msg_class.decode_payload
        else:
            if msg_class.__dict__.get('decode_client_payload') != None:
                msg.decode_client_payload = msg_class.decode_client_payload
            if msg_class.__dict__.get('decode_server_payload') != None:
                msg.decode_server_payload = msg_class.decode_server_payload
        
    except AttributeError:
        continue

class BadAck(Exception):
    pass

class Range:
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max
    
    def __str__(self):
        return f'[{self.min},{self.max}]'

class Acknowledgments:
    def __init__(self, ranges=list()):
        # [Range(min,max), Range(min,max), ...]
        self.ranges = ranges
    
    def __str__(self):
        return f'<Acknowledgments {"".join([str(r) for r in self.ranges])}>'
    
    def add(self, n):
        #self.acks.append(number)
        for r in self.ranges:
            if r.min <= n <= r.max: # already present
                return
            elif n == r.min - 1: # add n to the start
                r.min -= 1
                # check if we can merge
                for r2 in self.ranges:
                    if r.min - 1 == r2.max:
                        r.min = r2.min
                        self.ranges.remove(r2)
                        return
                return
            elif n == r.max + 1: # add n to the end
                r.max += 1
                # check if we can merge
                for r2 in self.ranges:
                    if r.max + 1 == r2.min:
                        r.max = r2.max
                        self.ranges.remove(r2)
                        return
                return
        # if we get we could not add 'n'; lets make a new range
        self.ranges.append(Range(n, n))
    
    def remove(self, ranges):
        for r in self.ranges[:]:
            for r2 in ranges:
                if not (r2.max < r.min or r2.min > r.max): # check if it will remove
                    if r2.min <= r.min and r2.max >= r.max: # remove
                        self.ranges.remove(r)
                    elif r2.min > r.min and r2.max < r.max: # split
                        self.ranges.append(Range(r2.max + 1, r.max))
                        r.max = r2.min - 1
                    elif r2.min <= r.min: # trim left
                        r.min = r2.max + 1
                    elif r2.max >= r.max: # trim right
                        r.max = r2.min - 1
    
    def encode(self, bs):
        if len(self.ranges) > 0:
            # write ack data
            bs.write_bit(1) # has acks
            bs.write_compressed_u16(len(self.ranges))
            for r in self.ranges:
                bs.write_bit(int(r.min == r.max))
                bs.write_u16(r.min)
                if r.min != r.max: # only write max if min!=max otherwise it'd redundant
                    bs.write_u16(r.max)
    
    @staticmethod
    def decode(bs):
        ranges = []
        has_acks = bs.read_bit()
        if has_acks: # parse them
            range_count = bs.read_compressed_u16() # read the amount of ranges
            for i in range(range_count): # iterate and decode each range
                min_equals_max = bs.read_bit()
                min = bs.read_u16()
                if min_equals_max == 0:
                    max = bs.read_u16()
                    if min > max:
                        raise BadAck # Exception(f'bad acks: min({min}) > max({max})')
                    ranges.append(Range(min, max))
        return Acknowledgments(ranges)

class Peer:
    def __init__(self, addr, is_server_peer=True, sendto=None):
        self.addr = addr
        if sendto != None:
            self.sendto = sendto
        
        if is_server_peer:
            self.encode_message = Message.encode_from_client
            self.decode_message = Message.decode_from_server
        else:
            self.encode_message = Message.encode_from_server
            self.decode_message = Message.decode_from_client
            
        self.first_packet_time = None
        self.last_packet_time = None
        self.first_message_time = None
        self.out_bs = Bitstream(capacity=1500)
        
        '''
        For every reliable message received from the peer, we add its sequence
        number to 'send_acks'. For every packet we send, we send as much
        acknowledgments as we can from 'send_acks' so the peer knows we received
        the reliable messages sent in the past.
        '''
        self.send_acks = Acknowledgments()
        self.expected_acks = Acknowledgments()
        #self.send_acks_lock = threading.Lock()
        
        self.split_packets = []
        
        self.ordered_packet_write_index = [0] * ORDERED_STREAMS_COUNT
        self.ordered_packet_read_index = [0] * ORDERED_STREAMS_COUNT
        
        self.sequenced_packet_write_index = [0] * ORDERED_STREAMS_COUNT
        self.sequenced_packet_read_index = [0] * ORDERED_STREAMS_COUNT
        
        self.ordering_list = [[]] * ORDERED_STREAMS_COUNT
        
        self.send_internal_packet_queues = [queue.Queue()] * NUMBER_OF_PRIORITIES
        #self.local_static_data = bytearray()
        
        # incremented for every messaged pushed 
        self.sequence_number = 0
        
        # incremented after each split message pushed
        self.split_message_id = 0
        
        self.connected_message_callbacks = [] # callback(message, internal_packet, peer)
        self.unconnected_message_callbacks = [] # callback(message, peer)
        
        self.connected = False
    
    def sendto(self, buffer):
        raise NotImplementedError('You must implement Peer.sendto()')
    
    def push_message(self, message, reliability=RELIABILITY.RELIABLE, priority=PRIORITY.HIGH, ordering_channel=None):
        self.push_encoded_message(self.encode_message(message), reliability, priority, ordering_channel)
    
    def push_encoded_message(self, message_data, reliability=RELIABILITY.RELIABLE, priority=PRIORITY.HIGH, ordering_channel=None):
        if reliability.sequenced():
            ordering_index = self.sequenced_packet_write_index[ordering_channel]
            self.sequenced_packet_write_index[ordering_channel] = (self.sequenced_packet_write_index[ordering_channel] + 1) % (2**16)
        elif reliability.ordered():
            ordering_index = self.ordered_packet_write_index[ordering_channel]
            self.ordered_packet_write_index[ordering_channel] = (self.ordered_packet_write_index[ordering_channel] + 1) % (2**16)
        else:
            ordering_index = None
            
        # check if message has to be split
        split_message_count = DIV_INT_CEIL(len(message_data), MAX_MESSAGE_SIZE)
        if split_message_count > 1:
            remaining_size = len(message_data)
            
            for i in range(split_message_count):
                split_size = min(MAX_MESSAGE_SIZE, remaining_size)
                remaining_size -= MAX_MESSAGE_SIZE
                
                split_data_offset = i * MAX_MESSAGE_SIZE
                split_data = message_data[split_data_offset : split_data_offset + split_size]
                
                packet = InternalPacket(self.sequence_number, reliability, ordering_channel, ordering_index, self.split_message_id, i, split_message_count, split_data)
                self.sequence_number = (self.sequence_number + 1) % (2**16)
                self.send_internal_packet_queues[priority].put(packet)
            self.split_message_id = (self.split_message_id + 1) % (2**32)
        else:
            packet = InternalPacket(self.sequence_number, reliability, ordering_channel, ordering_index, payload=message_data)
            self.sequence_number = (self.sequence_number + 1) % (2**16)
            self.send_internal_packet_queues[priority].put(packet)
    
    def generate_packet(self, bs):
        #with self.send_acks_lock:
        self.send_acks.encode(bs)
        
        for internal_packet_queue in self.send_internal_packet_queues:
            try:
                internal_packet = internal_packet_queue.get_nowait()
            except queue.Empty:
                continue
            
            # check if fits
            internal_packet_size = MAX_INTERNAL_PACKET_HEADER_SIZE + len(internal_packet.payload)
            if bs.write_offset + TO_BITS(internal_packet_size) > TO_BITS(MAX_UDP_PACKET_PAYLOAD_SIZE):
                internal_packet_queue.put(internal_packet) # put back into queue
                break
            
            if bs.write_offset == 0: # if nothing was written
                bs.write_bit(0) # no acks
            
            internal_packet.encode(bs)
        
        self.send_acks.ranges = []
        
        return bs.len > 0
    
    def update(self):
        # process send queue
        # send all available data(acks + messages in send queue) to the socket
        while self.generate_packet(self.out_bs):
            buffer_size = TO_BYTES(self.out_bs.len)
            buffer = self.out_bs.data[:buffer_size]
            self.sendto(buffer)
            self.out_bs.reset()
    
    def handle_unconnected_packet(self, data):
        # if this peer is not connected, a message is present at the
        # start of the packet, instead of acks or internal packet headers
        try:
            message = self.decode_message(data)
        except Exception as e:
            e.add_note(f'Peer.handle_packet(data={data.hex(" ")})')
            raise e
        self.handle_unconnected_message(message)
    
    def handle_connected_packet(self, data):
        bs = Bitstream(data)
        try:
            '''
            Decode acknowlegements for reliable raknet messages we sent in the
            past. We use these to know the peer receive our reliable message.
            If we do not receive an acknowlegement we need to send the message
            again. 'self.expected_acks' tracks these.
            '''
            # decode acknowledgments in this packet
            acks = Acknowledgments.decode(bs)
            
            # remove these acknowledgments from 'expected_acks'
            self.expected_acks.remove(acks.ranges)
            #todo reliable send list; resend
            
            # decode raknet messages
            # do not decode leftover bits(<16; not necessarily a bad packet)
            while bs.unread_bits_count() > 16:
                packet = InternalPacket.decode(bs)
                # if we didn't have GIl I guess I'd be beneficial to push the packet
                # into a queue and process it on another thread potentially in
                # parallel; but because we use asyncio I guess I won't matter if we
                # just handle it here
                
                if packet.reliability.reliable():
                    #with self.send_acks_lock:
                    # add message to acknowlegements queue so we can later tell the peer we received this [reliable] message
                    self.send_acks.add(packet.sequence_number)
                    
                if packet.reliability.sequenced():
                    expected_index = self.sequenced_packet_read_index[packet.ordering_channel]
                    if packet.ordering_index < expected_index:
                        # ignore old sequenced packet
                        continue
                    else:
                        # update expected index
                        self.sequenced_packet_read_index[packet.ordering_channel] = (packet.ordering_index + 1) % (2**16)
                
                if packet.split_id != None:
                    now = time.time()
                    packet.time = now
                    self.split_packets.append(packet)
                    
                    index_sum = 0
                    count = 0
                    for p in self.split_packets[:]:
                        # remove split packets older than 10s
                        if now - p.time > 10 * 1000:
                            self.split_packets.remove(p)
                            continue
                        
                        # find related split packets
                        if p.split_id == packet.split_id:
                            index_sum += p.split_index
                            count += 1
                    
                    # check if this was the last part of a split packet
                    if count == packet.split_count and index_sum == sum(range(count)):
                        parts = [None] * count
                        
                        # remove split packets from list
                        for p in self.split_packets[:]:
                            if p.split_id == packet.split_id:
                                parts[p.split_index] = p
                                self.split_packets.remove(p)
                        
                        payload = bytearray()
                        for part in parts:
                            payload += part.payload
                            
                        # make internal packet to represent the assembled split messages
                        packet.split_id = packet.split_count = packet.split_index = None
                        packet.payload = payload
                        # assemble whole packet and handle it
                    else: # could not assemble whole packet from split packets; do not handle it yet
                        continue
                else: # internal packet contains a whole message; handle it
                    pass
                
                if packet.reliability.ordered():
                    expected_index = self.ordered_packet_read_index[packet.ordering_channel]
                    if packet.ordering_index == expected_index:
                        self.ordered_packet_read_index[packet.ordering_channel] = (self.ordered_packet_read_index[packet.ordering_channel] + 1) % (2**16)
                        
                        # handle expected ordered packet
                        message = self.decode_message(packet.payload)
                        self.handle_connected_message(message, packet)
                        
                        # handle all adjacent sucessors
                        while True:
                            expected_index = self.ordered_packet_read_index[packet.ordering_channel]
                            try:
                                p = next(p for p in self.ordering_list[packet.ordering_channel] if p.ordering_index == expected_index)
                                message = self.decode_message(p.payload)
                                self.handle_connected_message(message, p)
                                self.ordering_list[packet.ordering_channel].remove(p)
                                self.ordered_packet_read_index[packet.ordering_channel] = (self.ordered_packet_read_index[packet.ordering_channel] + 1) % (2**16)
                            except StopIteration: # no more adjacent sucessors
                                break
                        continue
                        
                        #0 1 2   4 5 6  3
                    else: # packet out of order
                        if packet.ordering_index < expected_index: # bad packet
                            continue
                        # save to handle in the future 
                        self.ordering_list[packet.ordering_channel].append(packet)
                        continue
                
                message = self.decode_message(packet.payload)
                self.handle_connected_message(message, packet)
        except Exception as e: # bad packet
            e.add_note(f'Peer.handle_packet(data={data.hex(" ")})')
            log(traceback.format_exc())

    def handle_packet(self, data):
        if self.connected:
            self.handle_connected_packet(data)
        else:
            self.handle_unconnected_packet(data)

    def handle_unconnected_message(self, message):
        if message.id == MSG.OPEN_CONNECTION_REPLY:
            self.connected = True
        for callback in self.unconnected_message_callbacks:
            if callback(message, self) == True:
                return

    def handle_connected_message(self, message, internal_packet):
        for callback in self.connected_message_callbacks:
            if callback(message, internal_packet, self) == True:
                return
      
    def send_unconnected_message(self, message):
        if message.id == MSG.OPEN_CONNECTION_REPLY:
            self.connected = True
        self.sendto(self.encode_message(message))