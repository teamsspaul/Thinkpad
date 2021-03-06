#!/usr/bin/env python

#This program will produce XY, histogram, and bar plots based on parameters provided
#in a python input deck provided on the command line (referred to as the 'parameters file').
#All of the current plotting options are explained in the file 'Defaults.py', which 
#contain default settings for the plotting program. 

#In the 'parameters file' a .csv file should be specified with the data for plotting.
#The first line should contain titles for each column and each value should be separated
#by commas. This program is tailored to divide columns 14 and 15 by 10^6 (just be aware).

import matplotlib.pyplot as plt
import numpy as np
import sys
from textwrap import wrap
import os
import matplotlib.mlab as mlab

#Take Plot Parameters from the command line
Plot_Variables=sys.argv[1]

#The Path to the input deck
if "/" in Plot_Variables:
    PathInput=Plot_Variables.split("/")
    print("Running Case "+Plot_Variables)
    PathInput=PathInput[0:len(PathInput)-1]
    PathInput="/".join(PathInput)
    cwd=os.getcwd()
    PathInput=cwd+"/"+PathInput
    sys.path.append(PathInput)

#If there is a .py extension in the input deck, delete it
if ".py" in Plot_Variables:
    Plot_Variables=Plot_Variables.split(".py")[0]
if "/" in Plot_Variables:
    Plot_Variables=Plot_Variables.split("/")[-1]


#Import default variables
var=__import__("Defaults")

#Overwrite defaults with specific plot parameters found in Plot_Variables
var.__dict__.update(__import__(Plot_Variables).__dict__)

#for the prop variable in legends
var.Lfont['size']=var.LegendFontSize
var.Lfont['weight']=var.LegendWeight


#############################################################################################################
############################################# Functions #####################################################
############################################################################################################# 

def class_ax_tick_params(class1,j):
    """
    This function takes in a class, and sets tick parameters with the information stored in the class
    """
    ax[j].tick_params(axis       = class1.axis,
                   labelsize     = class1.labelsize,
                   which         = class1.which,
                   length        = class1.length,
                   color         = class1.color,
                   labelcolor    = class1.labelcolor,
                   width         = class1.width,
                   left          = class1.left,
                   right         = class1.right,
                   top           = class1.top,
                   bottom        = class1.bottom,
                   labelleft     = class1.labelleft,
                   labelright    = class1.labelright,
                   labeltop      = class1.labeltop,
                   labelbottom   = class1.labelbottom)

def class_ax_grid(class1,j):
    """
    This takes in a class, and sets grid parameters with the information stored in the class.
    """
    ax[j].grid       (axis          = class1.axis,
                   which         = class1.which,
                   color         = class1.color,
                   alpha         = class1.alpha,
                   linestyle     = class1.linestyle,
                   linewidth     = class1.linewidth,
                   marker        = class1.marker,
                   markersize    = class1.markersize)

#############################################################################################################
############################################# Open File #####################################################
######################################### Store info in array ###############################################
#############################################################################################################

a,index=var.File_To_Plotable_Matrix(var.DataLocation,var.filename)

#      a[:,0] = File Name
#      a[:,1] = k-eff_o
#      a[:,2] = std_o
#      a[:,3] = k-eff__m
#      a[:,4] = std_m
#      a[:,5] = k-eff_bench
#      a[:,6] = std_bench
#      a[:,7] = k_normalized
#      a[:,8] = std_normalized
#      a[:,9] = geometry
#      a[:,10] = percent of fissions caused by thermal neutrons
#      a[:,11] = percent of fissions caused by intermediate neutrons
#      a[:,12] = percent of fissions caused by fast neutrons
#      a[:,13] = percent of fission casued by epi thermal neutrons
#      a[:,14] = the average neutron energy causing fission ev
#      a[:,15] = the average neutron lethargy causing fission ev

if var.Compare_Data:
    a_2,index_2=var.File_To_Plotable_Matrix(var.DataLocation,var.filename_2)

#############################################################################################################
######################################### Modify above array ################################################
############################################################################################################# 

for update in var.Updates:
    a=var.update_columns_data(a,update)

if var.Compare_Data:
    for update in var.Updates:
        a_2=var.update_columns_data(a_2,update)


#########################################################################################################
######################################### Preplotting  ##################################################
######################################################################################################### 

(a,unique_names,ranges)=var.Group_by_Parameter(a,var.Group_by,var.Group_by2)

if var.Compare_Data:
    (a_2,unique_names_2,ranges_2)=var.Group_by_Parameter(a_2,var.Group_by,var.Group_by2)


#############################################################################################################
############################################ Plot Settings ##################################################
############################################################################################################# 

#Set up figure 

fig = plt.figure(figsize = var.FigureSize)

if var.Center_Title and var.No_Title_Mod:
    fig.suptitle("\n".join(wrap(var.Title,60)),fontsize=var.TitleFontSize,fontweight=var.TitleFontWeight,fontdict=var.Tfont,ha='center')
if var.Center_Title and not var.No_Title_Mod:
    fig.suptitle("\n".join(wrap(var.Title,60)),fontsize=var.TitleFontSize,
                 fontweight=var.TitleFontWeight,fontdict=var.Tfont,ha='center',y=var.TitleYPosition)
if not var.Center_Title and not var.No_Title_Mod:
    fig.suptitle("\n".join(wrap(var.Title,60)),fontsize=var.TitleFontSize,
                 fontweight=var.TitleFontWeight,fontdict=var.Tfont,ha='center',
                 x=var.TitleXPosition,y=var.TitleYPosition)


if len(var.PlotSetup) > 1:
    ax = [fig.add_subplot(111)]    # The big subplot

    # Turn off axis lines and ticks of the big subplot
    ax[0].spines['top'].set_color('none')
    ax[0].spines['bottom'].set_color('none')
    ax[0].spines['left'].set_color('none')
    ax[0].spines['right'].set_color('none')
    ax[0].tick_params(labelcolor='w', top='off', bottom='off', left='off',
                      labelleft='off',labelright='off',labeltop='off',
                      labelbottom='off',right='off')

a_hold=a;ranges_hold=ranges;index_hold=index;unique_names_hold=unique_names
################################################################################################
############################# Start of var.PlotSetup loop ######################################
################################################################################################

for i in range(0,len(var.PlotSetup)):
    
    try:
        ax=np.append(ax,fig.add_subplot(var.PlotSetup[i]))
        j=i+1
    except NameError:
        ax=[fig.add_subplot(var.PlotSetup[i])]
        j=i

##################################################################################
##################################################################################
##################### To Turn off features in second graph #######################
##################### and to redefine variables ##################################
##################################################################################

    if i==0:
        A_Variable_That_I_Will_Never_Use=0
        if var.Title_subplot: #Set up subtitles and sub axis for plots
            ax[j].set_title(var.Title_subplot1,fontsize=var.TitleSFontSize,fontweight=var.TitleSFontWeight,
                            fontdict=var.tfont,ha='center')
        #Set things false for first graph
    if i==1: #Update variables for second graph
        a=a_2
        ranges=ranges_2
        index=index_2
        unique_names=unique_names_2
        if var.Title_subplot: #Set up subtitles and sub axis for plots
            ax[j].set_title(var.Title_subplot2,fontsize=var.TitleSFontSize,fontweight=var.TitleSFontWeight,
                            fontdict=var.tfont,ha='center')
        #Set things false for second graph
        var.XMajorDetails.labelbottom = 'off'
        #var.YMajorDetails.labelleft = 'off'


##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################


#############################################################################################################
############################################### Plotting ####################################################
############################################################################################################# 


