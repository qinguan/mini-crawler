#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import urllib2
import BeautifulSoup
from Utils import *
from Crawler import *
from DatabaseOperator import *
import Queue

class CrawlerManager():
    def __init__(self,
                 url,
                 keyword,
                 depth,
                 #task_queue,
                 #result_queue,
                 #url_used_set,
                 logger,
                 dbfile,
                 thread_num=10,
                 interval=10):
        self.task_queue = Queue.Queue()#task_queue
        self.result_queue = Queue.Queue()#result_queue
        self.url = url
        self.keyword = keyword
        self.depth = depth
        self.url_used_set = set() #url_used_set
        self.dbfile = dbfile
        self.thread_num = thread_num
        self.logger = logger
        self.interval = interval
        self.init_tasks()
    
    def extract_link_from__page(self):
        '''
        extract all links and corresponding text in given html page provided in url.
        '''
        try:
            context = urllib2.urlopen(self.url).read()
        except:
            self.logger.error('CrawlerManager: can not open ' + self.url)
            return
            
        result = []
        try:
            soup = BeautifulSoup.BeautifulSoup(safe_decode(context))
        except:
            self.logger.error('CrawlerManager: ' + self.url + ' page context is None.')
            return
        
        links = soup('a')

        for link in links:
            if 'href' in dict(link.attrs) and link['href'][0:4] == 'http':
                # del the navigation location flag
                url = link['href'].split('#')[0] 
                
                # del the '/' eg. http://www.baidu.com/ ==> http://www.baidu.com
                url = url.strip('/ \n') 
                result.append((url,link.text))
                
        return result

    def init_tasks(self):
        urls_list = self.extract_link_from__page()
        if not urls_list:
            self.logger.info('CrawlerManager: ***************no tasks.***************')
            return
        
        urls_list = list(set(urls_list))
        for url in urls_list:
            self.task_queue.put((url[0],2))  # url[0]-->url,url[1]-->text
                
        self.logger.info('CrawlerManager: *******************************************************')
        self.logger.info('CrawlerManager: ***************tasks initialization completed.***************')
        self.logger.info('CrawlerManager: *****************A total of ' + str(self.task_queue.qsize()) + ' tasks initialized.*****************')
        self.logger.info('CrawlerManager: *******************************************************')
        
    def do_tasks(self):
        for _ in range(self.thread_num):
            Crawler(self.task_queue,self.result_queue,self.url_used_set,self.keyword,self.depth,self.logger)
            
        # if got results, store it
        self.submit_thread()
        
        # monitor the task until finish all the task.
        self.monitor()
        
        #self.task_queue.join()
        self.logger.info('CrawlerManager: *******************tasks done.*******************')
        self.logger.info('CrawlerManager: A total of ' + str(self.result_queue.qsize()) + ' mactching results.')
        
        #test:
        while not self.result_queue.empty():
            self.logger.info('CrawlerManager: ' + self.result_queue.get()[0].encode('UTF-8','ignore'))
            self.result_queue.task_done()
            
        print len(self.url_used_set)
        for _ in self.url_used_set:
            print _
        #test
            
    def submit_result(self):
        dbOp = DatabaseOperator(logger = self.logger, dbfile = self.dbfile)
        while True:
            if self.task_queue.empty() and self.result_queue.empty():
                break
            elif not self.result_queue.empty():
                #print 'result: ',self.result_queue.qsize()
                res = self.result_queue.get()
                dbOp.insert_item(res[0],res[1])
                self.result_queue.task_done()
            elif not self.task_queue.empty(): 
                time.sleep(10)
        dbOp.logger.info('************submit thread is existing.*****************')
                
    def submit_thread(self):
        res_thread = threading.Thread(target = self.submit_result, name = 'Sumbit_Thread')
        res_thread.start()
                
            
    def monitor(self):
        while True:
            time.sleep(self.interval)
            if self.task_queue.qsize() > 0:
                print 'left task: ', self.task_queue.qsize()
                print 'got results:', self.result_queue.qsize()
                time.sleep(self.interval)
            else:
                print 'left task---',self.task_queue.qsize()
                break
            
if __name__ == '__main__':
    import Queue
    import logging
    logger = create_log(logging.INFO,logfile = 'crawler.log')
    crawlerManger = CrawlerManager('http://www.163.com','iPhone',2,logger,'database',10)
    crawlerManger.do_tasks()
    print '**************finished*******************'