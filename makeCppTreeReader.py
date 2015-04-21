
import ROOT as rt
ROOTtypes = { "F" : "float", "I" : "int", "S" : "short int", "O" : "bool" }



f = rt.TFile("../../babyTuples_1030/ttbar_madgraph_2l.root")

##############################################
#  Get and parse list of branches from ROOT  #
##############################################

rawListOfBranches = f.Get("babyTuple").GetListOfBranches()
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

print "#ifndef babyFormat"
print "#define babyFormat"

##########################
#  Baby event structure  #
##########################

print " "
print "typedef struct"
print "{"

maxTypeLength = len(max(branchTypes, key=len))
maxNameLength = len(max(branchNames, key=len))

for name, type in zip(branchNames,branchTypes) :
    #print "{:>8} {:>8}".format(type, name)
    print "    "+type.ljust(maxTypeLength)+" "+name+";"

print "}"
print "babyEvent;"

#############################################
#  Intermediate pointers for special types  #
#############################################

print " "
print "typedef struct"
print "{"

for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (not isSpecialType) : continue
    print "    "+(type+"*").ljust(maxTypeLength+1)+" pointerFor"+name+";"

print "}"
print "babyIntermediatePointers;"

################################
#  Function to read one event  #
################################

print " "
print "void ReadEvent(TTree* theTree, long int i, babyIntermediatePointers* pointers, babyEvent* myEvent)"
print "{"
print "    theTree->GetEntry(i);"
print " "

for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (not isSpecialType) : continue
    print "    myEvent->"+name.ljust(maxNameLength)+" = *(pointers->pointerFor"+name+");"
print "}"


#############################
#  Branches initialization  #
#############################

print " "
print "void InitializeBranchesForReading(TTree* theTree, babyEvent* myEvent,babyIntermediatePointers* pointers)"
print "{"

for name, type, isSpecialType in zip(branchNames,branchTypes,branchHasSpecialType) :
    if (not isSpecialType) :
        print "    theTree->SetBranchAddress(\""+(name+"\",").ljust(maxNameLength), "&(myEvent->"+name+"));"
    else :
        print "    pointers->pointerFor"+name+" = 0;"
        print "    theTree->SetBranchAddress(\""+(name+"\",").ljust(maxNameLength), "&(pointers->pointerFor"+name+"));"
print "}"

################
#  Close file  #
################

print " "
print "#endif"

