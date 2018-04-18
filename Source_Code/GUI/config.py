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

	def __init__(self,run_list, basepath, files, rock_type, abrasion_radius, 
				abrasionX, abrasionY, band_size, buffer, analysis_option):
		self.run_list = run_list
		self.basepath = basepath
		self.files = files
		self.rock_type = rock_type
		self.analysis_option = analysis_option
		self.abrasionX = abrasionX
		self.abrasionY = abrasionY
		self.abrasion_radius = abrasion_radius
		self.band_size = band_size
		self.buffer = buffer

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
		
	def get_analysis_option(self):
		return self.analysis_option
		
	def get_abrasionX(self):
		return self.abrasionX
		
	def get_abrasionY(self):
		return self.abrasionY
		
	def get_abrasion_radius(self):
		return self.abrasion_radius
	
	def get_band_size(self):
		return self.band_size
		
	def get_buffer(self):
		return self.buffer
		
