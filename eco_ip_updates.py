import csv
from ups import UPSConfig


def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


try:
    csv_file = 'devices.csv'
    data = read_csv(csv_file)

    for item in data:
        host = None
        if 'ups_name' in item.keys():
            host = item['ups_name']
        ip = item["ups_ip"]
        username = ""
        password1 = ""
        password2 = ""

        if ip is None:
            continue

        if host is not None:
            print("\n\n########## Configuring device: " + host + " - " + ip)
        else:
            print("\n\n########## Configuring device: " + ip)
        try:
            config = UPSConfig(ip, username, [password1, password2])
        except Exception as e:
            print("Unable to connect: " + str(e))
            continue
        configurations = [
            config.snmp_eco_ip1,
            config.snmp_eco_ip2,
            config.reboot
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
