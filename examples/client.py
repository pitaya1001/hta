import asyncio
from sa import samp
from sa.samp import RPC, MSG

def on_message(message, internal_packet, peer, client):
    if message.id == MSG.RPC:
        rpc = message
        print(rpc)

async def main():
    c = samp.Client(('127.0.0.1', 7777))
    c.message_callbacks.append(on_message)
    await c.start()
    while True:
        await asyncio.sleep(0.01)
        c.update()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass