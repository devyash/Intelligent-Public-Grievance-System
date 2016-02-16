from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from IPGSdb import *

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def showIssues():

	return render_template('index.html')

@app.route('/issues/new/', methods=['GET', 'POST'])
def newIssues():
    if request.method == 'POST':
    	#New Issue = createIssues(I_Author = login_session['U_Id'],I_Title = request.form['I_Title'],I_Content = request.form['I_Content'],I_Lat= request.form['I_Lat'],I_Lng= request.form['I_Lng'],I_Image= request.form['I_Image'],I_AnonFlag= request.form['I_AnonFlag'],I_Type= request.form['I_Type'])
        #newIssues = Issues(name=request.form['name'])
        #flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        print request.form['I_Lat']
        print request.form['I_Lng']
        print request.form['I_Title']
        print request.form['I_Content']
        print request.form['I_Type']
        print request.form['I_AnonFlag']
        return redirect(url_for('showIssues'))
    else:
        return render_template('newIssues.html')


@app.route('/issues/<int:I_Id>/edit/', methods=['GET', 'POST'])
def editIssues(I_Id):
 #   editedRestaurant = session.query(
  #      Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        #if request.form['name']:
           # editedRestaurant.name = request.form['name']
            #flash('Restaurant Successfully Edited %s' % edited:
        return render_template('editIssues.html', I_Id=I_Id )
    else:
        return redirect(url_for('showIssues'))
# Delete a restaurant
@app.route('/issues/<int:I_Id>/delete/', methods=['GET', 'POST'])
def deleteIssues(I_Id):
    #restaurantToDelete = session.query(
    #   Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
       # session.delete(restaurantToDelete)
       # flash('%s Successfully Deleted' % restaurantToDelete.name)
       #session.commit()
        return redirect(url_for('showIssues', restaurant_id=restaurant_id))
    else:
        return render_template('deleteIssues.html', I_Id=I_Id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
