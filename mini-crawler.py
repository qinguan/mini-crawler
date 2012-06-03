#! /usr/bin/env python
# -*- coding: utf-8 -*-  

from Utils import *
from CrawlerManager import *
import Queue

def start_program():
    options, args = set_optparse()
    
    if options.testself:
        return CrawlerManager('http://www.google.com','google',2,create_log(logging.INFO,'logfile'),'database',5).do_tasks()
        
    if options.url == None:
        print 'plz input a seed url!'
        return
    url = options.url
    
    if options.depth == None:
        depth = 2
        #print 'plz input the depth of page!'
    depth = int(options.depth)
    
    if options.threadnumber == None:
        threadnumber = 10
    else:
        threadnumber = int(options.threadnumber)
    
    if options.dbfile == None:
        dbfile = 'mini-crawler.db'
    else:
        dbfile = options.dbfile
        
    if options.loglevel == None:
        loglevel = logging.INFO
    elif int(options.loglevel) == 1:
        loglevel = logging.DEBUG
    elif int(options.loglevel) == 2:
        loglevel = logging.INFO
    elif int(options.loglevel) == 3:
        loglevel = logging.WARNING
    elif int(options.loglevel) == 4:
        loglevel = logging.ERROR
    elif int(options.loglevel) == 5:
        loglevel = logging.CRITICAL
        
    if options.logfile == None:
        logfile = 'mini-crawler.log'
    else:
        logfile = options.logfile        
        
    if options.keyword == None:
        print 'plz imput the key word!'
        return 
    keyword = options.keyword
    
    logger = create_log(loglevel,logfile)
    CrawlerManager(url,keyword,depth,logger,dbfile,threadnumber).do_tasks()
    
if __name__ == '__main__':
    start_program()
