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
# Imports
from Source_Code import Config, Control


import sys									# System Variables
import os
import numpy as np							# Numbered python array
import cv2									# openCV library
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
		home.title("Hindsight")
		home.wm_iconbitmap("logo.ico")
		home.configure(background='#FCE5B3')
		
	# Place buttons/labels/entry boxes
		entered = StringVar() # file handle
		self.entered = entered
		hLabel = Label (home, text="Hindsight: Image Analysis Tool", bg = '#FCE5B3')
		hLabel.grid(row=0, column=1)

		browseButton = Button(home,text="Browse...",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.browseFolder)

		selectButton = Button(home,text="Select",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.create_window)
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
		analysis.configure(background='#FCE5B3')
		
		
		# Set up Labels and Buttons
		self.controller = None
		self.runList = []
		self.runVar1 = StringVar()
		self.runVar2 = StringVar()
		self.runVar3 = StringVar()
		self.file_names = [20]
		self.file_names = files
		nl = '\n'
		text = f"Files in use {nl}{nl.join(self.file_names)}"
		fLabel = Label(analysis, text=text, bg='#FCE5B3') # display what images are in use
		blabel = Label(analysis,bg='#FCE5B3', text="Basepath: {}".format(basepath)) # display basepath to images
		changeFileButton = Button(analysis,width=20, text="Change File",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.browseFolder) # change folder

		sendButton = Button(analysis,width=20,text="Send Configuration",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.sendConfig) # send image data

		runButton = Button(analysis,width=20,text="Run",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.run) # run image analysis


		self.imageSubButton = Checkbutton(analysis,width=20,text="Image Subtraction",bg='#FCE5B3',
											onvalue = "subtract", offvalue = None, variable = self.runVar1,  anchor = W) # run image analysis

		self.colorSegButton   = Checkbutton(analysis,width=20,text="Color Segmenation",bg='#FCE5B3',
											onvalue = "color_segment", offvalue = None, variable = self.runVar2, anchor = W) # run image analysis

		self.heatMapButton    = Checkbutton(analysis,width=20,text="Heat Map",bg='#FCE5B3',
											onvalue = "analyze_mask_block", offvalue = None, variable = self.runVar3, anchor = W) # run image analysis


		saveButton = Button(analysis,width=20,text="Save Result",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command = self.saveImage)# save results


		blabel.grid(row=0, column=1, padx=5, pady=5)
		fLabel.grid(row=1, column=1, rowspan = 10, padx=5, pady=5)
		changeFileButton.grid(row=0, column=0, padx=5, pady=5)
		sendButton.grid(row=2, column=0, padx=5, pady=5)
		runButton.grid(row=3, column=0, padx=5, pady=5)
		saveButton.grid(row=4, column=0,padx=5,pady=5)
		self.imageSubButton.grid(row=6, column=0,padx=5,pady=5, sticky=W)
		self.colorSegButton.grid(row=7, column=0,padx=5,pady=5, sticky=W)
		self.heatMapButton.grid(row=8, column=0,padx=5,pady=5, sticky=W)

		self.imageSubButton.deselect()
		self.colorSegButton.deselect()
		self.heatMapButton.deselect()

		self.rock_type = StringVar(analysis)

		self.rock_type.set("Rock-E") # default value

		self.rockSelect = OptionMenu(analysis, self.rock_type, "Rock-A",
															   "Rock-B",
															   "Rock-C",
															   "Rock-D",
															   "Rock-E",
															     command=self.func)
		self.rockSelect.configure(bg = "#881600", fg = '#ffffff', activebackground= "#881600")
		self.rockSelect["menu"].configure(bg = "#881600", fg = '#ffffff')
		self.rockSelect.grid(row=3, column=2, padx=5, pady=5)


	#======================================
	# Function to return rock_type
	def func(self, value):
		self.heatMapButton.deselect()
		self.imageSubButton.deselect()
		self.colorSegButton.deselect()
		self.colorSegButton.grid_remove()
		self.imageSubButton.grid_remove()
		self.heatMapButton.grid_remove()

		self.rock_type = value
		if self.rock_type == "Rock-A":
			#self.rockAoptions()
			pass

		elif self.rock_type == "Rock-B":
			self.rockBoptions()

		elif self.rock_type == "Rock-C":
			#self.rockCoptions()
			pass

		elif self.rock_type == "Rock-D":
			#self.rockDoptions()
			pass

		elif self.rock_type == "Rock-E":
			self.rockEoptions()

		else:
			self.rockEoptions()

		return self.rock_type

	# Send the configuration to the Controller
	def sendConfig(self):
		run_list = [self.runVar1.get(), self.runVar2.get(), self.runVar3.get()]
		configData = Config(run_list, self.basepath, self.file_names, self.rock_type.get())
		self.controller = Control.from_config(configData)

	# Run the current functions in the controller
	def run(self):
		self.controller.run()

	def rockEoptions(self):
		self.imageSubButton.grid(row=6, column=0,padx=5,pady=5, sticky=W)
		self.colorSegButton.grid(row=7, column=0,padx=5,pady=5, sticky=W)
		self.heatMapButton.grid(row=8, column=0,padx=5,pady=5, sticky=W)


	def rockBoptions(self):
		self.colorSegButton.grid(row=7, column=0,padx=5,pady=5, sticky=W)

	def allOptions(self):
		self.imageSubButton.grid(row=6, column=0,padx=5,pady=5, sticky=W)
		self.colorSegButton.grid(row=7,  column=0,padx=5,pady=5, sticky=W)
		self.heatMapButton.grid(row=8, column=0,padx=5,pady=5, sticky=W)

	#Save image set
	def saveImage(self):
		self.controller.save()

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
