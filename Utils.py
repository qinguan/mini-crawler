#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import urllib2
import BeautifulSoup
import logging

def init_log(logfile = 'crawler.log'):
    '''
    output log to logfile.
    '''
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s  ')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


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
    
def extract_link_from__page(url):
    '''
    extract all links and corresponding text in given html page provided in url.
    just used in init the tasks.
    '''
    try:
        context = urllib2.urlopen(url).read()
    except:
        print 'can not open %s' % url
        
    result = []
    soup = BeautifulSoup.BeautifulSoup(safe_decode(context))
    links = soup('a')
    
    for link in links:
        if 'href' in dict(link.attrs) and link['href'][0:4] == 'http':
            # del the navigation location flag
            url = link['href'].split('#')[0] 
            
            # del the '/' eg. http://www.baidu.com/ ==> http://www.baidu.com
            url = url.strip('/') 
            result.append((url,link.text))
            
    return result
    
        
#test:
if __name__ == '__main__':
    logger = init_log()
    logger.error('KKKKKKK')
    #print extract_link_from__page('http://www.baidu.com')
        
    