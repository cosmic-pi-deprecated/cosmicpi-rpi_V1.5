# Cosmic Pi Software on the Raspberry Pi

[![Build Status](https://travis-ci.org/CosmicPi/cosmicpi-rpi_V1.5.svg?branch=rest)](https://travis-ci.org/CosmicPi/cosmicpi-rpi_V1.5)

This software runs on the Raspberry Pi, which is integral to the CosmicPi V1.5.
The central point is a SQLite database into which data is stored, as well as read from.
More instructions will follow when the software has reached the state of the V2 mock-up software.

## Installation
For CosmicPi software installation only please use:
```
pip install cosmicpi
```

If you have scratch Raspbian image and you want to install software, expand filesystem, configure AP... please use:
```
curl https://gist.githubusercontent.com/lukicdarkoo/e33e00c6780ad0215d3932b810a10e46/raw | sh
```


## Run
The software is normally controlled via SystemD. The following services are available:
- cosmicpi-ui
- cosmicpi-rest
- cosmicpi-mqtt
- cosmicpi-dbcleaner
- cosmicpi-detector

From the Raspberry Pi itself the application is available at:

`http://cosmicpi.local/` or `http://127.0.0.1/`

When used as an access point the application is available at:

`http://cosmicpi.local/` or `http://10.0.0.1/`

#### Debugging the software:
Stop all mentioned services. After this you should be able to run the software directly via the commandline.