########################################################################################
######################################## XY Plotting ###################################
########################################################################################

    check=0  #Index for unique_names and other stuff
    MaxMarker=max(var.MarkSize)
    MaxAlpha=max(var.Alpha_Value)
    for k in ranges:                              ############################
        start=int(k.split("-")[0])                ############################
        end=int(k.split("-")[1])                  ############################

        Cycle=False
        for omit in var.OmitCases:
            if omit in unique_names[check]:
                check=check+1
                Cycle=True
                break
        if Cycle:
            continue
        
        #If we are highlighting a specific item, reduce all others
        if var.Highlight and var.PlotType == "XY":
            IndexMarker=var.loop_index(var.MarkSize,check)
            IndexAlpha=var.loop_index(var.Alpha_Value,check)
            if var.HighlightCase not in unique_names[check]:
                var.MarkSize[IndexMarker]=MaxMarker*var.ReduceMarker
                var.Alpha_Value[IndexAlpha]=MaxAlpha*var.ReduceAlpha
            else:
                var.MarkSize[IndexMarker]=MaxMarker
                var.Alpha_Value[IndexAlpha]=MaxAlpha


        #Plot each set of points, if XValues == 1000, plot index numbers
        #If you want to plot a second y value
        if var.XValues != 1000 and var.PlotType == "XY" and var.Second_Y_Values and not var.ERRORBARS:
            ax[j].plot(a[start:end+1,var.XValues],a[start:end+1,var.YValues2],
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check)*0.5,
                       alpha=var.loop_values(var.Alpha_Value,check)*0.5,
                       label=unique_names[check],linewidth=var.Linewidth)
            #check=check+1
        elif var.PlotType == "XY" and var.Second_Y_Values and not var.ERRORBARS:
            ax[j].plot(index[start:end+1],a[start:end+1,var.YValues2],
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check)*0.5,
                       alpha=var.loop_values(var.Alpha_Value,check)*0.5,
                       label=unique_names[check],linewidth=var.Linewidth)
            #check=check+1

        #Plot each set of points, if XValues == 1000, plot index numbers
        if var.XValues != 1000 and var.PlotType == "XY" and not var.ERRORBARS:
            ax[j].plot(a[start:end+1,var.XValues],a[start:end+1,var.YValues],
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check),
                       alpha=var.loop_values(var.Alpha_Value,check),
                       label=unique_names[check],linewidth=var.Linewidth)
            check=check+1
        elif var.PlotType == "XY" and not var.ERRORBARS:
            ax[j].plot(index[start:end+1],a[start:end+1,var.YValues],
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check),
                       alpha=var.loop_values(var.Alpha_Value,check),
                       label=unique_names[check],linewidth=var.Linewidth)
            check=check+1



############################################################################
####################    IF Error Bars #####################################
############################################################################
        if var.XValues != 1000:
            PLOTX=var.Convert_To_Float(a[start:end+1,var.XValues])
        PLOTY=var.Convert_To_Float(a[start:end+1,var.YValues])
        PLOTY2=var.Convert_To_Float(a[start:end+1,var.YValues2])
        try:
            yErr=var.Convert_To_Float(a[start:end+1,var.YERROR])
        except TypeError:
            yErr=None
        try:
            xErr=var.Convert_To_Float(a[start:end+1,var.XERROR])
        except TypeError:
            xErr=None

        #Plot each set of points, if XValues == 1000, plot index numbers
        #If you want to plot a second y value
        if var.XValues != 1000 and var.PlotType == "XY" and var.Second_Y_Values and var.ERRORBARS:
            ax[j].errorbar(PLOTX,PLOTY2,
                       yerr=yErr,xerr=xErr,
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check)*0.5,
                       alpha=var.loop_values(var.Alpha_Value,check)*0.5,
                       label=unique_names[check],linewidth=var.Linewidth)
            #check=check+1
        elif var.PlotType == "XY" and var.Second_Y_Values and var.ERRORBARS:
            ax[j].errorbar(index[start:end+1],PLOTY2,
                       yerr=yErr,xerr=xErr,
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check)*0.5,
                       alpha=var.loop_values(var.Alpha_Value,check)*0.5,
                       label=unique_names[check],linewidth=var.Linewidth)
            #check=check+1

        #Plot each set of points, if XValues == 1000, plot index numbers
        if var.XValues != 1000 and var.PlotType == "XY" and var.ERRORBARS:
            ax[j].errorbar(PLOTX,PLOTY,
                       yerr=yErr,xerr=xErr,
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check),
                       alpha=var.loop_values(var.Alpha_Value,check),
                       label=unique_names[check],linewidth=var.Linewidth)
            check=check+1
        elif var.PlotType == "XY" and var.ERRORBARS:
            ax[j].errorbar(index[start:end+1],PLOTY,
                       yerr=yErr,xerr=xErr,
                       linestyle=var.loop_values(var.LineStyles,check),
                       marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       markersize=var.loop_values(var.MarkSize,check),
                       alpha=var.loop_values(var.Alpha_Value,check),
                       label=unique_names[check],linewidth=var.Linewidth)
            check=check+1


