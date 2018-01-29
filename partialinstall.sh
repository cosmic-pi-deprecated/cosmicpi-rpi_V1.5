#!/bin/bash
echo "Sorry. This procedure isn't ready yet, We're working on it! "

echo "--- Part 2: Updates and installation ---"
echo "--- Updating packages"
sudo apt --yes update
sudo apt --yes upgrade

echo "--- Installing packages via apt"
# needed for the CosmicPi software
sudo apt --yes install git python-pip htop python-numpy python-matplotlib python-flask mosquitto mosquitto-clients

echo "--- Installing python packages via pip"
sudo pip  --no-cache-dir install pyserial configparser flask_googlemaps Flask-BasicAuth --extra-index-url https://www.piwheels.hostedpi.com/simple
#echo "we might need some more packages"

echo "--- Getting executable path"
EXECPATH="`dirname \"$0\"`"              # relative
EXECPATH="`( cd \"$EXECPATH\" && pwd )`"  # absolutized and normalized
if [ -z "$EXECPATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  exit 1  # fail
fi
echo "$EXECPATH"
TOREPLACE="PATH_TO_EXECUTABLE"

echo "--- Setting up systemd services"
sed -i -e "s+$TOREPLACE+$EXECPATH+g" install_files/CosmicPi-mqtt.service
sed -i -e "s+$TOREPLACE+$EXECPATH+g" install_files/CosmicPi-database_cleaner.service
sed -i -e "s+$TOREPLACE+$EXECPATH+g" install_files/CosmicPi-detector.service
sed -i -e "s+$TOREPLACE+$EXECPATH+g" install_files/CosmicPi-UI.service
sudo cp -f install_files/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable CosmicPi-mqtt.service
sudo systemctl enable CosmicPi-database_cleaner.service
sudo systemctl enable CosmicPi-detector.service
sudo systemctl enable CosmicPi-UI.service
#the ap was already done

echo "--- changing static ip address to 192.168.12.1 ---" 
cp -f dhcpcd.conf /etc/dhcpcd.conf

echo"--- preventing this script from running next reboot ---"
cp -f normalrc.local /etc/rc.local

echo "--- Finished setup! Rebooting now ---"
sleep 10
sudo reboot now
