#!/usr/bin/python
import MySQLdb
import sys
sys.path.insert(0,'/home/jong/Desktop/SoftDes2015-FinalProject/cooksmart_flask/FlaskApp/')
#import merge1
import soeun
#import mysql.connector
import find_stores

def config(name_list,unit_list,amount_list):
	global indb_num
	global cache_data
	global store_inventory
	global names
	global amounts
	global units
	indb_num=[]
	cache_data=[]
	store_inventory=[]
	names = soeun.refine_name(name_list)
	amounts = soeun.unify_recipe_unit(amount_list, unit_list)[0]
	units = soeun.unify_recipe_unit(amount_list, unit_list)[1]

	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="cooksmart",  # your password
	                     db="cooksmart")        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	global cur
	cur = db.cursor()

	#check name number which is included in the cache 

	#waldb_num=names

def checkexist():
	for i in range(len(names)):

		name=names[i]
		check_exist="SELECT EXISTS(SELECT * FROM cache WHERE product LIKE '%"+name+"%')"	
		cur.execute(check_exist)
		# print all the first cell of all the rows
		for row in cur.fetchall():
			
			print row
			if row[0]!=0:
				indb_num.append(i)
				#del waldb_num[i]
	print indb_num

def find_cache_data():
	checkexist()
	for j in indb_num:
		name=names[j]
		
		find_data="SELECT * FROM cache WHERE product LIKE '%"+name+"%' LIMIT 1"
		cur.execute(find_data)
		# print all the first cell of all the rows
		for row in cur.fetchall():
			print row
			cache_data.append(row)

	for index in sorted(indb_num, reverse=True):
		# remove the data which is in the database
		del names[index]
		del amounts[index]
		del units[index]
	return cache_data

## search local DB and look for proper local shops
def find_local_data(storedic):
	stores=storedic.keys()
	for store in stores:
		
		#num_inventory
		# store=stores[index]
		
		# a=store.split(' ')
		# store = ' '.join(a)
		#print store
		a=store.split("'")
		store=' '.join(a)
		a=store.split(" ")
		store=' '.join(a[:2])
		find_store_ex="SELECT * FROM GroceryUPC WHERE brand LIKE '%"+store+"%' LIMIT 1"
	
		cur.execute(find_store_ex)
		for row in cur.fetchall():
			#print row
			store_inventory.append(row[3])
		return store_inventory
