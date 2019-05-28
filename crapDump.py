class Camera():
	def __init__(self):
		self.title = ''
		self.row = -1
		
	def setValues(self, row, networkID, title):
		self.row = row
		self.networkID = networkID
		self.title = title
		self.connected = 'No'
		self.isRecording = 'No'