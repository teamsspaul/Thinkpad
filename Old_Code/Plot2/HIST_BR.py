#!/usr/bin/evn python

#Saves settings for HIST plots

#############################################################################################################
############################################# Packages ######################################################
############################################################################################################# 

import numpy as np
import Defaults as D

#############################################################################################################
############################################## Inputs #######################################################
############################################################################################################# 

###################################################################################################
####################################### Basic Information #########################################
###################################################################################################

# This is the directory where the file is stored should have the information separated by commas
BenchmarkInfoDir = "/home/paulmmendoza/WORK/Presentation/Quick_Plots/"
# This is the directory file name
filename = "output_80c.csv"

# Do you want to show your figure? If not do you want to save?
ShowFig = True
SaveFig = False # If ShowFig=True, the figure will not save
SaveFigName = "HIST_BR.pdf"

PlotType = "Hist"   

# For histogram
HistColor = 'green';HistAlpha = 0.8;numBins = 100;HistEdgeColor='k'

###################################################################################################
####################################### Plots? ####################################################
###################################################################################################

PlotSetup = [212,211];LPY = 40;LPX = 20;SS = 1       # Two plots one on top of each other

Compare_Data = True            # Select true if the data is to be compared
filename_2 = "output_10c.csv"  # Make sure this file is stored in the same directory as the first file

Title_subplot = True
Title_subplot1 = "80c"         # These will be used if you want them
Title_subplot2 = "10c"

###################################################################################################
######################################### Legend ##################################################
###################################################################################################

###################################################################################################
################################## Highlight Certain data #########################################
###################################################################################################

###################################################################################################
################################### Select data ###################################################
###################################################################################################

# Use Key Below
XValues = 7

#      array[:,0] = File Name
#      array[:,1] = k-eff_o
#      array[:,2] = std_o
#      array[:,3] = k-eff__m
#      array[:,4] = std_m
#      array[:,5] = k-eff_bench
#      array[:,6] = std_bench
#      array[:,7] = k_normalized
#      array[:,8] = std_normalized
#      array[:,9] = geometry
#      array[:,10] = percent of fissions caused by thermal neutrons
#      array[:,11] = percent of fissions caused by intermediate neutrons
#      array[:,12] = percent of fissions caused by fast neutrons
#      array[:,13] = percent of fission casued by epi thermal neutrons
#      array[:,14] = the average neutron energy causing fission ev
#      array[:,15] = the average neutron lethargy causing fission ev

Group_by = 0   # Plots will be grouped by this index 

###################################################################################################
########################################## Grid ###################################################
###################################################################################################


GridXMinor           = D.GridXMinor         # Grid class
#GridXMinor.Run       = False               # To have no X Minor grid lines

GridYMinor           = D.GridYMinor         # Grid class
GridYMinor.alpha     = 0
#GridYMinor.Run       = False               # To have no Y Minor Grid lines

GridXMajor           = D.GridXMajor         # Grid class
#GridXMajor.Run       = False               # To have no X Major Grid lines

GridYMajor           = D.GridYMajor         # Grid class
#GridYMajor.Run       = False               # To have no Y Major Grid lines

###################################################################################################
######################################### Title ###################################################
###################################################################################################

Title = 'Histogram Comparison of Cross Section Libraries'
TitleFontSize = 22
TitleFontWeight = "bold"  # "bold" or "normal"
TitleXPosition = 0.42     # Set title location of plots
TitleYPosition = 0.98

Center_Title = True; No_Title_Mod=False  # This will do the same as above, but can raise and 
TitleYPosition=1                         # lower the title based on the "TitleYPosition" variable

###################################################################################################
######################################## X axis ###################################################
###################################################################################################

ShowXLabels=True                                                   # To show the x label
Xlabel='MCNP $k_{eff}$ / Benchmark $k_{eff}$'                      # X label

Xlimits=True                                                       # Set xlimits?
XLim=[0.97,1.03]                                                   # Limits that will be set

XticksMajor=True                                                   # Modify X major ticks?
Xlabels=['0.97','0.98',    
         '0.99','1.00','1.01','1.02','1.03']                       # Labels for X major ticks X ticks
Xlocs=np.array([0.97,0.98,0.99,1.00,1.01,1.02,1.03])               # Locations for labels major
                                                                   # I know its lame, but this has 
                                                                   # to be a numpy array

XMinorDetails             = D.XMinorDetails                 # tick class

XMajorDetails             = D.XMajorDetails                 # tick class

###################################################################################################
######################################## Y axis ###################################################
###################################################################################################

ShowYLabels=True                                                  # Show the y labels
Ylabel='Count'                                                    # Y label
Ylimits=True                                                      # Set Ylimits?
YLim=[0,90]                                                       # Limits that will be set

YticksMajor=True                                                  # Modify Y major ticks?

Ylabels=['0','30','60','90']                                 # Labels for Y major ticks
Ylocs=[0,30,60,90]                                             # Locations for labels of y
                                                                  # major ticks

YMinorDetails              = D.YMinorDetails         # tick class

YMajorDetails              = D.YMajorDetails         # tick class


###################################################################################################
######################################## Markers ##################################################
###################################################################################################
