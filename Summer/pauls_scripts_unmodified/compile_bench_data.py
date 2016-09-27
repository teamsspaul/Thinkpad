#!/usr/bin/env python

#This script does not analyze benchmark yet. It does pull out information from the benchmarks, there is still
#quite a bit of work to do on this program


#############################################################################################################
############################################  Packages ######################################################
#############################################################################################################

from mcnptools import Mctal, MctalKcode #To parse the mctal file
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
topdir="/lustre/scratch3/yellow/paulmmendoza/BM"
outputDir="/lustre/scratch3/yellow/paulmmendoza/BM_OUTPUT_80c"
RunDir="/yellow/users/paulmmendoza/project/Run_BM_80c"


#If there are files that cannot be found in Skips list, then the 'closest' names will be shown
#If you want to refine the list, increase this number to something like 10 (or less)
#If you want more names to be shown in the list change this number to something like 1
Debug=10


#############################################################################################################
############################################ Gather Data ####################################################
#############################################################################################################

####################################################################################
####################### Static Benchmark Information ###############################
####################################################################################

#This is the directory where a file called Info.xlsx is stored
#Info.xlsx should have the information described below
#separated by commas
BenchmarkInfoDir="/yellow/users/paulmmendoza/project/Backup/Benchmark_Info/"

#Open Info.xlsx and store each line as a string
#'content[1]' contains the first line, 'content[2]' the second, and so on
with open(BenchmarkInfoDir+'output.csv') as f:
     content = f.readlines()

#Store in 'array' a list of the first line
array=np.array(content[0].split("\n")[0].split(","))
counter=0
for i in content:
     counter=counter+1
     if (counter==1):
         continue
     hold=np.array(i.split("\n")[0].split(","))
     array=np.append(array,hold,axis=0)

Rows=len(content)
Cols=int(len(array)/Rows)

array=np.reshape(array,(Rows,Cols))

#  array[:,0 ]  Has first benchmark names
#  array[:,1 ]  Has the keff value for the benchmark
#  array[:,2 ]  Has the uncertainty for the keff value
#  array[:,3 ]  Has information abarray the geometry
#  array[:,4 ]  Has information abarray the reflector
#  array[:,5 ]  Has information abarray the moderator
#  array[:,6 ]  Has information abarray a secondary reflector
#  array[:,7 ]  Has information abarray a secondary moderator
#  array[:,8 ]  Has comments 
#  array[:,9 ]  Has lab info
#  array[:,10]  Ratio of Vfuel/Vh
#  array[:,11]  Ratio VH/Vfuel
#  array[:,12]  Unit cell hydrogen water number density over U235 unit cell number 
#               density
#  array[:,13]  Fuel Pellet Radius
#  array[:,14]  Fuel Rod Radius  
#  array[:,15]  Lattice unit cell pitch, cm
#  array[:,16]  Information on unit cell geometry
#  array[:,17]  Unit cell water number density
#  array[:,18]  Unit cell U235 number density   

################## Please note that everything below here is subject to change
################## If the isotopes gathered in 'format_static_bench_info.py'
################## were changed than these numbers will be shifted around

