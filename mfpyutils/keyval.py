#!/usr/bin/python

#A key value db for embeded use

try:
	import cPickle as pickle
except:
	import pickle
import sqlite3
import os, sys
import atexit
import threading

class KeyVal(object):

	TABLE_CREATE = '''create table IF NOT EXISTS keyvalue ( key TEXT PRIMARY KEY , value TEXT)'''
	GET_KEY      = '''select value from keyvalue where key=?'''

	def __init__(self, db_path=':memory:'):
		#db path should be the path and name of the db file i.e. /tmp/keyval.db
		self.db = sqlite3.connect(db_path, isolation_level=None)
		atexit.register(self.close)
		self.db.execute(self.TABLE_CREATE)
		self.lock = threading.Lock()
		
	def get(self, key):
		with self.lock:
			result = self.db.execute(self.GET_KEY , ( key, ) )
			x=result.fetchone()
		if x:
			return pickle.loads(str(x[0]))
		else:
			return None
			
	def get_all(self):
		'''gets all key values pairs'''
		return [(k,pickle.loads(str(v))) for k,v in self.db.execute('''select * from keyvalue''')]
		
	def get_ns(self, ns):
		'''Gets all of the keys that start with ns.
			requres a '.' seperating ns and the remainder of the key'''
		if not ns.endswith('.'):
			ns += '.'
		results = []
		for k,v in self.get_all():
			if k.startswith(ns):
				k1=k.partition(ns)[2]
				results.append((k1,v))
		return results
			
	def set(self, key, value):
		pvalue = pickle.dumps(value)
		with self.lock:
			c = self.db.cursor()
			try:
				result = c.execute('''insert into keyvalue values ( ? , ? )''', ( key , pvalue ) )
			except sqlite3.IntegrityError:
				result = c.execute('''update keyvalue set value=? where key=? ''', ( pvalue , key ) )
			finally:
				self.db.commit()
	
	def close(self):
		try:
			print 'close'
			self.db.close()
		except:
			pass
		
if __name__ == '__main__':
	x = KeyVal()
	for i in range(10):
		x.set('xxx.yyy.%s' % i, i)
		
	
	
	
	
