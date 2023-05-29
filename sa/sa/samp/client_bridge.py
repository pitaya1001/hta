'''
This VERY EXPERIMENTAL module communicates with gta_sa.exe
We hook some functions there to get info e.g. viewangles.
We can send commands like OPEN_CHAT, CLOSE_CHAT, set the viewangles(useful for interpolation)

TODO:
 make a proper hook function
 
Dev Notes:

GTA REPLAY ACTIONS
 attack/fire
 aim
 set viewangles
 jump
 crouch
 walk
 walk(slow)
 run (stamina)
 vehicle special action(honk, light, siren,..)
 enter vehicle(as driver or passenger)
 exit vehicle

SAMP REPLAY ACTIONS
 SPECIAL ACTION (keys H N F ...)

 RAKNET MESSAGES/RPCS

 KILL FEED visibility (visible, hidden)
 HUD visibility (visible, partial, hidden)
 NET STATS visibility (visible, hidden)
 
 CHAT
  open
  close
  set pos
  set text
  send
 
 TAB
  open
  close
  set pos
  select row
 
 DIALOG
  set text
  select row
  hover button (animation)
  click button (animation)

 TEXTDRAW
  hover selectable(animation)
  click selectable(animation)

chat samp: try to manipulate buffer? instead of calling funcs like press...
send raknet message samp

packet interception: easy to modify existing ones, hard to add/remove


impl samp voice?
'''

SAMP_WINDOW_NAME = 'GTA:SA:MP'

# makes /dl only show the vehicle health
SET_DL_STRING_ONLY_VEHICLE_HEALTH = True

# makes /dl on by default
SHOW_DL_BY_DEFAULT = True

# internal the remote thread sleeps between reads for messages pushed by Client.push_message()
REMOTE_READ_SB_INTERVAL = 2 # in ms

VIEWANGLE_READ_PERIOR_MOVING_AVERAGE_N = 100 # lower values cause a faster response

#import ctypes
#import ctypes.wintypes
import struct
from multiprocessing import shared_memory
import time

import math

# pip install pywin32
import win32api
import win32con
import win32gui
import win32process

from win32process import ReadProcessMemory, WriteProcessMemory, VirtualAllocEx, CreateRemoteThread
from win32con import MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE
from win32event import WaitForSingleObject

#kernel32 = ctypes.windll.kernel32
#user32 = ctypes.windll.user32

from .common import *
class HUD(enum.IntEnum):
    HIDDEN  = 0
    PARTIAL = 1
    VISIBLE = 2

# our(i.e. non samp) message ids
class CLIENT(enum.IntEnum):
    CHAT_OPEN            = 0xdc # 220 none              samp.dll+0x69440=83 ec 10 56 8b f1 8b 86 e0 14 00 00   open_chat(ecx=[samp.dll + 0x26E9FC])               
    CHAT_CLOSE           = 0xdd # 221 none              samp.dll+0x69540=56 8b f1 8b 86 e0 14 00 00 85 c0 74   close_chat(ecx=[samp.dll + 0x26E9FC])              
    #TAB_OPEN              = 0xde # 222 none              samp.dll+0x6e9a0                                       open_tab(ecx=[samp.dll + 0x26E9C4])
    #TAB_CLOSE             = 0xdf # 223 none              samp.dll+0x6f3a0                                       close_tab(ecx=[samp.dll + 0x26E9C4], push{1})
    KILL_FEED_VISIBILITY = 0xe0 # 224 visibility(u8)          samp.dll+0x613a6                                       death_chat_visibility* = [samp.dll + 0x26EA00]
    VIEWANGLES           = 0xe1 # 225 yaw(16)+pitch(16) 
    HUD_VISIBILITY       = 0xe2 # 226 visibility(u8)
    NET_STATS_VISIBILITY = 0xe3 # 227 visibility(u8(u8)
    WNDPROC_MESSAGE      = 0xe4
    BEGIN = CHAT_OPEN
    END = NET_STATS_VISIBILITY


# note: yaw(horizontal movement)), pitch(vertical movement)

# yaw = [-pi, +pi], range = 2pi = 360° ( actual range )
# san andreas map perspective
#
#                     up -1.570796327 = -90°
#                             |
# left(sf) 0.0 = 0° -------- yaw --------  +-pi = +-180° (between lv and ls)
#                             |
#                   down 1.570796327 = +90°

# pitch = [-pi/2, +pi/2], range = pi = 180°
# actual pitch range = 2.27 = 130°
#
#    up = +half pi ~ 1.57 = 90°
#    |
#    |  actual up limit = 0.785398185 = 45°
#    |  /
#    | / 
#   pitch ----- forward(0.00) 0°
#    |  \
#    |   \
#    |  actual down limit -1.483529925 = -85°
#    |
#   down = -half pi ~ -1.57 = -90°
#

# map [-pi,+pi] to [0,1]
def normalize_yaw(yaw):
    return (yaw + math.pi) / (2 * math.pi)

# map  [-pi/2, +pi/2] to [0,1]
def normalize_pitch(pitch):
    return (pitch + (math.pi / 2)) / (math.pi)

# map [0,1] to [-pi,+pi]
def unormalize_yaw(yaw):
    return yaw * (2 * math.pi) - math.pi

# map [0,1] to [-pi/2, +pi/2]
def unormalize_pitch(pitch):
    return pitch * math.pi - (math.pi / 2)

#
# gta_sa.exe@d9 06 8b 03 d9 ff; [ebx]=yaw [esi]=pitch; read/write there;
#float* my_pos =(float*)MemIn::ReadMultiLevelPointer(0xB6F5F0,{0x14,0x30});
#yaw = *(float*)0x00B6F258 + PI
#pitch = *(float*)0x00B6F248

# samp+67290 page up
# samp+672F0 page down

# samp+695F0 up
# samp+69660 down

# set_hud_visibility 
# show chat status = {0=hidden 1=partial 2=full} (cycle from right to left, 2->1 1->0 0->2)
# show_chat_status* = [samp.dll + 26EA00] + 8
# redraw_chat* = [samp.dll + 26EA00] + 63da
# samp+61280 where chat status is modified
# hud_visiblity*=[samp+26e9f8]+8

# samp+70660 close_dialog([samp.dll + 26E9C8], 0)

# 11-178 RPC
# 200-212 SYNC

# chat type                 222    key(u8)
# chat change show status   224    status(u8)
# chat set pos              225    pos(u32?)  ; instead of scroll,up,down,page up,page down
# chat previous input
# chat next input

# tab set pos

#220 chat open
#221 chat close
#222 chat type
#223 chat send
#224 chat change show status
#225 chat up
#226 chat down
#227 chat page up
#228 chat page down

# [0x58F4C8] = money str?
# [0x58F50A] = neg money str?
# 0x58F58D = money border thickness
# 0x58EB70 = clock border thickness ( offline only)?

# GetSystemTimePreciseAsFileTime
UNIX_TIME_START = 0x019DB1DED53E8000
TICKS_PER_MS = 10000

class AddressNotFound(Exception):
    pass

import re
def pattern_scan(h_process, address, size, pattern):
    #any_byte_pattern = b'[\x00-\xff]'
    pattern = b''.join([b'[\x00-\xff]' if b == '??' else re.escape(int(b, base=16).to_bytes(1, 'little')) for b in pattern.split()])
    #pattern = b''
    #for b in pattern_.split():
    #    pattern += (any_byte_pattern if (b == '??') else re.escape(int(b, base=16).to_bytes(1, 'little')))
    
    buffer = ReadProcessMemory(h_process, address, size)
    match = re.search(pattern, bytes(buffer))
    if match:
        return address + match.start()
    else:
        raise AddressNotFound
    
    #buffer = (ctypes.c_ubyte * size)()
    #if kernel32.ReadProcessMemory(h_process, address, ctypes.byref(buffer), size, 0):
    #    match = re.search(pattern, bytes(buffer))
    #    if match:
    #        return address + match.start()
    #raise AddressNotFound(f'pattern_scan(start={address:x}, size={size:x}, "{pattern_}")')

# todo patterns_and_masks so we only read each page once
#def pattern_scan_batch(h_process, start, end, patterns_and_masks):
#    # [pattern, mask] -> [index, pattern, mask]
#    for i, pattern_and_mask in enumerate(patterns_and_masks):
#        patterns_and_masks[i] = [i] + pattern_and_mask
#    patterns_and_masks2 = patterns_and_masks[:]
#
#    buffer = (ctypes.c_ubyte * 0x10000)()
#    address = start
#    match_counts = [0] * len(patterns_and_masks)
#    number_of_bytes_read = ctypes.c_uint32()
#    outputs = [None] * len(patterns_and_masks)
#    remaining_size = end - start
#    while address < end:
#        if kernel32.ReadProcessMemory(h_process, address, ctypes.byref(buffer), min(len(buffer), remaining_size), ctypes.byref(number_of_bytes_read)):
#            for i in range(number_of_bytes_read.value):
#                for k, (j, pattern, mask) in enumerate(patterns_and_masks):
#                    if buffer[i] == pattern[match_counts[j]] or mask[match_counts[j]] == '?':
#                        match_counts[j] += 1
#                    else:
#                        match_counts[j] = 0
#                    if match_counts[j] == len(pattern):
#                        outputs[j] = address + i - match_counts[j] + 1
#                        del patterns_and_masks[k]
#            address += number_of_bytes_read.value
#            remaining_size -= number_of_bytes_read.value
#        else:
#            raise AddressNotFound(f'pattern_scan_batch(start={start:x}, end={end:x}); ReadProcessMemory({address:x}) failed')
#    
#    for i, output in enumerate(outputs):
#        if output == None:
#            raise AddressNotFound(f'pattern_scan_batch(start={start:x}, end={end:x}, "{patterns_and_masks2[i][1].hex(" ")}", "{patterns_and_masks2[i][2]}"); not found')
#    return outputs

# pattern scan, batch, regex, multithreaded

