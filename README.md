
# PiPyDASH

A script to derush camera from a Raspberry using Python.
The main purpose is to been able to identify sequences of "black frame" 

## Install

- Check that Python 3.5 is installed 
- Install FFMPEG and export bin to PATH

## Setup
Create a file name secret_pass.py à la racine du dossier avec les variables suivantes :

```
host = "IP du server"
username = "user name"
password = "user password"
poUSER_KEY = "PushOver user key"
poTOKEN = "Pushover Token"
port = 22
```

## Run

```
python3.5 agent.py
```