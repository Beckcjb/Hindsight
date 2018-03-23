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

	def get_basepath(self):
		return self.basepath

	def get_run_list(self):
		return self.run_list

	def get_file_paths(self):
		return self.files

	def get_rock_type(self):
		rock_type_dict = {"Rock-A": "RockA",
						  "Rock-B": "RockB",
						  "Rock-C": "RockC",
						  "Rock-D": "RockD",
						  "Rock-E": "RockE"}

		return rock_type_dict[self.rock_type]
