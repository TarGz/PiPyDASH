
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

		self.camera_PATH  = "/mnt/usbstorage/DCIM/100MEDIA/" 
		self.remote_PATH  = "/var/www/_DERUSH_CAM/"
		self.folder_RUSH  = "/home/pi/PiPyDASH/STORAGE/"
		self.folder_TODO 	= "/home/pi/PiPyDASH/TODO/"
		self.folder_DONE 	= "/home/pi/PiPyDASH/DONE/"
		self.folder_ERROR 	= "/home/pi/PiPyDASH/ERROR/"
		self.folder_NEW 	= "/home/pi/PiPyDASH/NEW/"
		





		if not os.path.exists(self.folder_RUSH):
			os.makedirs(self.folder_RUSH)
		if not os.path.exists(self.folder_TODO):
			os.makedirs(self.folder_TODO)
		if not os.path.exists(self.folder_DONE):
			os.makedirs(self.folder_DONE)
		if not os.path.exists(self.folder_ERROR):
			os.makedirs(self.folder_ERROR)
		if not os.path.exists(self.folder_NEW):
			os.makedirs(self.folder_NEW)



		print("PiPyDASH 	: " + colored(version, 'magenta'))
		print("camera_PATH 	: " + colored(self.camera_PATH, 'magenta'))
		print("remote_PATH 	: " + colored(self.remote_PATH, 'magenta'))
		print("folder_RUSH 	: " + colored(self.folder_RUSH, 'magenta'))
		print("folder_DONE 	: " + colored(self.folder_DONE, 'magenta'))
		print("folder_NEW 	: " + colored(self.folder_NEW, 'magenta'))
		print("folder_ERROR : " + colored(self.folder_ERROR, 'magenta'))




		self.failetimeout = 300;

		init(poTOKEN)
		self.po = Client(poUSER_KEY, api_token=poTOKEN)

		self.hagThings	 	= True; # Startup message

		try:
			while True:
				self.hasCameraFILE 	= False;
				self.hasRushFILE 	= False;
				self.hasNewFILE 	= False;
				self.hasDoneFILE 	= False;
				

				self.cameraFILE 	= glob.glob(self.camera_PATH+"*.MP4")
				self.rushFILE 		= glob.glob(self.folder_RUSH+"*.MP4")
				self.doneFILE		= glob.glob(self.folder_DONE+"*.MP4")
				self.newFILE		= glob.glob(self.folder_NEW+"*.MP4")

				if(len(self.cameraFILE) > 0):
					self.hasCameraFILE 	= True;
				if(len(self.rushFILE) > 0):
					self.hasRushFILE 	= True;
				if(len(self.doneFILE) > 0):
					self.hasDoneFILE 	= True;
				if(len(self.newFILE) > 0):
					self.hasNewFILE 	= True;

				# print("self.hasCameraFILE " + str(self.hasCameraFILE))
				# print("self.hasRushFILE " + str(self.hasRushFILE))
				# print("self.hasDoneFILE " + str(self.hasDoneFILE))
				# print("self.hasNewFILE " + str(self.hasNewFILE))
				
				

				time.sleep(3)


				# BACKUP
				if (self.hasCameraFILE):
					self.hagThings	 	= True;
					print ("\nTASK : " + colored("Backuping camera "+ self.cameraFILE[0], 'green'))
					self.backupVideo(self.cameraFILE[0])

				# UPLOAD NEW
				elif (self.hasCameraFILE == False and self.hasNewFILE == True):
					print ("\nTASK : " + colored("Upload report", 'green'))
					self.uploadREPORT(self.newFILE[0],self.remote_PATH+"NEW/")

				# SEEK BLACK FRAME
				elif (self.hasCameraFILE == False and  self.hasRushFILE == True ):
					print ("\nTASK : " + colored("Seek black frame", 'green'))
					vid = self.rushFILE[0];
					file = os.path.basename(vid)
					videoID, file_extension = os.path.splitext(file)
					report = self.seekBlackFrame(vid)
					print("majoritaireREPORT", report);
					dest = self.folder_DONE+videoID+"-"+report+file_extension
					print("dest", str(dest));
					shutil.move(vid,dest)


				# UPLOAD RUSH
				elif (self.hasCameraFILE == False and  self.hasRushFILE == False and  self.hasNewFILE == False and  self.hasDoneFILE == True):
					print ("\nTASK : " + colored("Uploading rush", 'green'))
					self.uploadRUSH(self.doneFILE[0],self.remote_PATH+"RUSH/")

				else:
					if(self.hagThings):
						self.hagThings	 	= False;
						print ("\nTASK : " + colored("Waiting for camera", 'green'))
						self.pushLog("TASK Waiting for camera","Raspberry is waiting fo a camera to be connected")


		except KeyboardInterrupt:
			print(colored("\nExiting by user request.", 'magenta'))
			sys.exit(0)



	def pushLog(_self,title,message,s="bike"):
		_self.po.send_message( message + " at " +  str(datetime.datetime.now()), title=title,sound=s)


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



	def backupVideo(_self,source):
		# Clean THM
		# self.camera_preview = glob.glob(_self.camera_PATH+"*.THM")
		# if(len(_self.camera_preview) > 0):
		# 	for entry in self.camera_preview:
		# 		os.remove(entry)
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

		except:
			e = sys.exc_info()
			print("unable to backup :	" + colored(source, 'white',  'on_red'))
			print(colored(e, 'white',  'on_red'))
			print("waiting:	" + colored(str(_self.failetimeout)+" seconds\n", 'magenta'))
			_self.pushLog("FAIL Backuping camera" + filename,e ,"siren")
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

			# If exist ( due to a prior backup fail)
			file_allready_there = _self.folder_TODO+dest
			if(os.path.isfile(file_allready_there)):
				print("RUSH file allready exist deleting it: "+ colored(file_allready_there, "red"))
				os.remove(file_allready_there)
				_self.pushLog("Backup allready there, removing ", dest)

			shutil.move(source,_self.folder_TODO)


			_self.po.send_message("upload RUSH done: " + dest, title="Upload done:"+dest,sound="bike")
			
		except:
			e = sys.exc_info()
			print("unable to backup :	" + colored(source, 'white',  'on_red'))
			print(colored(e, 'white',  'on_red'))
			print("waiting:	" + colored(str(_self.failetimeout)+" seconds\n", 'magenta'))
			_self.pushLog("FAIL Uploading RUSH "+filename, str(e) ,"siren")
			time.sleep(_self.failetimeout)

	def uploadREPORT(_self,source,remote_PATH):

		dest = os.path.basename(source)
		filename = ntpath.basename(source)
		_self.pushLog("Uploading REPORT", filename)
		print("\nUploading file : " + colored(source + " -> "+ remote_PATH, 'white',  'on_blue'))
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


			_self.po.send_message("upload REPORT done: " + dest, title="Upload done:"+dest,sound="bike")
			
		except:
			e = sys.exc_info()
			_self.po.send_message(e, title="unable to upload :	"+source,sound="bike")
			print("unable to backup :	" + colored(source, 'white',  'on_red'))
			print(colored(e, 'white',  'on_red'))
			print("waiting:	" + colored(str(_self.failetimeout)+" seconds\n", 'magenta'))
			_self.pushLog("FAIL Uploading REPORT "+filename, str(e) ,"siren")
			time.sleep(_self.failetimeout)




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
					clipbegin = t-cduration-gap
					if(clipbegin < 0): clipbegin = 2

					if(len(sequences)>0) : # Avoiding overlap 
						pre_end_time = (sequences[len(sequences)-1][1])
						begin_time = datetime.timedelta(seconds=clipbegin)
						if(begin_time < pre_end_time):
							clipbegin = pre_end_time # TODO : Add gap  
					clipend = t-(gap*2)

					begin_time = datetime.timedelta(seconds=clipbegin)
					end_time = datetime.timedelta(seconds=clipend)
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
		
		# os.remove(videofile)



os.system('cls' if os.name == 'nt' else 'clear')




try:
	dash = PiPyDASH()
except KeyboardInterrupt:
	self.pushLog("DASH AGENT FAIL", ":-(","siren")



