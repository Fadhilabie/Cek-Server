import paramiko

# Inisialisasi klien SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.20.116', username='root', password='rahasiats')

# Membuka file yang berisi daftar alamat IP
ipAddresses = open('inputIp.txt', 'r')
ipWithPass = []

# Fungsi untuk mendapatkan kata sandi dari suatu IP
def getPass(ip):
    try:
        # Menjalankan perintah 'ssbb' pada remote server
        stdin, stdout, stderr = ssh.exec_command('ssbb')
        # Mengirimkan alamat IP ke perintah 'ssbb'
        stdin.write(f'{ip}\n')
        # Membaca hasil output untuk mendapatkan kata sandi
        password = stdout.read().decode('utf-8').split("[35m")[1].split('[0m')[0]
        return [ip, password]
    except:
        # Menangani kesalahan jika terjadi
        print(f'retry {ip}')
        return 0

# Membaca setiap baris dari file alamat IP
while (ip := ipAddresses.readline().strip()):
    # Mendapatkan kata sandi untuk IP tersebut
    haved = getPass(ip)
    count = 0
    # Mengulang percobaan hingga 3 kali jika terjadi kesalahan
    while haved == 0 and count < 3:
        haved = getPass(ip)
        count += 1
    # Menambahkan IP dan kata sandi ke dalam list jika berhasil
    if isinstance(haved, list):
        ipWithPass.append(haved)

print(ipWithPass)

outputRes = []
# Menggunakan IP dan kata sandi yang berhasil untuk koneksi SSH dan mendapatkan informasi sistem
for ip, password in ipWithPass:
    try:
        ssh.connect(ip, username='root', password=password)
        # Perintah-perintah yang akan dijalankan pada remote server
        commands = ['lscpu', 'free -h', 'lsblk', 'hostnamectl', 'dmidecode -t system']
        for command in commands:
            # Menjalankan perintah dan mendapatkan output
            stdin, stdout, stderr = ssh.exec_command(command)
            rows = stdout.read().decode('utf-8').split('\n')
            # Menyimpan output perintah beserta header perintahnya
            outputRes.append(f'\n==== {command.upper()} ====\n')
            for row in rows:
                outputRes.append(row.strip())
    except Exception as err:
        # Menangani kesalahan jika terjadi
        print(f'Error {ip} :', err)

# Menyimpan hasil output ke dalam file 'output'
with open('output', 'w') as fp:
    fp.write('\n'.join(outputRes))

# Menutup koneksi SSH
ssh.close()
