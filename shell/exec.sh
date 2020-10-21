#!/bin/bash

POD_ID=$(kubectl get po | awk '{print $1}' | grep -v NAME | grep titaniadb-sentinel)
kubectl exec -it ${POD_ID} -- bash