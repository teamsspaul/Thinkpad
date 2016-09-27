#!/usr/bin/env python

#This file contains default settings for the plotting program 'plot.py'.
#To overwrite settings, create a separate python file and modify specific parameters

#############################################################################################################
############################################# Packages ######################################################
############################################################################################################# 

import numpy as np
import matplotlib.pyplot as plt
import fnmatch #For wildcard matches 
from string import digits
import re
import os

#############################################################################################################
############################################# Classes #######################################################
############################################################################################################# 

class ticks:
    def __init__(self):
        self.axis        = 'both'
        self.labelsize   = 14
        self.which       = 'both'
        self.length      = 4
        self.color       = 'k' 
        self.labelcolor  = 'k'
        self.width       = 1
        self.left        = 'off'
        self.right       = 'off'
        self.top         = 'off'
        self.bottom      = 'off'
        self.labelleft   = 'off'
        self.labelright  = 'off'
        self.labelbottom = 'off'
        self.labeltop    = 'off'
        self.Run         = True

class grids:
    def __init__(self):
        self.axis        = 'both'
        self.alpha       = 1
        self.which       = 'both'
        self.color       = 'k' 
        self.linestyle   = 'dotted' #'solid' 'dashed' 'dashdot' 'dotted'
        self.linewidth   = 0.7
        self.marker      = ''
        self.markersize  = 8
        self.Run         = True


#############################################################################################################
############################################## Inputs #######################################################
############################################################################################################# 

###################################################################################################
####################################### Basic Information #########################################
###################################################################################################

# This is the directory where the file is stored should have the information separated by commas
# We assume its in the current working directory
BenchmarkInfoDir = os.getcwd()+"/"
OutputDir=BenchmarkInfoDir+"figures/"

DataLocation=BenchmarkInfoDir+"Data_To_Plot/"

# This is the directory file name
filename = "output_80c.csv"

# http://matplotlib.org/api/pyplot_summary.html   <- helpful link

# Basic information
FigureSize = (11, 6) # Dimensions of the figure

# Do you want to show your figure? If not do you want to save?
ShowFig = False
SaveFig = False # If ShowFig=True, the figure will not save
SaveFigName = "Default_name_for_figure.pdf"

TypeOfFamily='monospace'   #This sets the type of font for text on plot
font = {'family' : TypeOfFamily}  # This sets the type of font for text on plot

PlotType = "XY"   

                    # Options: "XY" (using "XValues" and "YValues"
                    #          "Hist" (Make hist out of "XValues") 
                    #          "Bar"  (Makes Bar with "XValues" bars of "Group_by")




# For histogram
HistColor = 'green';        #The color of the bars
HistEdgeColor='k'           #The edge color of the bars
HistAlpha = 0.8;            #opacity of the hist bars
numBins = 50;               #number of bins 
HISTTEXTTIME=False          #For looking at time, if you want to add a textbox
                            #stating what percentage of runs were under 10,20,30 and 40 minutes put true


HISTTIMEX=0.70              #location of hist box (default for only one axis)
HISTTIMEY=0.95
HISTalign='top'             #'top' 'bottom' 'center' 'baseline' (location of box)
HISTprops=dict(boxstyle='round',facecolor='wheat',alpha=1) #Details for your box
GaussFit=False
GaussStyle='dashed';GaussMarker='.';GaussColor='green';Gaussmarkersize=8;GaussAlpha=1;
GaussLineWidth=2



# For Bar              
Width=0.5;                  # Width of each Bar
HalfBarWidth=0.25;          # Half width of each Bar (make sure xlimits are set with this)
BarColor=['green','blue'];  # Color of the Bar
NumberOfSTDs=[1,2];           # If a benchmark is "NumberOfSTDs"*STD out from what is expected, it is counted
STD_COMPARE=8               # Index corresponding to the STD of "XValues" (check Select Data section)
STD_Expected=1              # Expected value for above
Compare_B=False;             # If you want to draw a line on the histogram corresponding to expected
                            # percentages with perfectly gaussian systems
Compare_Bar='r';            # Color of the line for "Compare_Bar"
C_BarLine='-';              # Type of line for the "Compare_Bar"
NumberOfPointsBar=25        # Number of points for the line
C_BarAlpha=0.35             # opacity of "Compare_Bar"
C_linewidth=2               # linewidth of "Compare_Bar"

# For NonBar
HalfBarWidth=0

Tightlayout=False
Extend_Bottom=False
How_Extend_Bottom=0.15



###################################################################################################
####################################### Plots? ####################################################
###################################################################################################

#PlotSetup = [111];LPX = 8;LPY = 8;LPXX = 0.45;LPXY = 0.02;LPYX = 0.05;LPYY = 0.5;SS = 1 # A Single plot
#PlotSetup = [212,211];LPY = 40;LPX = 30;SS = 1       # Two plots one on top of each other
#PlotSetup = [121,122];LPY = 40;LPX = 30;SS = 2      # Two plots next to each other

Compare_Data = False            # Select true if the data is to be compared
filename_2 = "output_10c.csv"  # Make sure this file is stored in the same directory as the first file

# If you want to turn off features on one plot and not the other search for 
# A_Variable_That_I_Will_Never_Use in the plotting file and in that section modify what you will, 
# some options are shown there


Title_subplot = False
Title_subplot1 = "80c"         # These will be used if you want them
Title_subplot2 = "10c"

TitleSFontSize = 16            # Font size and weight for sub plot titles
TitleSFontWeight = 'normal'    # 'bold' or 'normal'

tfont=font

###################################################################################################
######################################### Legend ##################################################
###################################################################################################

legend = False           # Add legend to plot?
LegendFontSize = 12
                        # Defaults to right side of plot on outside
                        # Can change http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend

LegendWeight='normal'  #'normal' or 'heavy'

Lfont = {'family' : TypeOfFamily}  # This sets the type of font for legend on plot
Lfont['size']=LegendFontSize

SquishGraph = 0.75      # Squeeze plots by this factor to fit legend outside of plot

Center_On_Graph = True  # If there is a legend, we can center axis labels based on graphs or the 
                        # entire figure. 

# Please note, if Center_On_Graph = False and PlotSetup=[111] and legend = True
# Might have to manually adjust x and y axis labels with the parameters. LPXX,LPXY,LPYX,LPYY

BBOXX = 1;BBOXY = 0.5       # Set legend on right side of graph
#BBOXX = 0.5;BBOXY = 1.25   # Set legend on top of graph

NumberOfLegendColumns = 1   # Better for legend on side (sets number of columns in the legend)
#NumberOfLegendColumns = 4  # Better for legend on top

###################################################################################################
################################## Highlight Certain data #########################################
###################################################################################################

# If you want to highlight a specific case, choose the case here
Highlight = False
HighlightCase = "LEU-COMP-THERM"
ReduceMarker = 0.7   # Factor by which you want to reduce all other Markers/Alphas
ReduceAlpha = 0.6

# If you want to omit certain cases
OmitCases=["Do_Not_Omit_Anything"]


###################################################################################################
################################### Select data ###################################################
###################################################################################################

# Use Key Below
#XValues = 15
# XValues=1000     # This plots the index values on the x axis (not set up for y axis)
# XValues=1
YValues = 7

Second_Y_Values=False
YValues2=6
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
Group_by2 = "None"    #If you want to have a subgroup, you may
                      #put in text the subgroup you would like

#Update the values in index 14 and 15 by dividing by 10 to the power 6
Updates=["'14'='14'/10**6","'15'='15'/10**6"]                            

ERRORBARS=False     #If you want error bars, set to true
ERRORFILL=False     #Please only pick one or the other (ERRORBARS ERRORFILL)
YERROR=None         #Add integer which corresponds to index above (8 = std)
XERROR=None         #Add integer which correspond to index for error if no error bars set to None

#For filling
Alpha_ValueE=[0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3]

