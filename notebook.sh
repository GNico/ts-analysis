#!/bin/bash
if [ -z $IP ]; then
  echo '$IP not set'
  exit
fi
echo "IP=$IP"
ipython3 notebook --ip $IP --port 8888 --NotebookApp.token=
