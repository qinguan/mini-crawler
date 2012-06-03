#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import logging
import zlib
import hashlib

def create_log(loglevel,logfile):
    '''
    set log param.
    '''
    #test
    import os 
    if os.path.exists(logfile):
        os.remove(logfile)
    #test
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s  ')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(loglevel)
    return logger

def set_optparse():
    '''
    module_name.py -u 'www.baidu.com' -d 2 -l log.txt -L 2 -n 10 -f hello.txt -k='python'
    
    output:
    (<Values at 0x1bd21c0: {'dbfile': 'hello.txt', 'keyword': "='python'", 'threadnumber': '10', \
    'url': "'www.baidu.com'", 'loglevel': '2', 'depth': '2', 'testself': None, 'logfile': 'log.txt'}>, [])
    '''
    from optparse import OptionParser
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    #parser.add_option('-h', '--help', action = 'store', help = 'a mini tool for fetching information with given keyword.')
    parser.add_option('-u', '--url', action = 'store', dest = 'url', help = 'the url which the script starts from.')
    parser.add_option('-d', '--depth', action = 'store', dest = 'depth', help = 'the depth of script will dig into where the initial url_depth=0.')
    parser.add_option('-l', '--logfile', action = 'store', dest = 'logfile', help = 'a file the script log will be written into.')
    parser.add_option('-L', '--loglevel',action = 'store', dest = 'loglevel', help = 'the level which log will be output.')
    parser.add_option('-t', '--testself', action = 'store_true', dest = 'testself', default=False)
    parser.add_option('-n','--thread number', action = 'store', dest = 'threadnumber', help = 'the thread number which script will initialization.')
    parser.add_option('-f', '--database file', action = 'store', dest = 'dbfile', help = 'the file where sqlite databse locates.')
    parser.add_option('-k', '--key', action = 'store', dest = 'keyword', help = 'word given more attention on html page.')
    
    (options, args) = parser.parse_args()
    return options, args

def safe_decode(orig):  
    '''
    decode the html to unicode.
    '''
    try:  
        return orig.decode('utf8')  
    except UnicodeDecodeError:  
        pass  
    try:  
        return orig.decode('gb2312')  
    except UnicodeDecodeError:  
        pass  
    try:  
        return orig.decode('gbk')  
    except UnicodeDecodeError:  
        pass  
    try:  
        return orig.decode('big5')  
    except UnicodeDecodeError:  
        pass 

def get_url_hashmd5(url):
    return hashlib.md5(url.encode('UTF-8','ignore')).hexdigest()

def compress_text(text):
    return zlib.compress(text)

def decompress_text(zlib_text):
    return zlib.decompress(zlib_text)