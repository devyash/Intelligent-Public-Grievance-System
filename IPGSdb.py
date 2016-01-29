#Listing all the functions that this webapp might require
#
#Major change update: forgot to add admin fucntions all togther.
import psycopg2

#------------------------------------------------------------------------------------------
#OTHER FUNCTIONS 
#------------------------------------------------------------------------------------------

#Kind of understanding closures and decorators but what the heck!
def readConnection(f):
    def readConnectionInner(*args, **kwargs):
        # or use a pool, or a factory function...
        conn = psycopg2.connect("dbname = IPGS")
        try:
            rv = f(conn, *args, **kwargs)
        except Exception, e:
            conn.rollback()
            raise
        else:
            conn.commit() # or maybe not
        finally:
            conn.close()

        return rv

    return readConnectionInner


def connect():
	#In case readConnection doesnt work use this to manually get connection and commit changes
	return psycopg2.connect("dbname=IPGS")

#--------------------------------------------------------------------------------------------------
#CREATE  FUNCTIONS PART OF THE CODE
#--------------------------------------------------------------------------------------------------
@readConnection
def createUsers(conn,U_Email, U_Name, U_Gender, U_StrAdr, U_City, U_Pincode, U_Dob):
	#if any value is missing just enter None instead of it(Only Values that can be null)
	#Check if the Users Email is Unique
	try:
		if(isU_Email(U_Email)):
			c=conn.cursor()
			c.execute("""INSERT INTO Users (U_Email,U_Name,U_Gender, U_StrAdr,U_City, U_Pincode, U_Dob)
			    VALUES(%s,%s,%s,%s,%s,%s,%s);""",(U_Email,U_Name,U_Gender,U_StrAdr,U_City,U_Pincode,U_Dob,) )
			c.execute("""SELECT U_Id FROM Users WHERE U_Email=%s;""",(U_Email,))
			U_Id = c.fetchone() [0]
			print "\nCreated User with U_Id:%s \n"%U_Id
			c.close()
			return U_Id
		else:
			print"\nUser NOT Created\n"
	except TypeError:
		print"Exception: You have entered a wrong type in the parameters,Please enter correct format(Maybe yu have entered None type which cannot be null)"
		conn.rollback()
		c.close()
		#raise(TypeError)

@readConnection
def createIssues(conn,I_Author,I_Title,I_Content,I_Lat,I_Lng,I_Image,I_AnonFlag,I_Type):
	#is there the author in the issues table?
	#Every New Issue Must have a unique Author and Title
	if(isU_Id(I_Author)):
		c=conn.cursor()
		c.execute("""INSERT INTO Issues (I_Author,I_Title,I_Content,I_Lat,I_Lng,I_Image,I_AnonFlag,I_Type)
		    VALUES(%s,%s,%s,%s,%s,%s,%s,%s);""",(I_Author,I_Title,I_Content,I_Lat,I_Lng,I_Image,I_AnonFlag,I_Type,) )
		c.execute("""SELECT I_Id FROM Issues WHERE I_Author=%s AND I_Title=%s;""",(I_Author,I_Title,))
		I_Id = c.fetchone()[0]
		print "\nCreated Issue in Issues with I_Id:%s \n"%I_Id
		c.close() 
		return I_Id

@readConnection
def createComments(C_Author,C_Content,I_Id):
	c=conn.cursor()
	c.execute("""INSERT INTO Comments (C_Author,C_Content,I_Id)
	    VALUES(%s,%s,%s);""",(C_Author,C_Content,I_Id,) )
	c.close() 
	pass

@readConnection
def createVotes(I_Id,U_Id,V_Flag):
	c=conn.cursor()
	#Checks if the votes exits if not it will insert the new vote
	c.execute("""IF( NOT EXITS(SELECT * FROM Votes WHERE V_IssueId=%s AND V_Author=%s))
				 BEGIN 
				 INSERT INTO Comments (I_Id,U_Id,V_Flag)
				 END;""",(I_Id,U_Id,))
	c.close()
	pass


def createMarkers(A_Issue):
	#this will set markers on the map based on I_type
	#this will call readAllIssues and read the basic detials of all the issues and set the marker accordingly
	pass


