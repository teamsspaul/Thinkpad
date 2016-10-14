#!/usr/bin/env python

import numpy as np #Gathering the benchmark data
import re #check if there are any characters in find_ending, also for some regex matching
import subprocess #For some other commands
import fnmatch #For wildcard matches

#############################################################################################################
############################################ Functions ######################################################
#############################################################################################################

def sed_command(command,filename):
    """
    This will run the sed command on the file
    """
    os.system("sed -i "+command+" "+filename)

def List_files_sys(directory,find):
    """
    Create list of files in 'directory' (and files in subdirectories), that match pattern 'find'
    Using system call (2x faster)
    """
    #Save in filesOut the output from the command in brakets (with error)
    filesOut=subprocess.Popen(["find "+directory+" -type f -name \""+find+"\""], stdout=subprocess.PIPE, shell=True)
    #Separate out the output from the previous line
    (filesOut,err)=filesOut.communicate()
    #Convert to a string (before it was something like byte)
    filesOut=str(filesOut,'utf-8')
    #Split the string up into a list based on newlines
    filesOut=filesOut.split(sep="\n")
    #Delete the last element of the list because its empty
    del filesOut[-1]
    return filesOut

def List_files(directory,find):
    """
    Create list of files in 'directory' (and files in subdirectories), that match pattern 'find'
    Using python, a little slower
    """
    filesOut=""
    for dirpath, dirnames, files in os.walk(directory): #Loop over all file names
        for name in files: 
            if fnmatch.fnmatch(name,find): #If there is a match on find, add file name to filesOut
                filesOut=filesOut+os.path.join(dirpath,name)+'\n'
    filesOut=filesOut.split(sep="\n") #Split based on newline
    del filesOut[-1] #delete last element because its empty
    return(filesOut)

def data_pull(Filename,Special_line,Delete,Skip,Delim,elements,Secret_Tunnel=0,Occurance=1):
    """
    This pulls out information from 'Filename', looks for the 'Special_line'
    Deletes what is found in the list 'Delete' (no regex), after skipping 'Skip' number of lines
    The line is deliminated based on 'Delim' (regex) and then the line elements specified by the variable
    'elements' is returned. 'elements' should be a list with at least 1 value.
    There is also a secret tunnel, if you set it equal to anything it will create a secret tunnel!
    which means everything above is the same except...
    that everything before the first thing deleted (whether skip=0 or no) is deleted as well
    For example if 'Secret_Tunnel=1, Skip=0, Special_line=tada!' if the line is 'I love Pandas tada! 0'
    Then 'I love Pandas tada!' will be deleted. If Skip=1, then everything before the first element
    in 'Delete' will be deleted....its like a secret tunnel. 
    'Occurance' specifies which occurance you are looking for, if there are multiple. 

    This script also checks if you are parsing an input file, if so it will pass over comment lines
    """
    file_in = open(Filename, 'r') #Open the input file
    a=["NONE"] #To stop the parsing
    Skips=0
    Times_Found=0
    #parse input file line by line
    line_count=0
    
    input_type_file=0

    if(Filename.split('.')[-1] == "i"): #we are parsing an input type file
        input_type_file=1

    for line in file_in:
        line_count=line_count+1 #Count which line we are on
        line=line.strip('\n') #Remove the newline character
        line=line.split("$")[0] #Remove potential ending comments         
        if(Special_line in line or Skips>0 ): #If this is the line we want, or if we have recently found it


            if (input_type_file==1): #if we are parsing an input type, and if we found a special line
                                     #check to see if its really special, if its a comment, its not special
                                     #skip it
                line_start=line[0:4]
                start_index=len(line_start)-len(line_start.lstrip())
                if(line[start_index] == "c" or line[start_index] == "C"):
                    if(line[start_index+1] == " "):
                        continue


            if(Special_line in line): # If we have found the special line, make sure we count how
                                      # mant times we have found the line
                Times_Found=Times_Found+1

            if(Times_Found!=Occurance): #if this is not the proper occurance of the special line, skip
                continue

            if(Skip==0): #If we don't have to skip any lines...then work with current line
                if(Secret_Tunnel==0):
                    line=line.replace(Special_line,"")
                else:
                    line=line.split(Special_line)[-1]
                    Secret_Tunnel=0 #The secret tunnel has been used.
            elif(Skip!=Skips): #If Skip does not equal 0 then we don't want this line
               Skips=Skips+1 
               continue
            for i in range(0,len(Delete)):
                if(Secret_Tunnel==0):
                    line=line.replace(Delete[i],"") #Globally delete from line items in "Delete"
                    #line=re.sub(Delete[i],"",line) #this has regex, but it doesn't work
                elif(Skip!=0):
                    line=line.split(Delete[i])[-1]
                    Secret_Tunnel=0 #The secret tunnel has been used
            a=re.split(Delim,line) #split up the entire line
            #a=line.split(Delim)
            b=[""]
            for i in elements: #loop over the elements we want and select those out of "a"
                b=np.append(b,a[i])
            a=b[1:len(b)]
            
            if (input_type_file==1):      #If we are parsing an input file, I have found it useful
                a=np.append(a,line_count) #to print out the line number with the information

        if(a[0] != "NONE"): #Quit if we found what we are looking for
            break
    #Close file, for closure
    file_in.close
        
    return(a)

