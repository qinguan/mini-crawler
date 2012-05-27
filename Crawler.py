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
    def __init__(self,task_queue,result_queue,keyword,depth,logger):
        threading.Thread.__init__(self)
        self.task_queue   = task_queue
        self.result_queue = result_queue
        self.keyword      = keyword
        self.depth        = depth
        self.context      = None # the return value of urllib2.urlopen() function
        self.logger       = logger
        self.db_operator  = DatabaseOperator(self.logger)
        self.start()
        
    def run(self):
        while True:
            if self.task_queue.empty():
                break
            task = self.task_queue.get()
            
            # do something
            self.analyse_page(task)
            #self.logger.info(self.getName() + ': analysing ' + task[0] + ' depth= ' + str(task[1]))
            try:
                print self.getName() + ': analysing ' + task[0].encode('UTF-8') + ' depth= ' + str(task[1])
            except:
                print 'encode error.'
            
            self.task_queue.task_done()
        self.logger.info(self.getName() + ' finished tasks and exit.')
    
    def extract_text(self,soup):
        '''
        extract all text on html body in given html page.
        '''
        if getattr(soup,'body'):
            text = ' '.join([_ for _ in soup.body(text=True)])
            return text#.encode(soup.originalEncoding)
    
    def is_page_has_keyword(self,text,default_occurrence_number=1):
        '''
        if key word appears one time in text, the text is treat as a page satisfied key word.
        '''
        import re
        patten = re.compile(self.keyword.lower())
        return len(patten.split(text)) >= default_occurrence_number
        
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
            try:
                soup = BeautifulSoup.BeautifulSoup(self.context)
                if not soup:
                    return 
            except:
                return
            
            # analyse the current page whether includes keyword or not,if yes,store it into result_queue.
            page_text = self.extract_text(soup)
            if page_text and self.is_page_has_keyword(page_text):
                self.result_queue.put((url,page_text))
        
            # analyse the current page and extract all urls.
            links = soup('a')
            for link in links:
                if 'href' in dict(link.attrs) and link['href'][0:4] == 'http':
                    # del the navigation location flag
                    url = link['href'].split('#')[0] 
                    
                    # del the '/' eg. http://www.baidu.com/ ==> http://www.baidu.com
                    url = url.strip('/') 
                    
                    # the url's depth is small than the given depth.
                    if page_url_with_depth[1] < self.depth:# and not self.is_indexed(url):
                        self.task_queue.put((url,page_url_with_depth[1]+1))
                    
if __name__ == '__main__':
    import Queue
    from Utils import *
    from DatabaseOperator import *
    logger = set_log()
    task = Queue.Queue()
    result = Queue.Queue()
    task.put(('http://www.sina.com.cn',0))
    crawler = Crawler(task,result,'Rights',1,logger)
    task.join()
    print 'task done.'
    while True:
        if result.empty():
            break
        res = result.get()
        print res
        result.task_done()
    exit()