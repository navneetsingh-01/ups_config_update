import os
import paramiko
import time
from dotenv import load_dotenv
load_dotenv()


class UPSConfig:
    def __init__(self, ip, username, passwords):
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False
        for password in passwords:
            try:
                self.client.connect(ip, username=username,
                                    password=password, timeout=10)
                print(f"Connected successfully!!")
                connected = True
                break
            except Exception as e:
                print(
                    f"Something went wrong, unable to connect to {ip}: {str(e)}")
        if not connected:
            username = os.getenv("SU_USERNAME")
            password = os.getenv("SU_PASSWORD")
            try:
                self.client.connect(ip, username=username,
                                    password=password, timeout=10)
                print(f"Connected successfully!!")
                connected = True
            except Exception as e:
                print(
                    f"Something went wrong, unable to connect to {ip}: {str(e)}")
        self.shell = self.client.invoke_shell()
        output = self.shell.recv(1000)

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
            bytes("ntp -s ntp.internal.salesforce.com\n", 'ascii'))
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

    def radius_config(self):
        self.shell.send(bytes("radius -a radiusLocal\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Enable RADIUS and local authentication")

    def radius_primary_server_config(self):
        self.shell.send(bytes("radius -p1 10.15.64.29\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Radius primary server configured")

    def radius_secondary_server_config(self):
        self.shell.send(bytes("radius -p2 10.192.64.27\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Radius secondary server configured")

    def radius_primary_server_timeout(self):
        self.shell.send(bytes("radius -t1 30\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Radius primary server timeout configured")

    def radius_secondary_server_timeout(self):
        self.shell.send(bytes("radius -t2 30\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Radius secondary server timeout configured")

    def radius_primary_server_secret(self):
        self.shell.send(bytes("radius -s1 $H@redKEy@Cs3\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Radius primary server secret configured")

    def radius_secondary_server_secret(self):
        self.shell.send(bytes("radius -s2 $H@redKEy@Cs3\n", 'ascii'))
        result = self.shell.recv(65535).decode('ascii')
        print("Radius secondary server secret configured")

    def snmp_acl_config(self):
        self.shell.send(bytes("snmpv3 -ac1 enable\n", 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("SNMP AC1 enabled")

        self.shell.send(bytes("snmpv3 -ac2 enable\n", 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("SNMP AC2 enabled")

        self.shell.send(bytes("snmpv3 -ac3 enable\n", 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("SNMP AC3 enabled")

    def snmp_access_users(self):
        self.shell.send(bytes("snmpv3 -au1 itsremon\n", 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("AU1 configured")

        self.shell.send(bytes("snmpv3 -au2 itsremon\n", 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("AU2 configured")

        self.shell.send(bytes("snmpv3 -au3 itsremon\n", 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("AU3 configured")

    def snmp_access_ips(self, newrelic_ip):
        cmd = f"snmpv3 -n1 {newrelic_ip}\n"
        self.shell.send(bytes(cmd, 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("NewRelic IP configured")

        eco_ip1 = "10.15.96.101"
        eco_ip2 = "10.192.100.37"

        cmd = f"snmpv3 -n2 {eco_ip1}\n"
        self.shell.send(bytes(cmd, 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("N2 IP configured")

        cmd = f"snmpv3 -n3 {eco_ip2}\n"
        self.shell.send(bytes(cmd, 'ascii'))
        time.sleep(60)
        result = self.shell.recv(10000000).decode('ascii')
        print("N3 IP configured")
