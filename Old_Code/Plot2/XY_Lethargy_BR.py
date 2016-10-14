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

PlotSetup = [212,211];LPY = 40;LPX = 30;SS = 1       # Two plots one on top of each other

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

# If you want to highlight a specific case, choose the case here
Highlight = True
HighlightCase = "LEU-COMP-THERM"
ReduceMarker = 0.7   # Factor by which you want to reduce all other Markers/Alphas
ReduceAlpha = 0.6

###################################################################################################
################################### Select data ###################################################
###################################################################################################

XValues = 15   # Select the X values you want to plot
YValues = 7

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

Title = 'Average Fission Lethargy vs. K-eigenvalue Ratio'

Center_Title = True; No_Title_Mod=False  # This will do the same as above, but can raise and 
TitleYPosition=1                         # lower the title based on the "TitleYPosition" variable

###################################################################################################
######################################## X axis ###################################################
###################################################################################################

ShowXLabels=True                                            # To show the x label
Xlabel='Energy of average Lethargy causing fission (MeV)'   # X label
XScale="log"                                                # 'linear' or 'log'
Xlimits=True                                                # Set xlimits?
XLim=[10**-8,10]                                            # Limits that will be set

XticksMajor=True                                            # Modify X major ticks?
Xlabels=['$10^{-8}$','$10^{-7}$','$10^{-6}$','$10^{-5}$',   # Labels for X major ticks
         '$10^{-4}$','$10^{-3}$','$10^{-2}$','$10^{-1}$',
         '$10^{0}$','$10^{1}$'] 
Xlocs=np.array([10**-8,10**-7,10**-6,10**-5,10**-4,10**-3,  # Locations for labels major X ticks.
       10**-2,10**-1,10**0,10**1])                          # I know its lame, but this 
                                                            # has to be a numpy array  

XMinorDetails             = D.XMinorDetails                 # tick class

XMajorDetails             = D.XMajorDetails                 # tick class

###################################################################################################
######################################## Y axis ###################################################
###################################################################################################

ShowYLabels=True                                     # Show the y labels
Ylabel='MCNP $k_{eff}$ / Benchmark $k_{eff}$'        # Y label
YFontSize=18                                         # Y label font size

Ylimits=True                                         # Set Ylimits?
YLim=[0.96,1.03]                                     # Limits that will be set

YticksMajor=True                                     # Modify Y major ticks?
Ylabels=['0.96','0.97','0.98','0.99',  
         '1.00','1.01','1.02','1.03']                # Labels for Y major ticks
Ylocs=[0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03]      # Locations for labels of y
                                                     # major ticks

YMinorDetails              = D.YMinorDetails         # tick class

YMajorDetails              = D.YMajorDetails         # tick class

###################################################################################################
######################################## Markers ##################################################
###################################################################################################