def GetProcAddressEx(h_process, module_base, proc_names):
    proc_names = [name.encode() for name in proc_names]
    
    # read module header
    header = ReadProcessMemory(h_process, module_base, 0x1000)
    pe_offset, = struct.unpack_from('<I', header, 0x3c)
    oh_offset = pe_offset + 24
    dir_offset = oh_offset + 96
    et_addr, et_size = struct.unpack_from('<II', header, dir_offset)
    
    # read export directory
    ed = ReadProcessMemory(h_process, module_base + et_addr, 0x1000)
    reserved, timestamp, v1, v2, rva_name, ordinal_base, num_addr_entries, num_names, rva_export_addrs, rva_names, rva_ordinals = struct.unpack_from('<IIHHIIIIIII', ed)
    
    # read func name offsets
    name_offsets = ReadProcessMemory(h_process, module_base + rva_names, 0x10000)
    func_offsets = struct.unpack_from('<'+'I'*num_names, name_offsets)
    
    # read func names
    names = ReadProcessMemory(h_process, module_base + func_offsets[0], 0x10000)
    base_offset = func_offsets[0]
    target_ordinals = [None] * len(proc_names)
    for i, func_offset in enumerate(func_offsets):
        off = func_offset - base_offset
        func_name = names[off:off+256].split(b'\x00')[0]
        for j, target_function in enumerate(proc_names):
            if target_function == func_name:
                target_ordinals[j] = i
                break
    
    # read ordinals
    ordinals = ReadProcessMemory(h_process, module_base + rva_ordinals, 0x10000)
    for i, target_ordinal in enumerate(target_ordinals):
        target_ordinals[i], = struct.unpack_from('<H', ordinals, target_ordinal*2)
    
    # read func rvas
    rvas = ReadProcessMemory(h_process, module_base + rva_export_addrs, 0x10000)
    addresses = [None] * len(proc_names)
    for i, ordinal in enumerate(target_ordinals):
        addresses[i] = module_base + struct.unpack_from('<I', rvas, ordinal*4)[0]
        if addresses[i] == 0:
            raise AddressNotFound(f'GetProcAddressEx("{proc_names[i]}")')
    
    return addresses

def GetModuleSizeEx(h_process, module_base):
    # read module header
    header = ReadProcessMemory(h_process, module_base, 0x1000)
    pe_offset, = struct.unpack_from('I', header, 0x3c)
    oh_offset = pe_offset + 24
    return struct.unpack_from('I', header, oh_offset + 56)[0]

class SharedBuffer:
    def __init__(self, address, start_offset, end_offset, read_offset_offset, write_offset_offset):
        # start
        self.start_offset = start_offset
        self.start_addr   = address + start_offset
        
        # end
        self.end_offset = end_offset
        self.end_addr   = address + end_offset
        
        # read offset
        self.read_offset        = self.start_offset
        self.read_offset_offset = read_offset_offset
        self.read_offset_addr   = address + read_offset_offset
        
        # write offset
        self.write_offset        = self.start_offset
        self.write_offset_offset = write_offset_offset
        self.write_offset_addr   = address + write_offset_offset

class TimedViewVector:
    def __init__(self, yaw, pitch, timestamp):
        self.yaw = yaw
        self.pitch = pitch
        self.timestamp = timestamp
    
    def __str__(self):
        return f'{self.yaw:.02f} {self.pitch:.02f} {self.timestamp}'

def calc_rel8(dst, src):
    return struct.pack('b', dst - (src + 2))

def calc_rel32(dst, src):
    return struct.pack('i', dst - (src + 5))

