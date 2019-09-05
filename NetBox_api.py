import requests
import config
import json


headers_init = {
        "Authorization": "Token {}".format(config.token),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def netbox_api(endpoint, **args):
    data = args.get('data')
    header = header_get(args['method'])
    http_req = config.http_req_server + endpoint

    resp = {
            'get': requests.get(http_req, headers=header),
            'post': requests.post(http_req, data=data, headers=header),
            'delete': requests.delete(http_req, headers=header),
            'put': requests.put(http_req, data=data, headers=header),
    }[args['method']]
    return resp


def header_get(http_req):
    header = headers_init.copy()
    if http_req == 'get':
        header.pop("Content-Type")
    return header


def add_interfaces(device_type_id, name, type_int=0, mgmt=False):

    data = json.dumps({"device_type": device_type_id,
                       "name": name,
                       "type": type_int,
                       "mgmt_only": mgmt})
    endpoint = 'dcim/interface-templates/'
    resp = netbox_api(endpoint, **{'data': data, 'method': 'post'})
    return resp
# res = header_get('get')
# print(res)
