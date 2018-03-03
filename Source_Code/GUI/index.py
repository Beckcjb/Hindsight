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
import os									
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
		self.files = askopenfilenames(title="Select files")
		self.basepath = os.path.split(self.files[0])[0]		
		self.file_names = [os.path.split(self.files[i])[1] for i in range(0, len(self.files))]
		return self.entered.set(self.files)

	#==========================================
	
	# Create new window upon press of "Select" button
	def create_window(self):
		self.fh = self.file_names
		analysis = tkinter.Toplevel(root)
		new = AnalysisWindow(analysis, self.fh, self.basepath)# pass file handle to new window
		self.home.withdraw()
		
	#==========================================
		
#==============================================================================================		
''' AnalysisWindow: This window is where the main section of the program is carrried out. Here we will us the
					path of the previously selected folder and apply our analysis on each image in the folder
					that is an after image of dust removal.'''
class AnalysisWindow():
	def __init__(self, analysis, files, basepath):
	# Set up analysis window
		self.basepath = basepath
		self.analysis = analysis
		analysis.title("Hindsight: Analysis")
		analysis.geometry("650x325")
		analysis.wm_iconbitmap("logo.ico")
		
	
		
		# Set up Labels and Buttons
		self.runList = []
		self.runVar1 = BooleanVar()
		self.runVar2 = BooleanVar()
		self.runVar3 = BooleanVar()
		self.file_names = [20]
		self.file_names = files
		nl = '\n'
		text = f"Files in use {nl}{nl.join(self.file_names)}"
		fLabel = Label(analysis, text=text) # display what images are in use
		blabel = Label(analysis, text="Basepath: {}".format(basepath)) # display basepath to images
		changeFileButton = Button(analysis,width=20, text="Change File",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.browseFolder) # change folder
							
		runButton   	 = Button(analysis,width=20,text="Run",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a", command=self.runFullAnalysis) # run image analysis
							
		self.colorSegButton   = Checkbutton(analysis,width=20,text="Color Segmenation",
											onvalue = True, offvalue = False, variable = self.runVar1, anchor = W) # run image analysis
							
		self.heatMapButton    = Checkbutton(analysis,width=20,text="Heat Map",
											onvalue = True, offvalue = False, variable = self.runVar2, anchor = W) # run image analysis
							
		self.imageSubButton   = Checkbutton(analysis,width=20,text="Image Subtraction", 
											onvalue = True, offvalue = False, variable = self.runVar3,  anchor = W) # run image analysis
							
		saveButton  	 = Button(analysis,width=20,text="Save Result",
							fg = "#ffffff", bg="#c40e0b", activebackground= "#4c4a4a")# save results
							

		fLabel.grid(row=1, column=1, rowspan = 4, padx=5, pady=5)
		blabel.grid(row=0, column=1, padx=5, pady=5)
		changeFileButton.grid(row=0, column=0, padx=5, pady=5)
		runButton.grid(row=2, column=0, padx=5, pady=5)
		saveButton.grid(row=3, column=0,padx=5,pady=5)
		self.colorSegButton.grid(row=5, column=0,padx=5,pady=5, sticky=W)
		self.heatMapButton.grid(row=6, column=0,padx=5,pady=5, sticky=W)
		self.imageSubButton.grid(row=7, column=0,padx=5,pady=5, sticky=W)
		

			
		self.rockType = StringVar(analysis)
		
		self.rockType.set("Rock-E") # default value
							
		self.rockSelect = OptionMenu(analysis, self.rockType, "Rock-A", "Rock-B", "Rock-C", "Rock-D", "Rock-E", command=self.func)
		self.rockSelect.grid(row=3, column=2, padx=5, pady=5)
		
		
	#======================================
	# Function to return rocktype
	def func(self, value):
		self.colorSegButton.grid_remove()
		self.imageSubButton.grid_remove()
		self.heatMapButton.grid_remove()
		
		
		self.rockType = value
		if self.rockType == "Rock-A":
			#self.rockAoptions()
			pass
			
		elif self.rockType == "Rock-B":
			self.rockBoptions()
			
		elif self.rockType == "Rock-C":
			#self.rockCoptions()
			pass
			
		elif self.rockType == "Rock-D":
			#self.rockDoptions()
			pass
			
		elif self.rockType == "Rock-E":
			self.rockEoptions()
			
		else:
			self.rockEoptions()
		
		return self.rockType
	
		
	
	
	# Run complete analysis
	def runFullAnalysis(self):
		self.runList = [self.runVar1.get(), self.runVar2.get(), self.runVar3.get()]
		configData = Config(self.runList, self.basepath, self.file_names, self.rockType)
		print(configData.returnRunList())
		
	def rockEoptions(self):
		self.colorSegButton.grid(row=5, column=0,padx=5,pady=5, sticky=W)
		self.heatMapButton.grid(row=6, column=0,padx=5,pady=5, sticky=W)
	
	def rockBoptions(self):
		self.colorSegButton.grid(row=5, column=0,padx=5,pady=5, sticky=W)

	def allOptions(self):
		self.colorSegButton.grid(row=5, column=0,padx=5,pady=5, sticky=W)
		self.heatMapButton.grid(row=6, column=0,padx=5,pady=5, sticky=W)
		self.imageSubButton.grid(row=7, column=0,padx=5,pady=5, sticky=W)



	#Save image set
	def saveImage(self):
		print("Hello")
		
	
	# File Browser
	def browseFolder(self):
		self.files = askopenfilenames(title="Select files")
		self.basepath = os.path.split(self.files[0])[0]		
		self.file_names = [os.path.split(self.files[i])[1] for i in range(0, len(self.files))]
		self.analysis.destroy()
		analysis = tkinter.Toplevel(root)
		new = AnalysisWindow(analysis, self.file_names, self.basepath)# pass file handle to new window

	#==========================================
	

		



		
	
root = tkinter.Tk()		
index = Window(root)
root.mainloop()
