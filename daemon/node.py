import paramiko
from flask import Flask

class Node:
    def __init__(self, name, host, username, password):
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.status = ''
        self.ssh_client = paramiko.SSHClient()
    
    def set(self):
        pass
    
    def connect(self):
        pass

if __name__ == "__main__":
    pass