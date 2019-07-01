#!/usr/bin/python

import sys
import getopt
import locale
import argparse

locale.setlocale(locale.LC_NUMERIC, 'en_US')


def processfile(inputfile):
    filesize = 0
    lineno = 1
    try:
        with open(inputfile, 'r') as f:
            print('File Name : %s' % inputfile)
            read_data = f.read(16)
            while read_data:
                filesize += len(read_data)
                outputdata(read_data, lineno)
                lineno += 1
                read_data = f.read(16)
    except IOError as e:
        print('Error %s : %s' % (e.errno, e.strerror))
        sys.exit(2)
    f.close()
    print('File size (bytes) : ' + locale.format_string('%i', filesize, grouping=True))


def outputdata(asciidata, linenum):
    origdata = ''
    print('%08X ' % linenum, end='')
    for s in asciidata:
        # remove any CR or LF characters
        escchr = ['\n', '\r', '\f', '\v', '\b', '\a']
        print(str(('0' + ((hex(ord(s)))[2:]))[-2:]), end='')
        if s in escchr:
            s = ' '
        origdata += s
    # Calc any missing spaces to align original data output.
    misspc = len(origdata) + (2 * (16 - len(asciidata))) + 1
    print(' %s' % (origdata.rjust(misspc)))


def main():
    my_parser = argparse.ArgumentParser(prog='ascii2hex.py',
                                        usage='%(prog)s [options] -i filename',
                                        description='Output the contents of a file in hex')
    my_parser.add_argument('-i', '--input', action='store',
                           metavar='filename',
                           dest='filename',
                           type=str, help='the file to be imported and output as hex.',
                           required=True)

    args = my_parser.parse_args()
    processfile(args.filename)


if __name__ == "__main__":
    main()
