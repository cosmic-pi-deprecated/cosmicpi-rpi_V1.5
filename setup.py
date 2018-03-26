from setuptools import setup
from setuptools.command.install import install
import os


class PostInstall(install):
    def run(self):
        install.run(self)
        #os.system('cosmicpi-postinstall')


setup(name='cosmicpi',
    version='1.5.2',
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
        ('/etc/systemd/system/', [
            'data_files/cosmicpi-ui.service',
            'data_files/cosmicpi-mqtt.service',
            'data_files/cosmicpi-detector.service',
            'data_files/cosmicpi-dbcleaner.service',
        ]),
        ('/etc', ['data_files/cosmicpi.config']),
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
        'bin/cosmicpi-postinstall',
    ],
    cmdclass={
        'install': PostInstall,
    },
)
