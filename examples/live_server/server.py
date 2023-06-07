'''
This example has a simple server.
If you type 'r' on the terminal it will reload the module.py file
You may use it to change server logic on the fly.
'''

import asyncio
import concurrent
import traceback
import importlib

import sa
from sa import *
from sa.samp import *

import module

server = None
module_instance = None

def on_message(message, internal_packet, peer, server):
    try:
        if module_instance is None:
            if module_instance.on_message(message, internal_packet, peer, server) is True:
                return
    except:
        traceback.print_exc()
    if message.id == MSG.RPC:
        rpc = message
        if rpc.rpc_id == RPC.REQUEST_CHAT_COMMAND:
            # WARNING: REALLY INSECURE, but useful for developing/debugging
            try:
                if rpc.command.startswith('/x'):
                    exec(rpc.command[2:])
                elif rpc.command.startswith('/rpc'):
                    peer.push_message(eval(rpc.command[4:]))
            except:
                for line in traceback.format_exc().split('\n'):
                    peer.push_message(ChatMessage(line, color=0xdd0000ff))

async def input_loop():
    with concurrent.futures.ThreadPoolExecutor() as pool:
        while True:
            s = await asyncio.get_event_loop().run_in_executor(pool, input)
            if s[0] == 'r': # reload module
                try:
                    global module_instance
                    module_instance.on_unload()
                    importlib.reload(module)
                    module_instance = module.Module()
                    module_instance.on_load(server)
                except:
                    traceback.print_exc()

async def main():
    asyncio.get_event_loop().create_task(input_loop())

    s = Server(('127.0.0.1', 7777))
    global server
    server = s
    s.message_callbacks.append(on_message)
    await s.start()

    try:
        global module_instance
        module_instance = module.Module()
        module_instance.on_load(server)
    except:
        traceback.print_exc()

    while True:
        await asyncio.sleep(0.01)
        s.update()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
