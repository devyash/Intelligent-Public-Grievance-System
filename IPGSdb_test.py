#Test class for IPGSdb.py 

from IPGSdb import *
from IPGSdb import deleteUsers

def testUsers():
	print readUsers()
	deleteUsers()
	print readUsers()
	A = createUsers('ayolo@yolo.com','dqsv','male','21','mumbai','13131','1-1-2012')
	B = createUsers('ayolo@yoki.com','dqsv','male','21','mumbai','13131','1-1-2012')
	deleteUsers(B)
	C=createUsers('ayolsca.com','dqsv','male','21','mumbai','13131','1-1-2012')
	D=createUsers('ayolo@yascasclo.com','dqsv','male','21','mumbai','13131','1-1-2012')
	print readUsers(A)
	updateUsers(A,"Dad","Dad","Dad","Dad","Dad",'1-1-2000')
	print readUsers(A)
	updateUsers(A,None,"SAD","SAD","SAD","SAD",'1-1-1994')
	print readUsers()

if __name__ == '__main__':
	testUsers()
	print "Success! All tests passed!"