#!/usr/bin/env python

#############################################################################################################
############################################  Packages ######################################################
#############################################################################################################

import os #For OS system commands
import subprocess #For some other commands
from datetime import datetime #To time myself
import fnmatch #For wildcard matches
import numpy as np #Gathering the benchmark data
import re #check if there are any characters in find_ending, also for some regex matching


#############################################################################################################
############################################ Functions ######################################################
#############################################################################################################
#This function pulls out a section of output to be worked with, and stores each line
#as a value in a list

def section_pull(Filename,Special_line,End_line):

    file_in = open(Filename, 'r') #Open the input file
    Collect=0

    #parse input file line by line
    for line in file_in:
        line=line.strip('\n') #Remove the newline character
        line=line.split("$")[0] #Remove potential ending comments         
        if(Special_line in line or Collect==1 ): #If this is the line we want, or if we have recently found it
            Collect=1
            try:
                a=np.append(a,line)
            except NameError:
                a=line
        if(End_line in line):
            break
    return(a)


### Code


text2=section_pull("test.txt", "x", "poop") 


counter=0

for value in text2:
	if(counter!=0):
		value=value.strip(",")
		array=re.split(", ",value)[-1]
		try:
			saved_values=np.append(saved_values,array)
		except NameError:
			saved_values=[array]
		
	counter = counter + 1


text=section_pull("mctl342c13", "vals", "tfc")
counter=0
counter2=0
string="  "
for value in text:
	if(counter!=0 and counter!=len(text)-1):
		array=re.split("[\s]+",value) #split up the entire line
		for i in range(0,len(array)):
			array[i]="0.0000"
		try:
			string=string+saved_values[counter2]+" "+array[2]+"  "+saved_values[counter2+1]+" "+array[4]+"  "+saved_values[counter2+2]+" "+array[6]+"  "+saved_values[counter2+3]+" "+array[8]+"\n  "
			counter2=counter2+4
		except IndexError:
			try:
				string=string+saved_values[counter2]+" "+array[2]+"  "+saved_values[counter2+1]+" "+array[4]+"  "+saved_values[counter2+2]+" "+array[6]+"\n  "
				counter2=counter2+3
			except IndexError:
				try:
					string=string+saved_values[counter2]+" "+array[2]+"  "+saved_values[counter2+1]+" "+array[4]+"\n  "
					counter2=counter2+2
				except IndexError:
					string=string+saved_values[counter2]+" "+array[2]+"\n  "
					counter2=counter2+1

	counter=counter+1	

print(string)

