import csv
from ups import UPSConfig


def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

try:
    csv_file = 'devices_test.csv'
    data = read_csv(csv_file)

    for item in data:
        host = item["ups_name"]
        ip = item["ups_ip"]
        newrelic_ip = item["snmp_ip"]
        eco_ip1=item['eco_ip1']
        eco_ip2=item['eco_ip2']
        username = "apc"
        password1 = "P@ss4apc"
        password2 = "apc"

        if host is None or ip is None:
            continue

        print("\n\n########## Configuring device: " + host + " - " + ip)
        try:
            config = UPSConfig(ip, username, [password1, password2])
        except Exception as e:
            print("Unable to connect: " + str(e))
            continue
        configurations = [
            # config.snmp_newrelic,
            config.snmp_acl_config,
            config.reboot
        ]
        params_required = ["snmp_newrelic"]
        for ups_config in configurations:
            try:
                if ups_config.__name__ in params_required:
                    ups_config(newrelic_ip, eco_ip1, eco_ip2)
                else:
                    ups_config()
            except Exception as e:
                print(
                    f"Something went wrong while executing {ups_config.__name__}: " + str(e))

        config.close_connection()
except Exception as e:
    print("Something went wrong: " + str(e))