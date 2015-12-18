#!/usr/bin/python
import MySQLdb
import sys
sys.path.insert(0,'/home/yoontae/Desktop/SoftDes2015-FinalProject')
#import merge1
import soeun
#import mysql.connector
import find_stores

stores=find_stores.a.datalist2

names = soeun.refine_name(soeun.name_list)
amounts = soeun.unify_recipe_unit(soeun.amount_list, soeun.unit_list)[0]
units = soeun.unify_recipe_unit(soeun.amount_list, soeun.unit_list)[1]

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="cooksmart",  # your password
                     db="cooksmart")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

#check name number which is included in the cache 
indb_num=[]
#waldb_num=names

# Use all the SQL you like
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

for j in indb_num:
	name=names[j]
	
	find_data="SELECT * FROM cache WHERE product LIKE '%"+name+"%' LIMIT 1"
	cur.execute(find_data)
	# print all the first cell of all the rows
	for row in cur.fetchall():
		print row

#print waldb_num
for index in sorted(indb_num, reverse=True):
	# remove the data which is in the database
	del names[index]
	del amounts[index]
	del units[index]

print names
print amounts
print units

## search local DB and look for proper local shops
for store in stores:
	# store=stores[index]
	# store=str(store)
	# a=store.split(' ')
	# store = ' '.join(a)
	# print store
	
	find_store_ex="SELECT * FROM GroceryUPC WHERE brand LIKE "+store
	cur.execute(find_store_ex)

	# print all the first cell of all the rows
	for row in cur.fetchall():
		print row