def section_pull(Filename,Special_line,End_line):
    """
    This function pulls out a section of output to be worked with, and stores each line
    as a value in a list. End_Line is where we end, blank lines are deleted
    """
    file_in = open(Filename, 'r') #Open the input file
    Collect=0
    
    #parse input file line by line
    for line in file_in:
        line=line.strip('\n') #Remove the newline character
        line=line.split("$")[0] #Remove potential ending comments         
        if(Special_line in line or Collect==1 ): #If this is the line we want, or if we have recently found it
            Collect=1 
            if len(line)>0 and not line.isspace():
                try:
                    a=np.append(a,line)
                except NameError:
                    a=line
        if(End_line in line):
            #break            #Dont do break so that 'End_line' can be more generic (else breaks early)
                              #If you don't break you have more freedom to pick your 'End_line'
            Collect=0         #Program takes longer this way though...good thing we only run once
    try:
        return(a)
    except UnboundLocalError:
        return(["None"])

def cut_ends(list1,Plus):
    """
    This function will cut everything in list1 after a number (except U233) plus the 
    number in 'Plus'? and store in list2.
    Example:
             Plus=0   : "U233-MET-FAST-001-001 -> U233-MET-FAST
             Plus=1   : "U233-MET-FAST-001-001 -> U233-MET-FAST-
    """
    for i in list1:
        
        i=i.split("/")[-1] #split Filename based on '/' and take the last element (just the file name)
        if(len(i.split("."))==3):
            i=i.split(".")[0]+"."+i.split(".")[1]
        else:
            i=i.split(".")[0] #split Filename based on '.' and take the first part

        i2=i[4:len(i)] #I do this because of U233   

        position=re.search("\d",i2).start()+3+Plus

        try:
            list2=np.append(list2,i[0:position])
        except NameError:
            list2=i[0:position]
    return(list2)


def Find_Close_Match(Filename,list1,Debug): #Filename = Jeremy's file, list1 = skips list
    Filename=Filename.split("/")[-1] #split Filename based on '/' and take the last element (just the file name)
    Filename=Filename.split(".")[0] #split Filename based on '.' and take the first part
    NumberOfMatches=[]
    Adding=range(0,Debug)
    for i in Adding:
        list2=cut_ends(list1[1:len(list1)-1],i)
        Matches=[]
        Count=1
        for file in list2:
            if file in Filename:
                Matches=np.append(Matches,list1[Count])
            Count=Count+1
        if len(Matches)==0:
            NumberOfMatches=np.append(NumberOfMatches,100000)
        else:
            NumberOfMatches=np.append(NumberOfMatches,len(Matches))
    #Rerun the above, but for the minimum case
    RunIndex=np.argmin(NumberOfMatches)
    list2=cut_ends(list1[1:len(list1)-1],RunIndex)
    Matches=[]
    Count=1
    for file in list2:
        if file in Filename:
            Matches=np.append(Matches,list1[Count])
        Count=Count+1
    return(Matches)

