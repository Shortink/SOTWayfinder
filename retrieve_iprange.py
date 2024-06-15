import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

region_pair = {
    'eastasia': 1, 'australiaeast': 3, 'northeurope': 17, 'westeurope': 18, 'japaneast': 24, 'centralus': 31,
    'eastus': 32, 'eastus2': 33, 'northcentralus': 34, 'southcentralus': 35, 'westcentralus': 36, 'westus': 37,
    'westus2': 38, 'westus3': 79,
}


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
    res = urlopen(url).read()
    soup = BeautifulSoup(res, "lxml")
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        # retrieve actual url
        temp_link = link.get('href')
        x = re.search(r'\.json$', str(temp_link))
        if x:
            return temp_link
        else:
            pass


def create_file(file_name):
    new_json = open('data.json', 'a')
    print("Updating IP database...")

    new_json.write("{\n")
    for keys, value in region_pair.items():
        new_json.write(f"\n{retrieve_ip(value, keys, file_name)}")
        if keys == 'westus3':  # ' prevent adding trailing comma to last json item
            pass
        else:
            new_json.write(",")

    new_json.write("\n}")
    print("Completed")


try:
    download_link = find_download_link()

except:
    print("Failed to download files, try again later")

else:
    r = requests.get(download_link, allow_redirects=True)
    open('ServiceTag_Public.json', 'wb').write(r.content)
    create_file('ServiceTag_Public.json')
