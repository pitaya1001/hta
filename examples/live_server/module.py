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

        #server.push_message_to_all(ServerJoin(10,'bob'))
        #server.push_message_to_all(StartPlayerStream(10))
        v=Vehicle(101,VEHICLE.HYDRA)
        server.vehicle_pool[101]=v
        server.push_message_to_all(AddVehicle(101, VEHICLE.HYDRA, SPOT.GROVE))
        #server.push_message_to_all(DriverSync
        
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
        #server.push_message_to_all(ShowTextdraw(textdraw_id=2095, text='hello', pos=Vec2(220.02, 355.63), flags=24, letter_size=Vec2(0.25, 1.18), letter_color=4294967295, line_size=Vec2(1280.00, 1280.00), box_color=2155905152, shadow=1, outline=1, background_color=268435456, style=2 ,clickable=0, model_id=0, rot=Vec3(0.00, 0.00, 0.00), zoom=1.00, color1=65535 ,color2=65535))

#0 stop
# 1-60 forward (same pace)

    async def timer(self):
        try:
            pass
            #i=0
            #x=0
            while True:
                await asyncio.sleep(1)
                #self.server.push_message_to_all()
                #for peer in self.server.peers.items():
                #    peer.push_message(Show3DTextLabel(i, str(peer.player.pos), 0xdd0000dd, Vec3(0,0,1), attached_player_id=id))
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
        #if message.id in [MSG.PLAYER_SYNC, MSG.DRIVER_SYNC]:
        #    ps = message
        #    print(f'{ps.key_data}')
        
       #if message.id == MSG.PLAYER_SYNC:
       #   print(peer.player.health)
       #   #print(message.health,
       #   #message.armor)
        
        pass
