#!/usr/bin/env python3

"""
FractionAM converts atom fractions to mass fractions
and mass fractions to atom fractions. Input is a 
single string with MCNP style fractions.
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
from uncertainties import unumpy as unp
import re

################################################################
######################### Functions ############################
################################################################

def ReturnUfloat(string):
    """
    string has format   238.023249814(23) 
            or format   [15.99903-15.99977]

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
    #print(df)
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

def CheckInParen(i,ChemicalFormula):
    """
    i = index inside the string 'ChemicalFormula
    ChemicalFormula = string that could potentially have ()

    Please note, this code is not complete
    """
    NumberOpenParen=ChemicalFormula.count("(")
    NumberCloseParen=ChemicalFormula.count(")")
    if NumberOpenParen != NumberCloseParen:
        print("Unbalanced parentheses in chemical formula")
        quit()
    if NumberOpenParen==0:
        return(1,False)
    
    print("Hello")
    Mul=4
    Test=True
    return(Mul,Test)

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

def StringToMass(string):
    """
    This function takes in a string of the form
    zaid fraction error zaid fraction error ...
    will read a file called 'AtomicWeights.csv'
    and find the atomic weight with error of the zaids
    and store those value in a list called Mass
    """
    ListOfString=string.split()

    if not len(ListOfString)%3==0:
        print("Check string variable missing fraction or error")
        quit()

    #Initialize fractions and zaid
    Zaid=0*np.arange(0,int(len(ListOfString)/3))

    #Gather fraction data and zaid data
    for i in range(0,int(len(ListOfString)/3)):
        Zaid[i]=int(ListOfString[i*3])


    df = pd.read_csv('../Data/AtomicWeights.csv')
    #Gather Mass Data
    for i in range(0,len(Zaid)):
        sZaid=str(Zaid[i])
        if len(sZaid)==4:
            proton=sZaid[0:2]
            if sZaid[2]=="0":
                Isotope=sZaid[3]
            else:
                Isotope=sZaid[2:4]
        elif len(sZaid)==5:
            proton=sZaid[0:2]
            if sZaid[2]=="0":
                Isotope=sZaid[3:5]
            if sZaid[3]=="0":
                Isotope=sZaid[4:5]
            if sZaid[2]!="0" and sZaid[3]!="0":
                Isotope=sZaid[2:5]
        elif len(sZaid)==6:
            proton=sZaid[0:3]
            Isotope=sZaid[3:6]
        else:
            print("Length of zaid is not 4 5 or 6 err")
            quit()
        try:
            Mass=np.append(Mass,FindAtomicMass(df,proton,Isotope))
        except NameError:
            Mass=FindAtomicMass(df,proton,Isotope)

    return(Mass,Zaid)

def ConvertFractions(string,Mass,MasstoAtom,Zaid):
    """
    This function will convert, with error, the mass or atom fraction
    to the other (mass to atom or atom to mass). It will use the masses
    provided in Mass, and the fractions provided in string. If its mass to Atom then
    MasstoAtom=True, otherwise set False
    """

    ListOfString=string.split()
    Total=ufloat(0.,0)

    for i in range(0,len(Zaid)):
 
        Fraction=ufloat(float(ListOfString[i*3+1]),float(ListOfString[i*3+2]))
        if MasstoAtom: #Calculate total Atoms
            Total=Total+Fraction/Mass[i]
        else: #Calculate total Mass
            Total=Total+Fraction*Mass[i]

    stringCalculated=''
    for i in range(0,len(Zaid)):

        Fraction=ufloat(float(ListOfString[i*3+1]),float(ListOfString[i*3+2]))
        if MasstoAtom:
            #Calculate atom fractions
            FractionCalculated=(Fraction/Mass[i])/Total
        else:
            #Calculate mass fractions
            FractionCalculated=(Fraction*Mass[i])/Total
        
        stringCalculated=stringCalculated+\
                          str(Zaid[i])+' '+\
                          str(FractionCalculated)+' '

    return(stringCalculated)