############################################################################
####################    Fill Between #####################################
############################################################################

        #Plot each set of points, if XValues == 1000, plot index numbers
        #If you want to plot a second y value
        if var.XValues != 1000 and var.PlotType == "XY" and var.Second_Y_Values and var.ERRORFILL:
            check=check-1
            ax[j].fill_between(PLOTX,PLOTY2-yErr,PLOTY2+yErr,
                       #linestyle=var.loop_values(var.LineStyles,check),
                       #marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       #markersize=var.loop_values(var.MarkSize,check)*0.5,
                       alpha=var.loop_values(var.Alpha_ValueE,check)*0.5)#,
                       #label=unique_names[check],linewidth=var.Linewidth)
            #check=check+1
            check=check+1
        elif var.PlotType == "XY" and var.Second_Y_Values and var.ERRORFILL:
            check=check-1
            ax[j].fill_between(index[start:end+1],PLOTY2-yErr,PLOTY2+yErr,
                       #linestyle=var.loop_values(var.LineStyles,check),
                       #marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       #markersize=var.loop_values(var.MarkSize,check)*0.5,
                       alpha=var.loop_values(var.Alpha_ValueE,check)*0.5)#,
                       #label=unique_names[check],linewidth=var.Linewidth)
            #check=check+1
            check=check+1
        #Plot each set of points, if XValues == 1000, plot index numbers
        if var.XValues != 1000 and var.PlotType == "XY" and var.ERRORFILL:
            check=check-1
            ax[j].fill_between(PLOTX,PLOTY-yErr,PLOTY+yErr,
                       #linestyle=var.loop_values(var.LineStyles,check),
                       #marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       #markersize=var.loop_values(var.MarkSize,check),
                       alpha=var.loop_values(var.Alpha_ValueE,check))#,
                       #label=unique_names[check],linewidth=var.Linewidth)
            check=check+1
        elif var.PlotType == "XY" and var.ERRORFILL:
            check=check-1
            ax[j].fill_between(index[start:end+1],PLOTY-yErr,PLOTY+yErr,
                       #linestyle=var.loop_values(var.LineStyles,check),
                       #marker=var.loop_values(var.MarkerType,check),
                       color=var.loop_values(var.Colors,check),
                       #markersize=var.loop_values(var.MarkSize,check),
                       alpha=var.loop_values(var.Alpha_ValueE,check))#,
                       #label=unique_names[check],linewidth=var.Linewidth)
            check=check+1






