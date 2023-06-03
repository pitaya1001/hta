import asyncio
from sa import samp
from sa.samp import MSG, RPC

def on_message(message, internal_packet, peer, server):
    if message.id == MSG.RPC:
        rpc = message
        if rpc.rpc_id == RPC.CLIENT_JOIN:
            peer.push_message(samp.ChatMessage('Welcome survivor!', 0x1aab84ff))
    
async def main():
    s = samp.Server(('127.0.0.1', 7777))
    s.hostname = 'Zombie Apocalypse'
    s.gamemode = 'Survival'
    s.language = 'Brain'
    s.post_connected_message_callbacks.append(on_message)
    await s.start()
    
    while True:
        await asyncio.sleep(0.01)
        s.update()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass