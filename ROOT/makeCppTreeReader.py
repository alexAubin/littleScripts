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

######################
#  Print C++ header  #
######################


print "// ############################################################"
print "// # Usage                                                    #"
print "// #                                                          #"
print "// # - Include this header in your code                       #"
print "// # - Create an instance of babyEvent, for instance event :  #"
print "// #      babyEvent event;                                    #"
print "// # - Open your tree, for example :                          #"
print "// #      TTree* theTree = f.Get(\"babyTuple\");                #"
print "// # - Init branches by calling :                             #"
print "// #      InitializeBranchesForReading(theTree,&event);       #"
print "// # - To read the i-ish event, call :                        #"
print "// #      ReadEvent(theTree,i,&event);                        #"
print "// # - Get the value of your branch by acessing               #"
print "// #      event.branchName;                                   #"
print "// ############################################################"

print " "
print "#ifndef babyFormat"
print "#define babyFormat"

print ""
print "// ##########################"
print "// #  Baby event structure  #"
print "// ##########################"
print " "

print "typedef struct"
print "{"

maxTypeLength = len(max(branchTypes, key=len))
maxNameLength = len(max(branchNames, key=len))

for name, type in zip(branchNames,branchTypes) :
    print "    "+type.ljust(maxTypeLength)+" "+name+";"

print " "
print "    // Intermediate pointers for special types"
print "    // Yes, this shit is needed because ROOT is crap."
print " "

for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (not isSpecialType) : continue
    print "    "+(type+"*").ljust(maxTypeLength+1)+" pointerFor"+name+";"

print "}"
print "babyEvent;"

print " "
print "// #############################"
print "// #  Branches initialization  #"
print "// #############################"
print " "

print "void InitializeBranchesForReading(TTree* theTree, babyEvent* myEvent)"
print "{"

for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (isSpecialType) :
        print "    myEvent->pointerFor"+name+" = 0;"

print " "
for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (not isSpecialType) :
        print "    theTree->SetBranchAddress(\""+(name+"\",").ljust(maxNameLength), "&(myEvent->"+name+"));"
    else :
        print "    theTree->SetBranchAddress(\""+(name+"\",").ljust(maxNameLength), "&(myEvent->pointerFor"+name+"));"
print "}"


print " "
print "// ################################"
print "// #  Function to read one event  #"
print "// ################################"
print " "

print "void ReadEvent(TTree* theTree, long int i, babyEvent* myEvent)"
print "{"
print "    theTree->GetEntry(i);"
print " "

print "    // Put actual content of special type branches where they should be..."
for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (not isSpecialType) : continue
    print "    myEvent->"+name.ljust(maxNameLength)+" = *(myEvent->pointerFor"+name+");"

print "}"

################
#  Close file  #
################

print " "
print "#endif"

