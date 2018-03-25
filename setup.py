from setuptools import setup
from setuptools.command.install import install
import os


class PostInstall(install):
    def run(self):
        install.run(self)
        #os.system('cosmicpi-postinstall')


setup(name='cosmicpi',
    version='1.5.2',
    description='Open source cosmic ray detector',
    long_description='The Cosmic Pi project aims to build the world\'s largest open source distributed cosmic ray telescope. You too can be a part of the project, by becoming a Cosmic Pixel!',
    platforms=['noarch'],
    maintainer='Cosmic Pi Team',
    maintainer_email='info@cosmicpi.org',
    url='http://cosmicpi.org/',
    license='GPL V2',
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
        ('/etc/systemd/system/', ['data_files/*.service']),
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
