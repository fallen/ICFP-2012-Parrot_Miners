#!/bin/bash

(./lifter < maps/$1.map $2) &
pid=$!
#echo "Found lifter pid "$pid
sleep $3
#echo "Sending sigint"
kill -2 $pid
#sleep 20
#echo "Sending sigterm"
#kill -15 $pid