#  array[:,19]  Fuel Atom Density
#  array[:,20]  Fuel Volume
#  array[:,21]  Fiss Atom Density
#  array[:,22]  Fiss Volume
#  array[:,23]  92233 Atom Density
#  array[:,24]  92233 Volume
#  array[:,25]  92235 Atom Density
#  array[:,26]  92235 Volume
#  array[:,27]  94239 Atom Density
#  array[:,28]  94239 Volume
#  array[:,29]  94241 Atom Density
#  array[:,30]  94241 Volume
#  array[:,31]  Fertile Atom Density
#  array[:,32]  Fertile Volume
#  array[:,33]  90232 Atom Density
#  array[:,34]  90232 Volume
#  array[:,35]  92232 Atom Density
#  array[:,36]  92232 Volume
#  array[:,37]  92234 Atom Density
#  array[:,38]  92234 Volume
#  array[:,39]  92236 Atom Density
#  array[:,40]  92236 Volume
#  array[:,41]  92238 Atom Density
#  array[:,42]  92238 Volume
#  array[:,43]  94238 Atom Density
#  array[:,44]  94238 Volume
#  array[:,45]  94240 Atom Density
#  array[:,46]  94240 Volume
#  array[:,47]  95241 Atom Density
#  array[:,48]  95241 Volume
#  array[:,49]  Moderator Atom Density
#  array[:,50]  Moderator Volume
#  array[:,51]  1001 Atom Density
#  array[:,52]  1001 Volume
#  array[:,53]  1002 Atom Density
#  array[:,54]  1002 Volume
#  array[:,55]  1003 Atom Density
#  array[:,56]  1003 Volume
#  array[:,57]  6000 Atom Density
#  array[:,58]  6000 Volume
#  array[:,59]  6012 Atom Density
#  array[:,60]  6012 Volume
#  array[:,61]  6013 Atom Density
#  array[:,62]  6013 Volume
#  array[:,63]  4009 Atom Density
#  array[:,64]  4009 Volume
#  array[:,65]  26054 Atom Density
#  array[:,66]  26054 Volume
#  array[:,67]  26056 Atom Density
#  array[:,68]  26056 Volume
#  array[:,69]  26057 Atom Density
#  array[:,70]  26057 Volume
#  array[:,71]  26058 Atom Density
#  array[:,72]  26058 Volume
#  array[:,73]  26000 Atom Density
#  array[:,74]  26000 Volume
#  array[:,75]  Poison Atom Density
#  array[:,76]  Poison Volume
#  array[:,77]  5010 Atom Density
#  array[:,78]  5010 Volume
#  array[:,79]  5011 Atom Density
#  array[:,80]  5011 Volume
#  array[:,81]  2003 Atom Density
#  array[:,82]  2003 Volume
#  array[:,83]  48111 Atom Density
#  array[:,84]  48111 Volume
#  array[:,85]  48113 Atom Density
#  array[:,86]  48113 Volume
#  array[:,87]  64154 Atom Density
#  array[:,88]  64154 Volume
#  array[:,89]  64155 Atom Density
#  array[:,90]  64155 Volume
#  array[:,91]  64156 Atom Density
#  array[:,92]  64156 Volume
#  array[:,93]  64157 Atom Density
#  array[:,94]  64157 Volume
#  array[:,95]  64158 Atom Density
#  array[:,96]  64158 Volume
#  array[:,97]  4009 Atom Density
#  array[:,98]  4009 Volume
#  array[:,99]  3006 Atom Density
#  array[:,100]  3006 Volume
#  array[:,101]  3007 Atom Density
#  array[:,102]  3007 Volume


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
    print("File Name,k-eff_o,std_o,k-eff__m,std_m,k-eff_bench," \
           "std_bench,k_normalized,std_normalized,geometry,therm fiss,int fiss," \
           "fast fiss, above therm fiss, Avg E, Avg leth causing fiss,"\
           "Fuel Atom Density,Fuel Volume,Fiss Atom Density,Fiss Volume,"\
           "92235 Atom Density, 92235 Volume, 94239 Atom Density,"\
           "94239 Volume,94241 Atom Density, 94241 Volume,"\
           "92238 Atom Density, 94241 Volume,"\
           "Moderator Atom Density,Moderator Volume",file=file_out)
if(output==1):
    file_out = open(filename_output,'a') #Open the output file



#  array[:,19]  Fuel Atom Density
#  array[:,20]  Fuel Volume
#  array[:,21]  Fiss Atom Density
#  array[:,22]  Fiss Volume
#  array[:,25]  92235 Atom Density
#  array[:,26]  92235 Volume
#  array[:,27]  94239 Atom Density
#  array[:,28]  94239 Volume
#  array[:,29]  94241 Atom Density
#  array[:,30]  94241 Volume
#  array[:,49]  Moderator Atom Density
#  array[:,50]  Moderator Volume



####################################################################################
############################ Loop over all files  ##################################
####################################################################################


number=range(0,len(oFiles))
#number=range(0,100)
#umber=range(500,502)
#umber=range(128,129)
#umber=range(925,950)
#number=range(68,69)
number=np.append(range(0,451),range(452,1098))  #Skip over seg fault  80c  
number=np.append(number,range(1099,len(oFiles))) #skip over another fault 80c

#number=np.append(range(0,755),range(756,1098))  #Skip over seg fault  10c "IEU-COMP-FAST-001"
#number=np.append(number,range(1099,len(oFiles))) #skip over another fault 10c


for one_file in number:
 
    filename=oFiles[one_file]
    
    #Use for 10 c (doesn't have .isoC)
    if ".isoC" in filename:
         continue

    #We are getting the input name (just the file name without the directory tree
    #or the extension
    input_name=filename.split("/")[-1]
    if len(filename.split("."))==3:
         input_name=input_name.split(".")[0]+"."+input_name.split(".")[1]
    else:
         input_name=input_name.split(".")[0]

    print(input_name +" " +str(one_file))




    skip_index=func.find_index(filename,array[:,0],"Skip",Debug)
    if(skip_index == 1000000):
        quit()
        continue


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

    #k-eff from mcnptools
