# Team Hindsight: Class for Configuration with back-end 
# Date: February 2017
# Team Members: Beck, Charels
#		Nelson, Alexanderia
#		Pacquett, Adam 
#		Rainen, Hunter 
#
# Client:		Iona Brockie 
#				NASA/JPL-Caltech
#==========================================================================================================
# Overview: This python file contains the class that the GUI will use to communicate to the back-end. It
#			will allow the pandas dataframe to gather the necessary data and for the other methods to pull
#			information from the class as well. 
#==========================================================================================================
# Includes
#include "stdafx.h"
#include <iostream>
#include <math.h>

import sys									# System Variables



class Config():
	
	def __init__(self, runType, files, rockType, parameter_1, parameter_2, parameter_3):
		self.runType = runType
		self.files = files
		self.rockType = rockType
		self.parameter_1 = parameter_1
		self.parameter_2 = parameter_2
		self.parameter_3 = parameter_3
	
	def returnRunType(self):
		return self.runType
	
	def returnFilePaths(self, index):
		return self.files[index]
		
	def returnRockType(self):
		return self.rockType.get()
		
	def returnParams(self, parameterNumber):
		if parameterNumber == 1:
			return str(self.parameter_1.get())
			
		elif parameterNumber == 2 :
			return str(self.parameter_2.get())
		
		elif parameterNumber == 3 :
			return str(self.parameter_3.get())
