import yaml
import uuid
from pathlib import Path
from requests import get

class Config:
    cfg={}
    uuid_str=''
    external_ip=''
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)
        uuid_file= Path(".uuid")
        if uuid_file.is_file():
            with open(".uuid", 'r') as uuidfile:
                self.uuid_str=uuidfile.readline()
        else:
            with open(".uuid", 'w') as uuidfile:
                self.uuid_str=str(uuid.uuid4())
                uuidfile.write(self.uuid_str)
                uuidfile.close()
        self.set_public_ip()
    
    def set_public_ip(self):
        self.external_ip=get('https://api.ipify.org').text