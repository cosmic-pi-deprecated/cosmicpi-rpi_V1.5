import configparser
import os
import cosmicpi.storage


Config = configparser.ConfigParser()
Config.read(['/etc/cosmicpi.config', 'data_files/cosmicpi.config'])


# Set SQLite database path if not exist in config
if not Config.has_option('Storage', 'sqlite_location'):
    storage_path = os.path.abspath(cosmicpi.storage.__file__)
    sqlite_path = os.path.join(os.path.dirname(storage_path), 'cosmicpi.sqlite3')
    Config.set('Storage', 'sqlite_location', sqlite_path)
