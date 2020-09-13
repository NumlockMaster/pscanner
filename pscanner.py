import sys
from funcs import *

def init():
	#  Check usage and setup initial parameters
	dict = {
		'copyflag': False,
		'srcdir': '',
		'dstdir': '',
		'basedir': '',
		'initstat': 0
	}

	if (len(sys.argv) < 3 or len(sys.argv) > 4):
		print("Usage: " + os.path.basename(sys.argv[0]) + " [-c] <Source Directory> <Destination Directory>")
		print("This utility scan source directory and copy all images to the following directory structure:")
		print("<destination dir>\YYYY\YYYY_MM\YYYY-MM-DD\\file")
		print("-c - Copy files")
		dict.update({"initstat": -1})
	else:
		dict.update({"basename": os.path.basename(sys.argv[0])})
		dprint('Running ' + dict["basedir"])

		argvlen = len(sys.argv)
		i = 1
		while i < argvlen:
			if sys.argv[i] == "-c":
				dict.update({"copyflag": True})
			else:
				dict.update({"srcdir": sys.argv[i]})
				dict.update({"dstdir": sys.argv[i+1]})
				dprint('Source dir: ' + dict["srcdir"])
				dprint('Destination dir: ' + dict["dstdir"])
				i+=1
			i+=1
		dict.update({"initstat": 0})

	return dict

def main():

	params = init() 			# init parameters and check usage
	check = params["initstat"]  # get status of init
	if check == -1:
		sys.exit(check)

	cnt = 0 							# count number of files processed
	copycnt = 0  						# counter of copied files
	expr_list = load_regex('reg.ini')	# load all regular expressions into a list

	# scan all directories and search for image/video files
	if os.path.isdir(params["srcdir"]):
		for root, dirs, files in os.walk(params["srcdir"]):
			for file in files:
				newfiledir = params["dstdir"]
				cnt += 1
				curfile = os.path.join(root, file)
				try:
					datetime = get_original_datetime(curfile)

				except Exception as err:
					dprint('Cant get info from file!')
					dprint(err)
					datetime = 'None'

				if datetime != 'None':
					# if a date was found using EXIF
					dateval = split_datetime(datetime)
					newfilename = setnewdst(file, dateval[0], dateval[1], dateval[2])
				else:
					# try to search a matching pattern
					newfilename = searchregex(file, expr_list)
					if newfilename == file:
						# did not find a matching pattern
						newfiledir =  os.path.join(params["dstdir"], 'unknown')
						if not os.path.exists(newfiledir):
							os.makedirs(newfiledir)

				newfile = os.path.join(newfiledir, newfilename)

				dprint(curfile + ' --> ' + newfile)

				if params["copyflag"]:
					# need to copy file to new location
					if copyfile(curfile, newfile):
						copycnt+=1

	dprint('Processed ' + str(cnt) + ' files!')
	dprint('Only ' + str(copycnt) + ' files were copied!')
	dprint('Have a nice day!')


if __name__ == "__main__":
	main()