class ClientBridge:
    def emit_jmp8(self, dst):
        self.asm += b'\xeb' + calc_rel8(dst, self.code + len(self.asm))

    def emit_je8(self, dst):
        self.asm += b'\x74' + calc_rel8(dst, self.code + len(self.asm))

    def emit_jz8(self, dst):
        self.emit_je8(dst)

    def emit_jne8(self, dst):
        self.asm += b'\x75' + calc_rel8(dst, self.code + len(self.asm))

    def emit_jl8(self, dst):
        self.asm += b'\x7c' + calc_rel8(dst, self.code + len(self.asm))

    def emit_jmp32_from(self, dst, src):
        self.asm += b'\xe9' + calc_rel32(dst, src)

    def emit_jmp32(self, dst):
        self.emit_jmp32_from(dst, self.code + len(self.asm))

    def emit_call_from(self, dst, src):
        self.asm += b'\xe8' + calc_rel32(dst, src)

    def emit_call(self, dst):
        self.emit_call_from(dst, self.code + len(self.asm))

    def __init__(self, pid):
        self.replaying = False
        self.interp_view_vecs = []
        
        self.wm_callbacks = []
        
        # last view vector written to the buffer
        # predicted time that the last viewangle in the buffer will be read
        # if the buffer is empty it should be the current view vector
        self.last_view_vec = None 
        self.viewangle_read_period = None
        self.viewangle_read_total = 0
        self.last_read_ang_timestamp = None
        self.send_ang_capacity = 100
        
        self.pid = pid
        #self.h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
        self.h_process = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        if not self.h_process:
            raise RuntimeError
        #return # BUG IS BETWEEN THIS RETUR AND THE NEXT ONE
        
        module_bases = win32process.EnumProcessModulesEx(self.h_process, win32process.LIST_MODULES_ALL)
        self.modules = {win32process.GetModuleFileNameEx(self.h_process, base).split('\\')[-1].lower():base for base in module_bases}
        self.gta_sa_base = self.modules['gta_sa.exe']
        self.gta_sa_size = GetModuleSizeEx(self.h_process, self.gta_sa_base)
        self.samp_base = self.modules['samp.dll']
        self.samp_size = GetModuleSizeEx(self.h_process, self.samp_base)
        
        self.kernel32_base = self.modules['kernel32.dll']
        self.user32_base = self.modules['user32.dll']
        self.win32u_base = self.modules['win32u.dll']
        #return # BUG IS BETWEEN THIS RETUR AND THE NEXT ONE
        
        self.message_callback = None
        self.asm = b''
        self.code = None
        self.data = None
        #self.buffer = (ctypes.c_ubyte * 0x10000)()
        
        OpenFileMappingA, MapViewOfFile, GetSystemTimePreciseAsFileTime, Sleep, GetProcAddress = GetProcAddressEx(self.h_process, self.kernel32_base, ['OpenFileMappingA', 'MapViewOfFile', 'GetSystemTimePreciseAsFileTime', 'Sleep', 'GetProcAddress'])

        # shared memory (data) structure
        # 0   (4) recv msg buf read offset  
        # 4   (4) recv msg buf write offset 
        # 8   (4) send msg buf read offset  
        # c   (4) send msg buf write offset 
        # 10  (4) recv ang buf read offset  
        # 14  (4) recv ang buf write offset 
        # 18  (4) send ang buf read offset  
        # 1c  (4) send ang buf write offset
        # 20  (4) self.chat_timestamp_diff_addr
        # 24  (4) self.chat_timestamp_tmp_addr ; temporary storage; used in hook function
        # 100-200 (0x100) /dl string
        # fff (1) remote thread exit flag
        # [1000-3000[  recv_msg_buf    ; hooked functions in the target process write to this buffer and we read from it
        # [3000-5000[  send_msg_buf    ; we write to this buffer and a thread in the target process reads from it
        # [8000-c000[  recv_angles_buf ; a hooked function in the target process writes to this buffer every call and we read from it
        # [c000-10000[ send_angles_buf ; we write viewangles to this buffer; a hooked function in the target process reads from it
        self.sm = shared_memory.SharedMemory(name=None, create=True, size=0x10000)
        
        #patterns_and_masks = [
        #[b'\x8b\x15\x00\x00\x00\x00\x85\xd2\x55', 'xx????xxx'],
        #[b'\x83\xec\x10\x56\x8b\xf1\x8b\x86\xe0\x14\x00\x00', 'xxxxxxxxxxxx'],
        #[b'\x56\x8b\xf1\x8b\x86\xe0\x14\x00\x00\x85\xc0\x74', 'xxxxxxxxxxxx'],
        #[b'\x8b\x0d\x00\x00\x00\x00\x85\xc9\x5f\x5b', 'xx????xxxx'],
        #[b'\x56\x8b\xf1\x83\x3e\x00\x75\x00\x8b\x46\x00\x85\xc0', 'xxxxxxx?xx?xx'],
        #[b'\x56\x8b\xf1\x83\x3e\x00\x74\x00\x8b\x46\x00\x85\xc0\x74\x00\xc6\x40', 'xxxxxxx?xx?xxx?xx'],
        #[b'\xa1\x00\x00\x00\x00\x8b\x10\x33\xc9', 'x????xxxx'],
        #[b'\x8b\x10\x33\xc9\x85\xd2\x0f\x94\xc1\x89\x08', 'xxxxxxxxxxx'],
        #[b'\x8d\x4b\xfc\x51\xe8', 'xxxxx'],
        #]
        #self.g_chat_addr, \
        #self.samp_open_chat_addr, \
        #self.samp_close_chat_addr, \
        #self.g_tab_addr, \
        #self.samp_open_tab_addr, \
        #self.samp_close_tab_addr, \
        #self.g_kill_feed_visibility_ptr_ptr, \
        #self.samp_set_kill_feed_visibility_addr, \
        #self.samp_chat_timestamp_addr, \
        #= pattern_scan_batch(self.h_process, self.samp_base, self.samp_base + self.samp_size, patterns_and_masks)
        
        # get chat addresses
        # g_chat = [g_chat_addr]
        #self.g_chat_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '8b 15 00 00 00 00 85 d2 55', 'xx????xxx')
        
        self.g_chat_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '8b 15 ?? ?? ?? ?? 85 d2 55')
        self.g_chat_addr, = struct.unpack('I', ReadProcessMemory(self.h_process, self.g_chat_addr + 2, 4))
        #kernel32.ReadProcessMemory(self.h_process, self.g_chat_addr, ctypes.byref(self.buffer), 6, 0)
        #self.g_chat_addr, = struct.unpack_from('I', self.buffer, 2)
        #kernel32.ReadProcessMemory(self.h_process, self.samp_base + 0x26E9FC, ctypes.byref(self.buffer), 4, 0)
        
        #b = bytearray(self.buffer)
        #self.g_chat, = struct.unpack('I', b[:4])
        #self.samp_open_chat_addr = self.samp_base + 0x69440
        #self.samp_close_chat_addr = self.samp_base + 0x69540
        
        self.samp_open_chat_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '83 ec 10 56 8b f1 8b 86 e0 14 00 00')
        self.samp_close_chat_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '56 8b f1 8b 86 e0 14 00 00 85 c0 74')

        # get tab addresses
        # g_tab = [g_tab_addr]
        #self.g_tab_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '8b 0d 00 00 00 00 85 c9 5f 5b', 'xx????xxxx')
        self.g_tab_addr, = struct.unpack('I', ReadProcessMemory(self.h_process, pattern_scan(self.h_process, self.samp_base, self.samp_size, '8b 0d ?? ?? ?? ?? 85 c9 5f 5b') + 2, 4))
        #kernel32.ReadProcessMemory(self.h_process, self.g_tab_addr, ctypes.byref(self.buffer), 6, 0)
        #self.g_tab_addr, = struct.unpack_from('I', self.buffer, 2)
        
        #kernel32.ReadProcessMemory(self.h_process, self.samp_base + 0x26E9C4, ctypes.byref(self.buffer), 4, 0)
        #b = bytearray(self.buffer)
        #self.g_tab, = struct.unpack('I', b[:4])
        #self.samp_open_tab_addr = self.samp_base + 0x6f3a0
        #self.samp_close_tab_addr = self.samp_base + 0x6e9a0
        #self.samp_open_tab_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '56 8b f1 83 3e 00 75 00 8b 46 00 85 c0', 'xxxxxxx?xx?xx')
        #self.samp_open_tab_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '56 8b f1 83 3e 00 75 ?? 8b 46 ?? 85 c0')
        #self.samp_close_tab_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '56 8b f1 83 3e 00 74 00 8b 46 00 85 c0 74 00 c6 40', 'xxxxxxx?xx?xxx?xx')
        #self.samp_close_tab_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '56 8b f1 83 3e 00 74 ?? 8b 46 ?? 85 c0 74 ?? c6 40')
        
        # get kill feed addresses
        self.g_kill_feed_visibility_ptr_ptr, = struct.unpack('I', ReadProcessMemory(self.h_process, pattern_scan(self.h_process, self.samp_base, self.samp_size, 'a1 ?? ?? ?? ?? 8b 10 33 c9') + 1, 4))
        #kernel32.ReadProcessMemory(self.h_process, self.g_kill_feed_visibility_ptr_ptr, ctypes.byref(self.buffer), 5, 0)
        #self.g_kill_feed_visibility_ptr_ptr, = struct.unpack_from('I', self.buffer, 1)
        self.samp_set_kill_feed_visibility_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '8b 10 33 c9 85 d2 0f 94 c1 89 08') + 9
        #self.samp_set_kill_feed_visibility_addr += 9
        
        # gta_sa.exe@d9 06 8b 03 d9 ff; [ebx]=yaw [esi]=pitch ; read/write there
        self.samp_viewangles_addr = pattern_scan(self.h_process, self.gta_sa_base, self.gta_sa_size, 'd9 06 8b 03 d9 ff')
        
        #self.samp_base + 0x6799f
        self.samp_chat_timestamp_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '8d 4b fc 51 e8') + 3
        #self.samp_chat_timestamp_addr += 3
        #kernel32.ReadProcessMemory(self.h_process, self.samp_chat_timestamp_addr + 2, ctypes.byref(self.buffer), 4, 0)
        #self.localtime_addr = struct.unpack_from('i', self.buffer, 0)[0] + ((self.samp_chat_timestamp_addr + 1) + 5)
        self.localtime_addr = struct.unpack('i', ReadProcessMemory(self.h_process, self.samp_chat_timestamp_addr + 2, 4))[0] + ((self.samp_chat_timestamp_addr + 1) + 5)
        
        self.samp_hud_visibility_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '8b 41 08 85 c0 ba')
        
        #self.g_hud = pattern_scan(self.h_process, self.samp_base, self.samp_size, 'c3 8b 0d ?? ?? ?? ?? e8 ?? ?? ?? ?? 33 c0')
        #kernel32.ReadProcessMemory(self.h_process, self.g_hud + 3, ctypes.byref(self.buffer), 4, 0)
        #self.g_hud, = struct.unpack_from('i', self.buffer, 0)
        self.g_hud, = struct.unpack('i', ReadProcessMemory(self.h_process, pattern_scan(self.h_process, self.samp_base, self.samp_size, 'c3 8b 0d ?? ?? ?? ?? e8 ?? ?? ?? ?? 33 c0') + 3, 4))
        
        #kernel32.ReadProcessMemory(self.h_process, self.g_hud, ctypes.byref(self.buffer), 4, 0)
        #self.g_hud, = struct.unpack_from('i', self.buffer, 0)
        self.g_hud, = struct.unpack('i', ReadProcessMemory(self.h_process, self.g_hud, 4))
        
        self.g_hud_visibility_ptr = self.g_hud + 8
        #kernel32.ReadProcessMemory(self.h_process, self.samp_hud_visibility_addr + 12, ctypes.byref(self.buffer), 4, 0)
        #hud_redraw_offset, = struct.unpack_from('i', self.buffer, 0)
        hud_redraw_offset, = struct.unpack('i', ReadProcessMemory(self.h_process, self.samp_hud_visibility_addr + 12, 4))
        self.g_hud_redraw_ptr = self.g_hud + hud_redraw_offset
        
        self.wndproc_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, 'A1 ?? ?? ?? ?? 83 EC 10 83 F8 0A')
        
        # create shared memory on the client process
        FILE_MAP_ALL_ACCESS = 0xf001f
        # self.code -> page (0x1000)
        #self.code = kernel32.VirtualAllocEx(self.h_process, 0, 0x1000, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
        self.code = VirtualAllocEx(self.h_process, 0, 0x1000, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
        
        sm_addr = self.code + 0xffc
        name_address = self.code + 0x100
        encoded_name = self.sm.name.encode()
        #kernel32.WriteProcessMemory(self.h_process, name_address, encoded_name, len(encoded_name), 0)
        WriteProcessMemory(self.h_process, name_address, encoded_name)
        
        # call get shared memory handle from OpenFileMappingA()
        self.asm  = b'\x68' + name_address.to_bytes(4, 'little') # push sm.name
        self.asm += b'\x6a\x00' # push 0
        self.asm += b'\x68' + FILE_MAP_ALL_ACCESS.to_bytes(4, 'little') # push FILE_MAP_ALL_ACCESS 
        self.emit_call(OpenFileMappingA)
        #self.asm += b'\xe8' + calc_rel32(OpenFileMappingA, self.code + code_offset + 0xc)# call OpenFileMappingA
            # map share memory using MapViewOfFile()
        self.asm += b'\x6a\x00' # push 0
        self.asm += b'\x6a\x00' # push 0
        self.asm += b'\x6a\x00' # push 0
        self.asm += b'\x68' + FILE_MAP_ALL_ACCESS.to_bytes(4, 'little') # push FILE_MAP_ALL_ACCESS 
        self.asm += b'\x50' # push eax
        self.emit_call(MapViewOfFile)
        #asm += b'\xe8' + calc_rel32(MapViewOfFile, self.code + code_offset + 0x1d) # call MapViewOfFile
        self.asm += b'\xa3' + sm_addr.to_bytes(4, 'little') # mov [sm_addr], eax
        
        proc_addr_addr = self.code + 0x200
        proc_name_addr = self.code + 0x300
        for i, proc_name in enumerate([b'NtUserSetWindowPos', b'NtUserSetCursorPos', b'NtUserGetRawInputData']):
            WriteProcessMemory(self.h_process, (proc_name_addr + i*64), proc_name)
            self.asm += b'\x68' + (proc_name_addr + i*64).to_bytes(4, 'little') # push proc_name_addr
            self.asm += b'\x68' + self.win32u_base.to_bytes(4, 'little') # push win32ubase
            self.emit_call(GetProcAddress)
            self.asm += b'\xa3' + (proc_addr_addr + i*4).to_bytes(4, 'little') # mov [proc_addr_addr], eax
        
        self.asm += b'\xc3' # ret
        #self.asm += self.sm.name.encode() + b'\x00'
        #kernel32.WriteProcessMemory(self.h_process, self.code, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.code, self.asm)
        
        # get address where the shared memory(self.data) was mapped to in the client process
        #self.h_bootstrap_sm_thread = kernel32.CreateRemoteThread(self.h_process, 0, 0, self.code, 0, 0, 0)
        self.h_bootstrap_sm_thread, _ = CreateRemoteThread(self.h_process, None, 0, self.code, 0, 0)
        #ret = kernel32.WaitForSingleObject(self.h_bootstrap_sm_thread, 1000)
        ret = WaitForSingleObject(self.h_bootstrap_sm_thread, 1000)
        
        if ret != 0: # if not signaled
            raise Exception(f'self.h_bootstrap_sm_thread not signaled; return={ret:08x}')
        #kernel32.ReadProcessMemory(self.h_process, self.code, ctypes.byref(self.buffer), 0x1000, 0)
        #self.data, = struct.unpack_from('I', self.buffer, 0xffc)
        self.data, = struct.unpack('I', ReadProcessMemory(self.h_process, self.code + 0xffc, 4))
        NtUserSetWindowPos, NtUserSetCursorPos, NtUserGetRawInputData  = struct.unpack('III', ReadProcessMemory(self.h_process, proc_addr_addr, 12))
        
        self.dl_string_ref_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, 'e8 ?? ?? ?? ?? 50 53 8d 84 24')
        if SET_DL_STRING_ONLY_VEHICLE_HEALTH:
            #self.dl_string_ref_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, 'e8 00 00 00 00 50 53 8d 84 24', 'x????xxxxx')
            
            # read original overwritten code to restore in shutdown()
            #kernel32.ReadProcessMemory(self.h_process, self.dl_string_ref_addr - 11, ctypes.byref(self.buffer), 18, 0)
            #self.chat_timestamp_original_code = bytes(self.buffer[:18])
            self.chat_timestamp_original_code = ReadProcessMemory(self.h_process, self.dl_string_ref_addr - 11, 18)
            
            #kernel32.ReadProcessMemory(self.h_process, self.dl_string_ref_addr + 15, ctypes.byref(self.buffer), 4, 0)
            #self.chat_timestamp_original_dl_string_addr, = struct.unpack_from('I', self.buffer, 0)
            self.chat_timestamp_original_dl_string_addr, = struct.unpack('I', ReadProcessMemory(self.h_process, self.dl_string_ref_addr + 15, 4))
            
            # overwrite code
            dl_string = '%.1f'
            self.sm.buf[0x100:0x100+len(dl_string)] = dl_string.encode()
            #kernel32.WriteProcessMemory(self.h_process, self.dl_string_ref_addr - 11, b'\x83\xec\x0c\xdd\x1c\x24' + b'\x90'*12, 18, 0)
            WriteProcessMemory(self.h_process, self.dl_string_ref_addr - 11, b'\x83\xec\x0c\xdd\x1c\x24' + b'\x90'*12)
            #kernel32.WriteProcessMemory(self.h_process, self.dl_string_ref_addr + 15, (self.data + 0x100).to_bytes(4, 'little'), 4, 0)
            WriteProcessMemory(self.h_process, self.dl_string_ref_addr + 15, (self.data + 0x100).to_bytes(4, 'little'))
        
        #self.dl_show_addr = pattern_scan(self.h_process, self.samp_base, self.samp_size, '74 05 e8 ?? ?? ?? ?? a0')
        #kernel32.ReadProcessMemory(self.h_process, self.dl_show_addr + 8, ctypes.byref(self.buffer), 4, 0)
        #self.dl_show_addr, = struct.unpack_from('I', self.buffer)
        self.dl_show_addr, = struct.unpack('I', ReadProcessMemory(self.h_process, pattern_scan(self.h_process, self.samp_base, self.samp_size, '74 05 e8 ?? ?? ?? ?? a0') + 8, 4))
        if SHOW_DL_BY_DEFAULT:
            #kernel32.WriteProcessMemory(self.h_process, self.dl_show_addr, (1).to_bytes(1), 1, 0)
            WriteProcessMemory(self.h_process, self.dl_show_addr, b'\x01')
        
        self.gta_hwnd = win32gui.FindWindow(0, SAMP_WINDOW_NAME)
        
        GetFocus, GetActiveWindow, GetForegroundWindow, SetWindowPos, SetCursorPos, GetKeyState, GetAsyncKeyState, GetRawInputData = GetProcAddressEx(self.h_process, self.user32_base, ['GetFocus', 'GetActiveWindow', 'GetForegroundWindow', 'SetWindowPos', 'SetCursorPos', 'GetKeyState', 'GetAsyncKeyState', 'GetRawInputData'])
        #print(f'code={self.code:x} data={self.data:x} self.g_chat_addr={self.g_chat_addr:x} samp_open_chat_addr={self.samp_open_chat_addr:x} samp_close_chat_addr={self.samp_close_chat_addr:x}  self.g_kill_feed_visibility_ptr_ptr={self.g_kill_feed_visibility_ptr_ptr:x} samp_set_kill_feed_visibility_addr={self.samp_set_kill_feed_visibility_addr:x} self.samp_chat_timestamp_addr={self.samp_chat_timestamp_addr:x} self.localtime_addr={self.localtime_addr:x} self.dl_string_ref_addr={self.dl_string_ref_addr:x} self.dl_show_addr={self.dl_show_addr:x} self.samp_hud_visibility_addr={self.samp_hud_visibility_addr:x} self.g_hud_visibility_ptr={self.g_hud_visibility_ptr:x} self.g_hud_redraw_ptr={self.g_hud_redraw_ptr:x} self.wndproc_addr={self.wndproc_addr:x} GetFocus={GetFocus:x} GetActiveWindow={GetActiveWindow:x} GetForegroundWindow={GetForegroundWindow:x} NtUserSetWindowPos={NtUserSetWindowPos:x} NtUserSetCursorPos={NtUserSetCursorPos:x} NtUserGetRawInputData={NtUserGetRawInputData:x}')
         #self.g_tab_addr={self.g_tab_addr:x} samp_open_tab_addr={self.samp_open_tab_addr:x} samp_close_tab_addr={self.samp_close_tab_addr:x}
        # helper variables related to shared memory
        self.remote_thread_exit_flag_offset = 0xfff
        self.remote_thread_exit_flag_addr = self.data + self.remote_thread_exit_flag_offset

        # create shared buffers
        self.recv_msg_sb = SharedBuffer(self.data, 0x1000, 0x3000 - 0x100,  0x0,  0x4)
        self.send_msg_sb = SharedBuffer(self.data, 0x3000, 0x5000 - 0x100,  0x8,  0xc)
        self.recv_ang_sb = SharedBuffer(self.data, 0x8000, 0xc000  - 0x100, 0x10, 0x14)
        self.send_ang_sb = SharedBuffer(self.data, 0xc000, 0x10000 - 0x100, 0x18, 0x1c)
        
        # write their offsets to shared memory
        self.sm.buf[0:0x20] = self.recv_msg_sb.start_addr.to_bytes(4, 'little') + \
                              self.recv_msg_sb.start_addr.to_bytes(4, 'little') + \
                              self.send_msg_sb.start_addr.to_bytes(4, 'little') + \
                              self.send_msg_sb.start_addr.to_bytes(4, 'little') + \
                              self.recv_ang_sb.start_addr.to_bytes(4, 'little') + \
                              self.recv_ang_sb.start_addr.to_bytes(4, 'little') + \
                              self.send_ang_sb.start_addr.to_bytes(4, 'little') + \
                              self.send_ang_sb.start_addr.to_bytes(4, 'little')
    
        self.chat_timestamp_diff_offset = 0x20
        self.chat_timestamp_diff_addr = self.data + 0x20
        self.chat_timestamp_tmp_addr = self.data + 0x24
        self.set_chat_timestamp_diff(0)
        
        self.block_wndproc_offset = 0x30
        self.block_wndproc_addr = self.data + self.block_wndproc_offset
        
        self.block_input_offset = 0x34
        self.block_input_addr = self.data + self.block_input_offset
    
    
        # push timestamp(8) and id(1)[cl]
        write_timestamp_and_id_addr = self.code + len(self.asm)
        self.asm += b'\xa1' + self.recv_msg_sb.write_offset_addr.to_bytes(4, 'little') # mov eax, [self.recv_msg_sb.write_offset_addr]
        self.asm += b'\x50'         # push eax ; save eax
        self.asm += b'\x51'         # push ecx ; save ecx
        self.asm += b'\x50'         # push eax ; parameter
        self.emit_call(GetSystemTimePreciseAsFileTime)
        self.asm += b'\x59'         # pop ecx ; restore ecx
        self.asm += b'\x58'         # pop eax ; restore eax
        self.asm += b'\x83\xc0\x08' # add eax, 8
        self.asm += b'\x88\x08'     # mov byte [eax], cl
        self.asm += b'\x40'         # inc eax
        self.asm += b'\xc3'         # ret
        
        # update_write_offset(offset=eax)
        update_write_offset_addr = self.code + len(self.asm)
        self.asm += b'\x3d' + self.recv_msg_sb.end_addr.to_bytes(4, 'little') # cmp eax, self.recv_msg_sb.end_addr ; check if write offset is at the end
        self.asm += b'\x7c\x05' # jl
        self.asm += b'\xb8' + self.recv_msg_sb.start_addr.to_bytes(4, 'little') # mov eax, self.recv_msg_sb.start_addr ; then set it to the start
        self.asm += b'\xa3' + self.recv_msg_sb.write_offset_addr.to_bytes(4, 'little') # mov [self.recv_msg_sb.write_offset_addr], eax ; store the new write offset
        self.asm += b'\xc3' # ret
        
        # function to save id and timestamp and no payload; one param: cl(id)
        save_timestamp_no_payload_addr = self.code + len(self.asm)
        self.emit_call(write_timestamp_and_id_addr)
        self.emit_call(update_write_offset_addr)
        self.asm += b'\xc3' # ret
        
        # HOOKS
        
        # open_chat hook
        hk_open_chat_addr = self.code + len(self.asm)
        self.asm += b'\xb3' + CLIENT.CHAT_OPEN.to_bytes(1, 'little') # mov bl, CLIENT.CHAT_OPEN
        self.emit_call(save_timestamp_no_payload_addr) # save_timestamp_no_payload_addr
        o_open_chat = self.code + len(self.asm)
        self.asm += b'\x83\xec\x10\x56\x8b\xf1' # original instructions
        self.emit_jmp32(self.samp_open_chat_addr + 6)
        
        # close_chat hook
        hk_close_chat_addr = self.code + len(self.asm)
        self.asm += b'\xb3' + CLIENT.CHAT_CLOSE.to_bytes(1, 'little') # mov bl, CLIENT.CHAT_CLOSE
        self.emit_call(save_timestamp_no_payload_addr) # save_timestamp_no_payload_addr
        o_close_chat = self.code + len(self.asm)
        self.asm += b'\x56\x8b\xf1\x8b\x86\xe0\x14\x00\x00' # original instructions
        self.emit_jmp32(self.samp_close_chat_addr + 9)
        
        ## open_tab hook
        #hk_open_tab_addr = self.code + len(self.asm)
        #self.asm += b'\xb3' + CLIENT.TAB_OPEN.to_bytes(1) # mov bl, CLIENT.TAB_OPEN
        #self.emit_call(save_timestamp_no_payload_addr) # save_timestamp_no_payload_addr
        #o_open_tab = self.code + len(self.asm)
        #self.asm += b'\x56\x8b\xf1\x83\x3e\x00' # original instructions
        #self.emit_jmp32(self.samp_open_tab_addr + 6)
        #
        ## close_tab hook
        #hk_close_tab_addr = self.code + len(self.asm)
        #self.asm += b'\xb3' + CLIENT.TAB_CLOSE.to_bytes(1) # mov bl, CLIENT.TAB_CLOSE
        #self.emit_call(save_timestamp_no_payload_addr) # save_timestamp_no_payload_addr
        #o_close_tab = self.code + len(self.asm)
        #self.asm += b'\x56\x8b\xf1\x83\x3e\x00' # original instructions
        #self.emit_jmp32(self.samp_close_tab_addr + 6)
        
        # set kill feed visibility hook
        hk_kill_feed_show_addr = self.code + len(self.asm)
        self.asm += b'\x60' # pushad
        self.asm += b'\x51' # push ecx ; save payload
        self.asm += b'\xb1' + CLIENT.KILL_FEED_VISIBILITY.to_bytes(1, 'little') # mov cl, CLIENT.KILL_FEED_VISIBILITY
        self.emit_call(write_timestamp_and_id_addr)
        self.asm += b'\x59'     # pop ecx ; restore payload
        self.asm += b'\x88\x08' # mov [eax], cl ; write cl(payload)
        self.asm += b'\x40'     # inc eax
        self.emit_call(update_write_offset_addr)
        self.asm += b'\x61' # popd
        self.asm += b'\x89\x08\x33\xc0\xc3' # original instructions
        
        # viewangles hook; we read/write to them; [ebx]=yaw [esi]=pitch
        hk_viewangles_addr = self.code + len(self.asm)
        self.asm += b'\x50' # push eax ; save eax
        # # read viewangles from buffer and modify the real viewangles
        
        self.asm += b'\xa1' + self.send_ang_sb.read_offset_addr.to_bytes(4, 'little') # mov eax, [self.send_ang_sb.read_offset_addr]; get read offset
        self.asm += b'\x3b\x05' + self.send_ang_sb.write_offset_addr.to_bytes(4, 'little') # cmp eax, [self.send_ang_sb.write_offset_addr] ; if read offset != write offset
        self.asm += b'\x74\x1d' # je write_viewangles
        
        self.asm += b'\xff\x30' # push [eax]
        self.asm += b'\x8f\x03' # pop [ebx] ; yaw (horizontal)
        self.asm += b'\xff\x70\x04' # push [eax+4]
        self.asm += b'\x8f\x06' # pop [esi] ; pitch (vertical)
        
        self.asm += b'\x83\xc0\x08' # add eax, 8
        self.asm += b'\x3d' + self.send_ang_sb.end_addr.to_bytes(4, 'little') # cmp eax, self.send_ang_sb.end_addr ; check if read offset is at the end
        self.asm += b'\x7c\x05' # jl update read offset
        self.asm += b'\xb8' + self.send_ang_sb.start_addr.to_bytes(4, 'little') # mov eax, self.send_ang_sb.start_addr ; then set it to the start
        self.asm += b'\xa3' + self.send_ang_sb.read_offset_addr.to_bytes(4, 'little') # mov [self.send_ang_sb.read_offset_addr], eax ; update read offset
        
         # write viewangles to buffer so we can get them from python
        self.asm += b'\xa1' + self.recv_ang_sb.write_offset_addr.to_bytes(4, 'little') # mov eax, [self.recv_ang_sb.write_offset_addr]
        self.asm += b'\x60' # pushad
        self.asm += b'\x50' # push eax
        self.emit_call(GetSystemTimePreciseAsFileTime)
        self.asm += b'\x61' # popad
        self.asm += b'\xff\x33'     # push [ebx]
        self.asm += b'\x8f\x40\x08' # pop [eax + 8]
        self.asm += b'\xff\x36'     # push [esi]
        self.asm += b'\x8f\x40\x0c' # pop [eax + 12]
        self.asm += b'\x83\xc0\x10' # add eax, 16
        self.asm += b'\x3d' + self.recv_ang_sb.end_addr.to_bytes(4, 'little') # cmp eax, self.recv_ang_sb.end_addr ; check if write offset is at the end
        self.asm += b'\x7c\x05' # jl
        self.asm += b'\xb8' + self.recv_ang_sb.start_addr.to_bytes(4, 'little') # mov eax, self.recv_ang_sb.start_addr ; then set it to the start
        self.asm += b'\xa3' + self.recv_ang_sb.write_offset_addr.to_bytes(4, 'little') # mov [self.recv_ang_sb.write_offset_addr], eax ; store the new write offset
        self.asm += b'\x58' # pop eax ; restore eax
        self.asm += b'\xd9\x06\x8b\x03\xd9\xff' # original instructions
        self.emit_jmp32(self.samp_viewangles_addr + 6)
        
        # chat timestamp hook
        hk_chat_timestamp_addr = self.code + len(self.asm)
        self.asm += b'\x8b\x01' # mov eax, [ecx] ; get timestamp
        self.asm += b'\x85\xc0' # test eax, eax  ; check if valid
        self.asm += b'\x74\x06' # jz ; if zero, return
        #self.asm += b'\x2b\x05' + self.chat_timestamp_diff_addr.to_bytes(4, 'little') # sub eax, [self.chat_timestamp_diff_addr]
        self.asm += b'\x03\x05' + self.chat_timestamp_diff_addr.to_bytes(4, 'little') # sub eax, [self.chat_timestamp_diff_addr]
        self.asm += b'\xa3' + self.chat_timestamp_tmp_addr.to_bytes(4, 'little') # mov [self.chat_timestamp_tmp_addr], eax
        self.asm += b'\x68' +  self.chat_timestamp_tmp_addr.to_bytes(4, 'little') # push self.chat_timestamp_tmp_addr
        self.emit_call(self.localtime_addr) # original instructions
        self.emit_jmp32(self.samp_chat_timestamp_addr + 6)
        
        # hud visibility hook
        hk_hud_visibility_addr = self.code + len(self.asm)
        self.asm += b'\x60' # pushad
        self.asm += b'\xff\x71\x08' # push [ecx+8] ; push current hud visibility
        self.asm += b'\xb1' + CLIENT.HUD_VISIBILITY.to_bytes(1, 'little') # mov cl, CLIENT.HUD_VISIBILITY
        self.emit_call(write_timestamp_and_id_addr)
        self.asm += b'\x8f\x00' # pop [eax] ; write current hud visibility(payload)
        self.asm += b'\x40'     # inc eax
        self.emit_call(update_write_offset_addr)
        self.asm += b'\x61' # popd
        self.asm += b'\x8b\x41\x08\x85\xc0' # original instructions
        self.emit_jmp32(self.samp_hud_visibility_addr + 5)
        
        # hud visibility hook
        #kernel32.ReadProcessMemory(self.h_process, self.wndproc_addr, ctypes.byref(self.buffer), 5, 0)
        #self.wndproc_original_bytes = bytes(self.buffer[:5])
        self.wndproc_original_bytes = ReadProcessMemory(self.h_process, self.wndproc_addr,  5)
        
        wndproc_trampoline_addr = self.code + len(self.asm) # trampoline
        self.asm += self.wndproc_original_bytes
        self.emit_jmp32(self.wndproc_addr + 5)
        
        hk_wndproc_end_addr = self.code + len(self.asm)
        self.emit_call(GetForegroundWindow) # GetForegroundWindow()
        self.asm += b'\x3d' + self.gta_hwnd.to_bytes(4, 'little') # cmp eax, self.gta_hwnd
        self.asm += b'\x74\x03' # je $+3
        self.asm += b'\x31\xc0\xc3' # mov eax, 0; ret
        # block wndproc if variable is set
        self.asm += b'\x80\x3d' + self.block_wndproc_addr.to_bytes(4, 'little') + b'\x00' # cmp byte[self.block_wndproc_addr], 0
        self.emit_jz8(wndproc_trampoline_addr)
        self.asm += b'\x31\xc0\xc3' # mov eax, 0; ret
        
        hk_wndproc_push_msg_addr = self.code + len(self.asm)
        self.asm += b'\xb1' + CLIENT.WNDPROC_MESSAGE.to_bytes(1, 'little') # mov cl, CLIENT.WNDPROC_MESSAGE
        self.emit_call(write_timestamp_and_id_addr)
        self.asm += b'\x8b\x4c\x24\x08' # mov ecx, [esp+8] ; write msg
        self.asm += b'\x89\x48\x00' # mov [eax], ecx
        self.asm += b'\x8b\x4c\x24\x0c' # mov ecx, [esp+c] ; write wparam
        self.asm += b'\x89\x48\x04' # mov [eax+4], ecx
        self.asm += b'\x8b\x4c\x24\x10' # mov ecx, [esp+10] ; write lparam
        self.asm += b'\x89\x48\x08' # mov [eax+8], ecx
        self.asm += b'\x83\xc0\x0c' # eax += 3*4
        self.emit_call(update_write_offset_addr)
        self.emit_jmp8(hk_wndproc_end_addr)
        
        hk_wndproc_addr = self.code + len(self.asm)
        #print(f'hk_wndproc_addr={hk_wndproc_addr:x}')
        self.asm += b'\x8b\x44\x24\x08' # mov eax, [esp+8] ; msg
        for x in [win32con.WM_NCACTIVATE, win32con.WM_KEYDOWN, win32con.WM_SYSKEYDOWN, win32con.WM_KEYUP, win32con.WM_SYSKEYUP, win32con.WM_MOUSEWHEEL]:
            self.asm += b'\x3d' + (x).to_bytes(4, 'little') # cmp msg, x
            self.emit_je8(hk_wndproc_push_msg_addr)
        self.emit_jmp8(hk_wndproc_end_addr)
        
        hk_ret_gta_hwnd_addr = self.code + len(self.asm)
        self.asm += b'\xb8' + self.gta_hwnd.to_bytes(4, 'little') # mov eax, self.gta_hwnd
        self.asm += b'\xc3' # ret
        
        hk_set_window_pos = self.code + len(self.asm)
        self.asm += b'\xc7\x44\x24\x08' + b'\xfe\xff\xff\xff' # mov [esp + 8], HWND_NOTOPMOST
        self.emit_jmp32(NtUserSetWindowPos)
        
        # GetKeyState hook
        hk_get_key_state = self.code + len(self.asm)
        self.asm += b'\x80\x3d' + self.block_input_addr.to_bytes(4, 'little') + b'\x00' # cmp byte [block_input], 0
        self.asm += b'\x74\x05' # je $+5; if not blocked, go to original code
        self.asm += b'\x31\xc0' # eax = 0
        self.asm += b'\xc2\x04\x00' # ret 4
        self.asm += b'\x8b\xff\x55\x8b\xec' # original code
        self.emit_jmp32(GetKeyState + 5)
        
        # GetAsyncKeyState hook
        hk_get_aync_key_state = self.code + len(self.asm)
        self.asm += b'\x80\x3d' + self.block_input_addr.to_bytes(4, 'little') + b'\x00' # cmp byte [block_input], 0
        self.asm += b'\x74\x05' # je $+5; if not blocked, go to original code
        self.asm += b'\x31\xc0' # eax = 0
        self.asm += b'\xc2\x04\x00' # ret 4
        self.asm += b'\x8b\xff\x55\x8b\xec' # original code
        self.emit_jmp32(GetAsyncKeyState + 5)
        
        # SetCursorPos hook
        hk_set_cursor_pos = self.code + len(self.asm)
        self.asm += b'\x80\x3d' + self.block_input_addr.to_bytes(4, 'little') + b'\x00' # cmp byte [block_input], 0
        self.asm += b'\x74\x08' # je $+8; if not blocked, go to original code
        self.asm += b'\xb8\x01\x00\x00\x00' # eax = 1
        self.asm += b'\xc2\x08\x00' # ret 8
        self.emit_jmp32(NtUserSetCursorPos) # original code
        
        # GetRawInputData hook
        hk_get_raw_input_data = self.code + len(self.asm)
        self.asm += b'\x80\x3d' + self.block_input_addr.to_bytes(4, 'little') + b'\x00' # cmp byte [block_input], 0
        self.asm += b'\x74\x05' # je $+5; if not blocked, go to original code
        self.asm += b'\x31\xc0' # eax = 0
        self.asm += b'\xc2\x14\x00' # ret 20
        self.emit_jmp32(NtUserGetRawInputData) # original code
        
        
        # function to execute actions(i.e. call functions) from the send_msg_buf
        
        # open_chat()
        self.open_chat_addr = self.code + len(self.asm)
        self.asm += b'\x8b\x0d' + self.g_chat_addr.to_bytes(4, 'little') # mov ecx, [g_chat_addr]
        self.emit_call(o_open_chat)
        self.asm += b'\xc3' # ret
        
        # close_chat()
        self.close_chat_addr = self.code + len(self.asm)
        self.asm += b'\x8b\x0d' + self.g_chat_addr.to_bytes(4, 'little') # mov ecx, [g_chat_addr]
        self.emit_call(o_close_chat)
        self.asm += b'\xc3' # ret
        
        ## open_tab()
        #self.open_tab_addr = self.code + len(self.asm)
        #self.asm += b'\x8b\x0d' + self.g_tab_addr.to_bytes(4, 'little') # mov ecx, [g_tab_addr]
        #self.emit_call(o_open_tab)
        #self.asm += b'\xc3' # ret
        #
        ## close_tab()
        #self.close_tab_addr = self.code + len(self.asm)
        #self.asm += b'\x8b\x0d' + self.g_tab_addr.to_bytes(4, 'little') # mov ecx, [g_tab_addr]
        #self.asm += b'\x6a\x01' # push 1
        #self.emit_call(o_close_tab)
        #self.asm += b'\xc3' # ret
        
        # set_kill_feed_visibility(visibility=al)
        self.set_kill_feed_visibility_addr = self.code + len(self.asm)
        self.asm += b'\x8b\x1d' + self.g_kill_feed_visibility_ptr_ptr.to_bytes(4, 'little') # mov ebx, [g_kill_feed_visibility_ptr_ptr] ; get ptr
        self.asm += b'\x88\x03' # mov [ebx], al
        self.asm += b'\xc3' # ret
        
        # set_hud_visibility(visibility=al)
        self.set_hud_visibility = self.code + len(self.asm)
        self.asm += b'\xa2' + self.g_hud_visibility_ptr.to_bytes(4, 'little') # mov [self.g_hud_visibility_ptr], al ; set visibility
        self.asm += b'\xb8\x01\x00\x00\x00' # mov eax, 1 ; force redraw
        self.asm += b'\xa3' + self.g_hud_redraw_ptr.to_bytes(4, 'little') # mov [self.g_hud_redraw_ptr], eax ; force redraw
        self.asm += b'\xc3' # ret
        
        # i'll use procedures because manually counting bytes for jumps is painful
        check_open_chat_addr = self.code + len(self.asm)
        self.asm += b'\x3c' + CLIENT.CHAT_OPEN.to_bytes(1, 'little') # cmp al, CLIENT.CHAT_OPEN ; cmp_chat_open
        self.asm += b'\x74\x03\xb3\x00\xc3' # if not equal return zero(bl)
        self.emit_call(self.open_chat_addr) # call open_chat
        self.asm += b'\xb3\x01\xc3' # return one(bl)
        
        check_close_chat_addr = self.code + len(self.asm)
        self.asm += b'\x3c' + CLIENT.CHAT_CLOSE.to_bytes(1, 'little') # cmp al, CLIENT.CHAT_CLOSE  ; cmp_chat_close
        self.asm += b'\x74\x03\xb3\x00\xc3' # if not equal return zero(bl)
        self.emit_call(self.close_chat_addr) # call close_chat
        self.asm += b'\xb3\x01\xc3' # return one(bl)
        
        #self.asm += b'\x3c' + CLIENT.TAB_OPEN.to_bytes(1) # cmp al, CLIENT.TAB_OPEN ; cmp_tab_open
        #self.asm += b'\x75\x07' # jne cmp_tab_close
        #self.emit_call(self.open_tab_addr) # call open_tab
        #self.emit_jmp8(loop_start_addr) # jmp loop_start
        #
        #self.asm += b'\x3c' + CLIENT.TAB_CLOSE.to_bytes(1) # cmp al, CLIENT.TAB_CLOSE ; cmp_tab_close
        #self.asm += b'\x75\x07' # jne 
        #self.emit_call(self.close_tab_addr) # call close_tab
        #self.emit_jmp8(loop_start_addr) # jmp loop_start
                
        check_set_kill_feed_visibility_addr = self.code + len(self.asm)
        self.asm += b'\x3c' + CLIENT.KILL_FEED_VISIBILITY.to_bytes(1, 'little') # cmp al, CLIENT.KILL_FEED_VISIBILITY
        self.asm += b'\x74\x03\xb3\x00\xc3' # if not equal return zero(bl)
        self.asm += b'\x8a\x06' # mov al, byte [esi]
        self.asm += b'\x46' # inc esi
        self.emit_call(self.set_kill_feed_visibility_addr) # call set_kill_feed_visibility_addr
        self.asm += b'\xb3\x01\xc3' # return one(bl)
        
        check_set_hud_visibility_addr = self.code + len(self.asm)
        self.asm += b'\x3c' + CLIENT.HUD_VISIBILITY.to_bytes(1, 'little') # cmp al, CLIENT.HUD_VISIBILITY
        self.asm += b'\x74\x03\xb3\x00\xc3' # if not equal return zero(bl)
        self.asm += b'\x8a\x06' # mov al, byte [esi]
        self.asm += b'\x46' # inc esi
        self.emit_call(self.set_hud_visibility) # call set_hud_visibility
        self.asm += b'\xb3\x01\xc3' # return one(bl)
        
        # function to process send_msg_buf where messages are added from self.push_message()
        process_send_msg_buf_addr = self.code + len(self.asm)
        # get read and write offsets
        self.asm += b'\x8b\x35' + self.send_msg_sb.read_offset_addr.to_bytes(4, 'little') # mov esi, [self.send_msg_sb.read_offset_addr] ; get read offset
        loop_start_sleep_addr = self.code + len(self.asm)
        self.asm += b'\x8b\x3d' + self.send_msg_sb.write_offset_addr.to_bytes(4, 'little') # mov edi, [self.send_msg_sb.write_offset_addr] ; get write offset
        # check exit flag
        self.asm += b'\x80\x3d' + self.remote_thread_exit_flag_addr.to_bytes(4, 'little') + b'\x01' # cmp [self.remote_thread_exit_flag_addr], 0x01 ; test exit flag
        self.asm += b'\x75\x01\xc3' # exit if exit flag is set
        # sleep
        self.asm += b'\x68' + REMOTE_READ_SB_INTERVAL.to_bytes(4, 'little') # push REMOTE_READ_SB_INTERVAL
        self.emit_call(Sleep) # Sleep(REMOTE_READ_SB_INTERVAL) 
        loop_start_sleep_no_sleep_addr = self.code + len(self.asm)
        # fix offset
        self.asm += b'\x81\xfe' + self.send_msg_sb.end_addr.to_bytes(4, 'little') # cmp esi, self.send_msg_sb.end_addr
        self.asm += b'\x7c\x05' # jl
        self.asm += b'\xbe'+ self.send_msg_sb.start_addr.to_bytes(4, 'little') # mov esi, self.send_msg_sb.start_addr
        self.asm += b'\x3b\xf7' # cmp esi, edi ; loop_start,  if read offset == write offset, loop again
        self.emit_je8(loop_start_sleep_addr) # je loop_start_sleep_addr
        # get id
        self.asm += b'\x8a\x06' # mov al, [esi]
        self.asm += b'\x46'     # inc esi
        # checks
        self.emit_call(check_open_chat_addr)
        self.asm += b'\x80\xfb\x01'; self.emit_je8(loop_start_sleep_no_sleep_addr) # jmp loop start(no sleep) if ret(bl) 1
        self.emit_call(check_close_chat_addr)
        self.asm += b'\x80\xfb\x01'; self.emit_je8(loop_start_sleep_no_sleep_addr) # jmp loop start(no sleep) if ret(bl) 1
        self.emit_call(check_set_kill_feed_visibility_addr)
        self.asm += b'\x80\xfb\x01'; self.emit_je8(loop_start_sleep_no_sleep_addr) # jmp loop start(no sleep) if ret(bl) 1
        self.emit_call(check_set_hud_visibility_addr)
        self.asm += b'\x80\xfb\x01'; self.emit_je8(loop_start_sleep_no_sleep_addr) # jmp loop start(no sleep) if ret(bl) 1
        # update offset
        #self.asm += b'\x89\x3d' + self.send_msg_sb.read_offset_addr.to_bytes(4, 'little') # ; mov [self.send_msg_buf.read_offset_addr], edi ;set read offset  = write offset
        self.emit_jmp8(loop_start_sleep_addr)
        
        # write asm to self.code
        #kernel32.WriteProcessMemory(self.h_process, self.code, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.code, self.asm)
        
        # open chat hook
        self.asm = b''
        self.emit_jmp32_from(hk_open_chat_addr, self.samp_open_chat_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_open_chat_addr, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.samp_open_chat_addr, self.asm)
        
        # close chat hook
        self.asm = b''
        self.emit_jmp32_from(hk_close_chat_addr, self.samp_close_chat_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_close_chat_addr, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.samp_close_chat_addr, self.asm)
        
        ## open_tab hook
        #self.asm = b''
        #self.emit_jmp32_from(hk_open_tab_addr, self.samp_open_tab_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_open_tab_addr, self.asm, len(self.asm), 0)
        #
        ## close tab hook
        #self.asm = b''
        #self.emit_jmp32_from(hk_close_tab_addr, self.samp_close_tab_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_close_tab_addr, self.asm, len(self.asm), 0)
        
        # kill feed visibility hook
        self.asm = b''
        self.emit_jmp32_from(hk_kill_feed_show_addr, self.samp_set_kill_feed_visibility_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_set_kill_feed_visibility_addr, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.samp_set_kill_feed_visibility_addr, self.asm)
        
        # view angles hook
        self.asm = b''
        self.emit_jmp32_from(hk_viewangles_addr, self.samp_viewangles_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_viewangles_addr, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.samp_viewangles_addr, self.asm)
        
        # chat timestamp hook
        self.asm = b''
        self.emit_jmp32_from(hk_chat_timestamp_addr, self.samp_chat_timestamp_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_chat_timestamp_addr, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.samp_chat_timestamp_addr, self.asm)
        
        # hud visibility hook
        self.asm = b''
        self.emit_jmp32_from(hk_hud_visibility_addr, self.samp_hud_visibility_addr)
        #kernel32.WriteProcessMemory(self.h_process, self.samp_hud_visibility_addr, self.asm, len(self.asm), 0)
        WriteProcessMemory(self.h_process, self.samp_hud_visibility_addr, self.asm)
        
        # wndproc hook
        self.asm = b''
        self.emit_jmp32_from(hk_wndproc_addr, self.wndproc_addr)
        WriteProcessMemory(self.h_process, self.wndproc_addr, self.asm)
        
        # GetFocus, GetActiveWindow hook
        for func in [GetFocus, GetActiveWindow]:
            self.asm = b''
            self.emit_jmp32_from(hk_ret_gta_hwnd_addr, func)
            WriteProcessMemory(self.h_process, func, self.asm)
            #kernel32.WriteProcessMemory(self.h_process, func, self.asm, len(self.asm), 0)
        
        # GetKeyState hook
        self.asm = b''
        self.emit_jmp32_from(hk_get_key_state, GetKeyState)
        WriteProcessMemory(self.h_process, GetKeyState, self.asm)
        
        # GetAsyncKeyState hook
        self.asm = b''
        self.emit_jmp32_from(hk_get_aync_key_state, GetAsyncKeyState)
        WriteProcessMemory(self.h_process, GetAsyncKeyState, self.asm)
        
        # SetCursorPos hook
        self.asm = b''
        self.emit_jmp32_from(hk_set_cursor_pos, SetCursorPos)
        WriteProcessMemory(self.h_process, SetCursorPos, self.asm)
        
        # GetRawInputData hook
        self.asm = b''
        self.emit_jmp32_from(hk_get_raw_input_data, GetRawInputData)
        WriteProcessMemory(self.h_process, GetRawInputData, self.asm)
        
        # SetWindowPos hook
        self.asm = b''
        self.emit_jmp32_from(hk_set_window_pos, SetWindowPos)
        WriteProcessMemory(self.h_process, SetWindowPos, self.asm)
        #kernel32.WriteProcessMemory(self.h_process, SetWindowPos, self.asm, len(self.asm), 0)

        #self.h_process_sm_buf_thread = kernel32.CreateRemoteThread(self.h_process, 0, 0, process_send_msg_buf_addr, 0, 0, 0)
        self.h_process_sm_buf_thread = CreateRemoteThread(self.h_process, None, 0, process_send_msg_buf_addr, 0, 0)
    
    def shutdown(self):
        return
        # restore open chat hook
        self.asm = b'\x83\xec\x10\x56\x8b\xf1'
        kernel32.WriteProcessMemory(self.h_process, self.samp_open_chat_addr, self.asm, len(self.asm), 0)
        
        # restore close chat hook
        self.asm = b'\x56\x8b\xf1\x8b\x86\xe0\x14\x00\x00'
        kernel32.WriteProcessMemory(self.h_process, self.samp_close_chat_addr, self.asm, len(self.asm), 0)
        
        ## restore open tab hook
        #self.asm = b'\x56\x8b\xf1\x83\x3e\x00'
        #kernel32.WriteProcessMemory(self.h_process, self.samp_open_tab_addr, self.asm, len(self.asm), 0)
        #
        ## restore close tab hook
        #self.asm = b'\x56\x8b\xf1\x83\x3e\x00'
        #kernel32.WriteProcessMemory(self.h_process, self.samp_close_tab_addr, self.asm, len(self.asm), 0)
        
        # restore kill feed visibiliyu hook
        self.asm = b'\x89\x08\x33\xC0\xC3'
        kernel32.WriteProcessMemory(self.h_process, self.samp_set_kill_feed_visibility_addr, self.asm, len(self.asm), 0)
        
        # restore viewangles hook
        self.asm = b'\xd9\x06\x8b\x03\xd9\xff'
        kernel32.WriteProcessMemory(self.h_process, self.samp_viewangles_addr, self.asm, len(self.asm), 0)
        
        # restore chat timestamp hook
        self.asm = b'\x51'
        self.emit_call_from(self.localtime_addr, self.samp_chat_timestamp_addr + 1)
        kernel32.WriteProcessMemory(self.h_process, self.samp_chat_timestamp_addr, self.asm, len(self.asm), 0)
        
        # restore /dl string
        kernel32.WriteProcessMemory(self.h_process, self.dl_string_ref_addr + 15, self.chat_timestamp_original_dl_string_addr.to_bytes(4, 'little'), 4, 0)
        kernel32.WriteProcessMemory(self.h_process, self.dl_string_ref_addr - 11, self.chat_timestamp_original_code, len(self.chat_timestamp_original_code), 0)
        
        # restore dl value
        if SHOW_DL_BY_DEFAULT:
            kernel32.WriteProcessMemory(self.h_process, self.dl_show_addr, (0).to_bytes(1), 1, 0)
        
        # restore hud visibility hook
        self.asm = b'\x8b\x41\x08\x85\xc0'
        kernel32.WriteProcessMemory(self.h_process, self.samp_hud_visibility_addr, self.asm, len(self.asm), 0)
        
        # restore wndproc
        kernel32.WriteProcessMemory(self.h_process, self.wndproc_addr, self.wndproc_original_bytes, len(self.wndproc_original_bytes), 0)
        
        # shutdown remote thread
        self.sm.buf[self.remote_thread_exit_flag_offset] = 1
        #ret = kernel32.WaitForSingleObject(self.h_process_sm_buf_thread, 500)
        ret = WaitForSingleObject(self.h_process_sm_buf_thread, 500)
        if ret != 0: # if not signaled
            raise Exception(f'h_process_sm_buf_thread not signaled; return={ret:08x}')
        
        # free memory
        MEM_RELEASE = 0x00008000
        kernel32.VirtualFreeEx(self.h_process, self.code, 0, MEM_RELEASE)
        self.sm.buf[0:0x10000] = bytearray(0x10000)
    
    def block_wndproc(self, should_block):
        self.sm.buf[self.block_wndproc_offset] = int(should_block)
    
    def block_input(self, should_block):
        self.sm.buf[self.block_input_offset] = int(should_block)
    
    def set_chat_timestamp_diff(self, diff): # in s
        self.sm.buf[self.chat_timestamp_diff_offset:self.chat_timestamp_diff_offset+4] = struct.pack('i', diff)
    
    def interpolate_viewangles_until(self, timed_view_vector):
        #print(f'interpolate_viewangles_until: {timed_view_vector.yaw} {timed_view_vector.pitch} {timed_view_vector.timestamp}')
        # add
        self.interp_view_vecs.append(timed_view_vector)
        # sort by timestamp
        self.interp_view_vecs = sorted(self.interp_view_vecs, key=lambda v: v.timestamp)
    
    def push_message(self, id, payload=b''):
        o = id.to_bytes(1, 'little') + payload
        
        self.sm.buf[self.send_msg_sb.write_offset:self.send_msg_sb.write_offset+len(o)] = o
        
        # boundary check
        self.send_msg_sb.write_offset += len(o)
        if self.send_msg_sb.write_offset >= self.send_msg_sb.end_offset:
            self.send_msg_sb.write_offset = self.send_msg_sb.start_offset
        # write new offset to shared memory
        #print(f'push_message id={id} wo={self.send_msg_sb.write_offset:x} {payload.hex(" ")}')
        self.sm.buf[self.send_msg_sb.write_offset_offset:self.send_msg_sb.write_offset_offset+4] = (self.data + self.send_msg_sb.write_offset).to_bytes(4, 'little')

    # read messages from shared memory and call message_callback
    def process_msg_shared_buffer(self):
        # read write offset
        write_offset, = struct.unpack_from('I', self.sm.buf, self.recv_msg_sb.write_offset_offset)
        write_offset -= self.data
        
        # amount written is unknown because messages have variable sizes
        while self.recv_msg_sb.read_offset != write_offset:
            file_time, id = struct.unpack_from('<QB', self.sm.buf, self.recv_msg_sb.read_offset)
            self.recv_msg_sb.read_offset += 9
            timestamp = (file_time - UNIX_TIME_START) // TICKS_PER_MS # ms since epoch
            timestamp //= 1000 # seconds since epoch
            
            payload = b''
            if id == CLIENT.KILL_FEED_VISIBILITY:
                payload = bytearray(self.sm.buf[self.recv_msg_sb.read_offset:self.recv_msg_sb.read_offset+1]) # visible(u8)
                self.recv_msg_sb.read_offset += 1
            elif id == CLIENT.HUD_VISIBILITY:
                # read visibility before change
                visibility = bytearray(self.sm.buf[self.recv_msg_sb.read_offset:self.recv_msg_sb.read_offset+1])[0]
                # determine new visibility
                # 2 1 0, 2 1 0, ...
                if visibility == 0:
                    visibility = 2
                else:
                    visibility -= 1
                payload = visibility.to_bytes(1, 'little')
                self.recv_msg_sb.read_offset += 1
            elif id == CLIENT.WNDPROC_MESSAGE:
                msg, wparam, lparam = struct.unpack_from('<III', self.sm.buf, self.recv_msg_sb.read_offset)
                self.recv_msg_sb.read_offset += 12
                
                if msg == win32con.WM_NCACTIVATE:
                    deactivate_window = wparam == 0
                    x=win32gui.SetWindowPos(self.gta_hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                    
                    self.block_input(should_block=deactivate_window)
                
                for callback in self.wm_callbacks:
                    callback(msg, wparam, lparam)
            
            if self.message_callback and id != CLIENT.WNDPROC_MESSAGE:
                self.message_callback(id, timestamp, payload)
                #print(f'message_callback({id}, {timestamp}({time.time()}), {payload.hex(" ")}')
            
            if self.recv_msg_sb.read_offset >= self.recv_msg_sb.end_offset:
                self.recv_msg_sb.read_offset = self.recv_msg_sb.start_offset
    
    def write_send_ang(self, yaw, pitch):
        self.sm.buf[self.send_ang_sb.write_offset:self.send_ang_sb.write_offset+8] = struct.pack('ff', yaw, pitch)
        self.send_ang_sb.write_offset += 8 
        if self.send_ang_sb.write_offset == self.send_ang_sb.end_offset:
            self.send_ang_sb.write_offset = self.send_ang_sb.start_offset
    
    def update_send_ang_write_offset(self):
        self.send_ang_sb.write_offset_addr = self.data + self.send_ang_sb.write_offset
        self.sm.buf[self.send_ang_sb.write_offset_offset:self.send_ang_sb.write_offset_offset+4] = self.send_ang_sb.write_offset_addr.to_bytes(4, 'little')
    
    def process_ang_shared_buffer(self):
        # read write offset
        write_offset, = struct.unpack_from('I', self.sm.buf, self.recv_ang_sb.write_offset_offset)
        write_offset -= self.data
        
        # read viewangles
        if self.recv_ang_sb.read_offset > write_offset: # the write pointer wrote to the end then to the start of the buffer
            count = (self.recv_ang_sb.end_offset - self.recv_ang_sb.read_offset) // 16
            viewangles = struct.unpack_from('<' + 'Qff' * count, self.sm.buf, self.recv_ang_sb.read_offset)
            
            count = (write_offset - self.recv_ang_sb.start_offset) // 16
            viewangles += struct.unpack_from('<' + 'Qff' * count, self.sm.buf, self.recv_ang_sb.start_offset)
        else:
            count = (write_offset - self.recv_ang_sb.read_offset) // 16
            viewangles = struct.unpack_from('<' + 'Qff' * count, self.sm.buf, self.recv_ang_sb.read_offset)
        
        write_count = len(viewangles) // 3
        
        for i in range(write_count):
            file_time, yaw, pitch = viewangles[i*3:(i+1)*3]
            timestamp = (file_time - UNIX_TIME_START) // TICKS_PER_MS # ms since epoch
            
            #print(f'period={self.viewangle_read_period} self.last_read_ang_timestamp={self.last_read_ang_timestamp} self.viewangle_read_total={self.viewangle_read_total}')
            
            if self.last_read_ang_timestamp:
                self.viewangle_read_total += 1
                if self.viewangle_read_period == None:
                    self.viewangle_read_period = (timestamp - self.last_read_ang_timestamp)
                else:
                    total = min(self.viewangle_read_total, VIEWANGLE_READ_PERIOR_MOVING_AVERAGE_N)
                    self.viewangle_read_period = (self.viewangle_read_period * (total - 1) + (timestamp - self.last_read_ang_timestamp) * 1) / total
                
            else:
                self.last_read_ang_timestamp = timestamp
                self.viewangle_read_total = 1
            
            if i == write_count - 1 and self.last_view_vec == None:
                self.last_view_vec = TimedViewVector(yaw, pitch, timestamp)
                #print(f'SET last_view_vec {self.last_view_vec}')
            
            timestamp /= 1000 # seconds since epoch
            if i == write_count-1:
                normalized_yaw = normalize_yaw(yaw)
                normalized_pitch = normalize_pitch(pitch)
                if self.message_callback:
                    payload = struct.pack('<HH', int(normalized_yaw * (2**16-1)), int(normalized_pitch * (2**16-1)))
                    self.message_callback(CLIENT.VIEWANGLES, timestamp, payload)
        
        # update read offset
        self.recv_ang_sb.read_offset = write_offset
        
        if len(self.interp_view_vecs) > 0 and self.last_view_vec:
            # interpolate viewangles
            # remove old angles
            now = time.time()
            for e in self.interp_view_vecs[:]:
                if e.timestamp < now:
                    self.interp_view_vecs.remove(e)
            
            # the remote function reads one viewangle in the buffer every self.viewangle_read_period milliseconds
            
            # we need to fill future angles in the buffer; we try to keep self.send_ang_capacity at alls times in the buffer
            # calculate how many viewangles are missing to get to self.send_ang_capacity
            read_offset, = struct.unpack_from('I', self.sm.buf, self.send_ang_sb.read_offset_offset) # get read offset
            read_offset -= self.data
            if self.send_ang_sb.write_offset >= read_offset:
                send_angle_count = (self.send_ang_sb.write_offset - read_offset) // 8
            else:
                send_angle_count = ((self.send_ang_sb.end_offset - read_offset) + (self.send_ang_sb.write_offset - self.send_ang_sb.start_offset)) // 8
            num_missing = self.send_ang_capacity - send_angle_count
            #print(f'wo={self.send_ang_sb.write_offset:x} ro={read_offset:x} num_missing={num_missing} send_angle_count={send_angle_count} self.send_ang_capacity={self.send_ang_capacity}')
            # fill angles
            # it may be easier to think in terms of vectors(arrows from the center of a sphere to points on the surface):
            # - start vector(v0): self.last_view_vec
            # - end vector(v1): first interp view vector in self.interp_view_vecs[] after timestamp in self.last_view_vec
            while num_missing > 0:
                v0 = self.last_view_vec
                interp_view_vec = None
                for v in self.interp_view_vecs:
                    if v.timestamp > v0.timestamp:
                        interp_view_vec = v
                        break
                v1 = interp_view_vec
                if not v1:
                    break
                
                dt = v1.timestamp - v0.timestamp # interp time in ms between v0 and v1
                num_steps = round(dt / self.viewangle_read_period) # how many interpolated vectors between v0 and v1
                
                if num_steps > 0:
                    delta_yaw = v1.yaw - v0.yaw
                    delta_pitch = v1.pitch - v0.pitch
                    
                    step_delta_yaw = delta_yaw / num_steps
                    step_delta_pitch = delta_pitch / num_steps
                    #print(f'T={self.viewangle_read_period:.02f} v0=({v0}) v1=({v1}); dt={dt} num_steps={num_steps} delta_yaw={delta_yaw:.02f} delta_pitch={delta_pitch:.02f} step_delta_yaw={step_delta_yaw:.02f} step_delta_pitch={step_delta_pitch:.02f}')
                    
                    # write interpolated view angles
                    for i in range(num_steps):
                        new_yaw = v0.yaw + step_delta_yaw * i
                        new_pitch = v0.pitch + step_delta_pitch * i
                        self.write_send_ang(new_yaw, new_pitch)
                    num_missing -= num_steps
                    self.last_view_vec = TimedViewVector(new_yaw, new_pitch, v1.timestamp)
            
            self.update_send_ang_write_offset()
    
    def update(self):
        self.process_msg_shared_buffer()
        self.process_ang_shared_buffer()
    
    @staticmethod
    def is_valid_client(proc):
        return proc.name() == 'gta_sa.exe'
    
    # visible = True or False
    def set_kill_feed_visibility(self, visible):
        if type(visible) != bool:
            raise TypeError
        self.push_message(CLIENT.KILL_FEED_VISIBILITY, int(visible).to_bytes(1))

    # HUD.HIDDEN(0) HUD.PARTIAL(1) HUD.VISIBLE(2)
    def set_hud_visibility(self, visibility):
        pass
    
    # (VISIBLE -> PARTIAL -> HIDDEN) -> (VISIBLE -> PARTIAL -> HIDDEN) -> ...
    def cycle_hud_visibility(self):
        pass
