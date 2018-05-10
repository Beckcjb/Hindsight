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
from Source_Code import matlab

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
		analysis.geometry("700x650")
		analysis.wm_iconbitmap("logo.ico")
		analysis.configure(background='#FCE5B3')

		# Set up Labels and Buttons
		self.bufferVal = IntVar(value = 10)
		self.abrasionX = IntVar(value = 1110)
		self.abrasionY = IntVar(value = 1135)
		self.abrasionRadi = IntVar(value = 320)
		self.bandSize = DoubleVar(value = 20)
		self.controller = None
		self.runVar1 = StringVar()
		self.runVar2 = StringVar()
		self.runVar3 = StringVar()
		self.file_names = files
		nl = '\n'
		text = f"Files in use: {nl}{nl.join(self.file_names)}"
		fLabel = Label(analysis, text=text, bg='#FCE5B3') # display what images are in use
		blabel = Label(analysis,bg='#FCE5B3', text="Basepath: {}".format(basepath)) # display basepath to images

		changeFileButton = 	Button(analysis,width=20, text="Change File",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.browseFolder) # change folder

		sendButton = 		Button(analysis,width=20,text="Send Configuration",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.sendConfig) # send image data

		runButton = 		Button(analysis,width=20,text="Run",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.run) # run image analysis

		self.applyButton = 	Button(analysis,width=10,text="View Changes",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command=self.applyCircle) # run image analysis

		saveButton = 		Button(analysis,width=20,text="Save Result",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command = self.saveImage)# save results
							
		quitButton = 		Button(analysis,width=10,text="Exit",
							fg = "#ffffff", bg="#881600", activebackground= "#EDB183", command = self.quit)# save results

		self.bufferEntry = 		Entry(analysis,	width=10, textvariable=self.bufferVal)
		self.abrasionXspot = 	Entry(analysis, text="Moves L/R:", width=10, textvariable=self.abrasionX)
		self.abrasionYspot = 	Entry(analysis, width=10, textvariable=self.abrasionY)
		self.abrasionRadius = 	Entry(analysis, width=10, textvariable=self.abrasionRadi)
		self.bandSizeEnt =		Entry(analysis, width=10, textvariable=self.bandSize)
		self.bufText = 			Label(analysis, text="Incriment Size(5-15):", bg = '#FCE5B3')
		self.abrasionXtext = 	Label(analysis, text="Move L/R:", bg = '#FCE5B3')
		self.abrasionYtext = 	Label(analysis,  text="Move U/D:", bg = '#FCE5B3')
		self.abrasionRadiText = Label(analysis, text="Change Radius:", bg = '#FCE5B3')
		self.bandSizeText = 	Label(analysis, text="Band Size(10-100):", bg='#FCE5B3')

		self.densityDetectionType = StringVar(analysis)

		self.densityDetectionType.set("Detecion Shape") # default value

		self.densityDetectionSelect = OptionMenu(analysis, self.densityDetectionType, "Detecion Shape","Circular","Square",
															     command=self.detectFunc)
		self.densityDetectionSelect.configure(bg = "#881600", fg = '#ffffff', activebackground= "#881600")
		self.densityDetectionSelect["menu"].configure(bg = "#881600", fg = '#ffffff')

		blabel.grid(row=0, column=1, padx=5, pady=5)
		fLabel.grid(row=1, column=1, rowspan = 5, padx=5, pady=5)
		changeFileButton.grid(row=0, column=0, padx=5, pady=5)
		sendButton.grid(row=2, column=0, pady=5)
		runButton.grid(row=3, column=0, pady=5)
		saveButton.grid(row=4, column=0,pady=5)
		quitButton.grid(row=0, column=2, pady=5, padx=5, sticky = E)


		self.rock_type = StringVar(analysis)

		self.rock_type.set("Rock-Type") # default value

		self.rockSelect = OptionMenu(analysis, self.rock_type, "Rock-Type", "Rock-B",
															   "Rock-E", command=self.func)
		self.rockSelect.configure(bg = "#881600", fg = '#ffffff', activebackground= "#881600")
		self.rockSelect["menu"].configure(bg = "#881600", fg = '#ffffff')
		self.rockSelect.grid(row=3, column=2, pady=5, padx=5)

		self.run_options = StringVar()

		self.run_options.set("Analysis Type") # default value

		self.run_select = OptionMenu(self.analysis, self.run_options, "Analysis Type","Color Analysis",
															     command=self.runFunc)
		self.run_select.configure(bg = "#881600", fg = '#ffffff', activebackground= "#881600")
		self.run_select["menu"].configure(bg = "#881600", fg = '#ffffff')


	#======================================
	# Function to return rock_type
	def func(self, value):
		self.run_select.grid_forget()
		self.densityDetectionSelect.grid_forget()
		self.bufText.grid_forget()
		self.bandSizeText.grid_forget()
		self.bandSizeEnt.grid_forget()
		self.abrasionXtext.grid_forget()
		self.abrasionYtext.grid_forget()
		self.abrasionRadiText.grid_forget()
		self.bufferEntry.grid_forget()
		self.abrasionXspot.grid_forget()
		self.abrasionYspot.grid_forget()
		self.abrasionRadius.grid_forget()
		self.applyButton.grid_forget()
		self.densityDetectionSelect.grid_forget()

		self.rock_type = value
		if self.rock_type == "Rock-B":
			self.rockBoptions()

		elif self.rock_type == "Rock-E":
			self.rockEoptions()

		else:
			self.rockEoptions()

		return self.rock_type

	def runFunc(self, value):
		self.densityDetectionSelect.grid_forget()
		self.bufText.grid_forget()
		self.bandSizeText.grid_forget()
		self.bandSizeEnt.grid_forget()
		self.abrasionXtext.grid_forget()
		self.abrasionYtext.grid_forget()
		self.abrasionRadiText.grid_forget()
		self.bufferEntry.grid_forget()
		self.abrasionXspot.grid_forget()
		self.abrasionYspot.grid_forget()
		self.abrasionRadius.grid_forget()
		self.applyButton.grid_forget()
		self.run_options = value
		if self.run_options == "Color Analysis":
			self.colorAnalysis()

		elif self.run_options == "Image Subtraction":
			self.imageSubtract()

		else:
			self.colorAnalysis()

		return self.run_options

	def detectFunc(self, value):
		self.bufText.grid_forget()
		self.bandSizeEnt.grid_forget()
		self.bandSizeText.grid_forget()
		self.abrasionXtext.grid_forget()
		self.abrasionYtext.grid_forget()
		self.abrasionRadiText.grid_forget()
		self.bufferEntry.grid_forget()
		self.abrasionXspot.grid_forget()
		self.abrasionYspot.grid_forget()
		self.abrasionRadius.grid_forget()
		self.applyButton.grid_forget()
		self.densityDetectionType = value
		if self.densityDetectionType == "Circular":
			self.circular()

		elif self.densityDetectionType == "Square":
			self.square()


		return self.densityDetectionType

	# Send the configuration to the Controller
	def imageSubtract(self):
		self.applyButton.grid_forget()
		self.bufferEntry.grid_forget()
		self.abrasionXspot.grid_forget()
		self.abrasionYspot.grid_forget()
		self.abrasionRadius.grid_forget()
		self.densityDetectionSelect.grid_forget()
		self.bandSizeText.grid_forget()
		self.bandSizeEnt.grid_forget()


	def colorAnalysis(self):
		self.densityDetectionSelect.grid(row=10, column=0, pady=5)


	def circular(self):
		self.runVar1.set("ml_color_segment")
		self.runVar2.set("analyze_mask")
		self.runVar3.set("")
		self.bufText.grid(row=11, column=0,pady=5)
		self.bandSizeText.grid(row=12, column=0, pady=5)
		self.abrasionXtext.grid(row=13, column=0, pady=5)
		self.abrasionYtext.grid(row=14, column=0, pady=5)
		self.abrasionRadiText.grid(row=15, column=0, pady=5)
		self.bufferEntry.grid(row=11, column=1 , pady=5, sticky = W)
		self.bandSizeEnt.grid(row=12, column=1, pady=5, sticky =W)
		self.abrasionXspot.grid(row=13, column=1, pady=5, sticky = W)
		self.abrasionYspot.grid(row=14, column=1,  pady=5, sticky = W)
		self.abrasionRadius.grid(row=15, column=1, pady=5, sticky = W)
		self.applyButton.grid(row=16, column=0, pady=5)

	def square(self):
		self.runVar1.set("ml_color_segment")
		self.runVar2.set("analyze_mask")
		self.runVar3.set("")
		self.bufText.grid(row=11, column=0,pady=5)
		self.abrasionXtext.grid(row=12, column=0, pady=5)
		self.abrasionYtext.grid(row=13, column=0, pady=5)
		self.abrasionRadiText.grid(row=14, column=0, pady=5)
		self.bufferEntry.grid(row=11, column=1 , pady=5, sticky = W)
		self.abrasionXspot.grid(row=12, column=1, pady=5, sticky = W)
		self.abrasionYspot.grid(row=13, column=1,  pady=5, sticky = W)
		self.abrasionRadius.grid(row=14, column=1, pady=5, sticky = W)
		self.applyButton.grid(row=15, column=0, pady=5)

	def sendConfig(self):
		run_list = [self.runVar1.get(), self.runVar2.get(), self.runVar3.get()]
		arg_list = [self.densityDetectionType, self.run_options, self.abrasionRadi.get(), self.abrasionX.get(),
					self.abrasionY.get(), self.bandSize.get(), self.bufferVal.get()]

		configData = Config(run_list, self.basepath, self.file_names,
							self.rock_type, arg_list)
		self.controller = Control.from_config(configData)

	# Run the current functions in the controller
	def run(self):
		self.controller.run()

	def rockEoptions(self):
		self.run_select.grid(row=9, column=0, padx=5, pady=5)

	def rockBoptions(self):
		self.run_select.grid(row=9, column=0, padx=5, pady=5)

	#Save image set
	def saveImage(self):
		self.controller.save()

	def applyCircle(self):
		image = self.basepath +'/'+ self.file_names[0]
		matlab.matlab_engine.drawAbrasion(image, self.abrasionX.get(),
										  self.abrasionY.get(),
										  self.abrasionRadi.get(), nargout=0)
		img = cv2.imread('circleImage.jpeg', 0)
		new_size = (int(len(img[0])/3), int(len(img)/3))
		imS = cv2.resize(img, new_size)
		cv2.imshow('image', imS)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# File Browser
	def browseFolder(self):
		self.files = askopenfilenames(title="Select files")
		self.basepath = os.path.split(self.files[0])[0]
		self.file_names = [os.path.split(self.files[i])[1] for i in range(0, len(self.files))]
		self.analysis.destroy()
		analysis = tkinter.Toplevel(root)
		new = AnalysisWindow(analysis, self.file_names, self.basepath)# pass file handle to new window
		
	# exit software
	def quit(self):
		self.analysis.quit()
	#==========================================


root = tkinter.Tk()
index = Window(root)
root.mainloop()
