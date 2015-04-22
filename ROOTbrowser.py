#/usr/bin/env python2.6

import sys, time
from array import *
import ROOT as rt

##########################
#  Palette for 2D plots  #
##########################

NRGBs = 5
NCont = 500
stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00  ])
red   = array("d",[0.25, 0.25, 0.95, 1.00, 1.00  ])
green = array("d",[0.25, 0.90, 1.00, 0.40, 0.25  ])
blue  = array("d",[0.75, 1.00, 0.30, 0.20, 0.25  ])

rt.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
rt.gStyle.SetNumberContours(NCont)

################################
#  Format for text on 2D plots #
################################

rt.gStyle.SetPaintTextFormat("4.1f");

###################################
#  Load files given in arguments  #
###################################

files = []
for file in sys.argv :
    if (file == sys.argv[0]) : continue
    files.append(rt.TFile(file))

################################################
#  Load TBrowser and wait for it to be closed  #
################################################

browser = rt.TBrowser()

while (browser != None) :
    time.sleep(1)
