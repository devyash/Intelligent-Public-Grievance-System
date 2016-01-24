#Listing all the functions that this webapp might require
#
#Major change update: forgot to add admin fucntions all togther.
#
import psycopg2
#--------------------------------------------------------------------------------------------------
#CREATE PART OF THE CODE
#--------------------------------------------------------------------------------------------------
@readConnection
#
def createUsers(U_Email, U_Name, U_Gender, U_StrAdr, U_City, U_Pincode,U_Dob):
	c=conn.cursor()
	c.execute("""INSERT INTO Users (U_Email,U_Name,U_Gender, U_StrAdr,U_City, U_Pincode, U_Dob)
	    VALUES(%s,%s,%s,%s,%s,%s,%s);""",(U_Email,U_Name,U_Gender,U_StrAdr,U_City,U_Pincode,U_Dob,) )
	c.close()
	pass

@readConnection
def createIssues(I_Author,I_Title,I_Content,I_Lat,I_Lng,I_Image,I_AnonFlag,I_Type):
	c=conn.cursor()
	c.execute("""INSERT INTO Issues (I_Author,I_Title,I_Content,I_Lat,I_Lng,I_Image,I_AnonFlag,I_Type)
	    VALUES(%s,%s,%s,%s,%s,%s,%s,%s);""",(I_Author,I_Title,I_Content,I_Lat,I_Lng,I_Image,I_AnonFlag,I_Type,) )
	c.close() 
	pass

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
#READ/DISPLAY PART OF THE CODE
#------------------------------------------------------------------------------------------------------

@readConnection
def readUsers(U_Id):
	#Returns the details of the User in a dictionary as UserDetail
	c=conn.cursor()
	c.execute("""SELECT U_Id, U_Email, U_Name, U_Gender, U_StrAdr, U_City, U_Pincode, U_Dob, U_Admin FROM Users where U_Id = %s;""",(U_Id,))
	row = c.fetchone()
	UserDetail = ( {'U_Id': str(row[0]), 'U_Email': str(row[1]), 'I_Name': str(row[2]),'I_Gender': str(row[3]),'U_StrAdr': str(row[4]),'U_City': str(row[5]),'U_Pincode': str(row[6]),'U_Dob': str(row[7]),'U_Admin': str(row[8]) } )
	c.close()
	return UserDetail
	pass

@getConnection
def readIssues(I_Id): 
	#Displaying Everything we have on that issue
	#NOTE:Before calling this method Check if the I_AnonFlag is set, if it is set then dont return author of the issue
	#return a dictonary which contains I_Id, I_Author, I_Title, I_Content, I_Lat, I_Lng, I_Image, I_AnonFlag, I_Type, I_time 
	c.execute("""SELECT I_Id, I_Author, I_Title, I_Content, I_Lat, I_Lng, I_Image, I_AnonFlag, I_Type, I_time, I_Image FROM Issues WHERE I_Id= %s);""",(I_Id,))
	row = c.fetchone() 
	IssuesDetail = ({'I_Id': str(row[0]), 'I_Author': str(row[1]),'I_Title': str(row[2]),'I_Content': str(row[3]),'I_Lat': str(row[4]),'I_Lng': str(row[5]),'I_AnonFlag': str(row[6]),'I_Type': str(row[7]),'I_time': str(row[8]),'I_Image':str(row[9])} )
	return IssueDetail
	pass

@getConnection
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
	c.execute("""SELECT count(*) FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = true) AS likes  GROUP BY V_flag;""",(I_Id,))
	likes=c.fetchall()
	c.execute("""SELECT count(*) FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = false) AS dislikes  GROUP BY V_flag;""",(I_Id,))
	dislikes=c.fetchall()
	c.close()
	return likes, dislikes
	#return number of flags set for a I_ID
	#count(*) from votes where I_Id=I_Id from Issues group by V_flag
	pass
	
def readNearbyIssues(lat, lng):
	#within a given area lat (lat +1 mintue - 1 mintue as 1 minute is 1.8 kms ) 
	#Select I_ID from Comments where (I_lat>lat-1 min & I_lat<lat+1 min)&&(I_lng>lng-1 min & I_lng<lng+1 min)
	#return List of Issue ID list_I_Id
	pass