###################################################################################################
########################################## Grid ###################################################
###################################################################################################

GridXMinor           = grids()
GridXMinor.axis      = 'x'
GridXMinor.alpha     = 0.6
GridXMinor.which     = 'minor'
GridXMinor.color     = 'k'
GridXMinor.linestyle = 'dotted'
GridXMinor.linewidth = 0.5
#GridXMinor.Run       = False               # To have no X Minor grid lines

GridYMinor           = grids()
GridYMinor.alpha     = 0
#GridYMinor.Run       = False               # To have no Y Minor Grid lines

GridXMajor           = grids()
GridXMajor.axis      = 'x'
GridXMajor.which     = 'major'
GridXMajor.color     = 'k'
GridXMajor.linestyle = 'dotted'
#GridXMajor.Run       = False               # To have no X Major Grid lines

GridYMajor           = grids()
GridYMajor.axis      = 'y'
GridYMajor.which     = 'major'
GridYMajor.color     = 'k'
GridYMajor.linestyle = 'dotted'
#GridYMajor.Run       = False               # To have no Y Major Grid lines

###################################################################################################
######################################### Title ###################################################
###################################################################################################

Title = 'Average Fission Lethargy vs. K-eigenvalue Ratio'
TitleFontSize = 22
TitleFontWeight = "bold"  # "bold" or "normal"
TitleXPosition = 0.42     # Set title location of plots
TitleYPosition = 0.98

Tfont=font
#Center_Title = True; No_Title_Mod=True   # This will center the title on the figure 
                                         # as a whole even with a legend

#Center_Title = True; No_Title_Mod=False  # This will do the same as above, but can raise and 
#TitleYPosition=1                         # lower the title based on the "TitleYPosition" variable

#Center_Title = False; No_Title_Mod=False # This gives you an opporunity to move your title to 
                                         # where you want, change "TitleXPosition" and "TitleYPosition"

Center_Title = False; No_Title_Mod=True  # No title 


###################################################################################################
######################################## X axis ###################################################
###################################################################################################

ShowXLabels=False                                            # To show the x label
Xlabel='Energy of average Lethargy causing fission (MeV)'   # X label
XFontSize=18                                                # X label font size
XFontWeight="normal"                                        # "bold" or "normal"
XScale="linear"                                             # 'linear' or 'log'
Xlimits=False                                                # Set xlimits?
XLim=[10**-8,10]                                            # Limits that will be set


XticksMajor=False                                           # Modify X major ticks?
Xlabels=['$10^{-8}$','$10^{-7}$','$10^{-6}$','$10^{-5}$',   # Labels for X major ticks
         '$10^{-4}$','$10^{-3}$','$10^{-2}$','$10^{-1}$',
         '$10^{0}$','$10^{1}$'] 
Xlocs=np.array([10**-8,10**-7,10**-6,10**-5,10**-4,10**-3,  # Locations for labels major
       10**-2,10**-1,10**0,10**1]) #I know its lame, but this has to be a numpy array  # X ticks

Xrotation=0                                                 # rotation of labels major ticks

XticksMinor=False                                           # modify Xminor tick locations?
XlocsMinor=np.logspace(-8,1,40)                             # Xminor locations

XMinorDetails             = ticks()                         # mod minor tick mark details
XMinorDetails.axis        = 'x'
XMinorDetails.which       = 'minor'
XMinorDetails.length      = 3
XMinorDetails.color       = 'k'
XMinorDetails.width       = 0.7
XMinorDetails.top         = 'on'
XMinorDetails.bottom      = 'on'
#XMinorDetails.Run         = False                          # For no minor tick modifications

XMajorDetails             = ticks()                         # mod major tick mark details
XMajorDetails.axis        = 'x'
XMajorDetails.labelsize   = 16
XMajorDetails.which       = 'major'
XMajorDetails.length      = 5
XMajorDetails.top         = 'on'
XMajorDetails.bottom      = 'on'
XMajorDetails.labelbottom = 'on'
#XMajorDetails.Run         = False                          # For no major tick modifications

###################################################################################################
######################################## Y axis ###################################################
###################################################################################################

ShowYLabels=False                                     # Show the y labels
Ylabel='MCNP $k_{eff}$ / Benchmark $k_{eff}$'        # Y label
YFontSize=18                                         # Y label font size
YFontWeight="normal"                                 # "bold" or "normal"
YScale="linear"                                      # 'linear' or 'log'
Ylimits=False                                         # Set Ylimits?
YLim=[0.96,1.03]                                     # Limits that will be set

YticksMajor=False                                     # Modify Y major ticks?
Ylabels=['0.96','0.97','0.98','0.99',  
         '1.00','1.01','1.02','1.03']                # Labels for Y major ticks
Ylocs=[0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03]      # Locations for labels of y
                                                     # major ticks

Yrotation=0                                          # rotation of labels major ticks

YticksMinor=False                                    # Modify Yminor tick locations?
YlocsMinor=np.arange(0.965,1.035,0.01)               # Ytick locations

YMinorDetails             = ticks()                  # mod minor tick mark details
YMinorDetails.axis        = 'y'
YMinorDetails.which       = 'minor'
YMinorDetails.length      = 3
YMinorDetails.color       = 'k'
YMinorDetails.width       = 0.7
YMinorDetails.left        = 'on'
YMinorDetails.right       = 'on'
#YMinorDetails.Run         = False                   # For no minor tick marks

YMajorDetails             = ticks()                  # mod major tick mark details
YMajorDetails.axis        = 'y'
YMajorDetails.labelsize   = 12
YMajorDetails.which       = 'major'
YMajorDetails.length      = 5
YMajorDetails.width       = 1
YMajorDetails.left        = 'on'
YMajorDetails.right       = 'on'
YMajorDetails.labelleft   = 'on'
#YMajorDetails.Run         = False                   # For nor major tick marks

###################################################################################################
######################################## Markers ##################################################
###################################################################################################

# These are some colors that I found that are distinct (the last two are repeats)
# For coloring the points on the plot, these colors will be used
# http://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
Colors=["aqua","gray","red","blue","black","green","magenta","indigo","lime","peru","steelblue",
        "darkorange","salmon","yellow","lime","black"]

# If you want to highlight a specific item, set its alpha value =1 and all others to 0.4
# You can also change the MarkSize (or just use the highlight option below)
Alpha_Value=[1  ,1  ,1  ,1  ,1  ,1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]
MarkSize=   [8  ,8  ,8  ,8  ,8  ,8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8]


Linewidth=[1  ,1  ,1  ,1  ,1  ,1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]

MarkerType=["8","s","p","D","*","H","h","d","^",">"] # Can change all these to "." or "" for nothing "x" isn't that good
                                                     # "*" "H" "h" "d" "^" ">" good ones
                                                     # http://matplotlib.org/1.4.1/api/markers_api.html for more options

# Set the line styles
# More options: http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D.set_linestyle
# LineStyles=["solid","dashed","dash_dot","dotted","."]
LineStyles=["."]


# Do not worry if you do not have enough values loaded in the above matricies (say if you have 20 groups
# but only 10 values in each array), the program will loop through these arrays. Same with too many values

#############################################################################################################
############################################# Functions #####################################################
############################################################################################################# 

def find_index(Filename,list1,ID):
    """
    This function will find the 'Filename' index match in list1. If an index is not 
    found then an error will print to the screen but the program will continue.
    """
    Count=0
    for file in list1:
        if fnmatch.fnmatch(file,Filename):
            index=Count
        Count=Count+1
    try :
         index
    except UnboundLocalError:
        print ("Hey Index was not defined for "+Filename+" in the list of "+ID+" files")
        index=1000000
    return(index)

def find_unique(list1):
    """
    This function will print out the unique values in the list1. The output is a list
    """
    for file in list1:
        check=0
        try:
            for values in unique_vals:
                if(file in values):
                    check=1
            if(check==0):
                unique_vals=np.append(unique_vals,file)
        except NameError:
            unique_vals=[file]
    return(unique_vals)