########################################################################################
################################# Bar or Hist Plotting #################################
########################################################################################
        
    
    if var.PlotType == "Hist" or var.PlotType == "Bar":

        a3=var.Convert_To_Float(a[:,var.XValues])   #Convert data from string to float

        if var.PlotType == "Hist":
            ax[j].hist(a3,var.numBins,color=var.HistColor,alpha=var.HistAlpha,edgecolor=var.HistEdgeColor)

        if var.GaussFit:
            mean=np.mean(a3)
            variance=np.var(a3)
            sigma=np.sqrt(variance)

            PLOTXX=np.linspace(min(a3),max(a3),100)
            ax[j].plot(PLOTXX,mlab.normpdf(PLOTXX,mean,sigma),
                       linestyle=var.GaussStyle,
                       marker=var.GaussMarker,
                       color=var.GaussColor,
                       markersize=var.Gaussmarkersize,
                       alpha=var.GaussAlpha,
                       linewidth=var.GaussLineWidth)
            Textstr="Mean = "+str(round(mean,4))+"\n"+"$\sigma$ = "+str(round(sigma,4))
                    
            ax[j].text(var.HISTTIMEX,var.HISTTIMEY,
                       Textstr,transform=ax[j].transAxes,
                       fontsize=var.LegendFontSize,
                       verticalalignment=var.HISTalign,
                       bbox=var.HISTprops,
                       fontweight=var.LegendWeight,fontdict=var.font)




            #I do try: Textstr so that we do the following once
            try:
                Textstr
            except NameError:
            #Use for time plots
            #This is for additional information, currently finding percentages 
            #of values that are less than 10, 20,30, and 40.
                asum=[0,0,0,0,0]
                for value in a3:
                    if value < 10:
                        asum[0]=asum[0]+1
                    if value < 20:
                        asum[1]=asum[1]+1
                    if value < 30:
                        asum[2]=asum[2]+1
                    if value < 40:
                        asum[3]=asum[3]+1
                    asum[4]=asum[4]+1

                asum[0]=round((asum[0]/asum[4])*100)
                asum[1]=round((asum[1]/asum[4])*100)
                asum[2]=round((asum[2]/asum[4])*100)
                asum[3]=round((asum[3]/asum[4])*100)
            
                Textstr=str(asum[0])+"% less than 10 mins\n"+str(asum[1])+"% less than 20 mins\n"+\
                        str(asum[2])+"% less than 30 mins\n"+str(asum[3])+"% less than 40 mins"
                    
                if var.HISTTEXTTIME:
                    ax[j].text(var.HISTTIMEX,var.HISTTIMEY,
                               Textstr,transform=ax[j].transAxes,
                               fontsize=var.LegendFontSize,
                               verticalalignment=var.HISTalign,
                               bbox=var.HISTprops,
                               fontweight=var.LegendWeight,fontdict=var.font)

        if var.PlotType == "Bar":

            a4=var.Convert_To_Float(a[:,var.STD_COMPARE])
            
            if i==0:
                Means=var.Count_Occurances_Outside_Event(unique_names,a3,var.STD_Expected,
                                                         a4,var.NumberOfSTDs[0],a[:,var.Group_by])
            else:
                HOLD=var.Count_Occurances_Outside_Event(unique_names,a3,var.STD_Expected,
                                                        a4,var.NumberOfSTDs[0],a[:,var.Group_by])
                Means=np.vstack([Means,HOLD])

            #Determine the number of each instances of each unique_name
            Unique_Counts=np.zeros(len(unique_names))
            for k in range(0,len(unique_names)):
                Unique_Counts[k]=var.Count_Occurances(a[:,var.Group_by],unique_names[k])

            #Divide "Means" by total (gives a percentage)
            try:
                for k in range(0,len(unique_names)):
                    Means[i,k]=Means[i,k]/Unique_Counts[k]
            except IndexError:
                for k in range(0,len(unique_names)):
                    Means[k]=Means[k]/Unique_Counts[k]
                    
            
            #change labels and locations for the bar graph
            for k in range(0,len(unique_names)):
                var.Xlabels[k]=unique_names[k]+"\n("+str(int(Unique_Counts[k]))+")"

            step=var.Width*2+var.HalfBarWidth
            var.Xlocs=np.arange(var.HalfBarWidth,(step)*len(unique_names)+var.HalfBarWidth,step)

            #Plot the data if we are doing that now
            doiplot=var.DO_I_Plot(len(var.PlotSetup),var.Compare_Data,len(var.NumberOfSTDs))
            if doiplot:
                var.Xlocs=np.arange(len(unique_names))
                try:
                    ax[j].bar(var.Xlocs,Means[i,:],var.Width,color=var.BarColor[0])
                except IndexError:
                    ax[j].bar(var.Xlocs,Means[:],var.Width,color=var.BarColor[0])

                #Plot a vertical line indicating something important
                if var.Compare_B:
                    XSpace=np.linspace(var.XLim[0],var.XLim[1],25)
                    #the 0.32, 0.05, and 0.01 correspond to the 65% 95% and 99% confidence intervals
                    if var.NumberOfSTDs[0]==1:
                        ax[j].plot(XSpace,np.ones(len(XSpace))*0.32,color=var.Compare_Bar,
                               linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)
                    if var.NumberOfSTDs[0]==2:
                        ax[j].plot(XSpace,np.ones(len(XSpace))*0.05,color=var.Compare_Bar,
                               linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)
                    if var.NumberOfSTDs[0]==3:
                        ax[j].plot(XSpace,np.ones(len(XSpace))*0.01,color=var.Compare_Bar,
                               linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)

