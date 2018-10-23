import os
import subprocess
import requests
import gfy
from obfuscate import sys_encode, sys_decode, decode
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import time

# Run background processes on a different thread
class ExecuteThread(QtCore.QThread):

	def __init__(self, gui, func, arguments):
		super(ExecuteThread, self).__init__()
		self.func = func
		self.arguments = arguments
		self.gui = gui
		self.gui.error_msg = None

	def run(self):
		try:
			self.func(*self.arguments)
		except:	
			self.gui.error_msg = "An unexpected error occurred."

###########
# METHODS #
###########
def timestamp_to_secs(timestamp):
	try:	
		t = timestamp.split(":")
		return int(t[0]) * 60 + int(t[1])
	except:
		return 0

# Open info window
def info_window(title, text):
	msg = QMessageBox()
	msg.setWindowTitle(title)
	msg.setText(text)
	msg.setIcon(1)
	msg.exec()

# Open error window
def error_window(text):
	msg = QMessageBox()
	msg.setWindowTitle("Error")
	msg.setText(text)
	msg.setIcon(3)
	msg.exec()

# Open file selection dialog to select video
def choose_video(gui):
	dialog = QFileDialog()
	file_filter = "Video Files (*.mp4);;All Files (*)"
	video, _filter = dialog.getOpenFileName(dialog, "", "", file_filter)
	if(video):
		gui.video_path.setText(video)
		gui.start_btn.setEnabled(True)

# Process video with  ffmpeg
def process_video(video, start, end, crop, merge_audio, destination):
	output_path = "video.mp4"
	if destination not in ["Gfycat", "Streamable"]:
		cur_time = str(time.time())
		output_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\video-'+cur_time+'.mp4')
	os.chdir("box")
	subprocess.call(
		'ffmpeg -y -i "%s" -ss %s -to %s %s %s -c:v libx264 -crf 20 %s' % (video, start, end, crop, merge_audio, output_path),
		shell=True
	)
	os.chdir("..")

# Upload to Gfycat
def upload_to_gfycat(gui, username=None, password=None):

	f = open("./box/cat", "r").read()
	cat = decode(f)

	# Upload anonymously if username or password not present
	anonymous = not (username or password)

	Gfycat = gfy.Client(cat["cid"], cat["csec"], username, password)
	gui.output_url = Gfycat.upload("./box/video.mp4", anonymous=anonymous)	
	os.remove("./box/video.mp4")

# Upload to Streamable
def upload_to_streamable(gui, username, password):
	r = requests.post("https://api.streamable.com/upload",
		auth=(username, password),
		files={"file": open("./box/video.mp4", "rb")}
	)

	shortcode = r.json()["shortcode"]
	gui.output_url = "https://streamable.com/" + shortcode
	os.remove("./box/video.mp4")

def load_creds(gui):
	try:
		f = open("./box/creds", "r").read()
		creds = sys_decode(f)
		gui.gfycat_username.setText(creds["gu"])	
		gui.gfycat_password.setText(creds["gp"])	
		gui.streamable_username.setText(creds["su"])	
		gui.streamable_password.setText(creds["sp"])	
	except:
		pass

def save_creds(gui):
	creds = sys_encode({
		"gu": gui.gfycat_username.text(),
		"gp": gui.gfycat_password.text(),
		"su": gui.streamable_username.text(),
		"sp": gui.streamable_password.text()
	})

	f = open("./box/creds", "w")
	f.write(creds)
	f.close()
	gui.statusbar.showMessage("Saved", 1000)

# Handle start button click
def handle_start_click(gui):
		# Collect info from UI 
		video = gui.video_path.text()
		start = gui.start_time_input.text()
		end = gui.end_time_input.text()
		destination = gui.destination_dropdown.currentText()
		crop = "-filter:v crop=ih/60*73:ih" if gui.crop_checkbox.isChecked() else ""
		audio_track_count = os.popen('ffmpeg -i %s 2>&1' % (video)).read().count(": Audio:") # Extremely hacky way to count audio tracks without ffprobe
		merge_audio = "-filter_complex amix=inputs=%s" % (audio_track_count) if gui.merge_audio_checkbox.isChecked() and audio_track_count > 0 else ""

		gfycat_user = gui.gfycat_username.text()
		gfycat_pass = gui.gfycat_password.text()
		streamable_user = gui.streamable_username.text()
		streamable_pass = gui.streamable_password.text()
	
		# Ensure trimmed video length is at least 1 second	
		if(timestamp_to_secs(end) + 1 - timestamp_to_secs(start) <= 1):
			return info_window(
				"Video too short",
				"Ensure video is at least 1 second long."
			)

		# Ensure Streamable account info is entered before uploading to streamable
		if destination == "Streamable" and (not streamable_user or not streamable_pass):
			return info_window(
				"Streamable Account Required",
				"Login under the \"Accounts\" tab before uploading to Streamable."
			)

		# Indcate to user that processing has begun
		gui.centralwidget.setEnabled(False)
		gui.statusbar.showMessage("Processing Video...")

		# Process Video
		gui.background_thread = ExecuteThread(gui, process_video, [video, start, end, crop, merge_audio, destination])	
		gui.background_thread.start()

		# After processing
		def next():

			# Upload to Gfycat/Streamable
			if destination == "Gfycat" or destination == "Streamable":
				gui.statusbar.showMessage("Uploading...")
				gui.background_thread = None
				if destination == "Streamable":
					gui.background_thread = ExecuteThread(gui, upload_to_streamable, [gui, streamable_user, streamable_pass])
				else:
					gui.background_thread = ExecuteThread(gui, upload_to_gfycat, [gui, gfycat_user, gfycat_pass])
				gui.background_thread.start()

				def done():
					gui.centralwidget.setEnabled(True)
					if(not gui.error_msg):
						QApplication.clipboard().setText(gui.output_url)
						gui.statusbar.showMessage("Done")
						info_window("Complete", "Link copied to clipboard (%s)" % (gui.output_url))
						gui.statusbar.showMessage("Done", 1000)
					else:
						error_window(gui.error_msg)
						gui.statusbar.clearMessage()

				gui.background_thread.finished.connect(done)

			# Do nothing else with the output video
			else:
				gui.centralwidget.setEnabled(True)
				if(not gui.error_msg):
					gui.statusbar.showMessage("Done")
					info_window("Complete", "Video successfully output to the Desktop")
					gui.statusbar.showMessage("Done", 1000)
				else:
					error_window(gui.error_msg)
					gui.statusbar.clearMessage()

		gui.background_thread.finished.connect(next)
			