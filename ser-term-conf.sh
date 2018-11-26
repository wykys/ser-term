#!/usr/bin/env bash
# actavated venv ans run ser-term client
# wykys 2018

if [ ! -d ".venv" ]; then
  echo ".venv not exist"
  ./venv.sh
fi

. .venv/bin/activate
./client.py $@
