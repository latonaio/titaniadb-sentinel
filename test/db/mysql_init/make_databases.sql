CREATE DATABASE Device;
CREATE DATABASE Pod;
use Device;

CREATE TABLE device (
    deviceName VARCHAR(20),
    projectSymbolFk VARCHAR(20),
    deviceIp VARCHAR(20),
    connectionStatus INT NOT NULL PRIMARY KEY,
    os VARCHAR(20));

use Pod;

CREATE TABLE pod(
    podName VARCHAR(20)NOT NULL PRIMARY KEY,
    deviceNameFk VARCHAR(20),
    imageName VARCHAR(20),
    currentVersion VARCHAR(20) ,
    latestVersion VARCHAR(20),
    deployedAt TIMESTAMP,
    status VARCHAR(20));