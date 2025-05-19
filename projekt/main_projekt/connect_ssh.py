
import os
from valaki import Valaki

#ssh -X h376477@linux.inf.u-szeged.hu

def connect(valaki: Valaki):
    print("Connect fut")
    hostname="linux.inf.u-szeged.hu"
    username=valaki.h_azonosito

    os.system(f"start ssh {username}@{hostname}")

    # client = paramiko.SSHClient()
    # client.load_system_host_keys()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #
    # try:
    #     client.connect(hostname=hostname, username=username, password=password)
    #     parancssor = client.invoke_shell()
    #     parancssor.send('ls -l\n')
    #     print(parancssor.recv(1024).decode())
    #
    #
    # except Exception as e:
    #     print(e)
