import os

class ccp4Job():

	def __init__(self,jobName,commandInput1,commandInput2,outputDir,outputLogfile,outputFile):

		self.jobName 		= jobName
		self.commandInput1 	= commandInput1
		self.commandInput2 	= commandInput2
		self.outputDir 		= outputDir
		self.outputLogfile 	= outputLogfile
		self.outputFile 	= outputFile # used to check success of job

		# automatically run ccp4 program
		self.runCCP4program()

	def runCCP4program(self):
		# generic method to run a ccp4 program on command line

		# write commandInput2 to txt file
		textinput = open('{}inputfile.txt'.format(self.jobName),'w')
		textinput.write(self.commandInput2)
		textinput.close()

		# run ccp4 program job
		os.system('{} < {}inputfile.txt > {}'.format(self.commandInput1,
												   self.jobName,
												   self.outputLogfile))
		# os.system('{} < {}inputfile.txt'.format(self.commandInput1,
		# 										   self.jobName))
		# move ccp4 job input and log files to working sub directory
		os.system('mv {}inputfile.txt {}/{}inputfile.txt'.format(self.jobName,self.outputDir,self.jobName))
		os.system('mv {} {}/{}'.format(self.outputLogfile,self.outputDir,self.outputLogfile))

	def checkJobSuccess(self):
		# job success checked, based on whether output files exist
		if os.path.isfile(self.outputFile) is False:
			ErrorString = '{} did not proceed to completion'.format(self.jobName)
			print ErrorString
			return False
		else:
			return True