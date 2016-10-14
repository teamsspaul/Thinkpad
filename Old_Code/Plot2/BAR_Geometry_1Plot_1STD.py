#!/usr/bin/evn python

#Saves settings for XY plots


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
SaveFigName = "Figurename.pdf"

PlotType = "Bar"    

# For Bar              
Width=0.5;                  # Width of each Bar
HalfBarWidth=0.25;          # Half width of each Bar (make sure xlimits are set with this)
BarColor=['green','blue'];  # Color of the Bar
NumberOfSTDs=[1];           # If a benchmark is "NumberOfSTDs"*STD out from what is expected, it is counted
STD_COMPARE=8               # Index corresponding to the STD of "XValues" (check Select Data section)
STD_Expected=1              # Expected value for above
Compare_B=True;             # If you want to draw a line on the histogram corresponding to expected
                            # percentages with perfectly gaussian systems
Compare_Bar='r';            # Color of the line for "Compare_Bar"
C_BarLine='-';              # Type of line for the "Compare_Bar"
NumberOfPointsBar=25        # Number of points for the line
C_BarAlpha=0.35             # opacity of "Compare_Bar"

###################################################################################################
####################################### Plots? ####################################################
###################################################################################################

PlotSetup = [111];LPX = 8;LPY = 8;LPXX = 0.45;LPXY = 0.02;LPYX = 0.05;LPYY = 0.5;SS = 1 # A Single plot

Compare_Data = True            # Select true if the data is to be compared
filename_2 = "output_10c.csv"  # Make sure this file is stored in the same directory as the first file

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

Group_by = 9   # Plots will be grouped by this index 

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

Title = 'Comparison between two cross section libraries'
TitleFontSize = 14

Center_Title = True; No_Title_Mod=True   # This will center the title on the figure 
                                         # as a whole even with a legend

###################################################################################################
######################################## X axis ###################################################
###################################################################################################

Xlimits=True                                                # Set xlimits?
XLim=[-HalfBarWidth,6.25]                                   # Limits that will be set


XticksMajor=True                                            # Modify X major ticks?

         ### These values are over written in a Bar Graph ###
Xlabels=['$10^{-8}$','$10^{-7}$','$10^{-6}$','$10^{-5}$',   # Labels for X major ticks
         '$10^{-4}$','$10^{-3}$','$10^{-2}$','$10^{-1}$',
         '$10^{0}$','$10^{1}$'] 
Xlocs=np.array([10**-8,10**-7,10**-6,10**-5,10**-4,10**-3,  # Locations for labels major X ticks
       10**-2,10**-1,10**0,10**1])                          # I know its lame, but this has to be a
                                                            # numpy array

XMinorDetails             = D.XMinorDetails                 # tick class

XMajorDetails             = D.XMajorDetails                 # tick class

###################################################################################################
######################################## Y axis ###################################################
###################################################################################################

ShowYLabels=True                                     # Show the y labels
Ylabel='Percent of cases outside 1 std'              # Y label

Ylimits=True                                         # Set Ylimits?
YLim=[0,1.1]                                         # Limits that will be set

YticksMajor=True                                     # Modify Y major ticks?
Ylabels=['0','10%','20%','30%',  
         '40%','50%','60%','70%',
          '80%','90%','100%']                        # Labels for Y major ticks
Ylocs=[0,.10,.20,.30,.40,.50,
       0.60,0.70,0.80,0.90,1.00]                     # Locations for labels of y
                                                     # major ticks
YMinorDetails              = D.YMinorDetails         # tick class

YMajorDetails              = D.YMajorDetails         # tick class

###################################################################################################
######################################## Markers ##################################################
###################################################################################################
