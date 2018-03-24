# CosmicPi REST API

## Development
Make sure that CosmicPi UI service does not run (`sudo systemctl stop CosmicPi-UI`), 
navigate to `/rest` and run:
```
FLASK_DEBUG=1 FLASK_APP=${PWD}/app.py python -m flask run --host=0.0.0.0
```

## API
- GET `/histogram.png?from=0&to=1521059693&bin_size=1`
- GET `/wifi`
- PUT `/wifi?ssid=CosmicPi&pass=12345678`
- GET `/series?format=csv`
