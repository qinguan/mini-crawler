#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import threading

class Monitor(threading.Thread):
    def __init__(self,task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.daemon = True
        self.start()
        
    def monitor(self,fun,time_length = 10):
        from threading import Timer
        import time
        half_time = time_length/2
        while True:
            if self.task_queue.qsize() == 0:
                break
            t = Timer(half_time,fun)
            t.start()
            time.sleep(time_length - half_time)
        print 'over!!!'
        
    def get_task_queue_number(self):
        if self.task_queue.qsize():
            print 'task_queue still has ', self.task_queue.qsize(), ' tasks to do.'
        else:
            print 'monitor is existing.'
            
    def run(self):
        self.monitor(self.get_task_queue_number)