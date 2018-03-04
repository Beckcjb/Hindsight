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

class Config():

	def __init__(self, runList, basepath, files, rockType):
		self.runList = runList
		self.basepath = basepath
		self.files = files
		self.rockType = rockType

	def get_basepath(self):
		return self.basepath

	def get_run_list(self):
		return self.runList

	def get_file_paths(self, index):
		return self.files[index]

	def return_rock_type(self):
		if self.rockType == "Rock-A":
			self.rockType = "RockA"
			return self.rockType
		elif self.rockType == "Rock-B":
			self.rockType = "RockB"
			return self.rockType
		elif self.rockType == "Rock-C":
			self.rockType = "RockC"
			return self.rockType
		elif self.rockType == "Rock-D":
			self.rockType = "RockD"
			return self.rockType
		elif self.rockType == "Rock-E":
			self.rockType = "RockE"
			return self.rockType
		else:
			self.rockType = "RockE"
			return self.rockType
