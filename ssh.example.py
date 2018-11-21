import socket
import paramiko

import config


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    connection = config.REMOTE["csie0"]
    print(connection)

    #socket.getaddrinfo(connection['hostname'], 22)

    client.connect(
        connection['hostname'], 
        connection['port'], 
        username=connection['username'], 
        password=connection['password'])

    print('connect success')
    (stdin, stdout, stderr) = client.exec_command('ls -l') # your stuff
    #print('stdin: ', stdin.readlines())
    output = stdout.readlines()
    for i in range(len(output)):
        print(output[i])
    #print('stdout:', stdout.readlines())
    #print('stderr:', stderr.readlines())

    client.close()
    

if __name__ == "__main__":
    main()