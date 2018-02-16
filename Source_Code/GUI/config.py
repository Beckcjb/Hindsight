# Team Hindsight: Class for Configuration with back-end 
# Date: February 2017
# Team Members: Beck, Charels
#				Nelson, Alexanderia
#				Pacquett, Adam 
#				Rainen, Hunter 
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
import numpy as np							# Numbered python array
import cv2									# openCV library


class Config():

	def __init__(self,runType, files, rockType, parameter_1, parameter_2, parameter_3):
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
			return self.parameter_1
			
		elif parameterNumber == 2 :
			return self.parameter_2
		
		elif parameterNumber == 3 :
			return self.parameter_3