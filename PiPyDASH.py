
# /etc/init.d/PiPyDASH.py
### BEGIN INIT INFO
# Provides:          sample.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from moviepy.editor import VideoFileClip, ImageClip
import time
import glob
import os.path
import paramiko
from pprint import pprint
from pushover import init, Client
import ntpath
from progress.bar import ChargingBar
from progress.spinner import Spinner
import datetime
from termcolor import colored, cprint
import shutil
import subprocess
from secret_pass import *
import sys
import logging

class PiPyDASH():
	def __init__(self):
		cprint("   	",'magenta',attrs=['bold'])
		cprint("  __________________________________________________	",'magenta',attrs=['bold'])
		cprint("   ____  ____  ____  _  _  ____    __    ___  _   _ 	",'magenta',attrs=['bold'])
		cprint("  (  _ \(_  _)(  _ \( \/ )(  _ \  /__\  / __)( )_( )	",'magenta',attrs=['bold'])
		cprint("   )___/ _)(_  )___/ \  /  )(_) )/(__)\ \__ \ ) _ ( 	",'magenta',attrs=['bold'])
		cprint("  (__)  (____)(__)   (__) (____/(__)(__)(___/(_) (_)	",'magenta',attrs=['bold'])
		cprint("  __________________________________________________	",'magenta',attrs=['bold'])
		cprint("   	",'magenta',attrs=['bold'])


		version = "0.1.0"

		logging.basicConfig(filename='/home/pi/PiPyDASH/debug.log',level=logging.WARNING)
		logging.info('Starting PiPyDASH')


		self.camera_PATH  = "/mnt/usbstorage/DCIM/100MEDIA/" 
		self.remote_PATH  = "/var/PiPyDASH/STORAGE/"
		self.folder_RUSH  = "/home/pi/PiPyDASH/STORAGE/"

		





		if not os.path.exists(self.folder_RUSH):
			os.makedirs(self.folder_RUSH)
			logging.info('Creating missing folder %s', self.folder_RUSH) 




		print("PiPyDASH 	: " + colored(version, 'magenta'))
		print("camera_PATH 	: " + colored(self.camera_PATH, 'magenta'))
		print("remote_PATH 	: " + colored(self.remote_PATH, 'magenta'))





		self.failetimeout = 300;

		init(poTOKEN)
		self.po = Client(poUSER_KEY, api_token=poTOKEN)

		self.hadThings	 	= True; # Startup message

		try:
			while True:
				self.hasCameraFILE 	= False;
				self.hasthmFILE 	= False;
				self.hasRushFILE 	= False;
				

				self.cameraFILE 	= glob.glob(self.camera_PATH+"*.MP4")
				self.thmFILE 		= glob.glob(self.camera_PATH+"*.THM")
				self.rushFILE 		= glob.glob(self.folder_RUSH+"*.MP4")

				


				if(len(self.thmFILE) > 0):
					self.hasthmFILE 	= True;
				if(len(self.cameraFILE) > 0):
					self.hasCameraFILE 	= True;
				if(len(self.rushFILE) > 0):
					self.hasRushFILE 	= True;

					self.hasNewFILE 	= True;

				logging.debug('self.hasthmFILE :  %s', self.hasthmFILE) 
				logging.debug('self.hasCameraFILE :  %s', self.hasCameraFILE) 
				logging.debug('self.hasRushFILE :  %s', self.hasRushFILE) 


									
				# Clean THM
				if (self.hasthmFILE):
					print ("\nTASK : " + colored("Cleaning THM "+ self.thmFILE[0], 'green'))
					logging.info('Cleaning THM %s', self.thmFILE[0]) 
					for entry in self.thmFILE:
						os.remove(entry)

				# BACKUP
				if (self.hasCameraFILE):
					self.hadThings	 	= True;
					print ("\nTASK : " + colored("Backuping camera "+ self.cameraFILE[0], 'green'))
					logging.info('Backuping camera %s', self.cameraFILE[0]) 
					self.backupCamera(self.cameraFILE[0])

				# UPLOAD RUSH
				elif (self.hasCameraFILE == False and  self.hasRushFILE == True):
					logging.info('Uploading rush  %s', self.rushFILE[0]) 
					print ("\nTASK : " + colored("Uploading rush", 'green'))
					self.uploadRUSH(self.rushFILE[0],self.remote_PATH)

				else:
					if(self.hadThings):
						self.hadThings	 	= False;
						print ("\nTASK : " + colored("Waiting for camera", 'green'))
						logging.info('Waiting for camera') 
						self.pushLog("TASK Waiting for camera","Raspberry is waiting fo a camera to be connected")

		except KeyboardInterrupt:
			print(colored("\nExiting by user request.", 'magenta'))
		# except:
		# 	e = sys.exc_info()
		# 	self.pushLog("DASH AGENT FAIL", str(e),"siren")
		# 	print(colored("\nDASH AGENT FAIL.", 'magenta'))
		# 	sys.exit(0)



	def pushLog(_self,title,message,s="bike"):
		_self.po.send_message( "Pi " + message + " at " +  str(datetime.datetime.now()), title=title,sound=s)


	def viewBar(_self,a,b):
	    # original version
	    res = a/int(b)*100
	    sys.stdout.write('\rComplete precent: %.2f %%' % (res))
	    sys.stdout.flush()

	def tqdmWrapViewBar(_self,*args, **kwargs):
	    try:
	        from tqdm import tqdm
	    except ImportError:
	        # tqdm not installed - construct and return dummy/basic versions
	        class Foo():
	            @classmethod
	            def close(*c):
	                pass
	        return viewBar, Foo
	    else:
	        pbar = tqdm(*args, **kwargs)  # make a progressbar
	        last = [0]  # last known iteration, start at 0
	        def viewBar2(a, b):
	            pbar.total = int(b)
	            pbar.update(int(a - last[0]))  # update pbar with increment
	            last[0] = a  # update last known iteration
	        return viewBar2, pbar  # return callback, tqdmInstance



	def backupCamera(_self,source):
		print("backupCamera")
	
		# If the same file allready is this should be a previous fail copy
		dest = os.path.basename(source)
		file_allready_there = _self.folder_RUSH+dest
		if(os.path.isfile(file_allready_there)):
			print("BACKUP file allready exist deleting it: "+ colored(file_allready_there, "red"))
			_self.pushLog("Backup allready there, removing ", dest)
			os.remove(file_allready_there)
		
		filename = ntpath.basename(source)
		print("\nBackuping CAMERA :	" + colored(source, 'magenta'))
		_self.pushLog("Backuping CAMERA", filename)

		try:
			shutil.move(source,_self.folder_RUSH)
		except shutil.Error as e:
			print("unable to backup :	" + colored(source, 'white',  'on_red'))
			print(colored(e, 'white',  'on_red'))
			print("waiting:	" + colored(str(_self.failetimeout)+" seconds\n", 'magenta'))
			_self.pushLog("FAIL Backuping camera" + filename,str(e) ,"siren")
			time.sleep(_self.failetimeout)






	def uploadRUSH(_self,source,remote_PATH):

		dest = os.path.basename(source)
		filename = ntpath.basename(source)
		print("\nUploading RUSH : " + colored(source + " -> "+ remote_PATH, 'white',  'on_blue'))
		_self.pushLog("Uploading RUSH", filename)
		try:
			transport = paramiko.Transport((host, port))
			transport.connect(username = username, password = password)
			sftp = paramiko.SFTPClient.from_transport(transport)
			path = remote_PATH + dest 
			localpath = source
			cbk, pbar = _self.tqdmWrapViewBar(ascii=True, unit='b', unit_scale=True)
			sftp.put(localpath, path,callback=cbk)
			sftp.close()
			transport.close()
			pbar.close()

			os.remove(source)


			_self.po.send_message("upload RUSH done: " + dest, title="Upload done:"+dest,sound="bike")
			
		except:
			e = sys.exc_info()
			print("unable to backup :	" + colored(source, 'white',  'on_red'))
			print(colored(e, 'white',  'on_red'))
			print("waiting:	" + colored(str(_self.failetimeout)+" seconds\n", 'magenta'))
			_self.pushLog("FAIL Uploading RUSH "+filename, str(e) ,"siren")
			time.sleep(_self.failetimeout)



os.system('cls' if os.name == 'nt' else 'clear')
dash = PiPyDASH()

	



