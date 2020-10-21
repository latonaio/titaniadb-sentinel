import datetime


project1 = {
    'projectSymbol': '1234567890abcdef',
    'projectName': 'exampleProject',
    'projectID': 'exampleProjectID',
    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

device1 = {
    'deviceName': 'titania',
    'projectSymbolFk': '1234567890abcdef',
    'deviceIp': '192.168.128.161',
    'connectionStatus': 1,
    'os': 'ubuntu:18.04'
}

pod1 = {
    'podName': 'podName',
    'deviceNameFk': 'titania',
    'imageName': 'nginx',
    'currentVersion': 'currentVersion',
    'latestVersion': 'latestVersion',
    'deployedAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'status': 'Running'
}

pod2 = {
    'podName': 'podName2',
    'deviceNameFk': 'titania',
    'currentVersion': 'currentVersion',
    'latestVersion': 'latestVersion',
    'deployedAt': '',
    'status': 'Running'
}
