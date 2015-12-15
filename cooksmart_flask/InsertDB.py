import sys
sys.path.insert(0,'/home/yoontae/Desktop/SoftDes2015-FinalProject')
import soeun
import mysql.connector

#list_grocery=soeun.main()
list_grocery=[u'great value chunk chicken breast', u'Walmart', u'12.5', u'oz', u'$5.46']
cnx = mysql.connector.connect(user='root', password='kaist0826',
                              host='localhost',
                              database='cooksmart')

cursor = cnx.cursor()
add_grocery = ("INSERT INTO Test "
           "(product,brand, amount, unit, price) "
           "VALUES (%s, %s, %s, %s, %s)")
data_grocery= (list_grocery[0],list_grocery[1],list_grocery[2],list_grocery[3],list_grocery[4])

cursor.execute(add_grocery, data_grocery)
emp_no=cursor.lastrowid

cnx.commit()

cursor.close()
cnx.close()