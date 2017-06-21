from tkinter import Tk
from multiprocessing import Process
from application import Application
from config import Config
from upnp.upnp import Upnp
import asyncio
import websockets
import concurrent.futures
import json

async def open_port_register():
    upnp=Upnp()
    upnp.delete_port_mapping(tensorflow_port)
    upnp.add_port_mapping(upnp.get_ip_address()) 
    async with websockets.connect(maneframe_web_uri) as websocket:
        await websocket.send(json.dumps(register_payload))
        print("> {}".format(json.dumps(register_payload)))
        while True: 
            greeting = await websocket.recv()
            print("< {}".format(greeting))

def start_web():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(open_port_register())

if __name__ == '__main__':
    # Get all config values
    config = Config()
    tensorflow_port=config.cfg['tensorflow']['port']
    webserver_port=config.cfg['webserver']['port']
    maneframe_web_uri=config.cfg['maneframe']['web']['uri']
    uuid = config.uuid_str
    register_payload={'ip':config.external_ip,'tensorflow_port':tensorflow_port, 'uuid': uuid}
    
    # Open ports and register code
    p = Process(target=start_web)
    p.start()
    
    # Visual components start
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    p.terminate()

