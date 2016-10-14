#!/usr/bin/env python

#This script does not analyze benchmark yet. It does pull out information from the benchmarks, there is still
#quite a bit of work to do on this program


#############################################################################################################
############################################  Packages ######################################################
#############################################################################################################

import os #For OS system commands
import subprocess #For some other commands
from datetime import datetime #To time myself
import fnmatch #For wildcard matches
import numpy as np #Gathering the benchmark data
import re #check if there are any characters in find_ending, also for some regex matching

#Import functions
func=__import__("functions")

#############################################################################################################
############################################## Inputs  ######################################################
#############################################################################################################

startTime = datetime.now() #Timeing code, starting now

#Directories to search for output files
topdir="/users/pavelg/Inputs"
outputDir="/users/pavelg/Inputs_OUTPUT"
RunDir="/users/pavelg/RunDir"


#If there are files that cannot be found in Skips list, then the 'closest' names will be shown
#If you want to refine the list, increase this number to something like 10 (or less)
#If you want more names to be shown in the list change this number to something like 1
Debug=10


#############################################################################################################
############################################ Gather Data ####################################################
#############################################################################################################


####################################################################################
############################### Initial Information ################################
####################################################################################

#Lists of output files (In case I need em)
iFiles=func.List_files_sys(topdir,"*.i")
oFiles=func.List_files_sys(outputDir,"*.o")
mFiles=func.List_files_sys(outputDir,"*.m")
sFiles=func.List_files_sys(RunDir,"slurm*")

#Name of the output file (saved in the directory with all the slurm files)
filename_output="output.csv"

output=0
#check if output file exists
if(os.path.isfile(filename_output)):
    os.system("rm "+filename_output) #Delete
    output=0
if(output==0):
    file_out = open(filename_output,'w') #Open the output file
    #Write the heading to the file
    print("File Name,k-eff_o,std_o,therm fiss,int fiss,fast fiss,"\
          "above therm fiss, Avg E, Avg leth causing fiss",file=file_out)
if(output==1):
    file_out = open(filename_output,'a') #Open the output file





####################################################################################
############################ Loop over all files  ##################################
####################################################################################


number=range(0,len(oFiles))
#number=range(0,100)
#umber=range(500,502)
#umber=range(128,129)
#umber=range(925,950)
#number=range(68,69)

for one_file in number:
 
    filename=oFiles[one_file]
    
    #We are getting the input name (just the file name without the directory tree
    #or the extension
    input_name=filename.split("/")[-1]
    if len(filename.split("."))==3:
         input_name=input_name.split(".")[0]+"."+input_name.split(".")[1]
    else:
         input_name=input_name.split(".")[0]

    print(input_name +" " +str(one_file))



####################################################################################
#################################### k-eff #########################################
####################################################################################

    #K-eff from output file

    #line to look for
    special_line="the final estimated combined collision/absorption/track-length keff = "
    delete=["with an estimated standard deviation of","|"] #text to delete
    delim="[\s+]+" #Deliminator any number of spaces
    skip=0 #Number of lines to skip
    elements=[1,2] #These are the elements that you want to pull out of the line after manipulation
    k_eff=func.data_pull(filename,special_line,delete,skip,delim,elements) #k_eff[0]=k_eff;k_eff[1]=std


####################################################################################
############################## %Thermal Fission ####################################
########################### %Intermediate Fission ##################################
################################ %Fast Fission #####################################
####################################################################################

    #line to look for
    special_line="the percentages of fissions caused by neutrons in the thermal,"\
                 " intermediate, and fast neutron ranges"
    delete=["(<0.625 ev):","(0.625 ev - 100 kev):","(>100 kev):","%","|"]
    delim="[\s]+"
    skip=1
    elements=[1,2,3]
    percent_fiss=func.data_pull(filename,special_line,delete,skip,delim,elements) 
    percent_fiss=np.append(percent_fiss,[round(100-float(percent_fiss[0]),2)])

              # percent_fiss[0] = % thermal fission <0.625 ev
              # percent_fiss[1] = % intermediate fission 0.625 ev - 100 kev
              # percent_fiss[2] = % fast fission <100 kev
              # percent_fiss[3] = % Above thermal fission fraction >0.625 ev


####################################################################################
################### Average Energy of a Neutron Causing Fission, ev ################
####################################################################################

    special_line="the average neutron energy causing fission ="
    delete=["mev","|"]
    delim="[\s]+"
    skip=0
    elements=[1]

    Avg_E_fiss=func.data_pull(filename,special_line,delete,skip,delim,elements) 

    Avg_E_fiss=str(float(Avg_E_fiss[0])*1000000)

              # Avg_E_fiss = Average Energy in ev
              
####################################################################################
################# Average Lethargy of a neutron causing fission, ev ################
####################################################################################

    special_line="the energy corresponding to the average neutron lethargy causing"\
                 " fission ="
    delete=["mev","|"]
    delim="[\s]+"
    skip=0
    elements=[1]

    Avg_l_fiss=func.data_pull(filename,special_line,delete,skip,delim,elements) 
    Avg_l_fiss=str(float(Avg_l_fiss[0])*1000000)

 
              # Avg_l_fiss = Average Lethargy of a neutron causing fission in ev


####################################################################################
######################## Print info from Skip with outputs  ########################
####################################################################################
    

    if(input_name == "None"):
         print("None value for "+input_name+": input_name = "+input_name)
         continue
    if(k_eff[0] == "None"):
         print("None value for "+input_name+": k_eff     = "+k_eff[0])
         continue
    if(k_eff[1] == "None"):
         print("None value for "+input_name+": keff err = "+k_eff[1])
         continue
    if(percent_fiss[0] == "None"):
         print("None value for "+input_name+": Percent fiss0 = "+percent_fiss[0])
         continue
    if(percent_fiss[1] == "None"):
         print("None value for "+input_name+": Percent fiss1= "+percent_fiss[1])
         continue
    if(percent_fiss[2] == "None"):
         print("None value for "+input_name+": Percent fiss2= "+percent_fiss[2])
         continue
    if(percent_fiss[3] == "None"):
         print("None value for "+input_name+": Percent fiss3= "+percent_fiss[3])
         continue


####################################################################################
############################### Printing ###########################################
####################################################################################


    print(input_name+','+k_eff[0]+','+k_eff[1]+','+percent_fiss[0]+','
          +percent_fiss[1]+','+percent_fiss[2]+','+percent_fiss[3]+','
          +Avg_E_fiss+','+Avg_l_fiss,file=file_out)


#  array[:,0]  input name
#         1    k_eff[0]
#        2      k_eff[1]
#percent_fiss[0]
#percent_fiss[1]
#percent_fiss[2]
#percent_fiss[3]
#Avg_E_fiss
#Avg_l_fiss,file=file_out)

####################################################################################
######################### Quiting code and showing time ############################
####################################################################################
file_out.close
print (datetime.now() - startTime)
quit()
####################################################################################
####################################################################################
####################################################################################



