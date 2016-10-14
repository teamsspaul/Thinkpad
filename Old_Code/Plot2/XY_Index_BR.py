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
SaveFig = False # if ShowFig=True, the figure will not save
SaveFigName = "XY_Index_BR.pdf"

PlotType = "XY"

Extend_Bottom=True

###################################################################################################
####################################### Plots? ####################################################
###################################################################################################

PlotSetup = [212,211];LPY = 40;LPX = 30;SS = 1      # Two plots one on top of each other

Compare_Data=True            #Select true if the data is to be compared
filename_2="output_10c.csv"  #Make sure this file is stored in the same directory as the first file


Title_subplot=True
Title_subplot1="80c"   #These will be used if you want them
Title_subplot2="10c"

###################################################################################################
######################################### Legend ##################################################
###################################################################################################

legend=True       #Add legend to plot?
Center_On_Graph=True  #If there is a legend, we can center axis labels based on graphs or the 
                      #entire figure. 

###################################################################################################
################################## Highlight Certain data #########################################
###################################################################################################

###################################################################################################
################################### Select data ###################################################
###################################################################################################

#Use Key Below
XValues=1000     # This plots the index values on the x axis (not set up for y axis)
YValues=7

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
#      array[:,1000] = index

Group_by=0   #Plots will be grouped by this index 

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

Title='Benchmark Number vs. K-eigenvalue Ratio'

TitleFontWeight="bold" # "bold" or "normal"
TitleXPosition=0.42     # Set title location of plots
TitleYPosition=1

Center_Title = False; No_Title_Mod=False # This gives you an opporunity to move your title to 
                                         # where you want, change "TitleXPosition" and "TitleYPosition"

###################################################################################################
######################################## X axis ###################################################
###################################################################################################

ShowXLabels=True                                                # To show the x label
Xlabel='Benchmark Number'                                       # X label

Xlimits=True                                                    # Set xlimits?
XLim=[0,1105]                                                   # Limits that will be set

XticksMajor=True                                                # Modify X major ticks?
Xlabels=['0','100','200','300','400','500','600','700',         # Labels for X major ticks
         '800','900','1000','1100'] 
Xlocs=np.array([0,100,200,300,400,500,600,700,800,              # Locations for labels major X ticks
       900,1000,1100])                                          # I know its lame, but this has 
                                                                # to be a numpy array 

XticksMinor=True                                                # modify Xminor tick locations?
XlocsMinor=np.arange(0.965,1.035,0.01)                          # Xminor locations

XMinorDetails             = D.XMinorDetails                     # tick class

XMajorDetails             = D.XMajorDetails                     # tick class


###################################################################################################
######################################## Y axis ###################################################
###################################################################################################

Ylimits=True                                                      # Set Ylimits?
YLim=[0.96,1.03]                                                  # Limits that will be set

YticksMajor=True                                                  # Modify Y major ticks?
Ylabels=['0.96','0.97','0.98','0.99', 
         '1.00','1.01','1.02','1.03']                             # Labels for Y major ticks
Ylocs=[0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03]                   # Locations for labels of y
                                                                  # major ticks


YMinorDetails             = D.YMinorDetails                       # tick class

YMajorDetails             = D.YMajorDetails                       # tick class

###################################################################################################
######################################## Markers ##################################################
###################################################################################################
