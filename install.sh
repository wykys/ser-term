#!/bin/bash

URL1=$(pwd)/ser-term.sh
URL2=$(pwd)/ser-term-conf.sh
cd /usr/bin
ln -s $URL1 ser-term
ln -s $URL2 ser-term-conf
