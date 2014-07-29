# Hernando Martinez 
# modified from code from Christoph Schiklenk
# EMBL July 2014

###
#This code creates a GUI which makes easier the binarization of registered in situ images
###

from javax.swing import JFrame, JButton, JPanel, JTextField, JSlider
from java.awt import GridLayout
from ij.io import OpenDialog, Opener, DirectoryChooser
from ij import ImagePlus, IJ
from ij.plugin import WindowOrganizer
from os import listdir, path, makedirs
import os
from ij.plugin.frame import SyncWindows, ThresholdAdjuster
from ij.process import ImageProcessor

#--- object oriented:

class gui(JFrame):
	def __init__(self): # constructor 
		#origing of coordinates
		self.coordx = 300
		self.coordy = 50

		self.imageCount = 0 #a counter for the image list
		self.listendFlag = 0 #some values to check
		#inintialize values
		self.imLeft = None
		self.imRight = None
		self.chosenOne = None
		self.chosenIm = None
		#create panel (what is inside the GUI)
		self.panel = self.getContentPane()
		self.panel.setLayout(GridLayout(5,2))

		#define buttons here:
		quitButton = JButton("Quit", actionPerformed=self.quit)
		loadButton = JButton("Load", actionPerformed=self.load)
		leftButton = JButton("Choose Left", actionPerformed = self.ChooseLeft)
		rightButton = JButton("Choose Right", actionPerformed = self.ChooseRight)
		ThresButton = JButton("Threshold",actionPerformed = self.ImThresh)
		self.ThreshField = JTextField("5", 1)
		StartConversionButton = JButton("Start Conversion", actionPerformed = self.StartConv)
		ConvertButton = JButton("Convert Image", actionPerformed = self.ImConvert)
		
		#Zslider = JSlider(JSlider.HORIZONTAL,0, 100, 0)

		#add buttons here
		self.panel.add(loadButton)
		self.panel.add(quitButton)
		self.panel.add(leftButton)
		self.panel.add(rightButton)
		self.panel.add(self.ThreshField)
		self.panel.add(ThresButton)
		self.panel.add(StartConversionButton)
		self.panel.add(ConvertButton)
		#self.panel.add(Zslider)

       	#other stuff to improve the look
		self.pack() # packs the frame
		self.setVisible(True) # shows the JFrame
		self.setLocation(0,self.coordy+200)


		




	#define functions for the buttons:
       
	def quit(self, event): #quit the gui
		if self.imLeft is not None:
			self.imLeft.close()
			self.imRight.close()
		self.dispose()
       

	def load(self, event): #choose a folder to load images
		self.imdir = DirectoryChooser("Select a dir, dude").getDirectory()

		self.pictureList = [path.join(self.imdir, f) for f in listdir(self.imdir) if path.splitext(f)[1]==".tiff" and 'AVG' not in f and 'Avg' not in f]  #list of pictures (not averages) with .tiff extension
		print self.pictureList #list of pictures
		self.imLeft = ImagePlus(self.pictureList[self.imageCount]) #read the image
		self.imageCount =self.imageCount+1 #increase counter
		self.imRight = ImagePlus(self.pictureList[self.imageCount]) #read the image
		self.imageCount =self.imageCount+1
		
		self.imLeft.show() #show image on the left
		self.imLeft.getWindow().setLocation(self.coordx,self.coordy) #reposition image
		
       
		self.imRight.show() #show image on the right
		self.rightImLocx = self.coordx+self.imLeft.getWindow().getWidth() #set a variable with the x position for right image
		self.imRight.getWindow().setLocation(self.rightImLocx,self.coordy) #reposition image

		#WindowOrganizer("Tile")
		
		#SyncWindows(self.imLeft.getTitle() + " " + self.imRight.getTitle())
		#IJ.run("Sync Windows")

		print len(self.pictureList)

		

	def ChooseLeft(self, event): #remove right image and load another
		if self.listendFlag==0: #if is not the end of the list
			print "You chose left, which is of course right"
			self.imRight.close()
		if self.imageCount>=len(self.pictureList): #if is the end of the list
			print "YOU HAVE A WINNER!!!"
			self.listendFlag = 1	#flag
			if self.imageCount==len(self.pictureList):
				self.chosenOne = 'L'	#a variable to know the position of the chosen one
			self.imageCount = self.imageCount+1	#this is to avoid changing the chosen one
		else:
			self.imRight = ImagePlus(self.pictureList[self.imageCount]) #read next image
			self.imageCount =self.imageCount+1	#increase counter
			self.imRight.show() #show image on the right
			self.imRight.getWindow().setLocation(self.rightImLocx,self.coordy) #reposition image

	
	def ChooseRight(self, event): #same as above but for the right image
		if self.listendFlag==0:
			print "You chose right, :)"
			self.imLeft.close()
		if self.imageCount>=len(self.pictureList):
			print "YOU HAVE A WINNER!!!"
			self.listendFlag = 1
			if self.imageCount==len(self.pictureList):
				self.chosenOne = 'R'
			self.imageCount = self.imageCount+1
		else:
			self.imLeft = ImagePlus(self.pictureList[self.imageCount])
			self.imageCount =self.imageCount+1
			self.imLeft.show() #show image on the left
			self.imLeft.getWindow().setLocation(self.coordx,self.coordy) #reposition image


	def ImThresh(self, event): #play wiht the threshold for every image
		IJ.setThreshold(float(self.ThreshField.getText()), 255)
		IJ.setOption("BlackBackground", false)



	def StartConv(self,event):
		print 'hola ', self.chosenOne
		os.path.makedirs('/Users/vergara/Desktop/EMBL/Images/PrImR6/4registered/AcTub/Average/test/')
		print 'adios'
		#print exists('/Users/vergara/Desktop/EMBL/Images/PrImR6/4registered/AcTub/Average/')
		#allow to use only if there is a chosen one
		
		#create a folder to store the binarized images
		if self.chosenOne == None:
			print 'Please choose one reference image first'
		elif self.chosenOne == 'L':
			#print 'You chose the left'
			self.chosenIm = self.imLeft
		elif self.chosenOne == 'R':
			#print 'You chose the right'
			self.chosenIm = self.imRight

		if self.chosenIm is not None:
			self.chosenIm.getWindow().setLocation(self.coordx,self.coordy) #reposition image
			
			#create directory
			self.bindir = path.join(self.imdir, 'CuratedBinarization/')
			print self.bindir
			makedirs(self.bindir)
			#IJ.File.makeDirectory(self.bindir)
			
			
			
			#if path.exists(self.bindir):
				
				#shutil.rmtree(self.bindir) #remove previous version if it already existed
			#	print 'Please remove previous directory and try again'
			#else:
			#	print self.bindir
			#	makedirs(self.bindir)
				
			
			#get the information of the the chosen one, binarize it, save it, and avoid open it again


			
	
	def ImConvert(self,event): #apply the threshold that the image has
		#allow to use only if StartConv has been pressed
		IJ.run("Convert to Mask", "method=Default background=Dark")
		#save

## MAIN
gui()