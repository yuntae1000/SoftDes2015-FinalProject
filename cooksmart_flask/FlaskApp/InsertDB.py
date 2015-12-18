import sys
sys.path.insert(0,'/home/jong/Desktop/SoftDes2015-FinalProject/cooksmart_flask/FlaskApp/')
import soeun
import mysql.connector

def searchnotindb(name_list,amount_list,unit_list):

	list_grocery=soeun.main(name_list, amount_list, unit_list)
	cnx = mysql.connector.connect(user='root', password='cooksmart',
	                              host='localhost',
	                              database='cooksmart')
	cursor = cnx.cursor()
	for i in range(len(list_grocery)):
		db_grocery=list_grocery[i]
	#list_grocery=[u'coffee', u'Walmart', u'10', u'oz', u'$7.46']



		add_grocery = ("INSERT INTO cache "
		           "(product,amount, unit, price, brand, set_num) "
		           "VALUES (%s, %s, %s, %s, %s, %s)")
		data_grocery= (db_grocery[0],db_grocery[1],db_grocery[2],db_grocery[3],db_grocery[4],db_grocery[5])

		cursor.execute(add_grocery, data_grocery)
		emp_no=cursor.lastrowid
		print emp_no

	cnx.commit()
	cursor.close()
	cnx.close()
	return list_grocery