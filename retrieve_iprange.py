import json

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


def create_file():
    file_name = input("Copy and enter name of downloaded file. ex 'ServiceTags_Public.......json': ")
    #file_name = 'ServiceTags_Public_20240610.json'
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


create_file()
