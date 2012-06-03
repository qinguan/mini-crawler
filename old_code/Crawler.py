#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import threading
import urllib2
import BeautifulSoup
from DatabaseOperator import *
from Utils import *
import pdb
pdb.set_trace

class Crawler(threading.Thread):
    def __init__(self,task_queue,result_queue,url_got_list,keyword,depth,logger):
        threading.Thread.__init__(self)
        self.task_queue   = task_queue
        self.result_queue = result_queue
        self.url_got_list = url_got_list #url already was fethed, in order to reduce the number of deplicate url fething.
        self.keyword      = keyword
        self.depth        = depth
        self.context      = None 
        self.logger       = logger
        self.db_operator  = DatabaseOperator(self.logger)
        self.daemon = True
        self.start()
        
    def run(self):
        while True:
            if self.task_queue.empty():
                break
            task = self.task_queue.get()
            
            # do something
            #url_hash_md5 = get_url_hashmd5(task[0])
            #if url_hash_md5 not in self.url_got_list:
                #self.url_got_list.append(url_hash_md5)
                
            self.analyse_page(task)
            try:
                self.logger.info(self.getName() + ': analysing ' + task[0].encode('UTF-8') + ' depth= ' + str(task[1]))
                #print self.getName() + ': analysing ' + task[0].encode('UTF-8') + ' depth= ' + str(task[1])
            except:
                #print 'encode error.'
                self.logger.error('encode error.')
                        
            self.task_queue.task_done()
        self.logger.info(self.getName() + ' finished tasks and exit.')
        
    def is_page_has_keyword(self,text,default_occurrence_number=1):
        '''
        if key word appears one time in text, the text is treat as a page satisfied key word.
        '''
        import re
        patten = re.compile(self.keyword.lower())
        return len(patten.findall(text)) >= default_occurrence_number
        
    def analyse_page(self,page_url_with_depth):
        '''
        page_url_with_depth = (url,depth)
        '''
        url   = page_url_with_depth[0]
        depth = page_url_with_depth[1]
        
        try:
            self.context = safe_decode(urllib2.urlopen(url.encode('UTF-8')).read())
        except:
            self.logger.error('can not open the ' + url)
            
        if self.context:
            # analyse the current page whether includes keyword or not,if yes,put (url,compress text) into result_queue.
            if self.is_page_has_keyword(self.context.encode('UTF-8')):
                self.result_queue.put((url,compress_text(self.context.encode('UTF-8'))))
                
            try:
                soup = BeautifulSoup.BeautifulSoup(self.context)
                if not soup:
                    return 
            except:
                return
                
            # if depth >= self.depth, namely the child page needn't be analysed.
            if depth >= self.depth:
                return 
            
            # the current url's depth is small than the given depth. Analyse the current page and extract all urls.
            links = soup('a')
            for link in links:
                if 'href' in dict(link.attrs) and link['href'][0:4] == 'http':
                    # del the navigation location flag
                    url = link['href'].split('#')[0] 
                    
                    # del the '/' eg. http://www.baidu.com/ ==> http://www.baidu.com
                    url = url.strip('/') 
                    
                    # get the md5 value of url
                    #url_hash_md5 = get_url_hashmd5(url)
                    
                    # url_hash_md5 not in self.url_got_list:
                    if url not in self.url_got_list:
                        self.task_queue.put((url,page_url_with_depth[1]+1))
                        #self.url_got_list.append(url_hash_md5)
                        self.url_got_list.append(url)
                    
if __name__ == '__main__':
    import Queue
    from Utils import *
    from DatabaseOperator import *
    logger = set_log()
    task = Queue.Queue()
    result = Queue.Queue()
    task.put(('http://www.sina.com.cn',0))
    crawler = Crawler(task,result,[],'Right',1,logger)
    task.join()
    print 'task done.'
    while True:
        if result.empty():
            break
        res = result.get()
        print res
        result.task_done()