from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import os,sys
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from DB_setup import Base, Issue, Vote, Comment, User
from flask import session as login_session


import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "IPGS"


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///IPGS.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#login_session['U_Id']=12

app = Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------------------------------------------------------------------------------
    

#MAIN PAGE
@app.route('/')
@app.route('/main')
def home():
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        AllIssue=session.query(Issue).all()
        AllComment=session.query(Comment).all()
        AllVote=session.query(Vote).all()
        AllUser=session.query(User).all()
        return render_template('index.html', Issue=AllIssue, Vote=AllVote, User=AllUser)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
         AllUser=session.query(User).all()
         for u in AllUser:
            if( request.form['username']==u.name and request.form['password']==u.password):
                login_session['logged_in'] = True
                flash('You were logged in.')
                login_session['U_Id']=u.id
                return redirect(url_for('home'))
         error = 'Invalid Credentials. Please try again.'
         return render_template('normallogin.html', error=error)
    else:
         return render_template('normallogin.html', error=error)

@app.route('/logout')
def logout():
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        login_session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
#--------------------------------------------------------------------------------------
@app.route('/user/new/', methods=['GET', 'POST'])
def newuser():
    if 'logged_in' in login_session:
        flash('You need to logout first.')
        return redirect(url_for('logout'))
    else:
        if request.method == 'POST':
            newuser=User(email=request.form['Email'],name=request.form['UserName'],password=request.form['Password'])
            login_session['U_Id'] =newuser.id
            flash('Hello %s'%request.form['UserName'])
            return render_template('normallogin.html')  
        else:
            return render_template('newuser.html')

@app.route('/user/edit', methods=['GET', 'POST'])
def edituser():
    return render_template('edituser.html')


#------------------------------------------------------------------------------------------------------------------
@app.route('/issue/new/', methods=['GET', 'POST'])
def newIssue():
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        #login_session['U_Id']=1
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
            target=os.path.join(APP_ROOT,'images/')
            #print target
            if not os.path.isdir(target):
               os.mkdir(target)
            for file in request.files.getlist("file"):
               print file
               filename=file.filename
                #os.rename(filename,request.form['I_Title'])
               destination="/".join([target,filename])
               # print destination
               file.save(destination)
                
            return redirect(url_for('home'))
        else:
            return render_template('newIssue.html')

@app.route('/issue/<int:I_Id>/view')
def  showDetailedIssue(I_Id):
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        showDetailedIssue = session.query(Issue).filter_by(id = I_Id).one()
        showDetailedComment = session.query(Comment).filter_by(id = I_Id).order_by(asc(Comment.sqNo)).all()
        showDetailedUser= session.query(User).filter_by(id= showDetailedIssue.author).one()
        Author=showDetailedUser.name
        #temporarily harcoding the likes and dislikes part
        like=2
        dislike=2
        #showDetailedVote = session.query(Issue).filter_by(id = I_Id).all()
        #showDetailedVote = session,query(func.count())   SELECT count(*) 
        #    FROM (SELECT V_flag FROM Votes where V_IssueId = %s AND V_flag = true)
        # AS likes  GROUP BY V_flag;""",(I_Id,))
        if showDetailedIssue.anonFlag == 1:
           Author="Anonymous"
        return render_template('showdetailedissue.html', Issue=showDetailedIssue, Comment=showDetailedComment, like=like, dislike=dislike, Author=Author)

@app.route('/issue/<int:I_Id>/edit/', methods=['GET', 'POST'])
def editIssue(I_Id):
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        editedIssue = session.query(Issue).filter_by(id=I_Id).one()
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

# Delete a Issue
@app.route('/issue/<int:I_Id>/delete/', methods=['GET', 'POST'])
def deleteIssue(I_Id):
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
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
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        #login_session['U_Id']=1
        issuetocomment= session.query(Issue).filter_by(id = I_Id).one()
        usertocomment=session.query(User).filter_by(id= login_session['U_Id']).one()
        if request.method == 'POST':
            newComment = Comment(content=request.form['C_Content'], user=usertocomment, issue=issuetocomment)
            session.add(newComment)
            session.commit()
            return redirect(url_for('showDetailedIssue',I_Id=issuetocomment.id ))
        else:
            return render_template('newcomment.html',Issue=issuetocomment)

