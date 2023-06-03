import asyncio
import sa
from sa import *
from sa.samp import *
import traceback

import math

def on_message(message, internal_packet, peer, server):
    if message.id == MSG.RPC:
        rpc = message
        if rpc.rpc_id == RPC.CLICK_SCOREBOARD_PLAYER:
            peer.push_message(ShowGameText(0, 5000, f'You clicked on id {rpc.player_id}'))
            if rpc.player_id == 0:
                peer.push_message(GiveWeapon(WEAPON.M4, 250))
            elif rpc.player_id == 1:
                peer.push_message(RemoveAllWeapons())
        elif rpc.rpc_id == RPC.REQUEST_CHAT_COMMAND:
            # WARNING: REALLY INSECURE, but useful for developing/debugging
            if rpc.command.startswith('/x'):
                try:
                    exec(rpc.command[2:])
                except:
                    for line in traceback.format_exc().split('\n'):
                        peer.push_message(ChatMessage(line, color=0xdd0000ff))
            elif rpc.command.startswith('/rpc'):
                try:
                    peer.push_message(eval(rpc.command[4:]))
                except:
                    for line in traceback.format_exc().split('\n'):
                        peer.push_message(ChatMessage(line, color=0xdd0000ff))
            elif rpc.command.startswith('/money'):
                try:
                    amount = int(rpc.command.split()[1])
                    peer.push_message(GiveMoney(amount))
                except:
                    peer.push_message(ChatMessage('Usage: /money <amount>', color=0x999900ff))
            elif rpc.command == '/nomoney':
                peer.push_message(ResetMoney())
            elif rpc.command.startswith('/face'):
                try:
                    angle = float(rpc.command.split()[1])
                    peer.push_message(SetFacingAngle(angle))
                except:
                    peer.push_message(ChatMessage('Usage: /face <angle>', color=0x999900ff))
            elif rpc.command == '/rhinos':
                for i in range(10):
                    peer.push_message(WorldVehicleRemove(100+i))
                    peer.push_message(WorldVehicleAdd(100+i,VEHICLE.RHINO,Vec3(0 + 20*math.cos(i/10*2*math.pi), 0 + 20*math.sin(i/10*2*math.pi), 3), dir_z=0))
                    peer.push_message(Show3DTextLabel(100+i, f'Bot Rhino {i}', 0xdddd00dd, Vec3(0,0,0),draw_distance=100, test_los=False, attached_vehicle_id=100+i))
            else:
                peer.push_message(ChatMessage('Invalid command', color=0xdd0000ff))
    
async def main():
    s = Server(('127.0.0.1', 7777))
    s.message_callbacks.append(on_message)
    s.fake_player_list = {'alice':123, 'zebra': 456}
    await s.start()
    
    while True:
        await asyncio.sleep(0.01)
        s.update()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass