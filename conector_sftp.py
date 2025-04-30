import os
import paramiko
from typing import Any
from dotenv import load_dotenv


class SftpDaycred:
    
    def __init__(self) -> None:
        load_dotenv()
        self.caminho_base = os.getenv('CAMINHO_BASE') 
        self.hostname = os.getenv('HOST')
        self.username = os.getenv('NAME')
        self.password = os.getenv('PASSWORD')
        self.port = os.getenv('PORTA')
        #self.dir_sftp_new = os.getenv('DIR_SFTP_TOO_NEW')
        #self.dir_sftp_old = os.getenv('DIR_SFTP_TOO_OLD')

    def __enter__(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(self.hostname, self.port, self.username, self.password)#type: ignore
        except:
            self.ssh_client.connect(self.hostname, self.port, self.username, self.password)#type: ignore
            
        self.sftp = self.ssh_client.open_sftp()
        return self
    
    def __exit__(self, exc_type:None|Any, exc_val:None|Any, exc_tb:None|Any) -> None:
        self.sftp.close()
        self.ssh_client.close()


'''HOST = 189.23.51.128
PORTA = 22
NAME = icrbackup
PASSWORD = BklSLjka@1AS551899Jkhsl!'''