import json
# import list_dev


from NetBox_api import netbox_api, add_interfaces
fname = 'ignored/filtred_map.json'


def main():
    find_unic = set()
    with open(fname, 'r') as json_file:
        js = json.load(json_file)
        for row in js:
            hint_dev_type = js[row].get('Hint').split('\n')[0]
            find_unic.update([hint_dev_type, ])

    for unic in find_unic:
        if get_device_type(unic) == 0:
            device_type_id = add_device_type(unic)
            print(unic, device_type_id)


def get_device_type(device_name):
    endpoint = 'dcim/device-types/?model=' + device_name
    count_dev = netbox_api(endpoint, **{'method': 'get'}).json()['count']
    return count_dev


def add_device_type(device_name):
    # vendor = list_dev(device_name)
    vendor = 2
    endpoint = 'dcim/device-types/'
    device_json = '{"manufacturer": %d,\
                    "model": "%s",\
                    "slug": "%s"}' % (vendor, device_name, device_name.lower())

    resp = netbox_api(endpoint, **{'data': device_json,
                                   'method': 'post'}).json()

    id_device_type = resp['id']
    print()
    return id_device_type


def delete_device_type(device_id):
    endpoint = f'dcim/device-types/{device_id}/'
    resp = netbox_api(endpoint, **{'method': 'get'})
    return resp.status_code, resp.json()


# def add_device(device_name):
#     add_device_json = '{"name": %s,"device_type": %d,\
#     "device_role": %d, "site":%d}' % ('', 0, 0, 0)
#     resp = netbox_api(endpoint, **{'data': add_device_json,
#                                    'method': 'post'}).json()
#     return add_device_json


def add_device_type_interfaces(device_type_id):

    type_list = list_interfaces({
        "System": 0,
        "01-24": 800,
        "25-28": 1100,
        # "73-90-td": 2000,
    })

    for name, type_int in type_list.items():
        if name == 'System':
            mgmt = True
        else:
            mgmt = False
        resp = add_interfaces(device_type_id, name, type_int, mgmt)

    return resp


def list_interfaces(interface_list):
    init_list = {}

    for item in interface_list:

        new_list = {}

        split_res = item.split('-')
        type_interface = interface_list[item]

        if len(split_res) > 1:

            if len(split_res) == 2:
                split_res.append('')

            iteration = int(split_res[0])

            while iteration <= int(split_res[1]):
                new_list.update({split_res[2]+str(iteration): type_interface})
                iteration = iteration + 1
        else:
            new_list.update({split_res[0]: type_interface})
        init_list.update(new_list)

    return init_list


if __name__ == "__main__":
    # type_list = list_interfaces({
    #     "System": 0,
    #     "01-24": 800,
    #     "25-28": 1100,
    #     # "73-90-td": 2000,
    # })
    delete_device_type(42)
    main()
    print(add_device_type_interfaces(43))
