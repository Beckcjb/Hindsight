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


import sys									# System Variables



class Config():
	
	def __init__(self, run_list, basepath, files, rock_type):
		self.run_list = run_list
		self.basepath = basepath
		self.files = files
		self.rock_type = rock_type
		self.imageDict = {}
		
	def get_basepath(self):
		return self.basepath
	
	def get_run_list(self):
		return self.run_list
	
	def get_filepaths(self):
		return self.files
		
	def get_rock_type(self):
		if self.rock_type == "Rock-A":
			self.rock_type = "RockA"
			return self.rock_type
		elif self.rock_type == "Rock-B":
			self.rock_type = "RockB"
			return self.rock_type
		elif self.rock_type == "Rock-C":
			self.rock_type = "RockC"
			return self.rock_type
		elif self.rock_type == "Rock-D":
			self.rock_type = "RockD"
			return self.rock_type
		elif self.rock_type == "Rock-E":
			self.rock_type = "RockE"
			return self.rock_type
		else:
			self.rock_type = "RockE"
			return self.rock_type



					
			