#------------------------------------------------------------------------------------------------------
#READ/DISPLAY FUNCTIONS PART OF THE CODE
#------------------------------------------------------------------------------------------------------

@readConnection
def readUsers(conn,U_Id=None):
	#Returns the details of the User in a dictionary as UserDetail
	c=conn.cursor()
	if U_Id==None:
		c.execute("""SELECT * FROM Users;""")
		print " \nUsers Details printed of all Users\n"
		UserDetail=list(c.fetchall())	
		c.close()
		return UserDetail	
	else:
		if (isU_Id(U_Id)):
			c.execute("""SELECT U_Id, U_Email, U_Name, U_Gender, U_StrAdr, U_City, U_Pincode, U_Dob, U_Admin FROM Users where U_Id = %s;""",(U_Id,))
			UserDetail = ( {'U_Id': str(row[0]), 'U_Email': str(row[1]), \
				'U_Name': str(row[2]),'U_Gender': str(row[3]),'U_StrAdr': str(row[4]),\
				'U_City': str(row[5]),'U_Pincode': str(row[6]),'U_Dob': str(row[7]),\
				'U_Admin': str(row[8]) } for row in c.fetchall() )
			print "\nUsers Details printed of:%s\n"%U_Id
			c.close()	
			return next(UserDetail)
		
	
@readConnection
def readIssues(conn,I_Id=None): 
	#Displaying Everything we have on that issue
	#NOTE:Before calling this method Check if the I_AnonFlag is set, if it is set then dont return author of the issue
	#return a dictonary which contains I_Id, I_Author, I_Title, I_Content, I_Lat, I_Lng, I_Image, I_AnonFlag, I_Type, I_time 
	c=conn.cursor()
	if I_Id==None:
		c.execute("""SELECT * FROM Issues;""")
		print " \nUsers Details printed of all Issues\n"
		IssuesDetail=list(c.fetchall())	
		c.close()
		return IssuesDetail	
	else:
		c.execute("""SELECT I_Id, I_Author, I_Title, I_Content, I_Lat, \
			I_Lng, I_Image, I_AnonFlag, I_Type, I_time, I_Image\
			 FROM Issues WHERE I_Id = %s""",(I_Id,));
		if(isI_AnonFlag(I_Id)):
		 	IssuesDetail = ({'I_Id': str(row[0]), 'I_Author': '',\
		 		'I_Title': str(row[2]),'I_Content': str(row[3]),'I_Lat': str(row[4])\
		 		,'I_Lng': str(row[5]),'I_AnonFlag': str(row[6]),'I_Type': str(row[7]),\
		 		'I_time': str(row[8]),'I_Image':str(row[9])}  for row in c.fetchall())
			print "\nAuthor is anonymous\n"
		else:
			IssuesDetail = ({'I_Id': str(row[0]), 'I_Author': '',\
		 		'I_Title': str(row[2]),'I_Content': str(row[3]),'I_Lat': str(row[4])\
		 		,'I_Lng': str(row[5]),'I_AnonFlag': str(row[6]),'I_Type': str(row[7]),\
		 		'I_time': str(row[8]),'I_Image':str(row[9])}  for row in c.fetchall())
			print "\nAuthor is  NOT anonymous\n"
		
		print "\nIssue Details printed of:%s\n"%I_Id
		c.close()
		conn.commit()
		return next(IssuesDetail)
		

@readConnection
def readComments(I_Id):
	#Display all the comments on an Issue.
	#returns a list of dictionary containing all the comments on that Issues
	c.execute("""SELECT C_Author, C_Content, C_time, C_Id, C_SqNo FROM Comments WHERE C_Id= %s ORDER BY C_SqNo);""",(I_Id,)) 
	CommentDetail = ({'C_Author': str(row[0]), 'C_Content': str(row[1]),'C_time': str(row[2]),'C_Id': str(row[3]),'C_SqNo': str(row[4])} for row in c.fetchall() )
	return CommentDetail
	pass

