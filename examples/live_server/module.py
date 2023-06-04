import asyncio
import math
import traceback

from sa import *
from sa.samp import *

class Module:
    def on_load(self, server):
        self.server = server
        
        self.timer_task = asyncio.get_event_loop().create_task(self.timer())
        
        #server.push_message_to_all(ChatMessage('on_load(): hello from module.py'))
        
        #for i in range(61,128):
        #    id = 10+i
        #    server.push_message_to_all(ServerQuit(id))
        #    server.push_message_to_all(WorldPlayerRemove(id))
        #    
        #    server.push_message_to_all(ServerJoin(id,f'{i}'))
        #    server.push_message_to_all(WorldPlayerAdd(id, pos=Vec3(10,10,5)))
        #    
        #    server.push_message_to_all(Hide3DTextLabel(i))
        #    
        #    #self.server.push_message_to_all(PlayerSync(id, pos=Vec3(2*i,0,3),ud_keys=2**i))
            
#0 stop
# 1-60 forward (same pace)
            
            
    async def timer(self):
        try:
            pass
            #i=0
            #x=0
            while True:
                await asyncio.sleep(1)
                
                #for i in range(61,128):
                #    id = 10+i
                #    self.server.push_message_to_all(PlayerSync(id, pos=Vec3(-1300+(i//32)*3, -150+2*(i%32),14),ud_keys=i,dir=Quat(0,0,0,0.5)))
                #    self.server.push_message_to_all(Show3DTextLabel(i, f'{i}', 0xdd0000dd, Vec3(0,0,1), attached_player_id=id))
            #    x+=16
            #    #self.server.push_message_to_all(PlayerSync(10, pos=Vec3(math.cos(i)*10,math.sin(i)*10,3),vel=Vec3(-math.cos(i)*0.1,-math.sin(i)*0.1,0)))
            #    #i+=36/360*2*3.14159265
            #    #i+=0.017453292500000002
        except asyncio.exceptions.CancelledError:
            pass
        except:
            traceback.print_exc()
            
    def on_unload(self):
        self.timer_task.cancel()
        pass
        
    def on_message(self, message, internal_packet, peer, server):
        #print('hello from module', message)
        if message.id in [MSG.PLAYER_SYNC, MSG.DRIVER_SYNC]:
            ps=message
            print(f'{ps.key_data}')
        pass