import json
import re
import requests
from bs4 import BeautifulSoup
import os

region_pair = {1: 'eastasia', 2: 'southeastasia', 3: 'australiaeast', 4: 'australiasoutheast', 8: 'taiwannorth',
               9: 'brazilsouth', 11: 'canadacentral', 12: 'canadaeast', 16: 'northeurope2', 17: 'northeurope',
               18: 'westeurope', 19: 'centralfrance', 20: 'southfrance', 21: 'centralindia', 22: 'southindia',
               23: 'westindia', 24: 'japaneast', 25: 'japanwest', 26: 'koreacentral', 27: 'uksouth', 28: 'ukwest',
               31: 'centralus', 32: 'eastus', 33: 'eastus2', 34: 'northcentralus', 35: 'southcentralus',
               36: 'westcentralus', 37: 'westus', 38: 'westus2', 48: 'centraluseuap', 49: 'eastus2euap',
               50: 'koreasouth', 52: 'polandcentral', 53: 'mexicocentral', 58: 'australiacentral',
               59: 'australiacentral2', 60: 'uaenorth', 61: 'uaecentral', 63: 'norwaye', 64: 'jioindiacentral',
               65: 'jioindiawest', 66: 'switzerlandn', 67: 'switzerlandw', 68: 'usstagee', 69: 'usstagec',
               71: 'germanywc', 72: 'germanyn', 74: 'norwayw', 75: 'swedensouth', 76: 'swedencentral', 77: 'brazilse',
               78: 'brazilne', 79: 'westus3', 82: 'southafricanorth', 83: 'southafricawest', 84: 'qatarcentral',
               85: 'israelcentral', 88: 'spaincentral', 93: 'italynorth', 96: 'taiwannorthwest', 98: 'malaysiasouth'}


def retrieve_ip(region, name, file):
    f = open(file)
    data = json.load(f)
    ip_array = []

    for entries in data['values']:
        if entries['properties']['regionId'] == region:
            range_array = (entries['properties']['addressPrefixes'])
            for ip in range_array:
                if "::" not in ip:
                    ip_array.append(ip)
        else:
            continue
    json_str = json.dumps(ip_array)
    return f'\"{name}\":\n{json_str}'


def find_download_link():
    url = 'https://www.microsoft.com/en-us/download/details.aspx?id=56519'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36'
    }
    request = requests.get(url, headers=header)
    soup = BeautifulSoup(request.text, "html.parser")
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        # retrieve actual url
        temp_link = link.get('href')
        x = re.search(r'\.json$', str(temp_link))
        if x:
            return temp_link
        else:
            pass


def create_file(file_name):
    if os.path.isfile('data.json'):
        os.remove('data.json')
    new_json = open('data.json', 'a')
    print("Updating IP database...")

    new_json.write("{\n")
    for keys, value in region_pair.items():
        new_json.write(f"\n{retrieve_ip(keys, value, file_name)}")
        if value == 'malaysiasouth':  # ' prevent adding trailing comma to last json item
            pass
        else:
            new_json.write(",")

    new_json.write("\n}")
    os.remove(file_name)
    print("Completed")


try:
    download_link = find_download_link()

except:
    print("Failed to download files, try again later")

else:
    r = requests.get(download_link, allow_redirects=True)
    open('ServiceTag_Public.json', 'wb').write(r.content)
    create_file('ServiceTag_Public.json')
