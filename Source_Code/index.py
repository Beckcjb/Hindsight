# Team Hindsight: Image Analysis Tool Graphical User Interface
# Date: February 2017
# Team Members: Beck, Charels
#				Nelson, Alexanderia
#				Pacquett, Adam 
#				Rainen, Hunter 
#
# Client:		Iona Brockie 
#				NASA/JPL-Caltech
#==========================================================================================================
# Overview: The purpose of this program is to read in a batch of images
#			,process them and return the image(s) showing which areas are 
#			dust free. The program will show these areas in correlation
#			with colors Red(complete dust coverage), Yellow(some dust coverage),
#			Green(little to no dust coverage). The program will then store the 
#			results in a corresponding folder.
#					
#			The graphical user interface begins with a window that allows the user
# 			to select a folder that will be analyzed. After the user selects the folder
#			they will then be directed to another window that is the main portion of the 
#			program. Here the user can run the images through the analyzer and the program
#			will display the images in order of 'Before'->'After'->'Analyzed'. 
#==========================================================================================================
# Includes
#include "stdafx.h"
#include <iostream>
#include <math.h>

# Imports 
import config								# configuration for image analysis settings
from config import Config					

import sys									# System Variables
import numpy as np							# Numbered python array
import cv2									# openCV library

# tkinter file tools 
import tkinter
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from PIL import ImageTk, Image
#==============================================

''' Window: This window is the first thing the user will see. It allows the user to
			search through the files on the system. Then the user will select the file
			and this will open up a new window that is the main section of the program.'''
class Window():
	def __init__(self, home):
	# Setup window
		self.home = home
		home.title("Hindisight")
		home.wm_iconbitmap("logo.ico")
		
	# Place buttons/labels/entry boxes
		entered = StringVar() # file handle
		self.entered = entered
		hLabel = Label (home, text="Hindsight: Image Analysis Tool")
		hLabel.grid(row=0, column=1)
		
		browseButton = Button(home,text="Browse...",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.browseFolder)
							
		selectButton = Button(home,text="Select",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.create_window)
		self.entry = Entry(home, width=50, textvariable=self.entered)
		self.entry.grid(row=1, column=1)
		browseButton.grid(row=1, column=2)
		selectButton.grid(row=1, column=3)
	#==========================================
	
	# File Browser
	def browseFolder(self):
		file_names = [20]
		self.files = askopenfilenames(title="Select files")
		self.file_names = self.files
		return self.entered.set(self.files)
	#==========================================
	
	# Create new window upon press of "Select" button
	def create_window(self):
		self.fh = self.file_names
		analysis = tkinter.Toplevel(root)
		new = AnalysisWindow(analysis, self.fh)# pass file handle to new window
		self.home.withdraw()
		
	#==========================================
		
#==============================================================================================		
''' AnalysisWindow: This window is where the main section of the program is carrried out. Here we will us the
					path of the previously selected folder and apply our analysis on each image in the folder
					that is an after image of dust removal.'''
class AnalysisWindow():
	def __init__(self, analysis, files):
	# Set up analysis window
		self.analysis = analysis
		analysis.title("Hindsight: Analysis")
		analysis.geometry("800x300")
		analysis.wm_iconbitmap("logo.ico")
		
		# Set up Labels and Buttons
		self.runType = 0
		self.file_names = [20]
		self.file_names = files
		nl = '\n'
		text = f"Files in use {nl}{nl.join(self.file_names)}"
		fLabel = Label(analysis, text=text) # display what folder is in use
		changeFileButton = Button(analysis,width=20, text="Change File",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.browseFolder) # change folder
							
		runButton   	 = Button(analysis,width=20,text="Complete Run",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.runFullAnalysis) # run image analysis
							
		colorSegButton   = Button(analysis,width=20,text="Color Segmenation",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.runColorSeg) # run image analysis
							
		heatMapButton    = Button(analysis,width=20,text="Heat Map",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.runHeatMap) # run image analysis
							
		imageSubButton   = Button(analysis,width=20,text="Image Subtraction",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.runImageSub) # run image analysis
							
		saveButton  	 = Button(analysis,width=20,text="Save Result",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.saveImage)# save results
							
		alterButton 	 = Button(analysis,width=20,text="Alter Parameters",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.create_window)# change parameters
							
		fLabel.grid(row=0, column=1, padx=5, pady=5)
		changeFileButton.grid(row=0, column=0, padx=5, pady=5)
		runButton.grid(row=3, column=0, padx=5, pady=5)
		saveButton.grid(row=3, column=1,padx=5,pady=5)
		colorSegButton.grid(row=4, column=0,padx=5,pady=5)
		heatMapButton.grid(row=5, column=0,padx=5,pady=5)
		imageSubButton.grid(row=6, column=0,padx=5,pady=5)
		alterButton.grid(row=3, column=2,padx=5,pady=5)
			
		self.rockType = StringVar(analysis)
		
		self.rockType.set("Rock-E") # default value

		
		saveButton  = Button(analysis,width=20,text="Save Result",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a")# save selcetions
							
		self.rockSelect = OptionMenu(analysis, self.rockType, "Rock-E", "Rock-B", "Rock-C", command=self.func)
		self.rockSelect.grid(row=0, column=2, padx=5, pady=5)
		
		
	#======================================
	# Function to return rocktype
	def func(self):
		self.rockType = var.get()
		return self.rockType
	
	# Run complete analysis
	def runFullAnalysis(self):
		self.runType = 0
		configData = Config(self.runType, self.file_names, self.rockType, 100, 75, 5)
		
	#HeatMap
	def runHeatMap(self):
		self.runType = 1
		print("Hello")
	
	#Color Segmentation
	def runColorSeg(self):
		self.runType = 2
		print("Hello")
	
	#Image Subtraction
	def runImageSub(self):
		self.runType = 3
		print("Hello")

	#Save image set
	def saveImage(self):
		print("Hello")
	
	# File Browser
	def browseFolder(self):
		file_names = [20]
		self.files = askopenfilenames(title="Select files")
		self.file_names = self.files
		self.analysis.destroy()
		analysis = tkinter.Toplevel(root)
		new = AnalysisWindow(analysis, self.file_names)# pass file handle to new window
		
	def create_window(self):
		parameters = tkinter.Toplevel(root)
		new = ParametersWindow(parameters)# pass file handle to new window
	#==========================================
	
	
'''ParametersWindow: This window handles the input from the changes to our thresholds 
					 that the user defines '''
					 
class ParametersWindow():

	def __init__(self, parameters, ):
		self.parameters = parameters
		parameters.title("Hindsight: Change Parameters")
		parameters.geometry("300x300")
		parameters.wm_iconbitmap("logo.ico")
		
		saveButton  = Button(parameters,width=20,text="Save Result",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.saveSelections)# save selcetions
		saveButton.grid(row=3, column=3, sticky=E)
		
	def saveSelections(self):
		self.parameters.destroy()
		
	
root = tkinter.Tk()		
index = Window(root)
root.mainloop()
