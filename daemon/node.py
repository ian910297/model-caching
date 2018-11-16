import paramiko

class node:
    def __init__(self, name, host, username, password):
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.ssh_client = paramiko.SSHClient()
    
    def set(self):
        pass
    
    def connect(self):
        pass