#####################################################################    if("PU-SOL-THERM" in filename):
####################################################################        print("This is before the mctal files")
    mctal_index=func.find_index(filename,mFiles,"mctal",Debug)
    # construct the mctal class from the mctal file
    m=Mctal(mFiles[mctal_index])
    #Get the kcode data
    kc=m.GetKcode()

    # alias for average combined keff
    keff_alias=MctalKcode.AVG_COMBINED_KEFF
    # alias for average combined keff standard deviation
    keff_std_alias=MctalKcode.AVG_COMBINED_KEFF_STD


    #Get the average combined keff after the last cycle
    keff_tools=str(kc.GetValue(keff_alias,kc.GetCycles()))
    std_tools=str(kc.GetValue(keff_std_alias,kc.GetCycles()))


    #print(m.SummaryString())

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

##############################################################    if("PU-SOL-THERM" in filename):
##############################################################        print("This is before the skip files")

    

    if(input_name == "None"):
         print("None value for "+input_name+": input_name = "+input_name)
         continue
    if(std_tools == "None"):
         print("None value for "+input_name+": ktoolsstd = "+std_tools)
         continue
    if(k_eff[0] == "None"):
         print("None value for "+input_name+": k_eff     = "+k_eff[0])
         continue
    if(skip_index == "None"):
         print("None value for "+input_name+": skip index = "+skip_index)
         continue
    if(array[skip_index,1] == "None"):
         print("None value for "+input_name+": Skip Keff   = "+array[skip_index,1])
         continue
    if(array[skip_index,2] == "None"):
         print("None value for "+input_name+": Skipp Keff err = "+array[skip_index,2])
         continue
    if(keff_tools == "None"):
         print("None value for "+input_name+": keff tools = "+keff_tools)
         continue
    if(k_eff[1] == "None"):
         print("None value for "+input_name+": keff err = "+k_eff[1])
         continue
    if(array[skip_index,3] == "None"):
         print("None value for "+input_name+": Geometry  = "+array[skip_index,3])
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



    k_normalized=str(float(k_eff[0])/float(array[skip_index,1]))
    k_norm_err=str(((float(std_tools)/float(array[skip_index,1]))**2+((float(array[skip_index,2])
                                                              *float(keff_tools))/
                                                              (float(array[skip_index,1])**2))**2)**0.5)


#  array[:,0 ]  Has first benchmark names
#  array[:,1 ]  Has the keff value for the benchmark
#  array[:,2 ]  Has the uncertainty for the keff value
#  array[:,3 ]  Has information abarray the geometry
#  array[:,4 ]  Has information abarray the reflector
#  array[:,5 ]  Has information abarray the moderator
#  array[:,6 ]  Has information abarray a secondary reflector
#  array[:,7 ]  Has information abarray a secondary moderator
#  array[:,8 ]  Has comments 
#  array[:,9 ]  Has lab info
#  array[:,10]  Ratio of Vfuel/Vh
#  array[:,11]  Ratio VH/Vfuel
#  array[:,12]  Unit cell hydrogen water number density over U235 unit cell number 
#               density
#  array[:,13]  Fuel Pellet Radius
#  array[:,14]  Fuel Rod Radius  
#  array[:,15]  Lattice unit cell pitch, cm
#  array[:,16]  Information on unit cell geometry
#  array[:,17]  Unit cell water number density
#  array[:,18]  Unit cell U235 number density   

################## Please note that everything below here is subject to change
################## If the isotopes gathered in 'format_static_bench_info.py'
################## were changed than these numbers will be shifted around

