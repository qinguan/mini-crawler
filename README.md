mini crawler
=====================

Hello!

This is a simple tool to fetch specified context from the Internet.

## usage:
python mini-crawler.py -u 'www.baidu.com' -d 2 -l logfile -L 2 -n 10 -f database.file -k='python'

you can type the command under CLI to get more information:

	$ python mini-crawler.py -h
	Usage: mini-crawler.py [options] arg1 arg2

	Options:
	  -h, --help            show this help message and exit
	  -u URL, --url=URL     the url which the script starts from.
	  -d DEPTH, --depth=DEPTH
							the depth of script will dig into where the initial
							url_depth=0.
	  -l LOGFILE, --logfile=LOGFILE
							a file the script log will be written into.
	  -L LOGLEVEL, --loglevel=LOGLEVEL
							the level which log will be output,you can use
							DEBUG--1,INFO--2,WARNING--3,ERROR--4,CRITICAL--5.
	  -t, --testself        use default setting:url--www.google.com
	  -n THREADNUMBER, --thread number=THREADNUMBER
							the thread number which script will initialize.
	  -f DBFILE, --database file=DBFILE
							the file where sqlite databse locates.
	  -k KEYWORD, --key=KEYWORD
							word given more attention on html page.
