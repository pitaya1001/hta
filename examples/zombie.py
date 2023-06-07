import asyncio
from sa import samp
from sa.samp import MSG, RPC

'''
Login; placeholders(username + password)
'''

class ZombieServer(samp.Server):
    def __init__(self):
        super().__init__(('127.0.0.1', 7777))
        self.hostname = 'Zombie Apocalypse'
        self.gamemode = 'Survival'
        self.language = 'Brain'
        self.message_callbacks.append(self.on_message)

    def on_message(self, message, internal_packet, peer, server):
        if message.id == MSG.RPC:
            rpc = message
            if rpc.rpc_id == RPC.CLIENT_JOIN:
                peer.push_message(samp.ChatMessage('Welcome survivor!', 0x1aab84ff))
                #todo peer.push_message(samp.ShowTextdraw(1, 0, samp.Vec2(5, 5), 0xff0000ff, samp.Vec2(5, 5), 0, 0, 0, 0, 0, 0, samp.Vec2(100, 100), 0, samp.Vec3(0,0,0), 0, 0, 0, 'aaa'))
        elif message.id == MSG.CONNECTION_REQUEST:
            peer.password = message.password

async def main():
    s = ZombieServer()
    await s.start()
    while True:
        await asyncio.sleep(0.01)
        s.update()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
