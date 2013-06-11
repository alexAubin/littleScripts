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
__author__ = 'Jeet Sukumaran'
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
 
dark_colors = ["black", "darkred", "darkgreen", "brown", "darkblue",
                "purple", "teal", "lightgray"]
light_colors = ["darkgray", "red", "green", "yellow", "blue",
                "fuchsia", "turquoise", "white"]
 
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
 
def reset_color():
    return codes["reset"]
 
def colorize(color_key, text):
    return codes[color_key] + text + codes["reset"]
 
 
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
##
##############################################################################
 
def print_message(
        status,
        fpath,
        lnum,
        msg,
        colorize=True):
    if colorize:
        filename = os.path.basename(fpath[1])
        dirname = os.path.dirname(fpath[1])
        if dirname != '':
            dirname.replace('storage1','opt/sbg/data/data1')
            dirname = os.path.relpath(dirname)


        print ansiformat(status[0],status[1].upper()), 
        if dirname != '':
            print ansiformat(fpath[0], dirname + os.path.sep), 
        print ansiformat("_"+fpath[0]+"_", filename), ":", 
        print ansiformat(msg[0], msg[1])

#		sys.stdout.write("{}: {}{} +{}: {}\n".format(
#           ansiformat(status[0], status[1].upper()),
#           ansiformat(fpath[0], dirname + os.path.sep),
#           ansiformat("_"+fpath[0]+"_", filename),
#           ansiformat(lnum[0], lnum[1]),
#           ansiformat(msg[0], msg[1]),
#           ))
    else:
		print status[1].upper(), ": ", fpath[1], ": ", msg[1]
#        sys.stdout.write("{}: {} +{}: {}\n".format(
#           status[1].upper(),
#           fpath[1],
#           lnum[1],
#           msg[1]
#			))
 
def main():
    """
Main CLI handler.
"""
 
    parser = argparse.ArgumentParser(description=__description__)
 
    parser.add_argument("-o", "--show-other",
            action="store_true",
            default=False,
            help="show non-error and non-warning messages as well")
 
    parser.add_argument("--hide-errors",
            action="store_true",
            default=False,
            help="hide error messages (why would you want to do this?)")
 
    parser.add_argument("--hide-warnings",
            action="store_true",
            default=False,
            help="hide warning messages")
 
    parser.add_argument("--no-color",
            action="store_true",
            default=False,
            help="do not colorize")
 
    args = parser.parse_args()
 
    lnum_color = "*green*"
    msg_color = "lightgray"
 
    # Errors
    err_pattern = re.compile(r"(.+?):([0-9]+?): error: (.+)")
    err_fpath_color = "yellow"
    err_lnum_color = lnum_color
    err_status_color = "red"
    err_msg_color = msg_color

    # Warnings
    warn_pattern = re.compile(r"(.+?):([0-9]+?): warning: (.+)")
    warn_fpath_color = "blue"
    warn_lnum_color = lnum_color
    warn_status_color = "fuchsia"
    warn_msg_color = msg_color

    # Note 1
    note1_pattern = re.compile(r"(.+?): In member function '(.+?)\((.+?)\)':")
    note1_fpath_color = "blue"
    note1_lnum_color = lnum_color
    note1_status_color = "yellow"
    note1_msg_color = "white"

    # Make errors 
    makeerr_pattern = re.compile(r"gmake: \*\*\* \[(.+?)\] Error 1")
    makeerr_fpath_color = "yellow"
    makeerr_lnum_color = lnum_color
    makeerr_status_color = "red"
    makeerr_msg_color = msg_color

    errors_present = False
    warnings_present = False
    note1_present = False
    makeerrors_present = False

    output_lines = sys.stdin.read().split("\n")
    for line in output_lines:
        err_match = err_pattern.match(line)
        warn_match = warn_pattern.match(line)
        note1_match = note1_pattern.match(line)
        makeerr_match = makeerr_pattern.match(line)
        if err_match and not args.hide_errors:
            errors_present = True
            fpath = err_match.groups()[0]
            lnum = err_match.groups()[1]
            msg = err_match.groups()[2]
            print_message(
                    (err_status_color, " [error] "),
                    (err_fpath_color, fpath),
                    (err_lnum_color, lnum),
                    (err_msg_color, msg),
                    colorize=not args.no_color,
                    )
        elif warn_match and not args.hide_warnings:
            warnings_present = True
            fpath = warn_match.groups()[0]
            lnum = warn_match.groups()[1]
            msg = warn_match.groups()[2]
            print_message(
                    (warn_status_color, "[warning]"),
                    (warn_fpath_color, fpath),
                    (warn_lnum_color, lnum),
                    (warn_msg_color, msg),
                    colorize=not args.no_color,
                    )
            continue
        elif note1_match and not args.hide_warnings:
            note1_present = True
            fpath = note1_match.groups()[0]
            func = note1_match.groups()[1]
            print_message(
                    (note1_status_color, "  [note] "),
                    (note1_fpath_color, fpath),
                    (note1_lnum_color, ""),
					(note1_msg_color, "In function "+func),
                    colorize=not args.no_color,
                    )
        elif makeerr_match:
            makeerrors_present = True
            print " "
            print ansiformat(makeerr_status_color," [Compilation failed] "), 
            print " "
        elif args.show_other:
            if args.no_color:
                print line
            else:
                print ansiformat("darkgray", line)
    if errors_present:
        sys.exit(1)
    else:
        sys.exit(0)
 
if __name__ == '__main__':
    main()


