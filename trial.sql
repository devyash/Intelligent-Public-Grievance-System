SELECT I_Id, I_Author, I_Title, I_Content, I_Lat,
				I_Lng, I_Image, I_AnonFlag, I_Type, I_time, I_Image
				 FROM Issues WHERE I_Id = 220;
IF( NOT EXITS(SELECT * FROM Votes WHERE V_IssueId=%s AND V_Author=%s))
					 BEGIN 
					 INSERT INTO Comments (I_Id,U_Id,V_Flag)
					 END