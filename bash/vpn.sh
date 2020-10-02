#!/bin/bash
key="$1"

case $key in
	-r)
	/opt/cisco/anyconnect/bin/vpn disconnect && /opt/cisco/anyconnect/bin/vpn connect host
	;;
-c)
	/opt/cisco/anyconnect/bin/vpn connect host
	;;
-d)
	/opt/cisco/anyconnect/bin/vpn disconnect
esac
