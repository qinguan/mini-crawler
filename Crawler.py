#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import threading
import urllib2
import BeautifulSoup
from Utils import *

class Crawler(threading.Thread):
    def __init__(self,
                 task_queue,
                 result_queue,
                 url_used_set,
                 keyword,
                 depth,
                 logger):
        threading.Thread.__init__(self)
        self.task_queue   = task_queue
        self.result_queue = result_queue
        self.url_used_set = url_used_set #url already was fethed, in order to reduce the number of deplicate url fething.
        self.keyword      = keyword
        self.depth        = depth
        self.logger       = logger
        self.daemon       = True
        self.start()
    
    def is_page_has_keyword(self,
                            text,
                            default_occurrence_number=1):
        '''
        if key word appears more than default_occurrence_number times in text, the text is treat as a page satisfied key word.
        '''
        import re
        patten = re.compile(self.keyword.lower())
        return len(patten.findall(text)) >= default_occurrence_number
        
    def analyse_page(self,
                     page_url_with_depth):
        '''
        page_url_with_depth = (url,depth)
        '''
        url   = page_url_with_depth[0]
        depth = page_url_with_depth[1]
        
        try:
            self.logger.info(self.getName() + ': analysing ' + url.encode('UTF-8','ignore') + ' depth= ' + str(depth))
        except:
            self.logger.error(self.getName() + ': ' + url.encode('UTF-8','ignore') + 'encode error.')
                
        try:
            context = safe_decode(urllib2.urlopen(url.encode('UTF-8','ignore')).read())
        except:
            self.logger.error(self.getName() + ': can not open the ' + url)
            return
            
        if context:
            # analyse the current page whether includes keyword or not,if yes,put (url,compress text) into result_queue.
            if self.is_page_has_keyword(context.encode('UTF-8','ignore')):
                self.result_queue.put((url.encode('UTF-8','ignore'),compress_text(context.encode('UTF-8','ignore'))))
                
            # if depth >= self.depth, namely the child page needn't be analysed.
            if depth >= self.depth:
                return
            
            # the current url's depth is small than the given depth. 
            # Analyse the current page and extract all urls.
            try:
                soup = BeautifulSoup.BeautifulSoup(context)
            except:
                return
            
            if not soup:
                return
            else:
                links = soup('a')
                
            for link in links:
                if 'href' in dict(link.attrs) and link['href'][0:4] == 'http':
                    # del the navigation location flag
                    url = link['href'].split('#')[0] 
                    
                    # del the '/' eg. http://www.baidu.com/ ==> http://www.baidu.com
                    url = url.strip('/') 
                    
                    # get the md5 value of url
                    url_hash_md5 = get_url_hashmd5(url)
                    
                    if url_hash_md5 not in self.url_used_set:
                    #if url not in self.url_used_set:
                        self.url_used_set.add(url_hash_md5)
                        #self.url_used_set.add(url)
                        self.task_queue.put((url,page_url_with_depth[1]+1))
                            
    def run(self):
        while True:
            if self.task_queue.empty():
                break
            task = self.task_queue.get()
            self.analyse_page(task)
            self.task_queue.task_done()
        self.logger.info(self.getName() + ': finished tasks and exit.')
        
if __name__ == '__main__':
    import Queue
    import logging
    logger = create_log(logg.INFO,logfile = 'db.log')
    task = Queue.Queue()
    result = Queue.Queue()
    task.put(('http://www.baidu.com',1))
    crawler = Crawler(task,result,[],'百度',2,logger)
    task.join()
    while True:
        if result.empty():
            break
        
        res = result.get()
        print res[0]
        result.task_done()
            
    print 'task done.'