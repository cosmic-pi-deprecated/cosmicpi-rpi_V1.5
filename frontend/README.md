# CosmicPi REST API

## Development
Make sure that CosmicPi UI service does not run (`sudo systemctl stop CosmicPi-UI`), 
navigate to `/frontend` and run:
```
FLASK_DEBUG=1 FLASK_APP=${PWD}/app.py python -m flask run --host=0.0.0.0
```