def find_index(Filename,list1,ID,Debug):
    """
    This function finds an index number in 'list1'. This index corresponds to the directory/filename that
    that is the same as 'Filename'. Basically looking for 'Filename' in 'list1', returning the index number
    so that list1[index] has 'Filename' in it.
    """
    Filename=Filename.split("/")[-1] #split Filename based on '/' and take the last element (just the file name)
    
    #Do this for compile (but not for format)
    if(len(Filename.split("."))==3):
        Filename=Filename.split(".")[0]+"."+Filename.split(".")[1]
    else:
        Filename=Filename.split(".")[0] #split Filename based on '.' and take the first part
    
    Count=0
    for file in list1:
        file=file.split("/")[-1]
        
        # Keep if doing format... but not with compile
        # if (len(file.split("."))==3):
        #     file=file.split(".")[0]+"."+file.split(".")[1]
        # else:
        #     file=file.split(".")[0]
        
        #Keep if doing format... but not with compile
        if ID == "mctal":
            if (len(file.split("."))==3):
                file=file.split(".")[0]+"."+file.split(".")[1]
            else:
                file=file.split(".")[0]
        


        if fnmatch.fnmatch(file,Filename):
            index=Count
            break
        Count=Count+1
    try :
        index
    except UnboundLocalError:
        print ("Hey Index was not defined for "+Filename+" in the list of "+ID+" files")
        index=1000000
        print ("Closest matches are")
        CloseMatch=Find_Close_Match(Filename,list1,Debug)
        print(CloseMatch)
    return(index)

def find_none(list1):
    """
    This function finds the range of 'None' values in a list. Output will be string listing out ranges of 'None'
    preceeded by a number and the word to, for example "2 to 3-6". This means the value stored in list1[2] needs
    to be copied over to list1[3], list1[4], lits1[5], and list1[6]. This assumes that 'None' values are assigned
    so that the first value found above it should be its value.
    Example: IF list1=["Name1","None","None","None","Name2","None"] this function would return "0 to 1-3,4 to 5"
    Meaning the value found in list1[0] should be stored in list1[1],list1[2], and list1[3].
    """
    tracker=0
    counter=0
    string=""
    Cycles=len(list1)-1
    for i in list1:
        if('None' in i and tracker==0):
            tracker=1
            string=string+str(counter-1)+" to "+str(counter)
            Start=counter
        if('None' not in i and tracker!=0):
            tracker=0
            string=string+"-"+str(counter-1)+","
        if(counter==Cycles and tracker!=0 and counter != Start):
            string=string+"-"+str(counter)
        counter=counter+1
    return(string)

def commit_change(list1,string):
    """
    Commit the changes that should be implemented as described for the function 'find_none'
    """
    #Make a list out of the string, each element should look like "2 to 3-6" - as described in the function
    #above
    listofString=string.split(",")
    for i in listofString: #loops over each section where a names needs to be modified
        if "to" not in i:
            continue
        Multi_index=i.split(" to ")  #Remember i has the form "2 to 3-6", Multi_index[0] = "2", Multi_index[1]="3-6"
        Name_index=int(Multi_index[0])
        Start_index=int(Multi_index[1].split("-")[0])
        try:
            End_index=int(Multi_index[1].split("-")[1])
        except IndexError:
            End_index=Start_index
        for j in range(Start_index,End_index+1): #added 1 to index because it doesn't include last entry for some
                                                 #reason
            list1[j]=list1[Name_index]
        
    return(list1)

def find_ending(list1):
    """
    This function pulls in a list of strings. If the string contains a ".", then everything after the dot
    is assumed to be a number. This number is divided by 1000 (for example 1/1000 = 0.001). Then everything
    after the decimal (001 in the example) is pulled out and stored in value. If the length of value is less
    than three (for example if a string in 'list1' contained 'HMF3.10' then 10 would be pulled off, divided 
    by 1000, and 01 would be stored in value (10/1000 = 0.01)) then extra 0s are added so that the total 
    length of value is 3. If a string in 'list1' does not contain a "." then a blank string is stored.
    All values calculated are passed to a list called 'endings'.
    If there are two dots in list, then this guy does something else
    """
    endings=[""]
    counter=0
    for i in list1:
        PRE=False
        if "pre" in i:
            PRE=True
        if "." in i and not PRE:
            if len(i.split("."))==2:
                if re.search('[a-zA-Z]',i.split(".")[1])!=None: #If there is an alphabetic character after decimal
                    value=i.split(".")[1]
                    #Do this ugly thing (this won't work for something like 10a, but will for 3a)
                    value=str(int(re.findall(r'\d+',value)[0]+"0")/1000).split(".")[1]+re.findall(r'[a-zA-Z]',value)[0]
                else:
                    #else if you are normal, do above
                    value=str(int(i.split(".")[1])/1000).split(".")[1]
                if len(value) == 2:
                    value=value+"0"
                if len(value) == 1:
                    value=value+"00"
                endings=np.append(endings,value)
            else:
                value="_"+i.split(".")[1]+i.split(".")[2]
                endings=np.append(endings,value)
        elif not PRE:
            endings=np.append(endings,"")
        elif PRE:
            value=i.split(".")[1]+"pre"
            endings=np.append(endings,value)
        counter=counter+1


    return(endings[1:len(endings)])