def cut_ends(list1):
    """
    This function will cut everything in list1 after a number? and store in list2
    """
    for i in list1:
        i2=i[4:len(i)] #I do this because of U233
        position=re.search("\d",i2).start()+3
        try:
            list2=np.append(list2,i[0:position])
        except NameError:
            list2=i[0:position]
    return(list2)

def loop_values(list1,index):
    """
    This function will loop through values in list even if outside range (in the positive sense not negative)
    """
    while True:
        try:
            list1[index]
            break
        except IndexError:
            index=index-len(list1)
    return(list1[index])

def loop_index(list1,index):
    """
    This function will loop through values in list and return non-outside range index
    """
    while True:
        try:
            list1[index]
            break
        except IndexError:
            index=index-len(list1)
    return(index)


def File_To_Plotable_Matrix(Directory,filename):
    """
    This function takes in a filename with its directory information and stores the contents
    of the file in a matrix. The file should have comma separated values.

    This function will then create an index array for the matrix
    """
    #Open file, and store information in list 'content' (each element in the list 'content' contains a line of 
    #of the file
    with open(Directory+filename) as f:
        content = f.readlines()

    #Loop over all the lines in the file (in content), and store values in 'array'
    for i in content:
        hold=np.array(i.split("\n")[0].split(","))
        try:
            array=np.append(array,hold,axis=0)
        except NameError:
            array=hold

    Rows=len(content)
    Cols=int(len(array)/Rows)

    array=np.reshape(array,(Rows,Cols))


    length=len(array[:,1]) #Determine number of lines in the file
    index=range(1,length) #create an index variable, subtract 1 because we are getting rid of the first
                            #row

    a=array[1:length,:] #save array in easier name, and cut off the first row

    return(a,index)

def cut_some_ends(list1):
    """
    This function will cut everything in list1 after a second set of numbers and store in list2
    """
    for i in list1:
        i2=i[4:len(i)] #I do this because of U233
        position=re.search("\d",i2).start()+3 #Position of last alpha before a number
        Position_end=position+1               #Position of first number
        Ending=i[Position_end:len(i)]         #End of the string
        Keep=Ending.split("-")[0]             #Keep only stuff before a dash (if there is one)
        try:
            list2=np.append(list2,i[0:position]+"-"+Keep)
        except NameError:
            list2=i[0:position]+"-"+Keep
    return(list2)

def count_digits(list1):
    """
    This function will count the number of digits in the list
    """
    c=0
    for string in list1:
        for i in string:
            if i.isdigit():
                c = c + 1
    return(c)

