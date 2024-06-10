import csv
import paramiko


def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


class UPSConfig:
    def __init__(self, ip, username, passwords):
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for password in passwords:
            try:
                self.client.connect(ip, username=username,
                                    password=password, timeout=10)
                print(f"Connected successfully!!")
                break
            except Exception as e:
                print(
                    f"Something went wrong, unable to connect to {ip}: {str(e)}")
        self.shell = self.client.invoke_shell()

    def FTP_config(self):
        self.shell.send(bytes("ftp -S disable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("FTP Disabled")

    def NTP_OM_config(self):
        self.shell.send(bytes("ntp -OM enable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("NTP Override Manual Option Enabled")

    def NTP_config(self):
        self.shell.send(bytes("ntp -e enable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("NTP Enabled")

    def HTTP_config(self):
        self.shell.send(bytes("web -h disable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("HTTP Disabled")

    def SSH_config(self):
        self.shell.send(bytes("console -s\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("SSH Enabled")

    def HTTPS_config(self):
        self.shell.send(bytes("web -s enable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("HTTPS Enabled")

    def NTP_primary_server_config(self):
        self.shell.send(bytes("ntp -p ntp.internal.salesforce.com\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Primary NTP Server configured")

    def NTP_secondary_server_config(self):
        self.shell.send(
            bytes("ntp -s \n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Secondary NTP Server configured")

    def create_user(self):
        self.shell.send(
            bytes("user -n admin -pw Ups#123! -pe Administrator -e enable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Admin user created")

    def setup_timezone(self):
        self.shell.send(bytes("date -z 00:00\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Timezone set to UTC")

    def change_su_password(self):
        self.shell.send(bytes("user -n apc -cp apc -pw P@ss4apc\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("SU password updated")

    def user_disable(self):
        self.shell.send(bytes("user -n admin -e disable\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Admin user disabled")

    def reboot(self):
        self.shell.send(bytes("reboot\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        self.shell.send(bytes("YES\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Rebooted successfully\n###############")

    def close_connection(self):
        self.client.close()


try:
    csv_file = 'devices_test.csv'
    data = read_csv(csv_file)

    for item in data:
        host = item["host"]
        ip = item["ip"]
        username = "apc"
        password1 = "P@ss4apc"
        password2 = "apc"

        if host is None or ip is None:
            continue

        print("\n\n########## Configuring device: " + host + " - " + ip)
        config = UPSConfig(ip, username, [password1, password2])
        configurations = [
            config.NTP_primary_server_config,
            config.NTP_secondary_server_config,
            config.NTP_OM_config,
            config.NTP_config,
            config.setup_timezone,
            config.reboot,
        ]
        for ups_config in configurations:
            try:
                ups_config()
            except Exception as e:
                print(
                    f"Something went wrong while executing {ups_config.__name__}: " + str(e))

        config.close_connection()
except Exception as e:
    print("Something went wrong: " + str(e))

'''
timezone 0 
ntp -e enable
servers 
local + radius
t1 = t2 = 30
$H@redKEy@Cs36
$H@redKEy@Cs36
'''