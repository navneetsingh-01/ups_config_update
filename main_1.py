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
                self.client.connect(ip, username=username, password=password, timeout=10)
                break
            except Exception as e:
                print(f"Something went wrong, unable to connect to {ip}: {str(e)}")
        self.shell = self.client.invoke_shell()

# def NTP_config():
#     shell.send(bytes("ftp -S disable\n", 'ascii'))
#     result = shell.recv(65535).decode('ascii')
#     print("FTP Disabled")

# def FTP_config():
#     # Disable FTP
#     shell.send(bytes("ftp -S disable\n", 'ascii'))
#     result = shell.recv(65535).decode('ascii')
#     print("FTP Disabled")

try:
    # CSV file path
    csv_file = 'devices_test.csv'

    # Read data from CSV
    data = read_csv(csv_file)
    for item in data:
        host = item["host"]
        ip = item["ip"]

        command = "help"

        username = "apc"
        password1 = "P@ss4apc"
        password2 = "apc"

        if host is None or ip is None:
            continue


        config = UPSConfig(ip, username, [password2, password1])


        # client = paramiko.client.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # try:
        #     client.connect(ip, username=username,
        #                    password=password1, timeout=10)
        # except Exception as e:
        #     print("Authentication failed, testing another password")
        #     try:
        #         client.connect(ip, username=username,
        #                        password=password2, timeout=10)
        #     except Exception as e:
        #         print("Something went wrong: " + str(e) + "\n\n")
        #         continue

        # shell = client.invoke_shell()
        # result = shell.recv(65535).decode('ascii')

        # print("\n\n########## Configuring device: " + host)
        # print(host, ip)
       
        # # Disable HTTP
        # shell.send(bytes("web -h disable\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("HTTP Disabled")
        # # Enable SSH
        # shell.send(bytes("console -s\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("SSH Enabled")
        # # Enable HTTPS
        # shell.send(bytes("web -s enable\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("HTTPS Enabled")

        # # Primary NTP Server
        # shell.send(bytes("ntp -p ntp.internal.salesforce.com\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("Primary NTP Server configured")
        # # Secondary NTP Server
        # shell.send(bytes("ntp -s phx-ntp.internal.salesforce.com\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("Secondary NTP Server configured")

        # # Timezone by default GMT - Same time is displayed in UTC

        # # Add an admin user
        # shell.send(
        #     bytes("user -n admin -pw Ups#123! -pe Administrator -e enable\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("Admin user created")

        # # Reboot
        # shell.send(bytes("reboot\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # shell.send(bytes("YES\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("Rebooted successfully\n######################")
        # client.close()
except Exception as e:
    print("Something went wrong: " + str(e))