def Group_by_Parameter(Matrix,Column,Second):
    """
    This function will sort 'Matrix' by its column 'Column'
    It will also return unique names of that column (discounting ending numbers)
    and provide a string 'ranges' that provides information about grouping the Matrix
    """
    #Sort array based on the Column chosen
    index_sort=Matrix[:,Column].argsort()
    Matrix=Matrix[index_sort]
    
    #Check if Second is in the list (and find first and last instance of it)
    Second_In=False
    SecondIndexStart=0
    if Second!="None":
        for name in Matrix[:,Column]:  #Loop through list
            if Second in name:         #check if Second is in list
                Second_In=True         #If so we are okay
                break                  #Stop searching
            SecondIndexStart=SecondIndexStart+1 #Save the first index where we find Second

        #Find the last index where we find Second
        SecondIndexEnd=0      
        Found=False
        if Second_In:
            for name in Matrix[:,Column]:
                if Second in name and not Found:
                    Found=True
                if not Second in name and Found:
                    break
                SecondIndexEnd=SecondIndexEnd+1
            SecondIndexEnd=SecondIndexEnd-1

    if Second=="None":
        #Cut off the ends of file names
        if  count_digits(Matrix[:,Column]) > 1: 
            names=cut_ends(Matrix[:,Column])
        else:
            names=Matrix[:,Column]
        #Find unique names
        unique_names=find_unique(names)

        #Come up with a string 'ranges' that will help us plot everything according 
        #to groups, and split this string into a list
        unique_index=0
        names_index=0
        ranges="0-"
        for i in names:
            if (i not in unique_names[unique_index]):
                unique_index=unique_index+1
                ranges=ranges+str(names_index-1)+" : "+str(names_index)+"-"
            names_index=names_index+1

        ranges=ranges+str(len(names)-1)
        ranges=ranges.split(" : ")
    elif Second_In: #If we are only printing a single group
        #Cut off the ends of file names
        if  count_digits(Matrix[:,Column]) > 1: 
            names=cut_some_ends(Matrix[:,Column])
        else:
            names=Matrix[:,Column]
        #Find unique names
        unique_names=find_unique(names[SecondIndexStart:SecondIndexEnd])

        #Come up with a string 'ranges' that will help us plot everything according to
        #groups, and split this string into a list
        unique_index=0
        names_index=SecondIndexStart
        ranges=str(SecondIndexStart)+"-"
        for i in names[SecondIndexStart:SecondIndexEnd]:
            if (i not in unique_names[unique_index]):
                unique_index=unique_index+1
                ranges=ranges+str(names_index-1)+" : "+str(names_index)+"-"
            names_index=names_index+1
        ranges=ranges+str(SecondIndexEnd)
        ranges=ranges.split(" : ")
        
    else:
        print("Variable 'Group_by2' can't be found in the group 'Group_by'")
        quit()
    return(Matrix,unique_names,ranges)

def Count_Occurances(list1,event):
    """
    This function will count the number of occurances of "event" in "list1" assuming strings
    """
    counter=0
    for i in list1:
        if event in i:
            counter=counter+1
    return(counter)

def Convert_To_Float(list1):
    """
    This function will convert every item in list1 to a float value and return the same list in float
    """
    list2=[]
    for i in list1:
        try:
            list2=np.append(list2,float(i))
        except NameError:
            list2=[floast(i)]
    return(list2)

def Count_Occurances_Outside_Event(Groups,list1,center_value,STDList,NumberOfSTDs,GroupList):
    """
    This function will loop through list1, and determine the value in list1 is outside
    so many standard deviations from a center value. If that is the case, a count is added
    to Occurances, which count the number of occurances of this event, but groups these counts
    based off Groups and GroupList. Groups is all the unique values of GroupList. GroupList correspond
    to the groups associated for each item in list1. 
    """
    count=0
    Occurances=np.zeros(len(Groups))
    for k in list1:
        if abs(k-center_value) > NumberOfSTDs*STDList[count]:
           count2=0
           for l in Groups:
               if l == GroupList[count]:
                   Occurances[count2]=Occurances[count2]+1
               count2=count2+1
        count=count+1
    return(Occurances)

def DO_I_Plot(Nplots,Compare,STDcases):
    """
    This function determines whether or not to plot in a loop, I'm sorry I know this is complicated and studpid
    """
    if(  Nplots==1 and Compare==False and STDcases==1):
        Decision=True
    elif(Nplots==2 and Compare==True  and STDcases==1):
        Decision=True
    else:
        Decision=False

    return(Decision)

