import copy
import datetime

from src import etcd
from src.examples import data


class Device():
    def __init__(self):
        self.etcd_client = etcd.Device()

    def get(self):
        _dict = copy.deepcopy(data.device1)
        new_dict = self.etcd_client.get_dict(_dict[self.etcd_client.ID])
        print(new_dict)
        return

    def put(self):
        _dict = copy.deepcopy(data.device1)
        _dict['deviceIp'] = datetime.datetime.now().isoformat()
        _dict['connectionStatus'] = datetime.datetime.now().timestamp()
        _dict['os'] = datetime.datetime.now().isoformat()
        res = self.etcd_client.put_dict(_dict)
        print(res)
        return

    def delete(self):
        _dict = copy.deepcopy(data.device1)
        res = self.etcd_client.delete(_dict)
        print(res)
        return

    def new(self):
        _dict = copy.deepcopy(data.device1)
        _dict['deviceName'] = datetime.datetime.now().isoformat()
        _dict['deviceIp'] = datetime.datetime.now().isoformat()
        _dict['connectionStatus'] = datetime.datetime.now().timestamp()
        _dict['os'] = datetime.datetime.now().isoformat()
        res = self.etcd_client.put_dict(_dict)
        print(res)
        return


class Pod():
    def __init__(self):
        self.etcd_client = etcd.Pod()

    def get(self):
        _dict = copy.deepcopy(data.pod1)
        new_dict = self.etcd_client.get_dict(_dict[self.etcd_client.ID])
        print(new_dict)
        return

    def put(self):
        _dict = copy.deepcopy(data.pod1)
        _dict['currentVersion'] = datetime.datetime.now().isoformat()
        _dict['latestVersion'] = datetime.datetime.now().isoformat()
        _dict['deployedAt'] = datetime.datetime.now().isoformat()
        _dict['status'] = datetime.datetime.now().timestamp()
        res = self.etcd_client.put_dict(_dict)
        print(res)
        return

    def delete(self):
        _dict = copy.deepcopy(data.pod1)
        res = self.etcd_client.delete(_dict)
        print(res)
        return

    def new(self):
        _dict = copy.deepcopy(data.pod1)
        _dict['podName'] = datetime.datetime.now().isoformat()
        _dict['imageName'] = datetime.datetime.now().isoformat()
        _dict['currentVersion'] = datetime.datetime.now().isoformat()
        _dict['latestVersion'] = datetime.datetime.now().isoformat()
        _dict['deployedAt'] = datetime.datetime.now().isoformat()
        _dict['status'] = datetime.datetime.now().timestamp()
        res = self.etcd_client.put_dict(_dict)
        print(res)
        return


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str)
    parser.add_argument('method', type=str)
    args = parser.parse_args()
    name = args.name
    method = args.method
    print(name, method)

    mapping = {
        'device': Device,
        'pod': Pod,
    }
    if mapping.get(name) is None:
        print(f'Not accept name: {name}')
        sys.exit(1)
    obj = mapping.get(name)()

    methods = {
        'g': 'get',
        'p': 'put',
        'd': 'delete',
        'n': 'new',
    }
    if methods.get(method) is None:
        print(f'Not accept method: {method}')
        sys.exit(1)
    new_method = methods.get(method)

    eval(f'obj.{new_method}')()
