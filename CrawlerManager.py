#! /usr/bin/env python
# -*- coding: utf-8 -*-  

from Utils import *
from DatabaseOperator import *
from Crawler import *
import Queue

class CrawlerManager():
    def __init__(self,url,keyword,depth,task_queue,result_queue,thread_num,logger):
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.url = url
        self.keyword = keyword
        self.depth = depth
        self.thread_num = thread_num
        self.logger = logger
        self.init_tasks()
        
    def init_tasks(self):
        urls_text = extract_link_from__page(self.url)
        if len(urls_text):
            for url in urls_text:
                self.task_queue.put((url[0],1))  # url[0]-->url,url[1]-->text
                self.logger.info(url[0]+' depth=1, initial tasks queue.')
        self.logger.info('tasks initialization completed.*******************************')
        self.logger.info('A total of ' + str(self.task_queue.qsize()) + ' tasks.')
        print 'tasks initialization completed.*******************************'
        print 'A total of ' + str(self.task_queue.qsize()) + ' tasks.'
        
    def do_tasks(self):
        for _ in range(self.thread_num):
            Crawler(self.task_queue,self.result_queue,self.keyword,self.depth,self.logger)
        self.task_queue.join()
        self.logger.info('tasks done.')
        self.logger.info('A total of ' + str(self.result_queue.qsize()) + ' mactching results.')
        print 'tasks done.'
        print 'A total of ' + str(self.result_queue.qsize()) + ' mactching results.'
        
        
import pdb
pdb.set_trace

def get_task_queue_number(task_queue):
        print 'thread pool still has ', task_queue.qsize(), ' to complete.'
            
def monitor_task(task_queue):
    def task(task_queue):
        get_task_queue_number(task_queue)
            
    monitor(task)
        
if __name__ == '__main__':
    logger = set_log()
    task_queue = Queue.Queue()
    result_queue = Queue.Queue()
    crawlerManger = CrawlerManager('http://www.sina.com.cn','新浪',2,task_queue,result_queue,20,logger)
    #crawlerManger = CrawlerManager('http://www.google.com','新浪',2,task_queue,result_queue,10,logger)
    #monitor_task(task_queue)
    crawlerManger.do_tasks()
    print 'okkk'
    exit()
