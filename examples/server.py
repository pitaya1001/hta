import asyncio
from sa import samp
from sa.samp import MSG, RPC

def on_message(message, internal_packet, peer, server):
    if message.id == MSG.RPC:
        rpc = message
        if rpc.rpc_id == RPC.CLICK_SCOREBOARD_PLAYER:
            peer.push_message(samp.ShowGameText(0, 5000, f'You clicked on id {rpc.player_id}'))
    
async def main():
    s = samp.Server(('127.0.0.1', 7777))
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