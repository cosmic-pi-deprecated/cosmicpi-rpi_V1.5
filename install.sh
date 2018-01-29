#!/bin/bash
echo "Sorry. This procedure isn't ready yet, We're working on it! "

echo "--- Expanding root file system ---"
sudo raspi-config --expand-rootfs
cp -f rebootrc.local /etc/rc.local