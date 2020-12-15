from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_from_directory
from flask_restful import Resource, Api
from flask_restful import reqparse

from werkzeug.utils import secure_filename

from tensorflow import keras
import tensorflow as tf
import numpy as np

import os
import re
import shutil


app = Flask(__name__,static_folder='static')
api = Api(app)
app.secret_key = 'secret'


app.config['UPLOAD_FOLDER'] = 'uploads/' #Flask-Backend/uploads/
app.config['STATIC_FOLDER'] = 'static/' #Flask-Backend/static/
app.config['MAX_CONTENT_PATH'] = 10*1024*1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

root = app.root_path

class_names = ['butterfly', 'chicken', 'elephant', 'horse', 'sheep', 'spider', 'squirrel']
model = keras.models.load_model('modelLatest000.h5') #Flask-Backend/modelLatest000.h5


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.uploads = []

    def __repr__(self):
        return f'{self.username}>'
    
    def addToUploads(self,picture):
        self.uploads.append(picture)
    
    def getUploads(self):
        return self.uploads

    def __iter__(self):
        return iter(self.getUploads())

users = []
id = 1
users.append(User(id=id, username='jeff', password='jeff'))
users.append(User(id=id+1, username='jeff', password='jeff'))


@app.before_request
def check():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        if request.endpoint == '/' or request.endpoint == 'login' or request.path == '/':
            return redirect(url_for('profile'))

def accepted_filetypes(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/Upload')
def upload():   
    if 'user_id' in session:
        return render_template('Upload.html', user=g.user.username)
    return render_template('Upload.html')


@app.route('/Uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return 'No File Specified'
        if accepted_filetypes(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            print('CLASSIFYING IMAGE:  '+f.filename)
            (winner, prob) = classifyImage(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            if prob < .6:
                return redirect(url_for('unk'))
            if 'user_id' in session:
                if g.user:
                    img = secure_filename(f.filename)
                    use = [x for x in users if x.username == g.user.username][0]
                    fol = str(use.id) + '_' + str(use.username) + '_' + img
                    fol2 = 'styles/priv/' + str(use.id) + '_' + str(use.username) + '_' + img
                    use.addToUploads(fol2)
                    shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)), os.path.join('static/styles/priv', fol))
                    #                  #                 #                 #                     # For the line above ^^^ Flask-Backend/static/styles/priv
            print('CLASSIFICATION:  '+str(winner)+', '+class_names[winner]+', '+str(prob))
            return redirect(url_for(class_names[winner]))
        else:
            return 'File type not accepted'
    return 

@app.route('/unk')
def unk():
    return render_template('unk.html')

@app.route('/squirrel')
def squirrel():
    return render_template('squirrel.html')

@app.route('/squirrel', methods = ['GET','POST'])
def squirrel_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))
        


@app.route('/spider')
def spider():
    return render_template('spider.html')

@app.route('/spider', methods = ['GET','POST'])
def spider_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/sheep')
def sheep():
    return render_template('sheep.html')

@app.route('/sheep', methods = ['GET','POST'])
def sheep_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))


@app.route('/elephant')
def elephant():
    return render_template('elephant.html')

@app.route('/elephant', methods = ['GET','POST'])
def elephant_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))


@app.route('/horse')
def horse():
    return render_template('horse.html')

@app.route('/horse', methods = ['GET','POST'])
def horse_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))


@app.route('/chicken')
def chicken():
    return render_template('chicken.html')

@app.route('/chicken', methods = ['GET','POST'])
def chicken_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))


@app.route('/butterfly')
def butterfly():
    return render_template('butterfly.html')

@app.route('/butterfly', methods = ['GET','POST'])
def butterfly_router():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify another animal':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Account page':
            return redirect(url_for('index'))


@app.route('/loginPage')
def loginPage():
    return render_template('loginPage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('user_id', None)
        tempUser = request.form['username']
        tempPass = request.form['password']
        temp = [x for x in users if x.username == tempUser]
        if temp == []:
            return redirect(url_for('loginPage'))
        user = [x for x in users if x.username == tempUser][0]
        if user and user.password == tempPass:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('loginPage'))
    use = [x for x in users if x.username == g.user.username][0]
    arr = use.getUploads()
    if arr != []:
        lengthArr = len(arr)
        return render_template('profile.html', lengthArr = lengthArr, arr = arr)
    return render_template('profile.html', lengthArr = 0, arr = [] )

@app.route('/profiler', methods = ['POST'])
def profiler():
    if request.method == "POST":
        if request.form['submit_button'] == 'Identify an animal':
            return redirect(url_for('upload'))
 



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods =['GET','POST'])
def contact():
    if request.method == "POST":
        if request.form['submit_button'] == 'Continue to homepage as guest':
            return redirect(url_for('upload'))
        if request.form['submit_button'] == 'Create account':
            return redirect(url_for('createAccount'))
        if request.form['submit_button'] == 'Login page':
            return redirect(url_for('loginPage'))
        if request.form['submit_button'] == 'Home page':
            return redirect(url_for('index'))



@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html')

@app.route('/makeAccount', methods=['GET','POST'])
def makeAccount():
    if request.method == "POST":
        tempUser = request.form['username']
        if request.form['password'] == request.form['password2']:
            tempPass = request.form['password']
            global id
            id += 1
            users.append(User(id=id, username=tempUser, password=tempPass))
            return redirect(url_for('loginPage'))
        else:
            return redirect(url_for('createAccount'))



def validEmailForm(email):
    email_re = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(email_re, email):
        return True
    else:
        return False

def clenseEmail(email):
    email = email.strip()
    if validEmailForm(email):
        return email
    else:
        return ''


def classifyImage(image_file):
    img = keras.preprocessing.image.load_img(image_file, target_size=(360, 360))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    winner = np.argmax(score)
    prob = np.max(score)
    return (winner, prob)
    

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)

