#!/usr/bin/env python

from PyQt5 import QtCore, QtGui, uic
print('Successful import of uic') #often reinstallation of PyQt5 is required

from PyQt5.QtCore import (QCoreApplication, QThread, QThreadPool, pyqtSignal, pyqtSlot, Qt, QTimer, QDateTime)
from PyQt5.QtGui import (QImage, QPixmap, QTextCursor, QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QLabel, QPushButton, \
QTableWidget, QTableWidgetItem, QVBoxLayout, QGridLayout, QSizePolicy, QMessageBox, \
QFileDialog, QSlider, QComboBox, QProgressDialog, QListWidget, QAbstractItemView, QListView)

import sys
import numpy as np
print('Loaded Packages and Starting IR Data...')

qtCreatorFile = "gp.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Window(QMainWindow, Ui_MainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.showMaximized()
		self.initUI()

	def initUI(self):
		print('Starting user interface...')
		self.camerasSelected = {} #dictionary to save all cameras and associated rows in tableWidget

		#setting up list and table
		self.model = QStandardItemModel()
		self.listView.setModel(self.model)
		self.model.itemChanged.connect(self.change) #if item is checked, update table
		self.vertLabels = []

		stringlist = ["RandomWiFi", "SmashCam01", "blastcam", "Parabilis"] #this is the string we will update of all networks available
		if stringlist is not None:
			for i in range(len(stringlist)):
				item = QStandardItem(stringlist[i])
				item.setEditable(False)
				item.setCheckable(True)
				item.setCheckState(Qt.Unchecked)
				self.model.appendRow(item)

		#record buttons
		self.startRecBut.clicked.connect(self.startRecFunc)
		self.stopRecBut.clicked.connect(self.stopRecFunc)

	def startRecFunc(self):
		self.history.insertPlainText('Starting Recording\n')
		self.listView.setEnabled(False)
		self.history.moveCursor(QTextCursor.End)

	def stopRecFunc(self):
		self.history.insertPlainText('Stopped Recording\n')
		self.listView.setEnabled(True)
		self.history.moveCursor(QTextCursor.End)

	def change(self, item):
		if item.checkState() == Qt.Checked:
			self.history.moveCursor(QTextCursor.End)
			self.history.insertPlainText('Attempting to connect to ' + item.text() + '...\n')
			self.history.moveCursor(QTextCursor.End)
			
			#print('Item changed: ' + item.text())
			insertRowNum = len(self.camerasSelected) #grabs from length of dictionary
			self.tableWidget.insertRow(insertRowNum) #inserts row at dictionary length

			#renumbers selected cameras
			self.vertLabels.append('GoPro ' + str(insertRowNum + 1))
			self.tableWidget.setVerticalHeaderLabels(self.vertLabels)

			#print('Inserted row at: ' + str(insertRowNum))
			networkID = -1 #networkID currently unknown
			connectionStatus = 'No'
			recordingStatus = 'No'
			connectedRecently = 'Yes'
			self.camerasSelected[item.text()] = [insertRowNum, networkID, connectionStatus, recordingStatus, connectedRecently] #adds item to dictionary with row number
			self.tableWidget.setItem(insertRowNum, 0, QTableWidgetItem(str(networkID))) #displays element
			self.tableWidget.setItem(insertRowNum, 1, QTableWidgetItem(item.text())) #displays element
			self.tableWidget.setItem(insertRowNum, 2, QTableWidgetItem(connectionStatus)) #displays element
			self.tableWidget.setItem(insertRowNum, 3, QTableWidgetItem(recordingStatus)) #displays element
			self.tableWidget.setItem(insertRowNum, 4, QTableWidgetItem(connectedRecently)) #displays element


			self.history.moveCursor(QTextCursor.End)
			self.history.insertPlainText('  ' + item.text() + ' -> Can Connect Verified\n')
			self.history.moveCursor(QTextCursor.End)

		if item.checkState() == Qt.Unchecked:
			#print('Item changed: ' + item.text())
			removeRowNum = self.camerasSelected[item.text()][0] #looks up row number
			self.tableWidget.removeRow(removeRowNum) #deletes that row number
			#print('Deleted row at: ' + str(removeRowNum))
			del self.camerasSelected[item.text()] #deletes that element from dictionary
			#print('Updates row numbers: ')
			for k, v in self.camerasSelected.items():
				if removeRowNum < v[0]:
					self.camerasSelected[k][0] = v[0] - 1
					#print(k + ': ' + str(v[0] - 1))
			#for k, v in self.camerasSelected.items():
			#	print(k + ': ' + str(v[0]))
				
			#renumbers selected cameras
			self.vertLabels.append('GoPro ' + str(removeRowNum + 1))
			self.tableWidget.setVerticalHeaderLabels(self.vertLabels)

			self.history.insertPlainText('ATTENTION: ' + item.text() + ' Disconnected\n')
			self.history.moveCursor(QTextCursor.End)

def main():
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
