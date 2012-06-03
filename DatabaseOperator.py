#! /usr/bin/env python
# -*- coding: utf-8 -*-  

from sqlalchemy import *
from sqlalchemy.sql import *
from Utils import *

class DatabaseOperator():
    def __init__(self,
                 logger,
                 dbfile):
        self.logger = logger
        self.dbfile = dbfile
        self.db_connect = None
        self.urls_table = None
        self.init_database()
        
    def init_database(self):
        try:
            engine = create_engine('sqlite:///' + self.dbfile)
            metadata = MetaData()
            self.urls_table = Table('urls',metadata,
                            Column('url',String,primary_key = True),
                            Column('text',String)
                            )
            metadata.create_all(engine)
            self.db_connect = engine.connect()
        except:
            self.logger.error('atabaseOperator: can not create or connect database.')
        
        
    def insert_item(self,
                    url,
                    text=''):
        try:
            if not text:
                ins_url = self.urls_table.insert().values(url = unicode(url, errors='ignore'), text = text)
            ins_url = self.urls_table.insert().values(url = unicode(url, errors='ignore'), text = unicode(text,errors='ignore'))
            self.db_connect.execute(ins_url)
            #self.logger.info('DatabaseOperator: insert ' + url + ' ' + text + ' ok.')
            self.logger.info('DatabaseOperator: insert ' + url + ' ok.')
            return True
        except:
            self.logger.error('databaseOperator: can not insert ' + url)
            return False
        
    def query_all(self):
        return self.db_connect.execute(self.urls_table.select()).fetchall()
    
if __name__ == '__main__':
    from Utils import *
    import logging
    logger = create_log(logging.INFO,logfile = 'db.log')
    db = DatabaseOperator(logger = logger,dbfile = 'test.db')
    #db.insert_item('www.baidu.com','huhu')
    res = db.query_all()
    print len(res)
    for i in res:
        print i[0]
        print