@readConnection
def readVotes(I_Id):
	c=conn.cursor()
	if(isI_Id):
		c.execute("""SELECT count(*) FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = true) AS likes  GROUP BY V_flag;""",(I_Id,))
		likes=c.fetchall()
		c.execute("""SELECT count(*) FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = false) AS dislikes  GROUP BY V_flag;""",(I_Id,))
		dislikes=c.fetchall()
		c.close()
		return (likes, dislikes)
	else:
		print"Issue doesnt have any votes"
		return (None,None)

	#return number of flags set for a I_ID
	#count(*) from votes where I_Id=I_Id from Issues group by V_flag
	pass
	
@readConnection
def readAllIssues(list_I_Id):
	#I_Ids is a array of issue I_Id
	#Call  if (isI_Visible(I_Id))=> true then proceed ahead else dont return that issue  
	#return: array of dictionary objects that will contain image,I_title,IssueID,votes(will call readvotes for this to return),I_lat,I_lng,I_type WITHIN LIMIT 20(So the webpage doesn't hang
	#A_Issue is an array of dictionary
	c=conn.cursor() 
	for i in list_I_Id:
		if(isI_Visible(i)):
			c.execute("""SELECT I_Id, I_Title, I_Lat, I_Lng, I_Image, I_Type  FROM Issues WHERE I_Id= %s LIMIT 20);""",(I_Id,)) 
			row=c.fetchone()
			A_Issues[i] = ({'I_Id': str(row[0]), 'I_Title': str(row[1]),'I_Lat': str(row[2]),'I_Lng': str(row[3]),'I_Image': str(row[4]),'I_Type': str(row[5])})
			pass
	#ERROR IN THE CODE HERE DONT KNOW HOW TO DO IT, WILL HAVE TO LEARN PYTHON
	return A_Issues

@readConnection
def readMyIssues(U_Id):
	#this fuction will return a list of I_Id which have author as U_Id passed
	#return an array list_I_Id
	c=conn.cursor()
	c.execute("""SELECT I_Id FROM Issues where I_Author = %s;""",(U_Id,))
	list_I_Id  = c.fetchall()
	c.close()
	return list_I_Id
	pass 

@readConnection
def readUserSatisfaction(I_Id):
	#returns the satisfaction in a percentage
	satis=readVotes(I_Id)
	if(satis[0]>satis[1]):
		print"Users are happy"
		satisfactionpercentage = ((float(satis[0])/(satis[0]+satis[1]))*100)

	elif(satis[0]<satis[1]):
		print"Users are unhappy"
		satisfactionpercentage = ((float(satis[1])/(satis[0]+satis[1]))*100)

	elif(satis[0]==satis[1]):
		print"Users are neither happy nor satisfied"
		satisfactionpercentage = 50.0
	return satisfactionpercentage
	pass

def readNearbyIssues(lat, lng):
	#within a given area lat (lat +1 mintue - 1 mintue as 1 minute is 1.8 kms ) 
	#Select I_ID from Comments where (I_lat>lat-1 min & I_lat<lat+1 min)&&(I_lng>lng-1 min & I_lng<lng+1 min)
	#return List of Issue ID list_I_Id
	pass

def readAboutus():
	#Static page about the us
	pass

def readMap():
	#will load raw read Map in the form of java script
	#this will be in a div tag within a box
	pass

#---------------------------------------------------------------------------------------------------
#CODE THAT CHECKS IF CERTAIN ROWS ARE THERE IN DATABASE OR NOT
#---------------------------------------------------------------------------------------------------
@readConnection
def isI_Visible(conn,I_Id):
	# return true if visible else return false
	c=conn.cursor()
	c.execute("""SELECT I_Visible FROM Issues WHERE I_Id=%s """,(I_Id,))
	value = c.fetchone()
	c.close()
	return value
	
@readConnection
def isI_AnonFlag(conn,I_Id):
	#returns FALSE if the anonymous flag is not set
	#returns TRUE if the anonymous flag is set=> Make the Issue anonymous  
	c=conn.cursor()
	c.execute("""SELECT I_AnonFlag FROM Issues WHERE I_Id=%s """,(I_Id,))
	I_AnonFlag=c.fetchone()[0]
	c.close()
	return I_AnonFlag
	
