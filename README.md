# ispovesti.ml-backend

This is the backend service for ispovesti.ml

## Installation

Clone this repository, setup the virtual environment, and install the requirements.

```
git clone git@github.com:dojitza/ispovesti.ml-backend.git
cd ispovesti.ml-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Launching the service:

Note the PYTHONHASHSEED environment variable. When deploying to production, take note to pass this environment variable to your server if you want to preserve your unique user identification over service restarts.

### bash shell

```
FLASK_APP=main.py FLASK_ENV=development PYTHONHASHSEED=124391405 flask run --host=0.0.0.0 -p 5000
```

### fish shell

```
env FLASK_APP=main.py FLASK_ENV=development PYTHONHASHSEED=124391405 flask run --host=0.0.0.0
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3 ](https://choosealicense.com/licenses/gpl-3.0/)
