#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import threading
import urllib2
import BeautifulSoup

class Crawler(threading.Thread):
    def __init__(self,queue,depth,db_operator,logger):
        threading.Thread.__init__(self)
        self.queue = queue
        self.depth = depth
        self.context = None # the return value of urllib2.urlopen() function
        self.db_operator = db_operator
        self.logger = logger
        self.start()
        
    def run(self):
        while True:
            if self.queue.empty():
                break
            task = self.queue.get()
            # do something
            self.analyse_page(task)
            self.logger.info(self.getName() + ': analysing ' + task[0])
            
            self.queue.task_done()
    
    def is_legal_url(self,url):
        try:
            self.context = urllib2.urlopen(url).read()
            return True
        except:
            return False
    
    def is_indexed(self,url):
        '''
        if indexed, return True else False.
        '''
        res = self.db_operator.query_url(url)
        if res:
            return not len(res) == 0
        return False
    
    def add_url(self,url,text):
        '''
        add a url with link text to the database.
        '''
        try:
            if self.db_operator.insert_url(url,text):
                self.logger.info('add ' + url)
            else:
                self.logger.error('can not add ' + url + ' to database.')
        except:
            pass
    
    def analyse_page(self,page_url_with_depth):
        '''
        page_url_with_depth = (url,depth)
        '''
        
        if not self.is_legal_url(page_url_with_depth[0]):
            return 
        
        if self.is_indexed(page_url_with_depth[0]):
            return
       
        soup = BeautifulSoup.BeautifulSoup(self.context)
        links = soup('a')
        
        for link in links:
            if 'href' in dict(link.attrs) and link['href'][0:4] == 'http':
                # del the navigation location flag
                url = link['href'].split('#')[0] 
                
                # del the '/' eg. http://www.baidu.com/ ==> http://www.baidu.com
                url = url.strip('/') 
                
                # the url's depth is small the given depth and the url is not stored in db.
                if page_url_with_depth[1] < self.depth and not self.is_indexed(url):
                    self.queue.put((url,page_url_with_depth[1]+1))
                    self.add_url(url,link.text)
    
    def extract_text(self,soup):
        '''
        extract all text on given html page.
        '''
        text = [_ for _ in soup.body(text=True)]
        return ' '.join(text).encode(soup.originalEncoding)
    
    def is_page_meet_keyword(text,keyword,default_occurrence_number=5):
        '''
        if key word appears five times in text, the text is treat as a page satisfied key word.
        '''
        import re
        patten = re.compile(keyword)
        return len(patten.split(text)) >= default_occurrence_numbers
        