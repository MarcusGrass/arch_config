#!/bin/bash
bluetoothctl -- untrust 4C:87:5D:2C:57:6A
bluetoothctl -- remove 4C:87:5D:2C:57:6A
timeout 5s bluetoothctl -- scan on
bluetoothctl -- trust 4C:87:5D:2C:57:6A
bluetoothctl -- pair 4C:87:5D:2C:57:6A
bluetoothctl -- connect 4C:87:5D:2C:57:6A
