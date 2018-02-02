#!/bin/bash
echo "Sorry. This procedure isn't ready yet, We're working on it! "

echo "--- Part 1: Expand the file system ---"
echo "--- Expanding root file system ---"
#chmod +x rebootrc.local
sudo raspi-config --expand-rootfs
#cp -f rebootrc.local /etc/rc.local
chmod +x installparttwo.sh

echo "--- Finished setup part 1! Rebooting, log back in and run sudo ./installparttwo.sh for part 2 ---"
sleep 10
sudo reboot now
