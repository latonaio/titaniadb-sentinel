import etcd3
import os
import datetime
import time
import json

pr1 = {
    'projectSymbol': '1234567890abcdef',
    'projectName': 'exampleProject',
    'projectID': 'exampleProjectID',
    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

d1 = {
    'deviceName': 'titania', #'titania'
    'projectSymbolFk': '1234567890abcdef',
    'deviceIp':'192.168.128.161', # 
    'connectionStatus': repr(1), #'1'
    'os': 'ubuntu:18.04'
}

p1 = {
    'podName': 'podName',
    'deviceNameFk': 'titania',
    'imageName': 'nginx',
    'currentVersion': 'currentVersion', #'currentVersion'
    'latestVersion': 'latestVersion',
    'deployedAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'status': 'Running'
}

p2 = {
    'podName': 'podName2',
    'deviceNameFk': 'titania',
    'currentVersion': 'currentVersion',
    'latestVersion': 'latestVersion',
    'deployedAt': '',
    'status': 'Running'
}

#convert to json
pr1_j = json.dumps(pr1)
d1_j = json.dumps(d1)
p1_j = json.dumps(p1)
p2_j = json.dumps(p2)

project1 = ["/Project/1/1", pr1_j]
device1 = ["/Device/1/1", d1_j]
pod1 = ["/Pod/1/1", p1_j]
pod2 = ["/Pod/2/1", p2_j]


client = etcd3.client(host = 'etcd', port = 2379)
KV_list = [project1, device1, pod1, pod2]

for KVs in KV_list :
    Key = KVs[0]
    Value = KVs[1]
    client.put(Key, Value)
    time.sleep(5)