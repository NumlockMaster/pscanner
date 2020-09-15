# pscanner.py
#
If you have thousands of unsorted pictures on your disk and you want to organize them, pscanner.py is the tool for you.
<br><br>
pscanner.py can organize unsorted picture files by their EXIF\DateTimeOriginal.<br><br>
pscanner.py will go over the source directory and all sub-directories, try to find the date when the picture was taken, and move the picture file to a matching directory.
pscanner.py will try to get the date from the picture file using exifread library. if it is unable to get the date using exifread, then it will try to get the date from the file name, using regular expressions.<br>
<br>
All the regular expressions are written in the reg.ini file.<br>
<br>
The new directory structure will be created as: YYYY\YYYY_MM\YYYY-MM-DD (year\year_mon\year-mon-day). 
<br><br>
Usage: pscanner.py \[-c\] \<source directory\> \<destination directory\>
