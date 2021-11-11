#!/usr/bin/env python3

#copyright 2021 aBoxofTentacles <gmoney@aboxoftentacles.com>

# This file is part of CalibreHentoid

# CalibreHentoid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CalibreHentoid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, re, sys, getopt
from zipfile import ZipFile

def simplify_path(full_path):
    print(full_path.path)
    path_array = full_path.path.split('/')
    if len(path_array) < 2: #catch windows file seperators
        path_array = full_path.path.split('\\')
    return os.path.join(path_array [-3], path_array[-2], path_array[-1])
    


HELP_TEXT = """hentoidArchiver.py for zipping up all of your hentoid downloads
-----------------------------------------------------------------------------
Usage: hentoidArchiver.py [-d <directory> -o <output directory> -v ...]
-----------------------------------------------------------------------------
Options
-----------------------------------------------------------------------------
-h, --help :        Display this screen
-d:                 Choose a directory to start in (defaults to current directory)
-o:                 Choose an output directory (defaults to current directory)
-v, --verbose:      Verbose mode
"""

#instance variables
rootDir = "."
outDir = "."
verbose = False
comicMode = False


try:
    opts, args = getopt.getopt(sys.argv[1:],"hvcd:o:", ['help', 'verbose'])
except getopt.GetoptError:
    print('hentoidArchiver.py -d <directory>')
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(HELP_TEXT)
        sys.exit()
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == ("-d"):
        rootDir = arg
    elif opt == ("-o"):
        outDir = arg

for source in os.scandir(rootDir):
    if source.is_dir():
        for book in os.scandir(source):
            if verbose:
                print('found ' + str(book))
            with ZipFile(os.path.join(outDir, book.name + '.cbz'), 'w') as comicZip:
                for page in os.scandir(book):
                    comicZip.write(page, arcname=simplify_path(page))
                comicZip.close
                if verbose:
                    print(str(book) + ' zipped')
