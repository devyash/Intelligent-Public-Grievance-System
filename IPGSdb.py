#Listing all the functions that this webapp might require
#
#Major change update: forgot to add admin fucntions all togther.
#
import psycopg2

def getConnection(f):
	def getConnectionInner(*args, **kwargs):
		global conn
		if not conn:
			conn = psycopg2.connect("dbname = IPGS")
		try:
    		rv = f(conn, *args, **kwargs)
    	except Exception, e:
    		cnn.rollback() 
    		raise
		else:
    		cnn.commit() # or maybe not
		finally:
        	return rv
		return getConnectionInner
		#return a connection object
	#return con 
	return conn
	
def getNearbyIssues(lat, lng):
	#within a given area lat (lat +1 mintue - 1 mintue as 1 minute is 1.8 kms ) 
	#Select I_ID from Comments where (I_lat>lat-1 min & I_lat<lat+1 min)&&(I_lng>lng-1 min & I_lng<lng+1 min)
	#return array OF Issue ID

def getAllIssues(array of I_Id):
	#Call  if (isI_Visible(I_Id))=> true then proceed ahead else dont return that issue  
	#return: a dictionary that will contain image,I_title,IssueID,votes(will call getvotes for this to return),I_lat,I_lng,I_type WITHIN LIMIT 20(So the webpage doesn't hang
	#A_Issue object

def getIssues(I_Id): 
	#Displaying Everything we have on that issue
	#return lat, lng, title, content, image, Author, I_type, timestamp, Votes

def getComment(I_Id):
	#Display all the comments presented by the user.
	#return

def setNewIssue(lat,lng, title, content,image, anonflag,Author,I_type,timestamp):
	# store the data in the data base
	#INSERT

def getMyIssues(U_Id):
	#this fuction will return a list of I_Id which have author as U_Id passed
	#return dictionary 

def setComments(I_Id, U_Id, C_Content, C_time):
	# insert into Comments values(U_Id, C_Content,  , I_ID)
	#

def setVote(U_Id,I_Id):
	#if U_Id not present in votes for I_Id then vote
	#Insert into votes

@getConnection
def getVote(I_Id):
	c=conn.cursor()
	c.execute("""SELECT count(*) FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = true) AS likes  GROUP BY V_flag;""",(I_Id,))
	likes=c.fetchall()
	c.execute("""SELECT count(*) FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = false) AS dislikes  GROUP BY V_flag;""",(I_Id,))
	dislikes=c.fetchall()
	c.close()
	return likes, dislikes
	#return number of flags set for a I_ID
	#count(*) from votes where I_Id=I_Id from Issues group by V_flag

def getAboutus():
	#Static page about the us
	#

#Kind of understanding closures and decorators but what the heck!

    
@getConnection
def getUserSatisfaction(I_Id):
	#calls getvotes() and if likes > dislike returns likes/total votes
	#

def getMap():
	#will load raw get Map in the form of java script
	#this will be in a div tag within a box

def setMarkers(A_Issue):
	#this will set markers on the map based on I_type
	#this will call getAllIssues and get the basic detials of all the issues and set the marker accordingly

@getConnection
def setI_Visible(I_Id, U_Id, I_Author,I_Visible):
	#this shall suspend the issue all togther(Can only be done by the admin or the issue creator).
	#still visible to the author though and not delete the issue from the table
	#Returns true if the change was successful else returns false
	c=conn.cursor()
	try:
		if U_Id = I_Author :
		c.execute("""UPDATE Issues SET I_Visible= %s WHERE I_Id=%s""",(I_Visible,I_Id,))
		c.close()
		return true
		else:
			print "User ID and Author ID donot match. You do not have access to suspend this Issue."
	except Exception, e:
		print "Exception im setting the Issue Visibility"
	else:
	return false

@getConnection
def isI_Visible(I_Id):
	# return true if visible else return false
	c=conn.cursor()
	try:
		c.execute("""SELECT I_Visible FROM Issues WHERE I_Id=%s """,(I_Id,))
		value = c.fetchone()
		c.close()
		return value
	except Exception, e:
		print "Exception in isI_Visible function "
	
@getConnection
def deleteComment(C_Id, C_SqNo):
	c=conn.cursor()
	try:
		c.execute("""DELETE FROM Comments WHERE C_Id=%s AND C_SqNo= %s""",(C_Id,C_SqNo,))
		c.close()
		return true
	except Exception, e:
		print "Exception in delete comment"
	else:
	return false

	#This function will return true if the comment is deleted successfully else false

@getConnection
def deleteIssue(I_Id):
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

@getConnection
def deleteVote(V_IssueId, V_Author):
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

