# class to determine the ordering of specific damage within a MX structure
# using multiple difference maps collected over increasing doses from the 
# same crystal

import numpy as np
from scipy import stats

class specificDamageRank(object):
	def __init__(self, residueName = "", atomType = "",densMetric = "",
				 damageRank = 0 ,densSlope = 0, slopeError = 0):

		self.residueName 		= residueName
		self.atomType			= atomType
		self.damageRank 		= damageRank
		self.densSlope 			= densSlope
		self.slopeError			= slopeError
		self.densMetric			= densMetric

class specificDamageRanking(object):
	def __init__(self,atomList = [],densMetric = "Loss",numLines = 0,normalised = False):
		self.atomList 	= atomList
		self.densMetric = densMetric # the density metric for which the ranking will be based
		self.numLines 	= numLines # specify the number of lines of output to display to command line
		self.normalised = normalised # (Boolian) specifies whether the 'Standard' or 'Calpha normalised' metric values are used
	
	def normaliseType(self):
		# determine the normalisation type 
		if self.normalised == False:
			# no normalisation (default)
			return 'Standard'
		else:
			return 'Calpha normalised'

	def calculateRanks(self):
		# for each atom within the atomList list of atom objects, group into 
		# residue/nucleotide types and determine the average slope for straight
		# lines of best fit for each residue/nucleotide type (for plots of 
		# dataset number vs max density loss)

		# don't run if density metric not specified
		if self.densMetric == "":
			print 'Need to specify density metric before this function can be run'
			return
		
		# determine the normalisation type for density metrics
		type = self.normaliseType()

		residueDict = {}
		for atom in self.atomList:
			identifier = "{} {}".format(atom.basetype,atom.atomtype)
			if identifier not in residueDict.keys():
				residueDict[identifier] = {}
				residueDict[identifier]['slope'] = []
				residueDict[identifier]['std_err'] = []

			if str(self.densMetric).lower() == 'loss':
				residueDict[identifier]['slope'].append(atom.maxDensLoss[type]['lin reg']['slope'])
				residueDict[identifier]['std_err'].append(atom.maxDensLoss[type]['lin reg']['std_err'])
			elif str(self.densMetric).lower() == 'mean':
				residueDict[identifier]['slope'].append(atom.meanDensChange[type]['lin reg']['slope'])
				residueDict[identifier]['std_err'].append(atom.meanDensChange[type]['lin reg']['std_err'])
			elif str(self.densMetric).lower() == 'gain':
				residueDict[identifier]['slope'].append(atom.maxDensGain[type]['lin reg']['slope'])
				residueDict[identifier]['std_err'].append(atom.maxDensGain[type]['lin reg']['std_err'])

		# calculate the average straight line slope for each residue/nucleotide type
		specificDamageRanks = []
		for key in residueDict.keys():
			damageStats = specificDamageRank(key.split()[0],key.split()[1],self.densMetric)
			damageStats.densSlope = np.mean(residueDict[key]['slope'])
			damageStats.slopeError = np.std(residueDict[key]['slope'])
			specificDamageRanks.append(damageStats)

		# rank residues/nucleotides by slope value
		specificDamageRanks.sort(key = lambda x: x.densSlope)
		counter = 0
		for residue in specificDamageRanks:
			residue.damageRank = counter
			counter += 1

		self.specificDamageRanks = specificDamageRanks

	def getDamageRanks(self):
		# following on from the above function, output the calculated ordering of
		# damage within the current structure

		# don't run if damage ranks not yet determined above
		try:
			self.specificDamageRanks
		except AttributeError:
			print 'Need to calculate damage rankings before this function can be run'
			return

		print '--------------------------------------------------------------------'
		print 'Ordering of damage with {} D{} metric as follows:'.format(type,str(self.densMetric).lower())
		
		# if the number of output lines is specified, use this value, otherwise print all lines
		if self.numLines != 0:
			numLines = self.numLines
		else:
			numLines = len(self.specificDamageRanks)
		for res in self.specificDamageRanks[0:numLines+1]:
			print '{}\t{} {}\tSlope: {}\tStd Dev: {}'.format(str(res.damageRank),res.residueName, res.atomType,
															 str(res.densSlope)[:6], str(res.slopeError)[:6])