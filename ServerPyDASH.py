
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
# from secret_pass import *
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


		version = "0.1.1"

		logging.basicConfig(filename='/var/PiPyDASH/debug.log',level=logging.WARNING)
		logging.info('Starting PiPyDASH')


		self.folder_RUSH  = "/var/PiPyDASH/STORAGE/"
		self.folder_TODO 	= "/var/PiPyDASH/TODO/"
		self.folder_DONE 	= "/var/PiPyDASH/DONE/"
		self.folder_ERROR 	= "/var/PiPyDASH/ERROR/"
		self.folder_NEW 	= "/var/PiPyDASH/NEW/"
		

		poTOKEN = "aw6mfguztvs6irod2k2o8yxqpuwkjx"
		poUSER_KEY = "gtwbip1rrtuduivghs14gw1s93ezee"



		if not os.path.exists(self.folder_RUSH):
			os.makedirs(self.folder_RUSH)
			logging.info('Creating missing folder %s', self.folder_RUSH) 
		if not os.path.exists(self.folder_TODO):
			os.makedirs(self.folder_TODO)
			logging.info('Creating missing folder %s', self.folder_TODO) 
		if not os.path.exists(self.folder_DONE):
			os.makedirs(self.folder_DONE)
			logging.info('Creating missing folder %s', self.folder_DONE) 
		if not os.path.exists(self.folder_ERROR):
			os.makedirs(self.folder_ERROR)
			logging.info('Creating missing folder %s', self.folder_ERROR) 
		if not os.path.exists(self.folder_NEW):
			os.makedirs(self.folder_NEW)
			logging.info('Creating missing folder %s', self.folder_NEW) 



		print("SERVER PiPyDASH 	: " + colored(version, 'magenta'))
		print("folder_RUSH 	: " + colored(self.folder_RUSH, 'magenta'))
		print("folder_DONE 	: " + colored(self.folder_DONE, 'magenta'))
		print("folder_NEW 	: " + colored(self.folder_NEW, 'magenta'))
		print("folder_ERROR : " + colored(self.folder_ERROR, 'magenta'))




		self.failetimeout = 300;

		init(poTOKEN)
		self.po = Client(poUSER_KEY, api_token=poTOKEN)

		self.hadThings	 	= True; # Startup message

		try:
			while True:


				self.hasRushFILE 	= False;
				self.rushFILE 		= glob.glob(self.folder_RUSH+"*.MP4")
				if(len(self.rushFILE) > 0):
					self.hasRushFILE 	= True;



				# SEEK BLACK FRAME 2
				if (self.hasRushFILE == True ):
					print ("\nTASK : " + colored("Seek black frame", 'green'))
					logging.info('Seek black frame') 
					vid = self.rushFILE[0];


					spinner = Spinner('Waiting file finish uploading... ')
					while True :
						filesize = os.path.getsize(vid)
						for x in range(0, 10):
							spinner.next()
							time.sleep(1)

						filesize2 = os.path.getsize(vid)
						if(filesize==filesize2):
							break




					file = os.path.basename(vid)
					videoID, file_extension = os.path.splitext(file)
					report = self.seekBlackFrame(vid)
					print("majoritaireREPORT", report);
					logging.info('report  %s', report) 
					dest = self.folder_DONE+videoID+"-"+report+file_extension
					print("dest", str(dest));
					shutil.move(vid,dest)


				else:
					if(self.hadThings):
						self.hadThings	 	= False;
						print ("\nTASK : " + colored("Waiting for RUSH", 'green'))
						self.pushLog("Waiting for RUSH","Waiting for RUSH")

		except KeyboardInterrupt:
			print(colored("\nExiting by user request.", 'magenta'))
		# except:
		# 	e = sys.exc_info()
		# 	self.pushLog("DASH AGENT FAIL", str(e),"siren")
		# 	print(colored("\nDASH AGENT FAIL.", 'magenta'))
		# 	sys.exit(0)



	def pushLog(_self,title,message,s="bike"):
		_self.po.send_message( "SERVER " + message + " at " +  str(datetime.datetime.now()), title=title,sound=s)


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






	def seekBlackFrame(self,videofile,gap=3,cduration=60):
		print(videofile)
		filename = ntpath.basename(videofile)
		self.pushLog("Seeking FRAME", filename)
		clip = VideoFileClip(videofile)
		fps= 1/gap
		nframes = clip.duration*fps # total number of frames used
		sequences=[]
		i=0
		blackframe=0
		report="MIN"
		try:

			for frame in clip.iter_frames(fps,dtype=int,progress_bar=True):
				i = i + 1
				red = frame[400,:,0].max();
				green = frame[400,:,1].max();
				blue = frame[400,:,2].max();
				average=int((red+green+blue)/3)
				t = i / fps
				timestamp = str(datetime.timedelta(seconds=t))

				if(average>0):
					
					if(blackframe>0):
						blackframe=0
						report="MAJ"
						print("MAJORITAIRE DETECTED");
						clipbegin = t-cduration-gap
						if(clipbegin < 0): clipbegin = 2
						print("clipbegin",clipbegin);
						if(len(sequences)>0) : # Avoiding overlap 
							pre_end_time = (sequences[len(sequences)-1][1])
							print("pre_end_time",pre_end_time)
							begin_time = datetime.timedelta(seconds=clipbegin)
							print("begin_time",begin_time)
							if(begin_time < pre_end_time):
								clipbegin = pre_end_time # TODO : Add gap  
								print("rewrite clipbegin",clipbegin)
						clipend = t-(gap*2)
						print("clipend",clipend)


						begin_time = datetime.timedelta(seconds=clipbegin)
						print("begin_time2",begin_time)
						end_time = datetime.timedelta(seconds=clipend)
						print("end_time2",end_time)
						sequences.append([(begin_time),(end_time)])

				elif(average == 0): # DETECTING BLACK FRAME
					blackframe=blackframe+1
					
			# bar.finish()
			
			if(len(sequences)>0):
				print(" ")
				print("Sequences founds")
				print(sequences)
				print("I founded %s" % colored( str(len(sequences))+" majority repport", 'red') )
				filename = os.path.basename(videofile)
				for seq in sequences:
					begin_time 		= str(seq[0])
					end_time 		= str(seq[1])
					print("begin_time",begin_time)
					print("end_time",end_time)
					new_filename 	= "%s%s-%s->%s.MP4" % (self.folder_NEW,filename,begin_time.replace(":", "-"),end_time.replace(":", "-"))
					# FFMEPG
					print("Exporting video to  :  %s" % colored("%s-%s->%s.MP4" % (filename,begin_time.replace(":", "-"),end_time.replace(":", "-")), 'green'))
					print(" ")
					os.chdir(self.folder_NEW)
					try:
						self.pushLog("MAJORITY REPORT", new_filename)
						subprocess.check_output([ 'ffmpeg','-ss',begin_time,'-i',videofile,'-to','0:01:00','-c','copy',new_filename],stderr=subprocess.STDOUT)
					except subprocess.CalledProcessError:
						e = sys.exc_info()
						print("Error  :	" + colored( str(len(e)), 'red', attrs=['reverse']) )
						self.pushLog("FAIL Saving REPORT", new_filename , "siren")
						print ("\nUnable to ffmpeg : "+videofile+"\n !")	
				return report
						

			else:
				print(" ")
				print("Reckon as a   %s" % colored("minority repport", 'red'))
				self.pushLog("MINORITY REPORT", filename)
				return report
		
		except:
			e = sys.exc_info()
			print("unable to seekblack frame :	" + colored(filename, 'white',  'on_red'))
			print(colored(e, 'white',  'on_red'))
			print("waiting:	" + colored(str(self.failetimeout)+" seconds\n", 'magenta'))
			self.pushLog("FAIL seekblack frame "+filename, str(e) ,"siren")
			time.sleep(self.failetimeout)


os.system('cls' if os.name == 'nt' else 'clear')
dash = PiPyDASH()

	



