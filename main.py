import csv
import paramiko

# Read data from CSV file
def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data



try:
    # CSV file path
    csv_file = 'devices.csv'

    # Read data from CSV
    data = read_csv(csv_file)
    for item in data:
        host = item["host"]
        ip = item["ip"]


        command = "help"

        username = "apc"
        password1 = "apc"
        password2 = "P@ss4apc"
        
        if host is None or ip is None:
            continue

        print(host, ip)
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, username=username, password=password1, timeout=20)
        except Exception as e:
            print("Authentication failed, testing another password")
            try:
                client.connect(ip, username=username, password=password2, timeout=20)
            except Exception as e:
                print("Something went wrong: " + str(e))
                continue

        shell = client.invoke_shell()
        result = shell.recv(65535).decode('ascii')

        print("\n\n########## Configuring device: " + host)
        print("Done")
        # # Disable FTP
        # shell.send(bytes("ftp -S disable\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("FTP Disabled")
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
        # shell.send(bytes("user -n admin -pw Ups#123! -pe Administrator -e enable\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("Admin user created")

        # # Reboot
        # shell.send(bytes("reboot\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # shell.send(bytes("YES\n", 'ascii'))
        # result = shell.recv(65535).decode('ascii')
        # print("Rebooted successfully")

        client.close()
except Exception as e:
    print("Something went wrong: " + str(e))

