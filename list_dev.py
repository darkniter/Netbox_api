import NetBox_api


def get_device_type(device_name=None):

    vendor = None

    http_req = NetBox_api.netbox_api('dcim/device-types/', **{'method': 'get'})
    count_devices = http_req.json()['count']

    results_request = http_req.json()['results']

    for row in results_request:
        print(row['display_name'], row['id'])
        if device_name == row['model']:
            vendor = row[id]

    if device_name is None:
        return count_devices, results_request
    else:
        return vendor


if __name__ == "__main__":
    print(get_device_type())
