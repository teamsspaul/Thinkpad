#!/usr/bin/env python3

"""
MolConversion converts Molarity to Molality
and Molality to Molarity with a concentration

"""

__author__     =  "Paul Mendoza"
__copyright__  =  "Copyright 2016, Planet Earth"
__credits__    = ["Sunil Chirayath",
                  "Charles Folden",
                  "Jeremy Conlin"]
__license__    =  "GPL"
__version__    =  "1.0.1"
__maintainer__ =  "Paul Mendoza"
__email__      =  "paul.m.mendoza@gmail.com"
__status__     =  "Production"

################################################################
##################### Import packages ##########################
################################################################

import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from uncertainties import ufloat
from uncertainties.umath import *
import re


################################################################
################### Import Own Functions #######################
################################################################


def ReturnUfloat(string):
    """
    string has format   238.023249814(23)
    Returns a uncertain number so python can do calculations
    """
    Number=str(string.split('(')[0])
    LastErrorNumber=str(string.split("(")[1].replace(")",""))
    NumberOfZeros=len(Number.split(".")[1])-len(LastErrorNumber)
    Error="0."
    for i in range(0,NumberOfZeros):
        Error=Error+"0"
    Error=Error+LastErrorNumber

    return(ufloat(float(Number),float(Error)))
    
def FindAtomicMass(df,proton,Isotope):
    """
    This function will take in a dataset 'df' look through the
    'df.Protons' column and find the column that matches with 
    'proton'. If the row that contains 'proton' also contains
    'Isotope' in the 'df.Isotope' column, then the value stored
    in 'df.Relative_Atomic_Mass' is reported for that row.
    Because the proton numbering scheme can have a format
    '10' for hydrogen and '10' for neon (following MCNP ZAID 
    naming conventions) if we don't find a value with the whole
    string of 'proton' then the program looks through the first
    element of string and tries to match that 'proton[0]'
    If no matches are found, and error is thrown out.

    df = dataset with columns 'Protons' 'Isotopes' and 
    'Relative_Atomic_Mass'. Dataset created with pandas

    proton = string with proton number (follow MCNP zaid format)

    Isotope = string with isotope number (just put the atomic mass
    do not follow MCNP format - different for few cases)
    """
    print(df)
    for i in range(0,len(df.Protons)):
        dfPro=str(df.Protons[i])
        if proton==dfPro:
            dfIso=str(df.Isotope[i])
            if Isotope==dfIso:
                Mass=df.Relative_Atomic_Mass[i]
                break
    try:
        Mass
    except NameError:
        for i in range(0,len(df.Protons)):
            dfPro=str(df.Protons[i])
            if proton[0]==dfPro:
                dfIso=str(df.Isotope[i])
                if Isotope==dfIso:
                    Mass=df.Relative_Atomic_Mass[i]
                    break
    try:
        Mass
    except NameError:
        print("Could not find atomic mass for proton = "\
              +proton+" and for Isotope = "+Isotope)
    Mass=ReturnUfloat(Mass)
    return(Mass)

def ChemList(ChemicalFormula):
    """
    This function will take in a string for a 
    chemical formula.

    Please modify your formula to fit the following rules
    
    1. No repeats of elements (sum up all the same time element)
    2. To enter a subscript use "_", for example He_3 indicates
       three helium atoms.
    3. Use captical letters for the first letter of an element.
       If there are multiple letters for an elemental symbol,
       then use lowercase for the second letter (program does
       not interpret three symbol elements)
    4. If there are more than 999 of a single atom in your chemical
       formula, you will have to write your own code. Or modify 
       this one.
    """
    i=0
    List=[]
    while (i <len(ChemicalFormula)-1):
        start=i
        #print("The beginning i index = "+str(i))
        if re.search('[A-Z]',ChemicalFormula[i]):               #Capital letter?
            if re.search('[a-z]',ChemicalFormula[i+1]):         #Followed by lowercase?
                if re.search('_',ChemicalFormula[i+2]):         #Followed by more than 1?
                    if re.search('[0-9]',ChemicalFormula[i+5]): #Hundreds check
                        List=np.append(List,ChemicalFormula[i:i+6])
                        #print(ChemicalFormula[i:i+6])
                        i=i+6
                    elif re.search('[0-9]',ChemicalFormula[i+4]): #tens check
                        List=np.append(List,ChemicalFormula[i:i+5])
                        #print(ChemicalFormula[i:i+5])
                        i=i+5
                    else:                                        #If not hundres or tens, then ones
                        List=np.append(List,ChemicalFormula[i:i+4])
                        #print(ChemicalFormula[i:i+4])
                        i=i+4
                else:                                           #If not more than one, print
                    List=np.append(List,ChemicalFormula[i:i+2])
                    #print(ChemicalFormula[i:i+2])
                    i=i+2
            elif re.search('_',ChemicalFormula[i+1]):           #If only single symbol, then do same as above
                if re.search('[0-9]',ChemicalFormula[i+4]):     #hundreds
                    List=np.append(List,ChemicalFormula[i:i+5])
                    #print(ChemicalFormula[i:i+5])
                    i=i+5
                elif re.search('[0-9]',ChemicalFormula[i+3]):   #tens
                    List=np.append(List,ChemicalFormula[i:i+4])
                    #print(ChemicalFormula[i:i+4])
                    i=i+4
                else:                                           #ones
                    List=np.append(List,ChemicalFormula[i:i+3])
                    #print(ChemicalFormula[i:i+3])
                    i=i+3
            else:
                List=np.append(List,ChemicalFormula[i])
                print(ChemicalFormula[i])
                i=i+1
        if start==i: #If we didn't find anything useful
            i=i+1
        #print("The end i index = "+str(i))
    return(List)

################################################################
######################## Conditions ############################
################################################################

MolarityToMolality=False

################################################################
####################### Gather Data ############################
################################################################

#digest chemical formula
ChemicalFormula='He_800O_2Na_1'
ChemicalFormula=ChemicalFormula+"    "

#Make sure your chemical form has no repeats
#Read 
List=ChemList(ChemicalFormula)



print(List)
#find atom fractions of elements
