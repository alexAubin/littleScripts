#! /usr/bin/env python2.6

import sys
import ROOT as rt
ROOTtypes = { "F" : "float", "I" : "int", "S" : "short int", "O" : "bool" }

inputFile = sys.argv[1]
treeName  = sys.argv[2]

f = rt.TFile(inputFile)

##############################################
#  Get and parse list of branches from ROOT  #
##############################################

rawListOfBranches = f.Get(treeName).GetListOfBranches()
branchNames = []
branchTypes = []
branchHasSpecialType = []
for branch in rawListOfBranches :

    if (branch.GetClassName() != "") :
        branchType = branch.GetClassName()
        specialType = True

    else :
        branchType = branch.GetTitle().split('/')[1]
        branchType = ROOTtypes[branchType]
        specialType = False

    branchName = branch.GetName()

    branchNames.append(branchName)
    branchTypes.append(branchType)
    branchHasSpecialType.append(specialType)

##################
#  Dump content  #
##################

maxTypeLength = len(max(branchTypes, key=len))
maxNameLength = len(max(branchNames, key=len))

for name, type in zip(branchNames,branchTypes) :
    print " "+type.ljust(maxTypeLength), name

