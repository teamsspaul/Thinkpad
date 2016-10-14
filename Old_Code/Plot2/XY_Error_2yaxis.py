#!/usr/bin/evn python

#Input deck for XY plot

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

# This is the directory file name
filename = "output_80c.csv"

# Do you want to show your figure? If not do you want to save?
ShowFig = True
SaveFig = False # If ShowFig=True, the figure will not save
SaveFigName = "XY_Lethargy_BR_H_LEU-COMP-THERM.pdf"

PlotType = "XY"   

###################################################################################################
####################################### Plots? ####################################################
###################################################################################################

PlotSetup = [111];LPX = 8;LPY = 8;LPXX = 0.45;LPXY = 0.02;LPYX = 0.05;LPYY = 0.5;SS = 1 # A Single plot

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
XValues=1000     # This plots the index values on the x axis (not set up for y axis)

YValues = 6
Second_Y_Values=True
YValues2=2
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

#Update the values in index 14 and 15 by dividing by 10 to the power 6
Updates=["'14'='14'/10**6","'15'='15'/10**6"]

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

Title = 'Error for K-eigenvalues (MCNP (bottom) & Benchmark)'
TitleFontSize = 18
TitleFontWeight = "bold"  # "bold" or "normal"
TitleXPosition = 0.42     # Set title location of plots
TitleYPosition = 0.98

Center_Title = True; No_Title_Mod=False  # This will do the same as above, but can raise and 
TitleYPosition=1                         # lower the title based on the "TitleYPosition" variable

###################################################################################################
######################################## X axis ###################################################
###################################################################################################

ShowXLabels=True                                            # To show the x label
Xlabel='Benchmark Number'                                   # X label

Xlimits=True                                                # Set xlimits?
XLim=[0,1100]                                               # Limits that will be set

XMinorDetails             = D.XMinorDetails                 # tick class

XMajorDetails             = D.XMajorDetails                 # tick class

###################################################################################################
######################################## Y axis ###################################################
###################################################################################################

ShowYLabels=True                                     # Show the y labels
Ylabel='Absolute Error'    # Y label

YMinorDetails              = D.YMinorDetails         # tick class

YMajorDetails              = D.YMajorDetails         # tick class

###################################################################################################
######################################## Markers ##################################################
###################################################################################################
