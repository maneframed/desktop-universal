from tkinter import Tk
from multiprocessing import Process
from handler import ThreadedHTTPServer, Handler
from application import Application
from config import Config
from upnp.upnp import Upnp

def launchWebServer():
    server = ThreadedHTTPServer(('localhost', 9090), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

if __name__ == '__main__':
    config = Config()
    tensorflow_port=config.cfg['tensorflow']['port']
    webserver_port=config.cfg['webserver']['port']
    upnp=Upnp()
    upnp.delete_port_mapping(tensorflow_port)
    upnp.add_port_mapping(upnp.get_ip_address())

    p = Process(target=launchWebServer)
    p.start()
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