def findnth(haystack, needle, n):
    """
    This function will look through a string 'haystack' and find
    the 'n'th 'needle' and return its position
    """
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def update_columns_data(a,text):
    """
    This function takes in a dtype=U (strings) matrix 'a' and either:
        
        modifies a column in a
        or appends a column to the end of a

    The modification is described in the variable 'text' (example below):

    If: text =  "'2'='2'/10**6"

    Then this code will replace the second column of 'a' with:
      Each element of the second column of 'a' divided by 10**6

    If: text = "'3'='2'/10**6"

    Then the third column of 'a' will store:
      Each element of the second column of 'a' divided by 10**6

      If 'a' only has two columns, then a third will be appended
      If 'a' has three columns, the third column will be overwritten
      If 'a' has one column, this function will fail

    Rules:
      Apostrophes should be in pairs, else this will fail
      Text inbetween apostrophes should be integers, else this will fail
    """

    #Convert type to object to modify some of the strings
    a=a.astype('object')

    #Loop through string and find all the locations of 
    #the particular text (') (the apostrophe)
    for i in range(0,1000): #Thats over 9000!!!

        #Look for the ith occurance of text
        Current_Position=[findnth(text,"'",i)]

        #If there is no ith occurance, then Current_Position==-1
        #And we can stop looping
        if Current_Position[0]==-1:
            break

        #If there is an occurance add it to our list of Positions
        try:
            Positions=np.append(Positions,Current_Position)
        except NameError:
            Positions=Current_Position

    #Check if Positions is divisble by 2
    DivByTwo=len(Positions) % 2 == 0
    if not DivByTwo:
        print("Check modification equation, improper number of (') characters.")
        quit()

    #Check if whats between (') characters is an integer
    #Also save the integers
    for i in range(0,int(len(Positions)/2)):
        #Start and end positions for string
        Start=Positions[i*2]+1
        End=Positions[i*2+1]
        try:
            Integer=np.append(Integer,int(text[Start:End]))
        except ValueError:
            print("Check modification equation, improper string between (') characters (should be integer).")
            quit()
        except NameError:
            Integer=[int(text[Start:End])]

    #Check if first integer in text is too high (can only append one column at a time)
    if Integer[0] > len(a[0,:]):
        print("The value between the first set of (') characters is too large, should be no more than"\
              " len(a)")
        quit()



    #String of replaces
    for i in range(0,int(len(Positions)/2)):

        #Start and end positions for string (if this is the first occurance)
        Start=Positions[i*2]
        End=Positions[i*2+1]+1
        try:
            StringOfReplaces=np.append(StringOfReplaces,text[Start:End])
        except NameError:
            StringOfReplaces=text[Start:End]


    #Replace whats inbetween (') characters with 'Replacement' (XXXXX is changed to what was inbetween ('))
    Replacement="a[i,XXXXX]"
    for i in range(0,int(len(Positions)/2)):

        #Start and end positions for string (if this is the first occurance)
        Start=Positions[i*2]
        End=Positions[i*2+1]+1
        
        #If not first iteration, then positions will have shifted by
        #the length of 'Replacement'
        if i != 0:
            Positions[i*2]=Positions[i*2]+len(Replacement_)-(End-Start)
            Positions[i*2+1]=Positions[i*2+1]+len(Replacement_)-(End-Start)
            Start=Positions[i*2]
            End=Positions[i*2+1]+1

        #What needs to be replaced
        To_Replace=text[Start:End]

        #Update Replacement
        Replacement_=Replacement.replace("XXXXX",str(Integer[i]))

        #Make float if not first value
        if i != 0:
            Replacement_="float("+Replacement_+")"

        ### Use if some things are not workin
        To_Replace=StringOfReplaces[i]

        #Act of replacement
        text=text.replace(To_Replace,Replacement_,1)
        

####################################################################
####################################################################
    #Make the modification and save in a holdarray
    text_try="holdarray=np.vstack((holdarray,str("+text.split("=")[1]+")))"
    text_except="holdarray=str("+text.split("=")[1]+")"


    for i in range(0,len(a[:,0])):
        try:
            exec(text_try) in globals(),locals()
        except NameError:
            exec(text_except) in globals(),locals()

    #The exec command doesn't store holdarray in the proper namespace 
    #(because I am calling a function in this function (I think))
    #So I save variable in new name
    NewHold=locals()['holdarray']
    
    #Put into array in the proper place
    if Integer[0]==len(a[0,:]): #Append
        a=np.append(a,NewHold,1)
    else: #Replace
        a[:,Integer[0]]=NewHold[:,0]

    #Convert type back to readable stuff
    a=a.astype('U')
    return(a)


