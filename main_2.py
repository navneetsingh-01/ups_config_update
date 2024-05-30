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

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, username=username,
                           password=password1, timeout=10)
        except Exception as e:
            print("Authentication failed, testing another password")
            try:
                client.connect(ip, username=username,
                               password=password2, timeout=10)
            except Exception as e:
                print("Something went wrong: " + str(e) + "\n\n")
                continue

        shell = client.invoke_shell()
        result = shell.recv(65535).decode('ascii')

        print("\n\n########## Configuring device: " + host)
        print(host, ip)

        # try: 
        #     # Change super user password
        #     shell.send(bytes("user -n apc -cp apc -pw P@ss4apc\n", 'ascii'))
        #     result = shell.recv(65535).decode('ascii')
        #     print("SU password updated")
        # except Exception as e:
        #     print("Something went wrong. Unable to change su password: " + str(e))

        # try:
        #     # Disable admin user 
        #     shell.send(bytes("user -n admin -e disable\n", 'ascii'))
        #     result = shell.recv(65535).decode('ascii')
        #     print("Admin user disabled")
        # except Exception as e:
        #     print("Something went wrong. Unable to delete admin user: " + str(e))

        try:
            # Setup timezone to UTC
            shell.send(bytes("date -z 00:00\n", 'ascii'))
            result = shell.recv(65535).decode('ascii')
            print("Timezone set to UTC")
        except Exception as e:
            print("Something went wrong. Unable to set timezone: " + str(e))

        

        # Reboot
        shell.send(bytes("reboot\n", 'ascii'))
        result = shell.recv(65535).decode('ascii')
        shell.send(bytes("YES\n", 'ascii'))
        result = shell.recv(65535).decode('ascii')
        print("Rebooted successfully\n######################")
        client.close()
except Exception as e:
    print("Something went wrong: " + str(e))