def Number_Density(ifilename,isotope):
    """
    This will find all non commented out instances in an input file of density, it will
    also find the lines they occured on
    """
    special_line=isotope
    delete=["$"]
    skip=0
    Secret_Tunnel="Initiate the secret Tunnel!"
    delim="[\s]+"
    elements=[1]

    for Occurance in [1,2,3,4,5,6,7,8,9,10]:
        Place_holder=data_pull(ifilename,special_line,delete,skip,delim,elements,Secret_Tunnel,Occurance)
        if Place_holder[0] == 'NONE':
            break
        try:
            Num_Den=Num_Den+" | "+Place_holder[0]+" "+Place_holder[1] #np.append(Num_Den,Place_holder)
        except NameError:
            Num_Den=Place_holder[0] + " " + Place_holder[1]
    try:
        return(Num_Den)
    except UnboundLocalError:
        return("0")

def remove_values_from_list(the_list, val):
    """
    This function removes values from list, use it wisely
    """
    return [value for value in the_list if value != val]

def Organize_Fractions(list1):
    """
    This function will take in a list of strings 'list1'. 'list1' will be parsed line by line.
    Each line will be split into a list. Then depending on:
           -whether the first element of the list (list_of_line[0]) is completely numeric '123,' = false
           -whether the first character of the first element of the list (list_of_line[0][0]) is numeric
    The list of strings will be reorganized so that a new list of strings will be created where each 
    element contains information for a single material (assuming data was pulled from MCNP).
    I know that isn't very helpful, but, it might be easier to explain with an example:

    If list1 =
    ['  number     component nuclide, atom fraction'
     '  1           92234, 1.02500E-02      92235, 9.37683E-01      92238, 5.20671E-02'
     '  900           92235, 1.00000E+00' ' material'
     '  number     component nuclide, mass fraction']
    
    Then Materials=
    
    ['1: 92234,1.02500E-02 92235,9.37683E-01 92238,5.20671E-02'
     '900: 92235,1.00000E+00']

     Sometimes MCNP will have a single material pass over several lines like:

    ['  number     component nuclide, atom fraction'
     '  1           92234, 1.02500E-02      92235, 9.37683E-01      92238, 5.20671E-02'
     '   94239, 1.02500E-02      94240, 9.37683E-01      94241, 5.20671E-02'
     '  900           92235, 1.00000E+00' ' material'
     '  number     component nuclide, mass fraction']

     This function will keep all of material 1 in the same string.

    """
    Materials=np.array([])
    Materials=Materials.astype("object") #Convert type to object to modify some of the strings
    Collect=0
    for line in list1:
        line=line.strip() # Remove white space on both sides
        list_of_line=re.split("[\s]+",line) #split up the entire line
        element_0_check=str.isdigit(list_of_line[0]) #Check if entire element is digit
        check_0_0=str.isdigit(list_of_line[0][0])    #check if first character of first element is digit
        if(Collect==1 and element_0_check):
            Collect=0
        if(element_0_check and Collect == 0): 
            Collect=1
            Materials=np.append(Materials,[list_of_line[0]+": "+
                                ' '.join(list_of_line[1:len(list_of_line)])])
            Materials[-1]=Materials[-1].replace(", ",",")
            continue
        if(Collect==1 and not element_0_check and check_0_0):
            Materials[-1]=Materials[-1]+' '+' '.join(list_of_line)
            #print(Materials[-1]+' '+' '.join(list_of_line))
            Materials[-1]=Materials[-1].replace(", ",",")
            continue

    Materials=Materials.astype("U") #Convert type to object readable stuff
    return(Materials)


def rreplace(s, old, new, occurrence):
    """
    Reverse replace. Takes string 's' and replaces old string 'old' with
    a new string 'new'. It does this 'occurrence' times. 
    It starts at the end of the string though and works backwards
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)
