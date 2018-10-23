# Theme by QuantumCD - ported to Python by lschmierer
# Lightly modified by DarylPinto
#
# https://gist.github.com/QuantumCD/6245215
# https://gist.github.com/lschmierer/443b8e21ad93e2a2d7eb

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

def style(qApp):
	qApp.setStyle("Fusion")

	dark_palette = QPalette()

	dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.WindowText, Qt.white)
	dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
	dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
	dark_palette.setColor(QPalette.ToolTipText, Qt.white)
	dark_palette.setColor(QPalette.Text, Qt.white)
	dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.ButtonText, Qt.white)
	dark_palette.setColor(QPalette.BrightText, Qt.red)
	dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.HighlightedText, Qt.black)

	qApp.setPalette(dark_palette)

	qApp.setStyleSheet('''

		*:disabled {
			color: gray;
		}

		QToolTip {
			color: #ffffff;
			background-color: #2a82da;
			border: 1px solid white;
		}

		QPushButton#start_btn, QPushButton#save_login_btn {
			background-color: #2365a7;
			padding: 8px 16px;
		}

		QPushButton#start_btn:disabled {
			background-color: gray;
			color: lightgray;
		}

		QLineEdit, QComboBox {
			background-color: #2a2a2a;
			padding: 3px;
		}
		
		QComboBox::item:selected{
			color: white;
		}
	
	''')
