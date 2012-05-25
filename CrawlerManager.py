#! /usr/bin/env python
# -*- coding: utf-8 -*-  

from Utils import *
from DatabaseOperator import *
from Crawler import *
import Queue

class CrawlerManager():
    def __init__(self,url,depth,thread_num,db_operator,logger):
        self.queue = Queue.Queue()
        self.url = url
        self.depth = depth
        self.thread_num = thread_num
        self.db_operator = db_operator
        self.logger = logger
        self.init_tasks()
        
    def init_tasks(self):
        urls_text = extract_link_from__page(self.url)
        if len(urls_text):
            for url in urls_text:
                self.queue.put((url[0],1))  # url[0]-->url,url[1]-->text
                self.db_operator.insert_url(url[0],url[1])
                self.logger.info(url[0])
        self.logger.info('taske init completed.')
        
    def do_tasks(self):
        for _ in range(self.thread_num):
            Crawler(self.queue,self.depth,self.db_operator,self.logger)
        self.queue.join()
        self.logger.info('tasks done.')
        
if __name__ == '__main__':
    logger = init_log()
    db_operator = DatabaseOperator(logger)
    crawlerManger = CrawlerManager('http://www.baidu.com',2,10,db_operator,logger)
    crawlerManger.do_tasks()
    print 'okkk'
    exit()