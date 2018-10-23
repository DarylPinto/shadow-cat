import sys
import os
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
import methods
from dark_fusion import style

class Window(QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		loadUi('box/layout.ui', self)
		self.background_thread = None
		self.output_url = ""
		self.error_msg = None
		self.connect_ui_items()
		methods.load_creds(self)

	def connect_ui_items(self):

		# Add input validation for time inputs
		for time_input in [self.start_time_input, self.end_time_input]:
			regex = QtCore.QRegExp("[0-9]?[0-9]:[0-5][0-9]")
			validator = QtGui.QRegExpValidator(regex)
			time_input.setValidator(validator)

		# Connect buttons to methods
		self.open_video_btn.clicked.connect(lambda: methods.choose_video(self))
		self.start_btn.clicked.connect(lambda: methods.handle_start_click(self))
		self.save_login_btn.clicked.connect(lambda: methods.save_creds(self))


app = QApplication(sys.argv)
style(app)
gui = Window()
gui.show()
sys.exit(app.exec_())
