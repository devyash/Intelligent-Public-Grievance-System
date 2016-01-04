def GetNearbyIssue(lat, lng):
	#within a given area lat (lat +1 mintue - 1 mintue as 1 minute is 1.8 kms ) 
	#Select I_ID from Comments where (I_lat>lat-1 min & I_lat<lat+1 min)&&(I_lng>lng-1 min & I_lng<lng+1 min)
	#return dictionary OF Issue ID

def RegisterIssue(lat,lng, title, content,image, anonflag,Author,I_type,timestamp):
	# store the data in the data base
	#INSERT 

def DisplayIssue(I_Id):
	#Displaying Everything we have on that issue
	#
	#return lat, lng, title, content, image, Author, I_type, timestamp, Votes, CC_Author serial references Users(U_Id),C_Content,C_time,C_SqNo

def MyIssues(U_Id):
	#this fuction will return a list of I_Id which have author as U_Id passed
	#return dictionary 

def DisplaySummary(dictionary of I_Id):
	#return: a dictionary that will contain image,I_title,votes,IssueID

def DisplayAboutus():
	#Static page about the us

def PostComment(I_Id, U_Id, C_Content, C_time):
	# insert into Comments values(U_Id, C_Content,  , I_ID)

