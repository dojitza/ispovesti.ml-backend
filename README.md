# ispovesti.ml-backend

This is the source code of the backend service for ispovesti.ml

## Installation
First, acquire the source code, either by cloning this repository or downloading it directly

Cloning:
```
git clone git@github.com:dojitza/ispovesti.ml-backend.git
```
Two installation methods are provided: You can use docker compose or manually install the components.

### A. Docker-compose
Use the provided docker-compose file to build and start the backend automatically. Make sure to have docker-compose installed prior to running this command.
```console
$ cd ispovesti.ml-backend
$ docker-compose up
```
### B. Manual

1. Setup the virtual environment, and install the requirements.

```console
$ cd ispovesti.ml-backend
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

2. Install the rabbitmq broker and make sure its service is started (you may wish to enable it as well)
. This assumes you use apt as your package manager and systemd as your init daemon

```console
$ sudo apt install rabbitmq-server
$ sudo systemctl start rabbitmq
$ sudo systemctl enable rabbitmq
```

3. Download and unpack the model from the corresponding version github assets (the following link is for v2.0)
https://github.com/dojitza/ispovesti.ml-backend/releases/download/v2.0/trained_model.tar \
After unpacking, your tree should look like this:

```
├── LICENSE.md
├── README.md
├── checkpoint
│   └── run1
│       ├── checkpoint
│       ├── counter
│       ├── encoder.json
│       ├── events.out.tfevents.1599479304.22233ed79ca3
│       ├── hparams.json
│       ├── model-39563.data-00000-of-00001
│       ├── model-39563.index
│       ├── model-39563.meta
│       └── vocab.bpe
├── constants.py
├── dailyReset.py
├── db.py
...
```


#### Launching the service:

You can use gunicorn, or any other wsgi server.

```
cd ispovesti.ml-backend
pip3 install gunicorn
gunicorn main:app --bind 0.0.0.0:8080
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3 ](https://choosealicense.com/licenses/gpl-3.0/)
