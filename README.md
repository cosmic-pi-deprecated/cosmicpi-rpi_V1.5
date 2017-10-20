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
*   Read data from the detector into the SQLite database    [DONE]
*   Display basic information in the Web-UI                 [DONE]
*   Start application on boot                               [In development]
*   Start hotspot on boot                                   [In development]
*   Connect to a different WiFi via the webinterface        [Not yet started]
*   Working install procedure                               [Not yet started]
*   SystemD services for all components                     [Not yet started]
    *   Detector readout
    *   WebUI
    *   Hotspot
* Interface for getting the raw data and database dumps     [Not yet started]
* Interface to create custom plots                          [DONE]
* Include about page                                        [DONE]

## Proposed future features
* Enforce read only access for the UI
* Create additional ways to work with the data, focused on the needs of teachers in schools
* Database maintainance: Look at ways to aggregate the data, to avoid bloating of the database

## Installation
Clone this repository to the home folder of your CosmicPi (e.g. `/home/pi`)
then run:

```./install```

This will currently do nothing. Just clone the repository.

## Run
The software is normally controlled via SystemD. This is not yet implemented, so you will need to run the scripts directly.


