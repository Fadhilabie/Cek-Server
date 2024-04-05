import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.20.116', username='root', password='rahasiats')

ipAddresses = open('inputIp.txt', 'r')
ipWithPass = []

def getPass(ip):
    try:
        stdin, stdout, stderr = ssh.exec_command('ssbb')
        stdin.write(f'{ip}\n')
        password = stdout.read().decode('utf-8').split("[35m")[1].split('[0m')[0]
        return [ip, password]
    except:
        print(f'retry {ip}')
        return 0

while (ip := ipAddresses.readline().strip()):
    haved = getPass(ip)
    count = 0
    while haved == 0 and count < 3:
        haved = getPass(ip)
        count += 1
    if isinstance(haved, list):
        ipWithPass.append(haved)

print(ipWithPass)

outputRes = []
for ip, password in ipWithPass:
    try:
        ssh.connect(ip, username='root', password=password)
        stdin, stdout, stderr = ssh.exec_command('lscpu')
        rows = stdout.read().decode('utf-8').split('\n')
        for row in rows:
            if 'CPU(s):' in row:
                outputRes.append(f'{ip} {row.split(":")[-1].strip()}')
                break

    except Exception as err:
        print(f'Error {ip} :', err)
with open('output', 'w') as fp: fp.write('\n'.join(outputRes))
ssh.close()