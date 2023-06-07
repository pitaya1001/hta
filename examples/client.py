import asyncio
from sa import samp
from sa.samp import RPC, MSG

def on_message(message, internal_packet, peer, client):
    if message.id == MSG.RPC:
        rpc = message
        print(rpc)

async def f(c):
    await asyncio.sleep(5)
    c.server_peer.push_message(samp.RconCommand('login changeme'))
    
async def main():
    c = samp.Client(('127.0.0.1', 7777))
    c.name = 'bob'
    c.message_callbacks.append(on_message)
    await c.start()
    
    asyncio.get_event_loop().create_task(f(c))
    
    while True:
        await asyncio.sleep(0.01)
        c.update()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