@readConnection
def isI_Id(conn,I_Id):
	#Checks if the I_Id exists
	c=conn.cursor()
	c.execute("""SELECT 1 FROM Issues WHERE I_Id=%s """,(I_Id,))
	if (c.fetchone()):
		c.close()
		return True
	else:
		print "\n I_Id:%s does not exist in the database!\n"%I_Id
		c.close()
		return False

@readConnection
def isU_Id(conn,U_Id):
	#Returns true if U_Id exists in the Users table
	c=conn.cursor()
	c.execute("""SELECT 1 FROM Users WHERE U_Id=%s """,(U_Id,))
	if (c.fetchone()):
		c.close()
		return True
	else:
		print "\nUser U_Id:%s does not exist in the database!\n"%U_Id
		c.close()
		return False

@readConnection
def isU_Email(conn,U_Email):
	#Returns true if U_Id exists in the Users table
	c=conn.cursor()
	c.execute("""SELECT 1 FROM Users WHERE U_Email=%s """,(U_Email,))
	if (c.fetchone()):
		c.close()
		print "\nUser User Email:%s Already exists in Database! It needs to be unique!\n"%U_Email
		return False
	else:
		c.close()
		return True

@readConnection
def isComments(C_Author,C_Id,C_SqNo):
	c=conn.cursor()
	c.execute("""SELECT 1 FROM Users WHERE C_Author=%s AND C_Id=%s AND C_SqNo """,(C_Author,C_Id,C_SqNo))
	if (c.fetchone()):
		return True
	else:
		return False
 
	c.close()
	pass

#-------------------------------------------------------------------------------------------------
#UPDATE FUNCTIONS PART OF THE API
#-------------------------------------------------------------------------------------------------

@readConnection
def updatePassword(U_Id):
	c=conn.cursor()
	c.close()
	pass

@readConnection
def updateUsers(conn,U_Id,U_Name=None,U_Gender=None,U_StrAdr=None,U_City=None,U_Pincode=None,U_Dob=None):
	# cannot update email,cannot update uid
	#Pass None in the variables you dont want ro update
	if (isU_Id(U_Id)):
		c=conn.cursor() 
		if U_Name != None:
			c.execute("""UPDATE Users SET U_Name=%s WHERE U_Id=%s;""",(U_Name,U_Id,))

		if U_Gender != None:
			c.execute("""UPDATE Users SET U_Gender=%s WHERE U_Id=%s;""",(U_Gender,U_Id,))
		
		if U_StrAdr != None:
			c.execute("""UPDATE Users SET U_City=%s WHERE U_Id=%s;""",(U_City,U_Id,))
		
		if U_City != None:
			c.execute("""UPDATE Users SET U_Pincode=%s WHERE U_Id=%s;""",(U_Pincode,U_Id,))
		
		if U_Pincode != None:
			c.execute("""UPDATE Users SET U_Dob=%s WHERE U_Id=%s;""",(U_Dob,U_Id,))
		
		print "\nUser details updated of U_Id:%s\n"%U_Id
		c.close()


@readConnection
def updateIssues(conn,I_Id,I_Title=None,I_Content=None,I_Lat=None,I_Lng=None,I_Image=None,I_AnonFlag=None,I_Type=None,I_Visible=None):
	#BUG:DOES NOT TELL IF THE CONTENT IS NOT UPDATE/ERROR
	#I_Id cannot be a string only int values are allowed
	c=conn.cursor()
	if(isI_Id(I_Id)):
		if I_Title != None:
			c.execute("""UPDATE Issues SET I_Title=%s WHERE I_Id=%s;""",(I_Title,I_Id,))
		if I_Content != None:
			c.execute("""UPDATE Issues SET I_Content=%s WHERE I_Id=%s;""",(I_Content,I_Id,))
		if I_Lat != None:
			c.execute("""UPDATE Issues SET I_Lat=%s WHERE I_Id=%s;""",(I_Lat,I_Id,))
		if I_Lng != None:
			c.execute("""UPDATE Issues SET I_Lng=%s WHERE I_Id=%s;""",(I_Lng,I_Id,))
		if I_Image != None:
			c.execute("""UPDATE Issues SET I_Image=%s WHERE I_Id=%s;""",(I_Image,I_Id,))
		if I_AnonFlag != None:
			c.execute("""UPDATE Issues SET I_AnonFlag=%s WHERE I_Id=%s;""",(I_AnonFlag,I_Id,))
		if I_Type != None:
			c.execute("""UPDATE Issues SET I_Type=%s WHERE I_Id=%s;""",(I_Type,I_Id,))
		if I_Visible != None:
			c.execute("""UPDATE Issues SET I_Visible=%s WHERE I_Id=%s;""",(I_Visible,I_Id,))
		print "\nIssue details updated of I_Id:%s\n"%I_Id
		c.close()