#  array[:,19]  Fuel Atom Density
#  array[:,20]  Fuel Volume
#  array[:,21]  Fiss Atom Density
#  array[:,22]  Fiss Volume
#  array[:,23]  92233 Atom Density
#  array[:,24]  92233 Volume
#  array[:,25]  92235 Atom Density
#  array[:,26]  92235 Volume
#  array[:,27]  94239 Atom Density
#  array[:,28]  94239 Volume
#  array[:,29]  94241 Atom Density
#  array[:,30]  94241 Volume
#  array[:,31]  Fertile Atom Density
#  array[:,32]  Fertile Volume
#  array[:,33]  90232 Atom Density
#  array[:,34]  90232 Volume
#  array[:,35]  92232 Atom Density
#  array[:,36]  92232 Volume
#  array[:,37]  92234 Atom Density
#  array[:,38]  92234 Volume
#  array[:,39]  92236 Atom Density
#  array[:,40]  92236 Volume
#  array[:,41]  92238 Atom Density
#  array[:,42]  92238 Volume
#  array[:,43]  94238 Atom Density
#  array[:,44]  94238 Volume
#  array[:,45]  94240 Atom Density
#  array[:,46]  94240 Volume
#  array[:,47]  95241 Atom Density
#  array[:,48]  95241 Volume
#  array[:,49]  Moderator Atom Density
#  array[:,50]  Moderator Volume
#  array[:,51]  1001 Atom Density
#  array[:,52]  1001 Volume
#  array[:,53]  1002 Atom Density
#  array[:,54]  1002 Volume
#  array[:,55]  1003 Atom Density
#  array[:,56]  1003 Volume
#  array[:,57]  6000 Atom Density
#  array[:,58]  6000 Volume
#  array[:,59]  6012 Atom Density
#  array[:,60]  6012 Volume
#  array[:,61]  6013 Atom Density
#  array[:,62]  6013 Volume
#  array[:,63]  4009 Atom Density
#  array[:,64]  4009 Volume
#  array[:,65]  26054 Atom Density
#  array[:,66]  26054 Volume
#  array[:,67]  26056 Atom Density
#  array[:,68]  26056 Volume
#  array[:,69]  26057 Atom Density
#  array[:,70]  26057 Volume
#  array[:,71]  26058 Atom Density
#  array[:,72]  26058 Volume
#  array[:,73]  26000 Atom Density
#  array[:,74]  26000 Volume
#  array[:,75]  Poison Atom Density
#  array[:,76]  Poison Volume
#  array[:,77]  5010 Atom Density
#  array[:,78]  5010 Volume
#  array[:,79]  5011 Atom Density
#  array[:,80]  5011 Volume
#  array[:,81]  2003 Atom Density
#  array[:,82]  2003 Volume
#  array[:,83]  48111 Atom Density
#  array[:,84]  48111 Volume
#  array[:,85]  48113 Atom Density
#  array[:,86]  48113 Volume
#  array[:,87]  64154 Atom Density
#  array[:,88]  64154 Volume
#  array[:,89]  64155 Atom Density
#  array[:,90]  64155 Volume
#  array[:,91]  64156 Atom Density
#  array[:,92]  64156 Volume
#  array[:,93]  64157 Atom Density
#  array[:,94]  64157 Volume
#  array[:,95]  64158 Atom Density
#  array[:,96]  64158 Volume
#  array[:,97]  4009 Atom Density
#  array[:,98]  4009 Volume
#  array[:,99]  3006 Atom Density
#  array[:,100]  3006 Volume
#  array[:,101]  3007 Atom Density
#  array[:,102]  3007 Volume

####################################################################################
############################### Printing ###########################################
####################################################################################


    print(input_name+','+k_eff[0]+','+k_eff[1]+','+keff_tools+','+std_tools+','
          +array[skip_index,1]+','+array[skip_index,2]+','+k_normalized[0:7]+','
          +k_norm_err[0:8]+','+array[skip_index,3]+','+percent_fiss[0]+','
          +percent_fiss[1]+','+percent_fiss[2]+','+percent_fiss[3]+','
          +Avg_E_fiss+','+Avg_l_fiss+','+array[skip_index,19]+','+array[skip_index,20]+','
          +array[skip_index,21]+','+array[skip_index,22]+','+array[skip_index,25]+','
          +array[skip_index,26]+','+array[skip_index,27]+','+array[skip_index,28]+','
          +array[skip_index,29]+','+array[skip_index,30]+','+array[skip_index,41]+','
          +array[skip_index,42]+','+array[skip_index,49]+','
          +array[skip_index,50],file=file_out)




#  array[:,19]  Fuel Atom Density
#  array[:,20]  Fuel Volume
#  array[:,21]  Fiss Atom Density
#  array[:,22]  Fiss Volume
#  array[:,25]  92235 Atom Density
#  array[:,26]  92235 Volume
#  array[:,27]  94239 Atom Density
#  array[:,28]  94239 Volume
#  array[:,29]  94241 Atom Density
#  array[:,30]  94241 Volume

#  array[:,41]  92238 Atom Density
#  array[:,42]  92238 Volume

#  array[:,49]  Moderator Atom Density
#  array[:,50]  Moderator Volume



####################################################################################
######################### Quiting code and showing time ############################
####################################################################################
file_out.close
print (datetime.now() - startTime)
quit()
####################################################################################
####################################################################################
####################################################################################