@app.route('/comment/<int:C_Id>/<int:C_SqNo>/edit/', methods=['GET', 'POST'])
def editComment(C_Id,C_SqNo):
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        #login_session['U_Id']=1
        issuetocomment= session.query(Issue).filter_by(id = C_Id).one()
        usertocomment=session.query(User).filter_by(id= login_session['U_Id']).one()
        editComment=session.query(Comment).filter_by(id=C_Id).filter_by(author=login_session['U_Id']).filter_by(sqNo=C_SqNo).one()
        if request.method == 'POST':
            if request.form['C_Content']:
                editComment.content = request.form['C_Content']
                session.add(editComment)
                session.commit()
            return redirect(url_for('showDetailedIssue',I_Id=C_Id ))
        else:
            #part to check if the user is the author of the comment
            return render_template('editcomment.html',Comment=editComment,Issue=issuetocomment)

@app.route('/comment/<int:C_Id>/<int:C_SqNo>/delete/', methods=['GET', 'POST'])
def deleteComment(C_Id,C_SqNo):
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        #login_session['U_Id']=1
        issuetocomment= session.query(Issue).filter_by(id = C_Id).one()
        usertocomment=session.query(User).filter_by(id= login_session['U_Id']).one()
        commenttodelete=session.query(Comment).filter_by(id=C_Id).filter_by(author=login_session['U_Id']).filter_by(sqNo=C_SqNo).one()
        if request.method == 'POST':
            session.delete(commenttodelete)
            # flash('%s Successfully Deleted' % restaurantToDelete.name)
            session.commit()
            return redirect(url_for('showDetailedIssue',I_Id=commenttodelete.id ))
        else:
            #part to check if the user is the author of the comment
            return render_template('deletecomment.html', Comment=commenttodelete)



#------------------------------------------------------------------------------------------------------------------

@app.route('/issue/my/', methods=['GET','POST'])
def  showMyIssue(): 
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        #login_session['U_Id']=2
        if login_session['U_Id']!=None:
            myissue = session.query(Issue).filter_by(author=login_session['U_Id']).all()
            return render_template('showmyissue.html', Issue=myissue)
        else:
            return redirect(url_for('login'))

@app.route('/comment/my/', methods=['GET','POST'])
def showMyComment():
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        #login_session['U_Id']=1
        if login_session['U_Id']!=None:
            mycomment = session.query(Comment).filter_by(author=login_session['U_Id']).all()
            return render_template('showmycomment.html', Comment=mycomment)
        else:
            return redirect(url_for('login'))
   
#-----------------------------------------------------------------------------------------------------------------

@app.route('/issue/nearby/map/', methods=['GET','POST'])
def showNearbyIssueMap():
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
           #Setting distance as 1KM radius 0.00654=1Km
            latmax=float(request.form['I_Lat'])+0.00654
            latmin=float(request.form['I_Lat'])-0.00654
            lngmax=float(request.form['I_Lng'])+0.00654
            lngmin=float(request.form['I_Lng'])-0.00654
            nearbyIssue=session.query(Issue).filter(Issue.lat<latmax,Issue.lat>latmin, Issue.lng<lngmax,Issue.lng>lngmin).all()
            return render_template('shownearbyissuemap.html', Issue=nearbyIssue,CurrentLat=request.form['I_Lat'],CurrentLng=request.form['I_Lng'])
        else:
            return render_template('getlocation.html')


@app.route('/issue/nearby/list/', methods=['GET','POST'])
def showNearbyIssueList():
    if 'logged_in' not in login_session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
           #Setting distance as 1KM radius 0.00654=1Km
            latmax=float(request.form['I_Lat'])+0.00654
            latmin=float(request.form['I_Lat'])-0.00654
            lngmax=float(request.form['I_Lng'])+0.00654
            lngmin=float(request.form['I_Lng'])-0.00654
            nearbyIssue=session.query(Issue).filter(Issue.lat<latmax,Issue.lat>latmin, Issue.lng<lngmax,Issue.lng>lngmin).all()
            return render_template('shownearbyissuelist.html', Issue=nearbyIssue)
        else:
            return render_template('getlocation.html')

#-----------------------------------------------------------------------------------------------------------------   

# LOGIN
@app.route('/glogin', methods=['GET'])
def GLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "%s"%login_session['state']
    # return "",login_session['state']
    return render_template('login.html',STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 409)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 409)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