@readConnection
def updateComments(C_Author,C_Id,C_SqNo,C_Content=None):
	c=conn.cursor()
	if 'C_Content' in locals():
		c.execute("""UPDATE Comments SET C_Content=%s WHERE C_Author=%s AND C_Id= %s AND C_SqNo =%s""",(C_Content,C_Author,C_Id,C_SqNo,))
	c.close()
	pass

@readConnection
def updateVotes(V_IssueId,V_Author,V_Flag):
	c=conn.cursor()
	c.execute("""UPDATE Votes SET V_Flag=%s WHERE V_IssueId=%s AND V_Author= %s""",(V_IssueId,V_Author,V_Flag,))
	c.close()
	pass

#@readConnection
#def updateI_Visible(I_Id, U_Id, I_Author,I_Visible):
	#this shall suspend the issue all togther(Can only be done by the admin or the issue creator).
	#still visible to the author though and not delete the issue from the table
	#Returns true if the change was successful else returns false
#	c=conn.cursor()
#	try:
		#if U_Id == I_Author :
		#	c.execute("""UPDATE Issues SET I_Visible=%s WHERE I_Id=%s""",(I_Visible,I_Id,))
		#	c.close()
		#	return true
		#else:
		#	print "User ID and Author ID donot match. You do not have access to suspend this Issue."
	#except Exception, e:
	#	print "Exception in setting the Issue Visibility"
	#else:
	#	return false

#----------------------------------------------------------------------------------------------
#DELETE FUNCTIONS PART OF THE CODE
#----------------------------------------------------------------------------------------------

@readConnection
def deleteIssues(I_Id):
	#This function will return true if the issue is deleted successfully else false
	#
	c=conn.cursor()
	try:
		c.execute("""DELETE FROM Issues WHERE I_Id=%s""",(I_Id,))
		c.close()
		return true
	except Exception, e:
		print "Exception in delete Issues"
	else:
		return false
	pass

@readConnection
def deleteVotes(V_IssueId, V_Author):
	#This function will return true if the vote is deleted successfully else false
	#
	c=conn.cursor()
	try:
		c.execute("""DELETE FROM Comments WHERE V_IssueId=%s AND V_Author= %s;""",(V_IssueId,V_Author,))
		c.close()
		return true
	except Exception, e:
		print "Exception in delete Vote"
	else:
	 return false
	pass

@readConnection
def deleteComments(C_Id, C_SqNo):
	#This function will return true if the comment is deleted successfully else false
	c=conn.cursor()
	try:
		c.execute("""DELETE FROM Comments WHERE C_Id=%s AND C_SqNo= %s;""",(C_Id,C_SqNo,))
		c.close()
		return true
	except Exception, e:
		print "Exception in delete comment"
	else:
		return false
	pass
	
def deleteUsers(U_Id=None):
	conn=connect()
	c = conn.cursor()
	if U_Id == None:
		c.execute("""DELETE FROM Users CASCADE; """)
		print "\nDeleted all the Users\n"
	else:
		if(isU_Id(U_Id)):
			c.execute("""DELETE FROM Users WHERE U_Id=%s CASCADE;""",(U_Id,))
			print "\nDeleted User U_Id:%s\n"%U_Id
	conn.commit()
	conn.close()
	c.close()



