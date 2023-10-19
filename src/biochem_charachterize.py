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