########################################################################################################
#################################### Setting up details of the plot ####################################
########################################################################################################


    #Set up the x and y labels
    if len(var.PlotSetup) != 1:
        if var.ShowXLabels:
            #ax[0].set_xlabel(var.Xlabel,fontsize=var.XFontSize,fontweight=var.XFontWeight,fontdict=var.font)
            ax[0].set_xlabel("\n".join(wrap(var.Xlabel,60)),
                             fontsize=var.XFontSize,fontweight=var.XFontWeight,fontdict=var.font)
            ax[0].xaxis.labelpad=var.LPX
            #ax.xaxis.set_label_coords(0,10)
        if var.ShowYLabels:
            #ax[0].set_ylabel(var.Ylabel,fontsize=var.YFontSize,fontweight=var.YFontWeight,fontdict=var.font)
            ax[0].set_ylabel("\n".join(wrap(var.Ylabel,60)),
                             fontsize=var.YFontSize,fontweight=var.YFontWeight,fontdict=var.font)
            ax[0].yaxis.labelpad=var.LPY
            #ax.yaxis.set_label_coords(.3,-.1)
    if len(var.PlotSetup) == 1 and var.Center_On_Graph or not var.legend:
        if var.ShowXLabels:
            #ax[0].set_xlabel(var.Xlabel,fontsize=var.XFontSize,fontweight=var.XFontWeight,fontdict=var.font)
            ax[0].set_xlabel("\n".join(wrap(var.Xlabel,60)),
                             fontsize=var.XFontSize,fontweight=var.XFontWeight,fontdict=var.font)
            ax[0].xaxis.labelpad=var.LPX
            #ax.xaxis.set_label_coords(0,10)
        if var.ShowYLabels:
            #ax[0].set_ylabel(var.Ylabel,fontsize=var.YFontSize,fontweight=var.YFontWeight,fontdict=var.font)
            ax[0].set_ylabel("\n".join(wrap(var.Ylabel,60)),
                             fontsize=var.YFontSize,fontweight=var.YFontWeight,fontdict=var.font)
            ax[0].yaxis.labelpad=var.LPY
            #ax.yaxis.set_label_coords(.3,-.1)



    #Log or linear scale?
    ax[j].set_xscale(var.XScale)
    ax[j].set_yscale(var.YScale)

    #Set up axis ticks
    if var.YticksMajor:
        ax[j].set_yticks(var.Ylocs)
        ax[j].set_yticklabels(var.Ylabels,rotation=var.Yrotation,fontdict=var.font)
    if var.YticksMinor:
        ax[j].set_yticks(var.YlocsMinor,minor=True)
    if var.XticksMajor:
        ax[j].set_xticks(var.Xlocs+var.HalfBarWidth)
        ax[j].set_xticklabels(var.Xlabels,rotation=var.Xrotation,fontdict=var.font)
    if var.XticksMinor:
        ax[j].set_xticks(var.XlocsMinor,minor=True)

    #Set up details of tick marks                      
    if var.YMinorDetails.Run:
        class_ax_tick_params(var.YMinorDetails,j) #Calls a function "class_ax_tick_params" -> passes class "YMinorDetails
    if var.YMajorDetails.Run:
        class_ax_tick_params(var.YMajorDetails,j)
    if var.XMinorDetails.Run:
        class_ax_tick_params(var.XMinorDetails,j)
    if var.XMajorDetails.Run:
        class_ax_tick_params(var.XMajorDetails,j)


    #Set up grid lines
    if var.GridXMinor.Run:
        class_ax_grid(var.GridXMinor,j)
    if var.GridYMinor.Run:
        class_ax_grid(var.GridYMajor,j)
    if var.GridXMajor.Run:
        class_ax_grid(var.GridXMajor,j)
    if var.GridYMajor.Run:
        class_ax_grid(var.GridYMajor,j)

    #Sets up limits of graphs
    if var.Xlimits:
            ax[j].set_xlim(var.XLim[0],var.XLim[1])
    if var.Ylimits:
        ax[j].set_ylim(var.YLim[0],var.YLim[1])



########################################################################################
################################# Legend ###############################################
########################################################################################

    #http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
    if var.legend and var.SS==1:
        box=ax[j].get_position()
        ax[j].set_position([box.x0, box.y0, box.width*var.SquishGraph, box.height])
        handles,labels = ax[j].get_legend_handles_labels()
    if var.legend and var.SS==2:
        box=ax[j].get_position()
        ax[j].set_position([box.x0, box.y0, box.width, box.height*var.SquishGraph])
        handles,labels = ax[j].get_legend_handles_labels()

################################################################################################
############################# End of loop over var.PlotSetup ###################################
################################################################################################

if var.legend and var.Center_On_Graph and var.SS==1:
    box=ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width*var.SquishGraph, box.height])
    ax[0].legend(handles,labels,loc='center left', bbox_to_anchor=(var.BBOXX,var.BBOXY),
                 fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)
    
if var.legend and var.Center_On_Graph and var.SS==2:
    box=ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width, box.height*var.SquishGraph])
    ax[0].legend(handles,labels,loc='center', bbox_to_anchor=(var.BBOXX,var.BBOXY),
                 fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)
    
if var.legend and not var.Center_On_Graph and len(var.PlotSetup) > 1 and var.SS==1:
    ax[0].legend(handles,labels,loc='center right',fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)

if var.legend and not var.Center_On_Graph and len(var.PlotSetup) > 1 and var.SS==2:
    ax[0].legend(handles,labels,loc='center right',fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)


if var.legend and not var.Center_On_Graph and len(var.PlotSetup) == 1 and var.SS==1:
    box=ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width*var.SquishGraph, box.height])
    ax[0].legend(handles,labels,loc='center left', bbox_to_anchor=(var.BBOXX,var.BBOXY),
                 fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)
    fig.text(var.LPXX,var.LPXY,var.Xlabel,ha='center',fontsize=var.XFontSize,fontweight=var.XFontWeight,fontdict=var.font)
    fig.text(var.LPYX,var.LPYY,var.Ylabel,va='center',rotation='vertical',fontsize=var.YFontSize,fontweight=var.YFontWeight,fontdict=var.font)

