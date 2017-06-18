from requests import post
from config import Config
import schedule

class Mothership():
    registered=False

    def register_with_mothership(self):
        config = Config()
        mothership_host= config.cfg['maneframe']['backend']['host']
        registration_endpoint= config.cfg['maneframe']['backend']['registrationEndpoint']
        webserver_port=config.cfg['webserver']['port']
        tensorflow_port=config.cfg['tensorflow']['port']
        if(post(mothership_host+registration_endpoint, json={'id':config.uuid_str, 'ip':config.external_ip, 'webserver_port': webserver_port, 'tensorflow_port': tensorflow_port}).ok):
            self.registered=True
        else:
            self.registered=False