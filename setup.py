from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
import os


# Development
# Install requirements: python-setuptools (`sudo apt install python-setuptools`)
# Run installation command: `sudo python setup.py install`

# Installation
# `sudo pip install cosmicpi`


PREINSTALL = """
    # Check if OS has `apt` command
    if [ "$(command -v apt)" != '' ]; then
        echo "--- Updating packages"
        sudo apt --yes update
        sudo apt --yes upgrade

        echo "--- Installing packages general purpose packages"
        sudo apt --yes install git \
            htop \
            mosquitto \
            mosquitto-clients

        echo "--- Installing Python packages"
        sudo apt --yes install python-numpy \
            python-matplotlib \
            python-flask \
            python-configparser \
            python-serial \
            python-flask-restful
    fi
"""


POSTINSTALL = """
    echo "--- Setting up services"
    # Hope an OS uses systemd (not SysVinit or similar)
    sudo systemctl enable cosmicpi-mqtt.service
    sudo systemctl start cosmicpi-mqtt.service
    sudo systemctl enable cosmicpi-dbcleaner.service
    sudo systemctl start cosmicpi-dbcleaner.service
    sudo systemctl enable cosmicpi-detector.service
    sudo systemctl start cosmicpi-detector.service
    sudo systemctl enable cosmicpi-ui.service
    sudo systemctl start cosmicpi-ui.service
    sudo systemctl daemon-reload

    echo "--- Finished setup! Rebooting now, when this is done your Cosmic Pi should start working ---"
    echo "--- To connect go to the IP address assigned by your network to the CosmicPi device, or  ---"
    echo "--- cosmicpi.local if you have the correct type of browser. If you are operating in      ---"
    echo "--- stand-alone mode via the CosmicPi wifi network, go directly to 192.168.12.1          ---"
    echo "--- Note that this Cosmic Pi will automatically publish all cosmic ray and associated    ---"
    echo "--- meta-data (position, accelerometer, magnetometer, temperature, humidity, pressure)   ---"
    echo "--- to the internet for anyone to use under a CC0 license (no rights reserved)           ---"
    echo "--- and placed in the public domain. For license details see:                            ---"
    echo "--- https://creativecommons.org/share-your-work/public-domain/cc0/                       ---"  
"""


class CustomInstallCommand(install):
    def run(self):
        os.system(PREINSTALL)
        install.run(self)
        os.system(POSTINSTALL)


class CustomDevelopCommand(develop):
    def run(self):
        os.system(PREINSTALL)
        develop.run(self)
        os.system(POSTINSTALL)


class CustomEggInfoCommand(egg_info):
    def run(self):
        os.system(PREINSTALL)
        egg_info.run(self)
        os.system(POSTINSTALL)


setup(name='cosmicpi',
    version='1.5.7',
    description='UI for the CosmicPi cosmic ray detector',
    long_description='This software provides the user interface, temporary storage and connection to the internet storage for the detectors of the CosmicPi project. The Cosmic Pi project aims to build the world\'s largest open source distributed cosmic ray telescope. You too can be a part of the project, by becoming a Cosmic Pixel!',
    platforms=['noarch'],
    maintainer='Cosmic Pi Team',
    maintainer_email='info@cosmicpi.org',
    url='http://cosmicpi.org/',
    license='GPL V2',
    project_urls={
        "Bug Tracker": "https://github.com/CosmicPi/cosmicpi-rpi_V1.5/issues",
        "Documentation": "https://github.com/CosmicPi/cosmicpi-rpi_V1.5/blob/master/README.md",
        "Source Code": "https://github.com/CosmicPi/cosmicpi-rpi_V1.5",
    },
    packages=[
        'cosmicpi',
        'cosmicpi.rest',
        'cosmicpi.storage',
        'cosmicpi.ui',
    ],
    package_data={
        'cosmicpi.ui': ['dist/*', 'index.html'],
        'cosmicpi.storage': ['cosmicpi.sqlite3'],
    },
    data_files=[
        ('/etc/systemd/system', [
            'data_files/cosmicpi-ui.service',
            'data_files/cosmicpi-mqtt.service',
            'data_files/cosmicpi-detector.service',
            'data_files/cosmicpi-dbcleaner.service',
        ]),
        ('/etc', [
            'data_files/cosmicpi.config',
            ]
        ),
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'flask',
        'configparser',
        'pyserial',
        'flask_restful',
        'flask_cors',
    ],
    scripts=[
        'bin/cosmicpi-dbcleaner',
        'bin/cosmicpi-detector',
        'bin/cosmicpi-mqtt',
        'bin/cosmicpi-rest',
        'bin/cosmicpi-ui',
    ],
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand,
    },
)
