from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from IPGSdb import *
import os,sys

app = Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------------------------------------------------------------------------------
#MAIN PAGE
@app.route('/')
@app.route('/main')
def home():

	return render_template('index.html')

#------------------------------------------------------------------------------------------------------------------
@app.route('/issues/new/', methods=['GET', 'POST'])
def newIssues():
    if request.method == 'POST':
    	#NewIssue = createIssues(I_Author = login_session['U_Id'],I_Title = request.form['I_Title'],
        #                         I_Content = request.form['I_Content'],I_Lat= request.form['I_Lat'],
        #                         I_Lng= request.form['I_Lng'], I_Image= request.form['I_Image'],
        #                         I_AnonFlag= request.form['I_AnonFlag'],I_Type= request.form['I_Type'])
        #newIssues = Issues(name=request.form['name'])
        #flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        print request.form['I_Lat']
        print request.form['I_Lng']
        print request.form['I_Title']
        print request.form['I_Content']
        print request.form['I_Type']
        print request.form['I_AnonFlag']
        target=os.path.join(APP_ROOT,'images/')
        print target
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            print file
            filename=file.filename
            #os.rename(filename,request.form['I_Title'])
            destination="/".join([target,filename])
            print destination
            file.save(destination)
            
        return redirect(url_for('showDetailedIssues'))
    else:
        return render_template('newIssues.html')

@app.route('/issues/<int:I_Id>/view', methods=['GET'])
def  showDetailedIssues(I_Id):
    return render_template('showdetailedissues.html')

@app.route('/issues/<int:I_Id>/edit/', methods=['GET', 'PUT'])
def editIssues(I_Id):
 #editedRestaurant = session.query(
 #       Restaurant).filter_by(id=restaurant_id).one()
    #editedIssue = readIssues(I_Id) 
    editedIssue={'I_Title':"fadfbfeiu",'I_Content':"THIS IS A TRIAL DETAIL ! BECAUSE YOLO!!",'I_Type':2,'I_Lat':19,'I_Lng':72.872997,'I_AnonFlag':True}
    if request.method == 'PUT':
        if request.form['I_Title']:
            #editedRestaurant.name = request.form['name']
            #flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('showDetailedIssues'), I_Id=I_Id)
    else:
        return render_template('editIssues.html', I_Title=editedIssue['I_Title'],I_Content=editedIssue['I_Content'],I_Type=editedIssue['I_Type'],I_Lat=editedIssue['I_Lat'],I_Lng=editedIssue['I_Lng'], I_AnonFlag=editedIssue['I_AnonFlag'])

# Delete a restaurant
@app.route('/issues/<int:I_Id>/delete/', methods=['GET', 'DELETE'])
def deleteIssues(I_Id):
    #restaurantToDelete = session.query(
    #   Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'DELETE':
       # session.delete(restaurantToDelete)
       # flash('%s Successfully Deleted' % restaurantToDelete.name)
       #session.commit()
        return redirect(url_for('showDetailedIssues', I_Id=I_Id))
    else:
        return render_template('deleteIssues.html', I_Id=I_Id)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/comments/<int:C_Id>/new/', methods=['GET', 'POST'])
def newComments(C_Id):
    if request.method == 'POST':
        return redirect(url_for('showDetailedIssues'))
    else:
        return render_template('newcomments.html')

@app.route('/comments/<int:C_Id>/<int:C_SqNo>/edit/', methods=['GET', 'PUT'])
def editComments(C_Id,C_SqNo):
    if request.method == 'PUT':
        return redirect(url_for('showDetailedIssues'),I_Id=I_Id))
    else:
        #part to check if the user is the author of the comment
        return render_template('editcomments.html')

@app.route('/comments/<int:C_Id>/<int:C_SqNo>/delete/', methods=['GET', 'DELETE'])
def deleteComments(C_Id,C_SqNo):
    if request.method == 'DELETE':
        return redirect(url_for('showDetailedIssues'), I_Id=I_Id))
    else:
        #part to check if the user is the author of the comment
        return render_template('deletecomments.html')



#------------------------------------------------------------------------------------------------------------------

@app.route('/issues/my/', methods=['GET','POST'])
def  showMyIssues():
    return render_template('showmyissues.html')

@app.route('comments/my/', methods=['GET','POST'])
def showMyComments():
    return render_template('showmycomments.html')
#-----------------------------------------------------------------------------------------------------------------

@app.route('/issues/nearby/map/', methods=['GET','POST'])
def showNearbyIssuesMap():
    return render_template('shownearbyissuesmap.html')

@app.route('/issues/nearby/map/', methods=['GET','POST'])
def showNearbyIssuesList():
    return render_template('shownearbyissueslist.html')

#-----------------------------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
