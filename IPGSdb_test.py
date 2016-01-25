#Test class for IPGSdb.py 

from IPGSdb import *

def testUsers():
	deleteUsers()
	createUsers('ayolo@yolo.com','dqsv','male','21','mumbai','13131','1-1-2012')
	createUsers('ayolo@yoki.com','dqsv','male','21','mumbai','13131','1-1-2012')
	deleteUsers(1)
	createUsers('ayolsca.com','dqsv','male','21','mumbai','13131','1-1-2012')
	createUsers('ayolo@yascasclo.com','dqsv','male','21','mumbai','13131','1-1-2012')
	readUsers()
	readUsers(2)
	updateUsers(2,"Dad","Dad","Dad","Dad","Dad","Dad")
	readUsers(2)
	updateUsers(2,None,"SAD","SAD","SAD","SAD","SAD")
	readUsers(2)
	readUsers(2)
