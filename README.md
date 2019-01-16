
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

## CHANGELOG

[X] Seek black frame kick FAIL notif

[X] Fix allready existing remote file :
```
Uploading RUSH : /home/pi/PiPyDASH/RUSH/FILE2119.MP4 -> /var/www/_DERUSH_CAM/RUSH/
100%|###############################################################################| 3.94G/3.94G [23:35<00:00, 2.78Mb/s]
unable to backup :	/home/pi/PiPyDASH/RUSH/FILE2119.MP4
(<class 'shutil.Error'>, Error("Destination path '/home/pi/PiPyDASH/DERUSH/TODO/FILE2119.MP4' already exists",), <traceback object at 0x737e4698>)
waiting:	300 seconds
```

