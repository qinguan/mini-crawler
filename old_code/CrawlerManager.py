#! /usr/bin/env python
# -*- coding: utf-8 -*-  

from Utils import *
from DatabaseOperator import *
from Crawler import *
import Queue
from Monitor import *

class CrawlerManager():
    def __init__(self,url,keyword,depth,task_queue,result_queue,url_got_list,thread_num,logger):
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.url = url
        self.keyword = keyword
        self.depth = depth
        self.url_got_list = url_got_list
        self.thread_num = thread_num if thread_num else 10
        self.logger = logger
        self.init_tasks()
        
    def init_tasks(self):
        urls_text = extract_link_from__page(self.url)
        if urls_text and len(urls_text):
            for url in urls_text:
                self.task_queue.put((url[0],2))  # url[0]-->url,url[1]-->text
                #self.logger.info(url[0]+' depth=2, initial tasks queue.')
        self.logger.info('tasks initialization completed.*******************************')
        self.logger.info('A total of ' + str(self.task_queue.qsize()) + ' tasks initialized.')
        
    def do_tasks(self):
        #monitor = Monitor(self.task_queue)
        commit_thread = self.CommitResult(self.result_queue)
        for _ in range(self.thread_num):
            Crawler(self.task_queue,self.result_queue,self.url_got_list,self.keyword,self.depth,self.logger)
        while True:
            time.sleep(5)
            if self.task_queue.qsize() > 0:
                print self.task_queue.qsize(),'task---1'
                print self.result_queue.qsize(),'result---1'
                time.sleep(5)
            else:
                print self.task_queue.qsize(),'---0'
                commit_thread.set_flag()
                commit_thread.join()
                break
        #self.task_queue.join()
        self.logger.info('tasks done.')
        self.logger.info('A total of ' + str(self.result_queue.qsize()) + ' mactching results.')
        while not self.result_queue.empty():
            print self.result_queue.get()[0].encode('UTF-8')
            self.result_queue.task_done()
            
        
    class CommitResult(threading.Thread):
        def __init__(self,queue,flag = 0,logfile = 'crawler_database.log'):
            threading.Thread.__init__(self)
            self.queue = queue
            self.flag = flag
            self.database = DatabaseOperator(logger = set_log(logfile))
            self.start()
            
        def set_flag(self):
            self.flag = 1
            
        def commit(self):
            while True:
                if self.flag:
                    break
                
                if self.queue.empty():
                    time.sleep(5)
                result = self.queue.get()
                try:
                    self.database.insert_url(result[0],result[1])
                except:
                    self.database.logger.error(result[0] + 'commit failed.')
                
                self.queue.task_done()
                
        
        def run(self):
            self.commit()
            
            
import pdb
pdb.set_trace
    
if __name__ == '__main__':
    logger = set_log()
    task_queue = Queue.Queue()
    result_queue = Queue.Queue()
    #crawlerManger = CrawlerManager('http://www.sina.com.cn','国务院',2,task_queue,result_queue,[],30,logger)
    #crawlerManger = CrawlerManager('http://www.163.com','国务院',2,task_queue,result_queue,[],30,logger)
    crawlerManger = CrawlerManager('http://www.google.com','google',2,task_queue,result_queue,[],20,logger)
    #monitor_task(task_queue)
    crawlerManger.do_tasks()
    print '**************finished*******************'
    exit()
