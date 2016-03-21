from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import os,sys
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from Db_setup import Base, Issue, Vote, Comment, User

from flask import session as login_session

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///IPGS.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#login_session['U_Id']=12

app = Flask(__name__)
#APP_ROOT=os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------------------------------------------------------------------------------
#MAIN PAGE
@app.route('/')
@app.route('/main')
def home():
	return render_template('index.html')

@app.route('/login')
def login():
    return render_template('index.html')

#------------------------------------------------------------------------------------------------------------------
@app.route('/issue/new/', methods=['GET', 'POST'])
def newIssue():
    login_session['U_Id']=1
    if request.method == 'POST':
        newIssue = Issue(author=login_session['U_Id'],title=request.form['I_Title'], content=request.form['I_Content'], 
                         lat=request.form['I_Lat'], lng=request.form['I_Lng'],
                        image="url for image",type = request.form['I_Type'],  anonFlag=request.form['I_AnonFlag']) 
        session.add(newIssue)
        session.commit()
        #flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        print request.form['I_Lat']
        print request.form['I_Lng']
        print request.form['I_Title']
        print request.form['I_Content']
        print request.form['I_Type']
        print request.form['I_AnonFlag']
 #       target=os.path.join(APP_ROOT,'images/')
        #print target
 #       if not os.path.isdir(target):
 #          os.mkdir(target)
 #      for file in request.files.getlist("file"):
 #           print file
 #          filename=file.filename
            #os.rename(filename,request.form['I_Title'])
 #           destination="/".join([target,filename])
           # print destination
 #           file.save(destination)
            
        return redirect(url_for('home'))
    else:
        return render_template('newIssue.html')

@app.route('/issue/<int:I_Id>/view')
def  showDetailedIssue(I_Id):
    showDetailedIssue = session.query(Issue).filter_by(id = I_Id).one()
    showDetailedComment = session.query(Comment).filter_by(id = I_Id).order_by(asc(Comment.sqNo)).all()
    #temporarily harcoding the likes and dislikes part
    like=2
    dislike=2
    #showDetailedVote = session.query(Issue).filter_by(id = I_Id).all()
    #showDetailedVote = session,query(func.count())   SELECT count(*) 
    #    FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = true)
    # AS likes  GROUP BY V_flag;""",(I_Id,))
    return render_template('showdetailedissue.html', Issue=showDetailedIssue, Comment=showDetailedComment, like=like, dislike=dislike)

@app.route('/issue/<int:I_Id>/edit/', methods=['GET', 'POST'])
def editIssue(I_Id):
    editedIssue = session.query(Restaurant).filter_by(id=I_Id).one()
    if request.method == 'POST':
        if request.form['I_Title']:
            editedIssue.title = request.form['I_Title']
        if request.form['I_Content']:
            editedIssue.content = request.form['I_Content']
        if request.form['I_Lat']:
            editedIssue.lat = request.form['I_Lat']
        if request.form['I_Lng']:
            editedIssue.lng = request.form['I_Lng']
        if request.form['I_Type']:
            editedIssue.type = request.form['I_Type']
        if request.form['I_AnonFlag']:
            editedIssue.anonFlag = request.form['I_AnonFlag']
        session.add(editedIssue)
        session.commit()        
        #flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
        return redirect(url_for('showDetailedIssue',I_Id=I_Id ))
    else:
        return render_template('editissue.html', Issue=editedIssue)

# Delete a restaurant
@app.route('/issue/<int:I_Id>/delete/', methods=['GET', 'POST'])
def deleteIssue(I_Id):
    issuetodelete = session.query(Issue).filter_by(id = I_Id).one()
    if request.method == 'POST':
        session.delete(issuetodelete)
        # flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('deleteissue.html', Issue=issuetodelete)

#-----------------------------------------------------------------------------------------------------------------
@app.route('/comment/<int:I_Id>/new/', methods=['GET', 'POST'])
def newComment(I_Id):
    issuetocomment= session.query(Issue).filter_by(id = I_Id).one()
    if request.method == 'POST':
        newComment = Comment(content=request.form['I_Content'],id=I_Id,author=login_session['U_Id'])
        session.add(newComment)
        session.commit()
        return redirect(url_for('showDetailedIssue',I_Id=issuetocomment.id ))
    else:
        return render_template('newcomment.html',Issue=issuetocomment)

@app.route('/comment/<int:C_Id>/<int:C_SqNo>/edit/', methods=['GET', 'POST'])
def editComment(C_Id,C_SqNo):
    issuetocommentedit= session.query(Issue).filter_by(id = C_Id).one()
    editComment=session.query(Comment).filter_by(id=C_Id).filter_by(author=login_session['U_Id']).filter_by(sqNo=SqNo).one()
    if request.method == 'POST':
        if request.form['C_Content']:
            editComment.content = request.form['C_Content']
        return redirect(url_for('showDetailedIssue',I_Id=C_Id ))
    else:
        #part to check if the user is the author of the comment
        return render_template('editcomment.html',Comment=editComment,Issue=issuetocommentedit)

@app.route('/comment/<int:C_Id>/<int:C_SqNo>/delete/', methods=['GET', 'POST'])
def deleteComment(C_Id,C_SqNo):
    deleteComment=session.query(Comment).filter_by(id=C_Id).filter_by(author=login_session['U_Id']).filter_by(sqNo=SqNo).one()
    if request.method == 'POST':
        return redirect(url_for('showDetailedIssue',I_Id=C_Id ))
    else:
        #part to check if the user is the author of the comment
        return render_template('deletecomment.html',Comment=deleteComment)



#------------------------------------------------------------------------------------------------------------------

@app.route('/issue/my/', methods=['GET','POST'])
def  showMyIssue(): 
    if login_session['U_Id']!=None:
        myissue = session.query(Issue).filter_by(author=login_session['U_Id']).all()
        return render_template('showmyissue.html', Issue=myissue)
    else:
        return redirect(url_for('login'))

@app.route('/comment/my/', methods=['GET','POST'])
def showMyComment():
    if login_session['U_Id']!=None:
        mycomment = session.query(Comment).filter_by(author=login_session['U_Id']).all()
        return render_template('showmycomment.html', Comment=mycomment)
    else:
        return redirect(url_for('login'))
   
#-----------------------------------------------------------------------------------------------------------------

@app.route('/issue/nearby/map/', methods=['GET','POST'])
def showNearbyIssueMap():
    return render_template('shownearbyissuemap.html')

@app.route('/issue/nearby/list/', methods=['GET','POST'])
def showNearbyIssueList():
    return render_template('shownearbyissuelist.html')

#-----------------------------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
