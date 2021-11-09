# CalibreHentoid
A plugin for Calibre that reads the metadata stored by Hentoid

# Warning
This plugin and included script(s) are still in early developement and are likely to have some issues. Only use if you would like to contribute or are fine with some bugs.

# Requirements for use
install the \__init__.py file in the plugin directory into Calibre in the plugin menu in preferences or run `calibre-customize -b .`

books need to be zipped individually and saved as .cbz files

included in this repository (in the scripts folder) is a python script for automatically zipping comics in the .Hentoid directory

syntax is `hentoidArchiver.py -d path/to/.Hentoid -o path/to/output`

you should then be able to add the resulting book files using the Calibre interface while keeping all the tag information!