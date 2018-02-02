#!/bin/bash
echo "In case of any issues please consult cosmicpi.org for help, or contact us via Facebook "

echo "--- Part 1: Expand the file system ---"
echo "--- Expanding root file system ---"
#chmod +x rebootrc.local
sudo raspi-config --expand-rootfs
#cp -f rebootrc.local /etc/rc.local
chmod +x installparttwo.sh

echo "--- Finished setup part 1! Rebooting, log back in and run sudo ./installparttwo.sh for part 2 ---"
sleep 10
sudo reboot now
