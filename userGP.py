#!/usr/bin/env python

from PyQt5 import QtCore, QtGui, uic
print('Successful import of uic') #often reinstallation of PyQt5 is required

from PyQt5.QtCore import (QCoreApplication, QThread, QThreadPool, pyqtSignal, pyqtSlot, Qt, QTimer, QDateTime)
from PyQt5.QtGui import (QImage, QPixmap, QTextCursor, QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QLabel, QPushButton, \
QTableWidget, QTableWidgetItem, QVBoxLayout, QGridLayout, QSizePolicy, QMessageBox, \
QFileDialog, QSlider, QComboBox, QProgressDialog, QListWidget, QAbstractItemView, QListView)

import sys
print('Loaded Packages and Starting IR Data...')

qtCreatorFile = "gp.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Window(QMainWindow, Ui_MainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.initUI()

	def initUI(self):
		print('Starting user interface...')
		self.camerasSelected = {} #dictionary to save all cameras and associated rows in tableWidget
		
		#setting up list and table
		self.model = QStandardItemModel()
		self.listView.setModel(self.model)
		self.model.itemChanged.connect(self.change) #if item is checked, update table
		self.vertLabels = []
		
		stringlist = ["SP7", "SmashCam01", "blastcam", "Parabilis"] #this is the string we will update of all networks available
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
			#print('Item changed: ' + item.text())
			insertRowNum = len(self.camerasSelected) #grabs from length of dictionary
			self.tableWidget.insertRow(insertRowNum) #inserts row at dictionary length
			
			#renumbers selected cameras
			self.vertLabels.append('GoPro ' + str(insertRowNum + 1))
			self.tableWidget.setVerticalHeaderLabels(self.vertLabels)
			
			#print('Inserted row at: ' + str(insertRowNum))
			self.tableWidget.setItem(insertRowNum, 1, QTableWidgetItem(item.text())) #displays element
			self.camerasSelected[item.text()] = insertRowNum #adds item to dictionary with row number
			
			self.history.insertPlainText(item.text() + ' selected\n')
			self.history.moveCursor(QTextCursor.End)
			
		if item.checkState() == Qt.Unchecked:
			print('Item changed: ' + item.text())
			removeRowNum = self.camerasSelected[item.text()] #looks up row number
			self.tableWidget.removeRow(removeRowNum) #deletes that row number
			print('Deleted row at: ' + str(removeRowNum))
			del self.camerasSelected[item.text()] #deletes that element from dictionary
			print('Updates row numbers: ')
			for k, v in self.camerasSelected.items():
				if removeRowNum < v:
					self.camerasSelected[k] = v - 1
					print(k + ': ' + str(v - 1))
			
			for k, v in self.camerasSelected.items():
				print(k + ': ' + str(v))
			#renumbers selected cameras
			self.vertLabels.append('GoPro ' + str(removeRowNum + 1))
			self.tableWidget.setVerticalHeaderLabels(self.vertLabels)
			
			self.history.insertPlainText(item.text() + ' removed\n')
			self.history.moveCursor(QTextCursor.End)
		
def main():
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()