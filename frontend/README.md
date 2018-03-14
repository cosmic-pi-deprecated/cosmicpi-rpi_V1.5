# CosmicPi REST API

## Development
Make sure that CosmicPi UI service does not run (`sudo systemctl stop CosmicPi-UI`), 
navigate to `/frontend` and run:
```
FLASK_DEBUG=1 FLASK_APP=${PWD}/app.py python -m flask run --host=0.0.0.0
```

## API
- GET `/histogram.png?start_time=0&end_time=1521059693&bin_size_seconds=1`
- GET `/params`
- GET `/wifi`
- PUT `/wifi?ssid=CosmicPi&pass=12345678`
- GET `/data?format=csv`