if var.legend and not var.Center_On_Graph and len(var.PlotSetup) == 1 and var.SS==2:
    box=ax[0].get_position()
    ax[0].set_position([box.x0, box.y0, box.width, box.height*var.SquishGraph])
    ax[0].legend(handles,labels,loc='center', bbox_to_anchor=(var.BBOXX,var.BBOXY),
                 fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)

    fig.text(var.LPXX,var.LPXY,var.Xlabel,ha='center',fontsize=var.XFontSize,fontweight=var.XFontWeight,fontdict=var.font)
    fig.text(var.LPYX,var.LPYY,var.Ylabel,va='center',rotation='vertical',fontsize=var.YFontSize,fontweight=var.YFontWeight,fontdict=var.font)



########################################################################################
################################# Bar Plotting Part Two ################################
########################################################################################


try:
    if not doiplot:
        a=a_hold;ranges=ranges_hold;index=index_hold;unique_names=unique_names_hold
        Nplots=len(var.PlotSetup);Compare=var.Compare_Data;STDcases=len(var.NumberOfSTDs)
        if(Nplots==1 and Compare==False and STDcases>1):
            print("I aplogize but I do not want to plot this right now, need to cycle through STDcases")
        elif(Nplots==1 and Compare==True and STDcases==1):
            print("Plotting the two cases on the same bar graph")
            #From pre loop
            a_2,index_2=var.File_To_Plotable_Matrix(var.DataLocation,var.filename_2)
            (a_2,unique_names_2,ranges_2)=var.Group_by_Parameter(a_2,var.Group_by,var.Group_by2)
            #from inside loop
            a=a_2
            ranges=ranges_2
            index=index_2
            unique_names=unique_names_2
            #From bar section inside loop
            a3=var.Convert_To_Float(a[:,var.XValues])   #Convert data from string to float
            a4=var.Convert_To_Float(a[:,var.STD_COMPARE])
            HOLD=var.Count_Occurances_Outside_Event(unique_names,a3,var.STD_Expected,
                                                    a4,var.NumberOfSTDs[0],a[:,var.Group_by])
            Means=np.vstack([Means,HOLD])
            #Determine the number of each instances of each unique_name
            Unique_Counts=np.zeros(len(unique_names))
            for k in range(0,len(unique_names)):
                Unique_Counts[k]=var.Count_Occurances(a[:,var.Group_by],unique_names[k])
                Means[1,k]=Means[1,k]/Unique_Counts[k]

            #change labels and locations for the bar graph
                var.Xlabels[k]=unique_names+"\n("+str(int(Unique_Counts[k]))+")"
            step=var.Width*2+var.HalfBarWidth
            var.Xlocs=np.arange(0,(step)*len(unique_names),step)
            Xlocs2=np.arange(var.Width,(step)*len(unique_names)+var.Width,step)
            #Plot Twice
            ax[0].bar(var.Xlocs,Means[0,:],var.Width,color=var.BarColor[0],label=var.Title_subplot1)
            ax[0].bar(Xlocs2,
                      Means[1,:],var.Width,color=var.BarColor[1],label=var.Title_subplot2)
            
            if var.Compare_B:
                XSpace=np.linspace(var.XLim[0],var.XLim[1],var.NumberOfPointsBar)
                #the 0.32, 0.05, and 0.01 correspond to the 65% 95% and 99% confidence intervals
                if var.NumberOfSTDs[0]==1:
                    ax[0].plot(XSpace,np.ones(len(XSpace))*0.32,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)
                if var.NumberOfSTDs[0]==2:
                    
                    ax[0].plot(XSpace,np.ones(len(XSpace))*0.05,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)

                if var.NumberOfSTDs[0]==3:
                    ax[0].plot(XSpace,np.ones(len(XSpace))*0.01,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)


            (handles,labels) = ax[0].get_legend_handles_labels()
            ax[0].legend(handles,labels,loc='best',
                 fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)

        elif(Nplots==2 and Compare==False and STDcases==2):
            print("I aplogize but no, cycle through STD cases")
        elif(Nplots==2 and Compare==True and STDcases==2):
            print("Plotting two cases two different standard deviation distances for two benchmark extensions")

            for i in range(0,len(var.PlotSetup)):

                j=i+1
    
                if i==1:
                    a=a_2
                    ranges=ranges_2
                    index=index_2
                    unique_names=unique_names_2
 

                a3=var.Convert_To_Float(a[:,var.XValues])   #Convert data from string to float
                a4=var.Convert_To_Float(a[:,var.STD_COMPARE])
                HOLD=var.Count_Occurances_Outside_Event(unique_names,a3,var.STD_Expected,
                                                        a4,var.NumberOfSTDs[1],a[:,var.Group_by])
                Means=np.vstack([Means,HOLD])
                #Determine the number of each instances of each unique_name
                Unique_Counts=np.zeros(len(unique_names))

                for k in range(0,len(unique_names)):
                    Unique_Counts[k]=var.Count_Occurances(a[:,var.Group_by],unique_names[k])
                    Means[i+2,k]=Means[i+2,k]/Unique_Counts[k]

            
            #change labels and locations for the bar graph
            var.Xlabels=unique_names
            step=var.Width*2+var.HalfBarWidth
            var.Xlocs=np.arange(0,(step)*len(unique_names),step)
            Xlocs2=np.arange(var.Width,(step)*len(unique_names)+var.Width,step)
            #Plot Twice
            ax[1].bar(var.Xlocs,Means[0,:],var.Width,color=var.BarColor[0],label=var.Title_subplot1)
            ax[1].bar(Xlocs2,
                      Means[1,:],var.Width,color=var.BarColor[1],label=var.Title_subplot2)

            ax[2].bar(var.Xlocs,Means[2,:],var.Width,color=var.BarColor[0],label=var.Title_subplot1)
            ax[2].bar(Xlocs2,
                      Means[3,:],var.Width,color=var.BarColor[1],label=var.Title_subplot2)


            if var.Compare_B:
                XSpace=np.linspace(var.XLim[0],var.XLim[1],var.NumberOfPointsBar)
                #the 0.32, 0.05, and 0.01 correspond to the 65% 95% and 99% confidence intervals
                if var.NumberOfSTDs[0]==1:
                    ax[1].plot(XSpace,np.ones(len(XSpace))*0.32,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)
                if var.NumberOfSTDs[0]==2:
                    
                    ax[1].plot(XSpace,np.ones(len(XSpace))*0.05,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)

                if var.NumberOfSTDs[0]==3:
                    ax[1].plot(XSpace,np.ones(len(XSpace))*0.01,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)


            if var.Compare_B:
                XSpace=np.linspace(var.XLim[0],var.XLim[1],var.NumberOfPointsBar)
                #the 0.32, 0.05, and 0.01 correspond to the 65% 95% and 99% confidence intervals
                if var.NumberOfSTDs[1]==1:
                    ax[2].plot(XSpace,np.ones(len(XSpace))*0.32,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)
                if var.NumberOfSTDs[1]==2:
                    
                    ax[2].plot(XSpace,np.ones(len(XSpace))*0.05,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)

                if var.NumberOfSTDs[1]==3:
                    ax[2].plot(XSpace,np.ones(len(XSpace))*0.01,color=var.Compare_Bar,
                           linestyle=var.C_BarLine,alpha=var.C_BarAlpha,linewidth=var.C_linewidth)


            ax[1].set_ylabel(str(var.NumberOfSTDs[0])+" standard deviation" ,
                             fontsize=var.YFontSize,fontweight=var.YFontWeight,
                             fontdict=var.font)
            ax[2].set_ylabel(str(var.NumberOfSTDs[1])+" standard deviation" ,
                             fontsize=var.YFontSize,fontweight=var.YFontWeight,
                             fontdict=var.font)


            (handles,labels) = ax[2].get_legend_handles_labels()
            ax[2].legend(handles,labels,loc='best',
                 fontsize=var.LegendFontSize,prop=var.Lfont,ncol=var.NumberOfLegendColumns)


        else:
            print("Not working on plotting this case, don't care")

except NameError:
    ItIsNotMeantToBeee=1

       
#############################################################################################################
############################################ Save or Plot ###################################################
############################################################################################################# 


if var.Tightlayout:
    plt.tight_layout(pad=1,w_pad=1,h_pad=1.0)
if var.Extend_Bottom:
    plt.gcf().subplots_adjust(bottom=var.How_Extend_Bottom)

if var.ShowFig:
    plt.show()
elif var.SaveFig:
    plt.savefig(var.OutputDir+var.SaveFigName,bbox_inches='tight')



