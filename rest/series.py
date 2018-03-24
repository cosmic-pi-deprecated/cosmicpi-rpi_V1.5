from flask import request, make_response
from flask_restful import Resource
from .config import Config
import sqlite3
import io
import csv


SQLITE_LOCATION = Config.get("Storage", "sqlite_location")


class Series(Resource):
    def get(self):
        format = request.args['format']
        limit = request.args.get('limit', 20)
        since = request.args.get('since', 0)

        conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
        cursor = conn.cursor()

        # Get column names
        cursor.execute("PRAGMA table_info(Events);")
        col_data = cursor.fetchall()
        col_names = []
        for i in range(0, len(col_data)):
            col_names.append(col_data[i][1])

        # Get data from database
        cursor.execute("SELECT * FROM Events WHERE UTCUnixTime >= %d ORDER BY UTCUnixTime DESC, SubSeconds DESC LIMIT %d;" % (since, limit))
        data = cursor.fetchall()
        conn.close()

        if format == 'json':
            return Series._get_json(col_names, data)
        elif format == 'csv':
            return Series._get_csv(col_names, data)

    @staticmethod
    def _get_json(col_names, data):
        items = []
        for row in data:
            item = {}
            for i in range(len(col_names)):
                item[col_names[i]] = row[i]
            items.append(item)
        return items

    @staticmethod
    def _get_csv(col_names, data):
        """
        Write CSV export to memory
        """
        output = io.BytesIO()
        writer = csv.writer(output)
        writer.writerow(col_names)
        writer.writerows(data)

        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        return response
