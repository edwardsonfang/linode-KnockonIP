from paramiko.client import SSHClient

SSH_USR = "root"
SSH_PASSWORD = "{Your RootPass}"
SSH_HOST = "Your Address"
SSH_PORT = 22
CPU = "7713"

client = SSHClient()

client.load_system_host_keys()
client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USR, password=SSH_PASSWORD)
CMD = "lscpu"
stdin, stdout, stderr = client.exec_command(CMD)

output = stdout.readlines()

with open("cpuinfo.txt", "w") as out_file:
    for line in output:
        #out_file.write(line)
        if CPU in line:
            print("this is the one!")
