import os
import json
import queue
import threading
import time
import pprint
import traceback

from aion.logger import lprint, initialize_logger
from mysql import DeviceTable as deviceTable, PodTable as podTable
from etcd import Device as etcdDevice, Pod as etcdPod
from etcd3.events import PutEvent, DeleteEvent

#環境変数の取得
SERVICE_NAME = os.environ.get("SERVICE", "titaniadb-sentinel")
DEVICE_INTERVAL = os.environ.get("DEVICE_INTERVAL", "30")
POD_INTERVAL = os.environ.get("POD_INTERVAL", "5")
initialize_logger(SERVICE_NAME)


def upsert_at_event(etcd_client_class, mysql_client_class, _queue):
    try:
        lprint(f'etcd Watch {etcd_client_class.BASE_KEY} key prefix.')
        etcd_client = etcd_client_class()
        for event in etcd_client.watch_start(): #watch_start()はetcd.pyにて定義.接頭辞のあるキーの変更を取得する.
            key = None
            value = None
            key = event.key.decode('utf-8')
            value = event.value.decode('utf-8')

            if type(event) == PutEvent:
                error_count = 0
                while True:
                    try:
                        error_count += 1
                        lprint(f'etcd get Put Event: {key}')
                        _dict = json.loads(value)
                        with mysql_client_class() as mysql_client:
                            mysql_client.upsert(_dict)
                        lprint(f'mysql upsert: {key}') #Put Eventを検知し、Valueを書き換える.
                        break
                    except Exception as e:
                        if error_count < 5:
                            lprint(f'Error was occurred at {error_count} times for {key} key. Retry it after sleep.')
                            time.sleep(2) #Error発生(５回以内)時の表示.
                        else:
                            lprint('=' * 50)
                            lprint(f'event: {event.__class__.__name__}')
                            lprint(f'key: {key}')
                            lprint(f'value:')
                            lprint(value)
                            lprint('=' * 50)
                            raise e #５回以上Errorが発生した場合の表示.Error内容と発生箇所を表示する.

            elif type(event) == DeleteEvent:
                lprint(f'etcd get Delete Event: {key}')

            else:
                raise RuntimeError(f'etcd get unexpected event: {event}')

    except Exception as e:
        lprint(e)
        message = f'etcd finish to Watch {etcd_client_class.BASE_KEY} key prefix.'
        _queue.put(message)
        return

    return


def upsert_all(etcd_client_class, mysql_client_class, interval, _queue): #すべてのデータの更新/挿入を行う.
    try:
        while True:
            etcd_client = etcd_client_class()
            dicts = etcd_client.get_dicts() #get_dicts()はetcd.pyにて定義.get_prefixで取得されたデータが取得される.
            with mysql_client_class() as mysql_client:
                for _dict in dicts:
                    mysql_client.upsert(_dict)
                    
            del etcd_client
            
            lprint(f'Success to upsert {mysql_client_class.__name__}.') 
            pprint.pprint(dicts)
            time.sleep(int(interval))

    except Exception:
        lprint('=' * 50)
        lprint(traceback.format_exc())
        message = f'Faild to upsert all. mysql_client_class class is {mysql_client_class.__name__}.'
        _queue.put(message)
    return


def main():
    _queue = queue.Queue()

    thread_device_event = threading.Thread(target=upsert_at_event, args=(etcdDevice, deviceTable, _queue), daemon=True)
    thread_pod_event = threading.Thread(target=upsert_at_event, args=(etcdPod, podTable, _queue), daemon=True)
    thread_device_interval = threading.Thread(target=upsert_all, args=(etcdDevice, deviceTable, DEVICE_INTERVAL, _queue), daemon=True)
    thread_pod_interval = threading.Thread(target=upsert_all, args=(etcdPod, podTable, POD_INTERVAL, _queue), daemon=True)

    thread_device_event.start()
    thread_pod_event.start()
    time.sleep(5)
    thread_device_interval.start()
    thread_pod_interval.start()

    message = _queue.get()
    lprint('=' * 50)
    lprint(message)
    lprint('Cancel all threads.')
    return


if __name__ == "__main__":
    main()
