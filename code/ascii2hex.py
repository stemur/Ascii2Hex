#!/usr/bin/python

import sys, getopt
import locale

locale.setlocale(locale.LC_NUMERIC, 'en_US')

# Global Variables
filesize = 0

def processfile(inputfile):
	global filesize
	lineno = 1
	try:
		with open(inputfile, 'r') as f:
			read_data = f.read(16)
			while read_data:
				filesize += len(read_data)
				outputdata(read_data, lineno)
				lineno += 1
				read_data = f.read(16)
	except IOError as e:
		print 'Error {0} : {1}'.format(e.errno, e.strerror)
		sys.exit(2)
	f.close()

def outputdata(asciidata, linenum):
	origdata = ''
	print '%08X ' % (linenum),
	for s in asciidata:
		# remove an CR or LF characters
		escchr = ['\n', '\r', '\f', '\v', '\b', '\a', '\e']
		print str(('0'+((hex(ord(s)))[2:]))[-2:]),
		if s in escchr:
			s = ' '
		origdata += s
	# Calc any missing spaces to align original data output.
	misspc = len(origdata) + (3*(16-len(asciidata)))+1
	print ' %s' % (origdata.rjust(misspc))
		
def main(argv):
	inputfile = ''
	usgstr = 'Correct useage is: ascii2hex -i <inputfile>'
	try:
		opts, args = getopt.getopt(argv,"i:",['ifile='])
	except getopt.GetoptError:
		print usgstr
		sys.exit(2)
	if len(opts) == 0:
		print "No options supplied. %s" % usgstr
		sys.exit()
	for opt, arg in opts:
		if opt == '-i':
			inputfile = arg
	if len(inputfile) == 0:
		print "No input file name supplied. %s" & usgstr
		sys.exit()
	print 'File Name : %s' % inputfile
	processfile(inputfile)
	print 'File size (bytes) : ' + locale.format('%i', filesize, grouping = True)

if __name__ == "__main__":
	main(sys.argv[1:])
