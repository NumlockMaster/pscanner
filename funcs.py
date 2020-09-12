import os
import re
from datetime import datetime
import configparser
import exifread
import shutil
import filecmp


def getime():
    # Returns the current date and time in the format YYYYmmDDHHMMSS
    return datetime.now().strftime('%Y:%m:%d %H:%M:%S')

def dprint (s):
    # print the current time before str
    try:
        print(getime() + ' ' + s)

    except Exception as err:
        print(err)
        pass

    return

def load_regex(filename):
    # read all regular expressions from ini file
    parser = configparser.ConfigParser()
    parser.read(filename)
    list = []

    for section_name in parser.sections():
        r = parser[section_name]['expr']
        d = parser[section_name]['day']
        m = parser[section_name]['mon']
        y = parser[section_name]['year']
        list.append([r,d,m,y])
    return list

def get_original_datetime(file):
    dt = None  # init dt (date time) variable
    try:
        f = open(file, 'rb')
        tags = exifread.process_file(f)
        f.close()
        dt = str(tags.get('EXIF DateTimeOriginal'))

    except IOError:
        dprint('Unable to access file!')

    except Exception:
        raise

    return dt

def getsubstr(str, pos):
    f, t = pos.split(':')
    return str[int(f):int(t)]

def setnewdst(file, y, m, d):
    # set new file location in the format:
    # for windows: \YYYY\YYYY_MM\YYYY-MM-DD\file
    # for linux: /YYYY/YYYY_MM/YYYY-MM-DD/file
    return os.path.join(y, y + '_' + m, y + '-' + m + '-' + d, file)


def splitdatetime(dt):
    # gets a date and time YYYY:MM:DD HH:mm:ss and return the Year, Month and Day
    date = dt.split(" ")
    y, m, d = date[0].split(":")
    return y, m, d

def searchregex(file, list):
    # list is [[expr,day,month,year],[expr,day,month,year],....]
    newfilename = file
    i = 0  # a counter to go over all the regular expressions in the list
    while i < len(list) :
        reg = list[i][0]
        if re.match(reg, file):
            day = getsubstr(file, list[i][1])
            mon = getsubstr(file, list[i][2])
            year = getsubstr(file, list[i][3])
            newfilename = setnewdst(file, year, mon, day)
            break
        i += 1
    return newfilename


def copyfile(curfile: object, newfile: object) -> object:
    newdir = os.path.dirname(newfile)
    remove = True  # boolean variable to determine if need to delete the file after a successful copy operation
    copy = True  # boolean variable to determine if need to copy file

    if not os.path.exists(newdir):
        os.makedirs(newdir)

    # check if newfile already exist - if exist check if they are the same - if the same dont copy
    if os.path.isfile(newfile):
        if filecmp.cmp(curfile, newfile):
            dprint(curfile+' and '+newfile+' are the same!')
            dprint('Dont need to copy the file!')
            copy = False  # dont need to copy file

    if copy:
        dprint("copy " + curfile + " to " + newfile)
        try:
            shutil.copy(curfile, newfile)

        except Exception as error:
            dprint(error)
            dprint("Unable to copy file " + curfile)
            remove = False

    if remove:
        try:
            os.remove(curfile)
        except Exception as e:
            dprint(e)
            dprint('Unable to remove file: ' + curfile)
    else:
        dprint('Will not remove ' + curfile)

    return copy