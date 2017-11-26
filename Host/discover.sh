#!/bin/bash
for ip in $(seq 1 254); do
    ping 192.168.181.$ip | grep "bytes from" | cut -d " " -f 4 | cut -d ":" -f 1 &
done