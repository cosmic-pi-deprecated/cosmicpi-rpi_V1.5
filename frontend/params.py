from flask_restful import Resource
from .config import Config
import sqlite3


SQLITE_LOCATION = Config.get("Storage", "sqlite_location")


class Params(Resource):
    def get(self):
        params = {'HardwareSerial': Params._get_serial()}

        # Get the latest datapoint
        conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
        latest_datapoint = cursor.fetchone()

        # Get column names
        cursor.execute("PRAGMA table_info(Events);")
        col_names = cursor.fetchall()
        conn.close()

        # Extract data
        for i in range(0, len(col_names)):
            # Field name
            f_name = col_names[i][1]

            # Fill in values
            params[f_name] = latest_datapoint[i]
        return params

    @staticmethod
    def _get_serial():
        """
        Extract serial from cpuinfo file
        """
        cpu_serial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpu_serial = line[10:26]
            f.close()
        except:
            cpu_serial = "ERROR000000000"
        return cpu_serial
