#!/bin/bash

if [ -f "/home/pi/.homebridge/scripts/wakeup_key" ]; then
  exit 0
fi
exit 1

