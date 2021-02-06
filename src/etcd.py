import json
import os

import etcd3


# Localhost
HOST = os.environ.get('MY_ETCD_HOST', '0.0.0.0')
PORT = int(os.environ.get('MY_ETCD_PORT', 2379))
TYPE_POSITION_INDEX = 1
STATUS_POSITION_INDEX = 3
RUNNINX_STATUS_INDEX = "0"
STOPPED_STATUS_INDEX = "1"
DEVICE_DATA_TYPE = "Device"
POD_DATA_TYPE = "Pod"


class Base(etcd3.Etcd3Client):
    def __init__(self):
        super().__init__(host=HOST, port=PORT)

    def watch_start(self): #prefixを持つkeyをwatchする.
        events_iter, self.cancel = self.watch_prefix(self.BASE_KEY)
        for event in events_iter:
            yield event
        return

#keyは、/self.BASE_KEY/ID の形でストアされている.
    def get_dicts(self): #prefixを持つkeyのmetadata, valueを取得し、pod_data_typeなどの状態をdictsに入れる.
        tuples = self.get_prefix(self.BASE_KEY, sort_order='ascend')
        dicts = []
        for b_value, b_metadata in tuples:
            value = b_value.decode('utf-8')
            _dict = json.loads(value)

            key = b_metadata.key.decode('utf-8')
            keyArr = key.split("/")
            if keyArr[STATUS_POSITION_INDEX] == STOPPED_STATUS_INDEX:
                if keyArr[TYPE_POSITION_INDEX] == DEVICE_DATA_TYPE:
                    _dict["connectionStatus"] = 1
                elif keyArr[TYPE_POSITION_INDEX] == POD_DATA_TYPE:
                    _dict["status"] = 1

            dicts.append(_dict)
        return dicts

    def get_dict(self, _id):
        key = f'{self.BASE_KEY}/{_id}'
        b_value, _ = self.get(key)
        if b_value is None:
            return b_value

        value = b_value.decode('utf-8')
        _dict = json.loads(value)
        return _dict

    def put_dict(self, _dict):
        _id = _dict[self.ID]
        key = f'{self.BASE_KEY}/{_id}'
        value = json.dumps(_dict)
        response = self.put(key, value)
        return response

    def delete(self, _dict):
        _id = _dict[self.ID]
        key = f'{self.BASE_KEY}/{_id}'
        response = super(Base, self).delete(key)
        return response


class Device(Base):
    BASE_KEY = '/Device'
    ID = 'deviceName'

    def __init__(self):
        super().__init__()


class Pod(Base):
    BASE_KEY = '/Pod'
    ID = 'podName'

    def __init__(self):
        super().__init__()
