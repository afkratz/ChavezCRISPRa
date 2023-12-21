# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

from localcider.sequenceParameters import SequenceParameters
import numpy as np
AllAAs="PGYWFVLIATSQNMCEDRKH" #ordered according to biochemical traits

#------------------------Whole protein charachterization------------------------
def getNCPR(AAseq):
    SeqOb = SequenceParameters(AAseq)
    return(SeqOb.get_NCPR())

def getKappa(AAseq):
    SeqOb = SequenceParameters(AAseq)
    return(SeqOb.get_kappa())

def getOmega(AAseq):
    SeqOb=SequenceParameters(AAseq)
    return SeqOb.get_kappa_X(['W','F','Y','L'],['D','E'])



def getHydropathy(AAseq):
    SeqOb = SequenceParameters(AAseq)
    return(SeqOb.get_mean_hydropathy())

def getAminoAcidFractions(AAseq):
    SeqOb = SequenceParameters(AAseq)
    return(SeqOb.get_amino_acid_fractions())

def getDisorderFraction(AAseq):
    SeqOb = SequenceParameters(AAseq)
    return(SeqOb.get_fraction_disorder_promoting())

def getAromaticity(AAseq):
    AAFractions = getAminoAcidFractions(AAseq)
    return AAFractions['F']+AAFractions['W']+AAFractions['Y']
#-------------------------------------------------------------------------------

#-------------------------Positional charachterization--------------------------


def getLinearTrait(AAseq:str,trait:str,rolling_window_size:int=1):
    SeqOb=SequenceParameters(AAseq)
    if trait=='NCPR':
        values = SeqOb.get_linear_NCPR(blobLen=1)[1]
    elif trait=='Hydropathy':
        values = SeqOb.get_linear_hydropathy(blobLen=1)[1]
    elif trait=='FDP':
        values = SeqOb.get_linear_sequence_composition(blobLen=1,grps=["TAGRDHQKSEP"])[1]
    else:
        raise ValueError("Error, {} is not either 'NCPR', 'Hydropathy', or 'FDP'".format(trait))
    return values

def rollingAverage(array:np.ndarray,n:int):
    averages=[]
    for start in range(0,len(array)-n+1):
        average = array[start:start+n].mean()
        averages.append(average)
    return np.stack(averages)

def samplePoints(array:np.ndarray,n:int):
    xs = np.linspace(0,len(array),n+1)
    ys = []
    for x in xs[:-1]:
        ys.append(array[int(x)])
    return np.stack(ys)

