import numpy as np
import sys

class NaiveBayes:

	def __init__(self, trainDataFileName, testDataFileName):
	# initialize necessary class variables
		self.traindata = []
		self.testdata = []
		# output set up
		self.outputtitle=['True Positive', 'False Negative', 'False Positive', 'True Negative']
		self.trainoutput= [0, 0, 0, 0]
		self.testoutput= [0, 0, 0, 0]

		# two classes 1(yes) and -1(no)
		self.yes= {} # mapping class = 1 attributes to frequency
		self.no = {} # mapping class = -1 attributes to frequency
		self.numberOfYes = 0
		self.numberOfNo = 0
		self.totalTrainset = 0

		# read test file
		with open(testDataFileName) as test:
			lines =test.readlines()
			for line in lines:
				splited = line.split()
				self.testdata.append(splited)

		# read train file
		with open(trainDataFileName) as train:
			lines = train.readlines()
			for line in lines:
				self.totalTrainset+=1
				splited = line.split()
				if len(splited) > 0:
					# store data as a array of list
					self.traindata.append(splited)
					
					# counting frequency of each attribute and store in Dictionary
					if splited[0] == '+1':
						self.numberOfYes += 1
						for i in range(1, len(splited)):
							keyval = splited[i].split(':')
							key = int(keyval[0])
							value = keyval[1]
							if key not in self.yes:
								self.yes[key] = 1
							else:
								self.yes[key] = self.yes[key]+1
					else:
						self.numberOfNo += 1
						for i in range(1, len(splited)):
							keyval = splited[i].split(':')
							key = int(keyval[0])
							value = keyval[1]
							if key not in self.no:
								self.no[key] = 1
							else:
								self.no[key] = self.no[key]+1
			# Handling unseen attributes in train dataset
				# add one to all the frequency
				# if unseem attributes appear, map to frquency = 1
			for key in self.yes:
				self.yes[key] += 1
			for key in self.no:
				self.no[key] += 1

	# helpper function: get all the attributes identity only
	def getAttrs(self,attrset):
		output = []
		for item in attrset:
			keyval = item.split(':');
			key = int(keyval[0])
			output.append(key)
		return output



	def classfier(self):
		trainAccuracy = 0
		testAccuracy = 0
		trainLine = 0
		testLine = 0
		#classifer train set
		for row in self.traindata:
			trainLine +=1
			target = row[0]
			attrs = self.getAttrs(row[1:])
			ppyes = float(self.numberOfYes)/self.totalTrainset
			ppno = float(self.numberOfNo)/self.totalTrainset
			for attrKey in attrs:
				# handle unseen atttributes by mapping with frequency = 1
				if attrKey not in self.yes:
					self.yes[attrKey] = 1
				if attrKey not in self.no:
					self.no[attrKey] = 1
				ppyes *= self.yes[attrKey]/float(self.numberOfYes)
			 	ppno *= self.no[attrKey]/float(self.numberOfNo)
			px = ppyes+ppno
			ppyes = ppyes/px
			ppno = ppno/px

			# confusion matrix
			if target =='+1':		
				if ppyes > ppno: 	# True positive
					self.trainoutput[0] += 1
					trainAccuracy += 1
				else:				# False Negative
					self.trainoutput[1] += 1
			elif target == '-1':	
				if ppyes > ppno:	# False Positive
					self.trainoutput[2] += 1
				else:				# True Negative 
					self.trainoutput[3] += 1
					trainAccuracy += 1


		# clissfier test dataset
		for row in self.testdata:
			testLine += 1
			target = row[0]
			attrs = self.getAttrs(row[1:])
			ppyes = float(self.numberOfYes)/self.totalTrainset
			ppno = float(self.numberOfNo)/self.totalTrainset
			for attrKey in attrs:
				if attrKey not in self.yes:
					self.yes[attrKey] = 1
				if attrKey not in self.no:
					self.no[attrKey] = 1
				ppyes *= self.yes[attrKey]/float(self.numberOfYes)
			 	ppno *= self.no[attrKey]/float(self.numberOfNo)
			px = ppyes+ppno
			ppyes = ppyes/px
			ppno = ppno/px

			# confusion matrix
			if target =='+1':
				if ppyes > ppno: 	# True positive
					self.testoutput[0] += 1
					testAccuracy += 1
				else:				# False Negative 
					self.testoutput[1] += 1
			elif target == '-1':	
				if ppyes > ppno:	# False Positive
					self.testoutput[2] += 1
				else:				# True Negative
					self.testoutput[3] += 1
					testAccuracy += 1

		print(self.outputtitle)
		print(self.trainoutput)
		print(self.testoutput)
		print('test Accuracy: ' + str(testAccuracy/float(testLine)))
		print('trainAccuracy: ' + str(trainAccuracy/float(trainLine)))
		print('train data stat')
		self.getStat(self.trainoutput)
		print('test data stat')
		self.getStat(self.testoutput)
		

# helper function: Evaluation!
	def getStat(self, array):
		if len(array) != 4:
			print('array size is not correct')
		TP = float(array[0])
		FN = float(array[1])
		FP = float(array[2])
		TN = float(array[3])
		accuracy = (TP+TN)/(TP+FN+FP+TN)
		if TP+FP == 0:
			precision = 0
		else: precision = TP/(TP+FP)
		sencitivityOrRecall = TP/(TP+FN)
		specificity = TN/(TN+FP)
		if precision==0 and sencitivityOrRecall ==0:
			f1 = 0
			F_half = 0
			F_two = 0
		else: 
			f1 = 2*(precision*sencitivityOrRecall)/(precision+sencitivityOrRecall)
			F_half = (1+0.25)*(precision*sencitivityOrRecall)/(0.25*precision+sencitivityOrRecall)
			F_two = 5*(precision*sencitivityOrRecall)/(4*precision+sencitivityOrRecall)
		print('Accuracy', 'Error', 'SencitivityOrRecall', 'Specificity', 'Precision', 'F1', 'F_half', 'F_two')
		print(round(accuracy,3), round(1-accuracy,3), round(sencitivityOrRecall, 3), round(specificity,3), round(precision,3), round(f1,3), round(F_half,3), round(F_two,3))




def run():
	# read arguments from command line
	files = sys.argv
	if(len(files) < 2 ):
		print('No train and test data files specified!')
	trainDataFileName = files[1]
	testDataFileName = files[2]
	naivebayes = NaiveBayes(trainDataFileName, testDataFileName)
	naivebayes.classfier()


if __name__ == '__main__':
    run()







