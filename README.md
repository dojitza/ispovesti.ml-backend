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

Install the rabbitmq broker and make sure its service is started (you may wish to enable it as well)
this assumes you use apt as your package manager and systemd as your init daemon

```
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq
sudo systemctl enable rabbitmq
```

## Launching the service:

You can use gunicorn.

```
cd ispovesti.ml-backend
pip3 install gunicorn
gunicorn main:app --bind 0.0.0.0:8080
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3 ](https://choosealicense.com/licenses/gpl-3.0/)
