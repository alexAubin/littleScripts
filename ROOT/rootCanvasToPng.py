#! /usr/bin/env python2.6

#
# Context
# -------
#
# You have a list of .root files, each one of them with
# a single canvas named "c1" in it and want to get a png
# output out of it.
#
# Usage
# -----
#
#   python thisScript.py plot1.root plot2.root plot3.root ...
#
#

canvasName = "c1"

print "#  Loading ROOT..."
import ROOT as rt
import sys

# Loop on each file
for fileName in sys.argv :
   
    # Skip arg 0 (it is the name of the script)
    if (fileName == sys.argv[0]) : continue
    
    print " "
    print "#  Converting "+fileName+" to png..."
    print " "

    # Get the canvas
    f = rt.TFile(fileName,"READ")
    plot = f.Get(canvasName)
    if (plot == None) : 
        print "Error : couldn't find canvas "+canvasName+"."
        continue
    
    # Save it as png
    pngOutput = fileName.replace(".root",".png")
    plot.SaveAs(pngOutput)

