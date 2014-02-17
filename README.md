littleScripts
=============

Little scripts for everyday life

launchScreen
------------

Description : Launch a screen session with the given name and execute the given command

Usage : ./launchScreen sessionName [command arg1 arg2 ...] 

colorGcc
--------

Description : Colorize gcc to avoid having to deal with the black-and-white default output

Usage : make 2>&1 | python colorGcc.py

diffFolder
----------

Description : Compare the source files of two folders recursively

Usage : edit DIR1 and DIR2 in scripts, run ./diffFolder and read the .diff files.

harvestProdOnDPM
----------

Description : Harvest NTuples from DPM after Crab production, (except duplicate output if there are some)

Usage : edit PROD in the script, then do ./harvestProdOnDPM [sampleName]

multiStatus, multiResubmit
----------

Description : Crab monitoring / resubimitting tools for large production. This create a status.tmp in the task folder.

Usage : edit the list TASKS inside multiStatus and multiResubmit, then use ./multiStatus -U do check the status of all the tasks, then use ./multiResubmit to resubmit all the job with errors/crash.


