# Cosmic Pi Software on the Raspberry Pi

[![Build Status](https://travis-ci.org/CosmicPi/cosmicpi-rpi_V1.5.svg?branch=rest)](https://travis-ci.org/CosmicPi/cosmicpi-rpi_V1.5)

This software runs on the raspberry pi, which is integral to the CosmicPi V1.5.
The central point is a SQLite database into which data is stored, as well as read from.
More instructions will follow when the software has reached the state of the V2 mock-up software.

#### If you encounter any problems, please follow these steps:
1. Consult the manual, if available to you
2. Consult the [CosmicPi blog](http://cosmicpi.org/posts) (maybe the issue is very common and we have posted a solution for you)
3. Submit an issue here on github via the *Issues* tab, make sure to include the following:
   * What you are expecting to get from the detector/software
   * What you are currently getting from the detector/software
   * The version of the software that you are running
   * Any log output available to you (the more the better)
   * Any and all clues that you have on what might be going wrong

## Current features
*   All that is checked off in the next section
*   *Note*: The parser will only store data if the detector is fully working, e.g. Sensors are working/enabled and the GPS has a connection / is working.
This behaviour is very much open to discussion.


## Needed features to match up with the Version 2 mock-up software
- [x]   Read data from the Arduino Due (detector) into the SQLite database
- [x]   Display basic information in the WebUI
- [x]   Start application on boot
- [x]   Start hotspot on boot
- [x]   Connect to a different WiFi via the WebUI
- [x]   Working install procedure
- [x]   SystemD services for all components
    - [x]   Detector readout
    - [x]   WebUI
    - [x]   Hotspot
- [x] Interface for getting the raw data and database dumps
- [x] Authentication for the settings page
- [x] Interface to create custom plots
- [x] Include about page
- [x] Add useful configurations to the config file
- [x] Do a test of the installation on a clean raspbian lite installation
- [ ] Do an as complete as possible test of all components after a fresh installation



## Installation
Clone this repository to the home folder of your CosmicPi (e.g. `/home/pi`). Switch into the repository (e.g. `cd /home/pi/cosmicpi-rpi_V1.5`).
Then run:

```./install```

Though I have tested different parts of the installation script, I have not yet tested the whole thing on a completely clean system.
E.g.: The installation may or may not work.
The installation will most likely take some time. Especially on the raspbian lite distribution numpy will need to be compiled first and that takes quite long.
It would be great if you were to give it a try anyways.
In case something fails, please submit an issue with the output you got. Thanks!

## Run
The software is normally controlled via SystemD.
*Optional:* Reboot to automatically start the software as a SystemD service.

**Start or stop the detector connector:** `sudo systemctl start CosmicPi-detector` or `sudo systemctl stop CosmicPi-detector`

**Start or stop the WebUI:** `sudo systemctl start CosmicPi-UI` or `sudo systemctl stop CosmicPi-UI`

**Start or stop the Hotspot:** `sudo systemctl start hostapd` or `sudo systemctl stop hostapd
Note that you should also start and stop the dnsmasq service with the hostapd.`

**View the log output:** `sudo systemctl status CosmicPi-detector` or `sudo systemctl status CosmicPi-UI` or `sudo systemctl status create_ap`

From the raspberry pi itself the application is available at:

`http://cosmicpi.local/` or `http://127.0.0.1/`

When used as an access point the application is available at:

`http://cosmicpi.local/` or `http://10.0.0.1/`

#### Debugging the software:
Stop all mentioned services. After this you should be able to run the software directly via the commandline.

## Proposed future features
* Enforce read only access to the DB for the UI
* Setup proper logging mechanisms for all parts of the software (maybe with journalD ?)
* Create additional ways to work with the data, focused on the needs of teachers in schools
* Database maintenance: Look at ways to aggregate the data, to avoid bloating of the database
* Do the installation in a proper way, as example with setuptools
* Run flask on an actual webserver, not the built-in development server
* Lock the settings page behind a password protection (create a session in flask, etc.) [DONE]
* Sqlite database on a ram disk, should speed up access times dramatically
