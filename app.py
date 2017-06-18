# Get task number from command line
import sys
from tkinter import Tk
from multiprocessing import Process
import yaml
from requests import get, post
from handler import ThreadedHTTPServer, Handler
from application import Application
import miniupnpc
from config import Config

def launchWebServer():
    server = ThreadedHTTPServer(('localhost', 9090), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

if __name__ == '__main__':
    config = Config()
    tensorflow_port=config.cfg['tensorflow']['port']
    webserver_port=config.cfg['webserver']['port']
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 10
    upnp.discover()
    upnp.selectigd()
    # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
    upnp.addportmapping(tensorflow_port, 'TCP', upnp.lanaddr, tensorflow_port, 'maneframe-tensorflow', '')
    upnp.addportmapping(webserver_port, 'TCP', upnp.lanaddr, webserver_port, 'maneframe-webserver', '')

    p = Process(target=launchWebServer)
    p.start()
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

