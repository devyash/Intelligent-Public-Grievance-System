#Listing all the functions that this webapp might require
#
#Major change update: forgot to add admin fucntions all togther.
#
def getNearbyIssues(lat, lng):
	#within a given area lat (lat +1 mintue - 1 mintue as 1 minute is 1.8 kms ) 
	#Select I_ID from Comments where (I_lat>lat-1 min & I_lat<lat+1 min)&&(I_lng>lng-1 min & I_lng<lng+1 min)
	#return array OF Issue ID

def getAllIssues(array of I_Id):
	#Call  if (isI_Visible(I_Id))=> true then proceed ahead else dont return that issue  
	#return: a dictionary that will contain image,I_title,IssueID,votes(will call getvotes for this to return),I_lat,I_lng
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

def getVote(I_Id):
	#return number of flags set for a I_ID
	#count(*) from votes where I_Id=I_Id from Issues group by V_flag

def getAboutus():
	#Static page about the us
	#


def getConnection():
	#return a connection object
	#return con 



def getUserSatisfaction():
	#if totalvotes >
	#

def getMap():
	#will load raw get Map in the form of java script
	#this will be in a div tag within a box

def setMarkers(A_Issue):
	#this will set markers on the map based on I_type
	#this will call getAllIssues and get the basic detials of all the issues and set the marker accordingly


def setI_Visible(I_Id, U_Id, I_Author):
	#this shall suspend the issue all togther(Can only be done by the admin or the issue creator).
	#still visible to the author though and not delete the issue from the table

def isI_Visible( an array of I_Id):
	# return true if visible else return false



