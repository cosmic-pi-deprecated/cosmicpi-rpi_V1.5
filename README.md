# Cosmic Pi Software on the Raspberry Pi

This software runs on the raspberry pi, which is integral to the CosmicPi V1.5.
The central point is a SQLite database into which data is stored, as well as read from.
More instructions will follow when the software has reached the state of the V2 mock-up software.

## Current features
*   Create a SQLite database
*   Read the serial output from the Arduino Due, parse it and store the information into the SQLite database
*   Application for the UI, under development
*   *Note*: The parser will only store data if the detector is fully working, e.g. Sensors are working/enabled and the GPS has a connection / is working


## Needed features to match up with the Version 2 mock-up software
- [x]   Read data from the detector into the SQLite database
- [x]   Display basic information in the Web-UI
- [x]   Start application on boot
- [x]   Start hotspot on boot
- [ ]   Connect to a different WiFi via the WebUI
- [ ]   Working install procedure
- [x]   SystemD services for all components
    - [x]   Detector readout
    - [x]   WebUI
    - [x]   Hotspot
- [ ] Interface for getting the raw data and database dumps
- [x] Interface to create custom plots
- [x] Include about page
- [ ] Add useful configurations to the config file
- [ ] Do a test of the installation on a clean raspbian lite installation
- [ ] Do an as complete as possible test of all components after a fresh installation

## Proposed future features
* Enforce read only access to the DB for the UI
* Setup proper logging mechanisms for all parts of the software
* Create additional ways to work with the data, focused on the needs of teachers in schools
* Database maintenance: Look at ways to aggregate the data, to avoid bloating of the database
* Do the installation in a proper way, as example with setuptools
* Run flask on an actual webserver, not the built-in development server
* Lock settings page behind a password protection (create a session in flask, etc.)

## Installation
Clone this repository to the home folder of your CosmicPi (e.g. `/home/pi`). Switch into the repository (e.g. `cd /home/pi/cosmicpi-rpi_V1.5`).
Then run:

```./install```

This may or may not work. It is not completely tested at the moment.
The installation will most likely take some time. Wspecially on the raspbian lite distro numpy will need to be compiled first and that takes quite long.
It would be great if you were to give it a try anyways.
In case something fails, please submit an issue with the output you got. Thanks!

## Run
The software is normally controlled via SystemD.
*Optional:* Reboot to automatically start the software as a SystemD service

**Start or stop** the detector connector as a service with: `sudo systemctl start CosmicPi-detector` or `sudo systemctl stop CosmicPi-detector`

**Start or stop** the WebUI as a service with: `sudo systemctl start CosmicPi-UI` or `sudo systemctl stop CosmicPi-UI`

**Start or stop** the Hotspot as a service with: `sudo systemctl start create_ap` or `sudo systemctl stop create_ap`

**View the log output** of either program with: `sudo systemctl status CosmicPi-detector` or `sudo systemctl status CosmicPi-UI` or `sudo systemctl status create_ap`

The application is available at:

`http://cosmicpi.local/` or `http://127.0.0.1/`

When used as an access point the application is available at:

`http://cosmicpi.local/` or `http://192.168.12.1/`

#### For debugging
Stop all mentioned services. After this you should be able to run the software directly via the commandline.

