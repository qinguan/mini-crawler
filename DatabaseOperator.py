#! /usr/bin/env python
# -*- coding: utf-8 -*-  

from sqlalchemy import *
from sqlalchemy.sql import *

class DatabaseOperator():
    def __init__(self,logger):
        self.db_connect = None
        self.urls_table = None
        self.logger = logger
        self.init_database()
    
    def init_database(self,dbname = 'crawler.db'):
        try:
            engine = create_engine('sqlite:///' + dbname)
        except:
            self.logger.error('can not create database.')
        metadata = MetaData()
        self.urls_table = Table('urls',metadata,
                        Column('url',String,primary_key = True),
                        Column('text',String)
                        )
        metadata.create_all(engine)
        self.db_connect = engine.connect()

    def insert_url(self,url,text=''):
        try:
            ins_url = self.urls_table.insert().values(url = url, text = text)
            self.db_connect.execute(ins_url)
            #print 'insert %s %s ok' % (url,text)
            #self.logger.info('insert ' + url + ' ' + text + ' ok.')
            return True
        except:
            #print 'can not insert (%s,%s)' % (url,text)
            #self.logger.info('can not insert ' + url +' ' + text)
            return False
            
    def query_url(self,url):
        try:
            query_url = self.urls_table.select(self.urls_table.c.url == url)
            return self.db_connect.execute(query_url).fetchall()
        except:
            #print 'query %s failed.' % url
            return None
            
    def delete_url(self,url):
        try:
            del_url = self.urls_table.delete().where(self.urls_table.c.url == url)
            self.db_connect.execute(del_url)
            print 'delete ok'
        except:
            print 'can not delete the url.'
            
    def query_all(self):
        return self.db_connect.execute(self.urls_table.select()).fetchall()
        
if __name__ == '__main__':
    from Utils import *
    logger = init_log()
    dbOp = DatabaseOperator(logger)
    dbOp.init_database('crawler.db')
    #dbOp.insert_url('http://www.baidu.com','baidu')
    res = dbOp.query_all()
    for i in res:
        print i
    #print dbOp.insert_url('http://www.baidu.com','baidu')
    #print not len(dbOp.query_url('http://www.baidu.com')) == 0
    #dbOp.delete_url(u'http://www.baidu.com')
    