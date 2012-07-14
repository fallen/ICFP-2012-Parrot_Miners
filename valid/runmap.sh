#!/bin/bash

(./lifter < maps/$1.map) &
pid=$!
#echo "Found lifter pid "$pid
sleep 150
#echo "Sending sigint"
kill -2 $pid
#sleep 10
#echo "Sending sigterm"
#kill -15 $pid

