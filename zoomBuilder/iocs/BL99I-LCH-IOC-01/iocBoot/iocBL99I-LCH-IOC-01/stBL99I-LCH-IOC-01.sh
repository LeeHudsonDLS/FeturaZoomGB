#!/bin/sh
# This file was automatically generated on Thu 18 Oct 2018 08:33:26 BST from
# source: /home/jjc62351/work/Zoom/zoomBuilder/etc/makeIocs/BL99I-LCH-IOC-01.xml
# 
# *** Please do not edit this file: edit the source file instead. ***
# 
cd "$(dirname "$0")"
if [ -n "$1" ]; then
    export EPICS_CA_SERVER_PORT="$(($1))"
    export EPICS_CA_REPEATER_PORT="$(($1 + 1))"
    [ $EPICS_CA_SERVER_PORT -gt 0 ] || {
        echo "First argument '$1' should be a integer greater than 0"
        exit 1
    }
fi
exec ./BL99I-LCH-IOC-01 stBL99I-LCH-IOC-01.boot
