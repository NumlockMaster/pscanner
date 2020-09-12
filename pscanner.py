import sys
from funcs import *

def init():

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

	# check the parameters from command line
	params = init()
	check = params["initstat"]
	if check == -1:
		sys.exit(check)

	cnt = 0 # count number of files processed

	# load all regular expressions into a list
	expr_list = load_regex('reg.ini')

	# scan all directories and search for image/video files
	if os.path.isdir(params["srcdir"]):
		for root, dirs, files in os.walk(params["srcdir"]):
			for file in files:
				cnt += 1
				try:
					datetime = get_original_datetime(os.path.join(root, file))

				except Exception as err:
					dprint('Cant get info from file!')
					dprint(err)
					datetime = 'None'

				if datetime != 'None':
					dateval = splitdatetime(datetime)
					newfilename = setnewdst(file, dateval[0], dateval[1], dateval[2])
				else:
					newfilename = searchregex(file, expr_list)

				newfile = os.path.join(params["dstdir"], newfilename)
				dprint(file + ' --> ' + newfile)

				if params["copyflag"]:
					# need to copy file to new location
					curfile = os.path.join(params["srcdir"], file)
					copyfile(curfile, newfile)

	dprint('Processed ' + str(cnt) + ' files!')
	dprint('Have a nice day!')


if __name__ == "__main__":
	main()
