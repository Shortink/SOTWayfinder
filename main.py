import netaddr
import pydivert
import json
import requests
from netaddr import IPNetwork, IPAddress


def find_ip():
    with pydivert.WinDivert("udp.DstPort >= 30000 and udp.DstPort <= 31000") as w:  # ' sot uses ports 30k - 31k
        while True:
            packet = w.recv()
            if packet:
                ip_port = str(packet.ipv4.dst_addr) + ":" + str(packet.udp.dst_port)
                break

            w.send(packet)
    return ip_port


def find_location(ip_port):
    ip = ip_port.split(":")[0]
    try:
        ip_json = json.loads((requests.get(f'hhttp://ip-api.com/json/{ip}?fields=status,regionName,city,org')).text)
    except requests.exceptions.RequestException:
        print(f"Unable to retrieve advanced location data for {ip_port}. Geolocation server might be down")

    else:
        if ip_json["status"] == "success":
            print(f'{ip_port}  {ip_json["city"]},{ip_json["regionName"]} {ip_json["org"]}')
        else:
            print(f"{ip_port} Failed to retrieve location")


def connect_region(region):
    with pydivert.WinDivert("udp.DstPort >=3070 and udp.DstPort<=3080") as w:  # 'xbox live ports
        for packet in w:
            if ip_query(packet.ipv4.dst_addr, region) is True:
                w.send(packet)


def ip_query(ip, region_to_connect):
    data = json.load(open('data.json'))
    for ip_range in data[region_to_connect]:
        if IPAddress(ip) in IPNetwork(ip_range):
            return True

