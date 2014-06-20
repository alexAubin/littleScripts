#! /usr/bin/env python2.6
 
###############################################################################
##
## Copyright 2012 Jeet Sukumaran.
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################
## 
##  Edited by Alexandre A., https://github.com/alexAubin
##
###############################################################################


"""
This program does something.
"""
 
import sys
import os
import re
import argparse
 
__prog__ = os.path.basename(__file__)
__version__ = "1.0.0"
__description__ = __doc__
__author__ = 'Jeet Sukumaran (edited by Alexandre Aubin)'
__copyright__ = 'Copyright (C) 2012 Jeet Sukumaran.'
 
##############################################################################
## From:
##
## http://dev.pocoo.org/hg/pygments-main/file/b2deea5b5030/pygments/console.py
##
## pygments.console
## ~~~~~~~~~~~~~~~~
## Format colored console output.
## :copyright: Copyright 2006-2009 by the Pygments team, see AUTHORS.
## :license: BSD, see LICENSE for details.
##



######################################
# Define colors and style characters #
######################################

esc = "\x1b["
 
codes = {}
codes[""] = ""
codes["reset"] = esc + "39;49;00m"
 
codes["bold"] = esc + "01m"
codes["faint"] = esc + "02m"
codes["standout"] = esc + "03m"
codes["underline"] = esc + "04m"
codes["blink"] = esc + "05m"
codes["overline"] = esc + "06m"
 
dark_colors = ["black", "darkred", "darkgreen", "brown", "darkblue", "purple", "teal", "lightgray"]
light_colors = ["darkgray", "red", "green", "yellow", "blue", "fuchsia", "turquoise", "white"]
 
x = 30
for d, l in zip(dark_colors, light_colors):
    codes[d] = esc + "%im" % x
    codes[l] = esc + "%i;01m" % x
    x += 1
 
del d, l, x
 
codes["darkteal"] = codes["turquoise"]
codes["darkyellow"] = codes["brown"]
codes["fuscia"] = codes["fuchsia"]
# codes["white"] = codes["bold"]

###############################
# Functions to print messages #
###############################

def ansiformat(attr, text):
    """
Format ``text`` with a color and/or some attributes::
color normal color
*color* bold color
_color_ underlined color
+color+ blinking color
"""
    result = []
    if attr[:1] == attr[-1:] == '+':
        result.append(codes['blink'])
        attr = attr[1:-1]
    if attr[:1] == attr[-1:] == '*':
        result.append(codes['bold'])
        attr = attr[1:-1]
    if attr[:1] == attr[-1:] == '_':
        result.append(codes['underline'])
        attr = attr[1:-1]
    result.append(codes[attr])
    result.append(text)
    result.append(codes['reset'])
    return ''.join(result)

def print_message(
        status,
        filePath,
        lineNumber,
        msg):
    filename = os.path.basename(filePath[1])
    dirname = os.path.dirname(filePath[1])
    if dirname != '':
        dirname = os.path.relpath(dirname)

    print ansiformat(status[0],status[1].upper()), 
    if (dirname != '' and dirname != './'):
        print ansiformat(filePath[0], dirname + os.path.sep)+ansiformat("_"+filePath[0]+"_", filename) + ":" + ansiformat(lineNumber[0], lineNumber[1]) + ":", 
    else :
        print ansiformat("_"+filePath[0]+"_", filename) + ":" + ansiformat(lineNumber[0], lineNumber[1]) + ":",
    print ansiformat(msg[0], msg[1])
 

##################
# Define regexes #
##################

# Errors
error_pattern   = re.compile(r"(.+?):([0-9]+?):([0-9]+?): (fatal error|error): (.+)")
# Link error
linkError_pattern   = re.compile(r"(.+?):([0-9]+?): undefined reference to (.+)")
# Warnings
warning_pattern = re.compile(r"(.+?):([0-9]+?):([0-9]+?): warning: (.+)")
# Notes
note_pattern    = re.compile(r"(.+?): In member function '(.+?)\((.+?)\)':")

# Message colors configuration

lineNumber_color = "*green*"
message_color    = "lightgray"

error_filePath_color = "yellow"
error_status_color   = "red"

warning_filePath_color = "blue"
warning_status_color   = "fuchsia"

note_filePath_color  = "blue"
note_status_color    = "yellow"

others_message_color = "darkgray"

finalMessage_fail_color    = "red"
finalMessage_warning_color = "yellow"
finalMessage_success_color = "green"

##################
# Main functions #
##################

def main():
    """
Main CLI handler.
"""
 
    parser = argparse.ArgumentParser(description=__description__)
 
    parser.add_argument("-o", "--show-other",
            action="store_true",
            default=False,
            help="show non-error and non-warning messages as well")
 
    args = parser.parse_args()
 
    errors_present = False
    warnings_present = False

    for line in sys.stdin:
        error_match = error_pattern.match(line)
        linkError_match = linkError_pattern.match(line)
        warning_match = warning_pattern.match(line)
        note_match = note_pattern.match(line)
        if error_match:
            errors_present = True
            filePath = error_match.groups()[0]
            lineNumber = error_match.groups()[1]
            msg = error_match.groups()[3]
            print_message(
                    (error_status_color, " [error] "),
                    (error_filePath_color, filePath),
                    (lineNumber_color, lineNumber),
                    (message_color, msg),
                    )
        elif linkError_match:
            errors_present = True
            filePath = linkError_match.groups()[0]
            lineNumber = linkError_match.groups()[1]
            msg = "Undefined reference to "+linkError_match.groups()[2]
            print_message(
                    (error_status_color, " [link error] "),
                    (error_filePath_color, filePath),
                    (lineNumber_color, lineNumber),
                    (message_color, msg),
                    )
     
        elif warning_match:
            warnings_present = True
            filePath = warning_match.groups()[0]
            lineNumber = warning_match.groups()[1]
            msg = warning_match.groups()[3]
            print_message(
                    (warning_status_color, "[warning]"),
                    (warning_filePath_color, filePath),
                    (lineNumber_color, lineNumber),
                    (message_color, msg),
                    )
            continue
        elif note_match:
            filePath = note_match.groups()[0]
            func = note_match.groups()[1]
            print_message(
                    (note_status_color, "  [note] "),
                    (note_filePath_color, filePath),
                    (lineNumber_color, ""),
					(message_color, "In function "+func),
                    )
        elif args.show_other:
            print ansiformat(others_message_color, line),


    if errors_present:
        print ansiformat(finalMessage_fail_color," [Compilation failed]") 
        sys.exit(1)
    else:
        print ansiformat(finalMessage_success_color," [Compilation succeeded]"),
        if warnings_present:
            print ansiformat(finalMessage_warning_color," ... but with warnings. Please fix them, it hurts ! :|"),
        sys.exit(0)
 
if __name__ == '__main__':
    main()