@readConnection
def readAllIssues(list_I_Id):
	#I_Ids is a array of issue I_Id
	#Call  if (isI_Visible(I_Id))=> true then proceed ahead else dont return that issue  
	#return: a dictionary that will contain image,I_title,IssueID,votes(will call readvotes for this to return),I_lat,I_lng,I_type WITHIN LIMIT 20(So the webpage doesn't hang
	#A_Issue dictionary
	c=conn.cursor() 
	for i in list_I_Id:
		if(readI_Visible(i)):
			c.execute("""SELECT I_Id, I_Title, I_Lat, I_Lng, I_Image, I_Type  FROM Issues WHERE I_Id= %s LIMIT 20);""",(I_Id,))
	row = c.fetchone() 
	IssuesDetail = ({'I_Id': str(row[0]), 'I_Title': str(row[1]),'I_Lat': str(row[2]),'I_Lng': str(row[3]),'I_Image': str(row[4]),'I_Lng': str(row[5]),'I_AnonFlag': str(row[6]),'I_Type': str(row[7]),'I_time': str(row[8])} )
			
	return A_Issues


def readMyIssues(U_Id):
	#this fuction will return a list of I_Id which have author as U_Id passed
	#return dictionary
	pass 



def readAboutus():
	#Static page about the us
	pass

@readConnection
def readUserSatisfaction(I_Id):
	#calls readvotes() and if likes > dislike returns likes/total votes
	pass

def readMap():
	#will load raw read Map in the form of java script
	#this will be in a div tag within a box
	pass

@readConnection
def readI_Visible(I_Id):
	# return true if visible else return false
	c=conn.cursor()
	try:
		c.execute("""SELECT I_Visible FROM Issues WHERE I_Id=%s """,(I_Id,))
		value = c.fetchone()
		c.close()
		return value
	except Exception, e:
		print "Exception in readI_Visible function "
	pass

@readConnection
def readI_AnonFlag():
	
	#returns true if the anonymous flag is not set
	#returns false if the anonymous flag is set=> Make the Issue anonymous  
	pass	



#-------------------------------------------------------------------------------------------------
#UPDATE PART OF THE API
#-------------------------------------------------------------------------------------------------

@readConnection
def updatePassword():
	c=conn.cursor()
	c.close()
	pass

@readConnection
def updateUsers(U_Name,U_StrAdr,U_City,U_Pincode):
	# cannot update email,cannot update uid
	c=conn.cursor()
	c.execute("""UPDATE Users SET U_Name=%s WHERE U_Name=%s""")#updates username
	c.execute("""UPDATE Users SET U_StrAdr=%s WHERE U_StrAdr=%s""")#updates stradr
	c.execute("""UPDATE Users SET U_City=%s WHERE U_City=%s""")#updates city
	c.execute("""UPDATE Users SET U_Pincode=%s WHERE U_Pincode=%s""")#updates pincode
	print "user details updated"
	c.close()
	pass

@readConnection
def updateIssues():
	c=conn.cursor()
	c.execute("""UPDATE Issues SET I_Content=%s WHERE I_Content=%s""")#updates issue content(not sure)
	c.execute("""UPDATE Issues SET I_Image= WHERE I_Image= """)#no idea
	if U_Name == I_Author
		c.execute("""UPDATE Issues SET I_Visible=%s WHERE I_Visible=%s""")
	else
		print "cannot change visibility"
	c.close()
	pass

@readConnection
def updateComments():
	c=conn.cursor()
	c.close()
	pass

@readConnection
def updateVotes():
	c=conn.cursor()
	c.close()
	pass

@readConnection
def updateI_Visible(I_Id, U_Id, I_Author,I_Visible):
	#this shall suspend the issue all togther(Can only be done by the admin or the issue creator).
	#still visible to the author though and not delete the issue from the table
	#Returns true if the change was successful else returns false
	c=conn.cursor()
	try:
		if U_Id == I_Author :
			c.execute("""UPDATE Issues SET I_Visible=%s WHERE I_Id=%s""",(I_Visible,I_Id,))
			c.close()
			return true
		else:
			print "User ID and Author ID donot match. You do not have access to suspend this Issue."
	except Exception, e:
		print "Exception in setting the Issue Visibility"
	else:
		return false

#----------------------------------------------------------------------------------------------
#DELETE PART OF THE CODE
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
		c.execute("""DELETE FROM Comments WHERE V_IssueId=%s AND V_Author= %s""",(V_IssueId,V_Author,))
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
		c.execute("""DELETE FROM Comments WHERE C_Id=%s AND C_SqNo= %s""",(C_Id,C_SqNo,))
		c.close()
		return true
	except Exception, e:
		print "Exception in delete comment"
	else:
		return false
	pass
	
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










