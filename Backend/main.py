from flask import Flask,jsonify,request,render_template,Response
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timedelta
from functools import wraps
from celery import Celery
from json import dumps
from celery.schedules import crontab
from flask_mail import Mail,Message
import bcrypt
import csv

from celery_system import make_celery

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from jinja2 import Template
from weasyprint import HTML
import uuid



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
)
celery=make_celery(app)

app.config['JWT_SECRET_KEY']='super-secret'
jwt=JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
CORS(app, resources={r"/*": {"origins": "*"}})

db=SQLAlchemy(app)


# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
# celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'],broker=app.config['CELERY_BROKER_URL'],timezone="Asia/Calcutta",enable_utc=False)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='deyroh777@gmail.com'
app.config['MAIL_PASSWORD']='vwbkeugpjgseunqj'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18,minute=30),
        task1.s(),
        name="periodic task"
    )
    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'),
        pdf.s(),
        name="pdf task"
    )

@celery.task
def task1():
    with app.app_context():
        users=UserModel.query.all()
        cutoff_time = datetime.now()
    for user in users:
        lasvi_time = datetime.strptime(user.lasvi, '%d/%m/%Y, %H:%M:%S')
        time_difference = cutoff_time - lasvi_time
        if time_difference > timedelta(seconds=86400):
            print(user.email)
            with app.app_context():
                msg=Message("Bloglite",sender='deyroh777@gmail.com',recipients=[user.email])
                msg.body='Hey there! We miss you, come visit our website and see whats new!.'
                mail.send(msg)
                print('sent')
    return "finished"

@celery.task()
def m(results):
    csv_file_path = 'post_data.csv'
    fieldnames = results[0].keys()

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for post in results:
            writer.writerow(post)
    return "done"


class UserModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100))
    lasvi=db.Column(db.String(100))
    name=db.Column(db.String(100))
    username=db.Column(db.String)
    password=db.Column(db.String)
    following=db.Column(db.String(300))
    follower=db.Column(db.String(300))


    def __repr__(self):
        return f"User(name={self.name}, username={self.username}, password={self.password}, following={self.following}, follower={self.follower},email={self.email},lasvi={self.lasvi})"

class PostModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userp_id=db.Column(db.Integer)
    namep=db.Column(db.String(150))
    image=db.Column(db.String(300))
    title=db.Column(db.String(150))
    caption=db.Column(db.String(300))
    date=db.Column(db.String(300))
    
    def __repr__(self):
        return f"User(user_id={self.userp_id}, title={self.title}, caption={self.caption},date={self.date},image={self.image},namep={self.namep})"

with app.app_context():
    db.create_all()


@app.route('/csv/<int:user_id>',methods=['GET'])
@jwt_required()
def c(user_id):
    results=PostModel.query.filter_by(userp_id=user_id).all()
    output=[]
    for result in results:
        post_data={}
        post_data['id']=result.id
        post_data['userp_id']=result.userp_id
        post_data['title']=result.title
        post_data['caption']=result.caption
        post_data['date']=result.date
        post_data['image']=result.image
        post_data['namep']=result.namep
        output.append(post_data)
    m.delay(output)
    return "c dispatch success"



@app.route('/search',methods=['GET'])
@jwt_required()
def search():
    result=UserModel.query.all()
    output=[]
    for user in result:
        user_data={}
        user_data['id']=user.id
        user_data['username']=user.username
        user_data['name']=user.name
        user_data['following']=user.following
        user_data['follower']=user.follower
        user_data['email']=user.email
        output.append(user_data)
    return jsonify(output)


#register
@app.route('/user',methods=['POST'])
def create_user():
    name=request.form.get("name")
    username=request.form.get("username")
    password=request.form.get("password")
    email=request.form.get("email")
    follower=''
    following=''
    user_id=None
    hpassword=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    new_user=UserModel(id=user_id,name=name,username=username,password=hpassword,follower=follower,following=following,email=email)
    db.session.add(new_user)
    db.session.commit()
    access_token=create_access_token(identity={"username":username})
    return {"token":access_token},200


@app.route('/user/<int:user_id>',methods=['GET'])
@jwt_required()
def get_one_user(user_id):
    user=UserModel.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'No user found'})
    user_data={}
    user_data['id']=user.id
    user_data['username']=user.username
    user_data['name']=user.name
    user_data['following']=user.following
    user_data['follower']=user.follower
    user_data['email']=user.email


    return jsonify(user_data)



@app.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    result = UserModel.query.filter_by(username=username).first()
    if result is None:
        abort(404, message="Could not find user with that username")
    if bcrypt.checkpw(password.encode('utf-8'),result.password):
        access_token=create_access_token(identity={"username":username})
        return {"token":access_token,'id':result.id,'username': result.username,'name':result.name,'follower':result.follower,'following':result.following},200
    else:
        return "wrong password"
    
@app.route('/user/<int:user_id>',methods=['PUT'])

@jwt_required()
def update_user(user_id):
    following=request.form.get("following")
    follower=request.form.get("follower")
    lasvi=request.form.get("lasvi")
    user=UserModel.query.filter_by(id=user_id).first()
    if following is not None:
        user.following=following
    if follower is not None:
        user.follower=follower

    if lasvi is not None:
        user.lasvi=lasvi

    db.session.commit()

    user_data={}
    user_data['id']=user.id
    user_data['username']=user.username
    user_data['name']=user.name
    user_data['following']=user.following
    user_data['follower']=user.follower
    user_data['email']=user.email
    user_data['lasvi']=user.lasvi
    return jsonify(user_data)

@app.route('/getPost/<int:post_id>',methods=['GET'])
@jwt_required()
def getPost(post_id):
    result=PostModel.query.filter_by(id=post_id).first()
    if not result:
        abort(404, message="Could not find post with that id")
    post_data={}
    post_data['id']=result.id
    post_data['userp_id']=result.userp_id
    post_data['title']=result.title
    post_data['caption']=result.caption
    post_data['date']=result.date
    post_data['image']=result.image
    post_data['namep']=result.namep
    return jsonify(post_data)

@app.route('/allPost',methods=['GET'])
@jwt_required()
def get_all_post():
    results=PostModel.query.all()
    if not results:
        abort(404, message="Could not find post with that id")
    output=[]
    for result in results:
        post_data={}
        post_data['id']=result.id
        post_data['userp_id']=result.userp_id
        post_data['title']=result.title
        post_data['caption']=result.caption
        post_data['date']=result.date
        post_data['image']=result.image
        post_data['namep']=result.namep
        output.append(post_data)
    return jsonify(output)

@app.route('/post/<int:userp_id>',methods=['GET'])
@jwt_required()
def get_post(userp_id):
    results=PostModel.query.filter_by(userp_id=userp_id).all()
    if not results:
        abort(404, message="Could not find post with that id")
    output=[]
    for result in results:
        post_data={}
        post_data['id']=result.id
        post_data['userp_id']=result.userp_id
        post_data['title']=result.title
        post_data['caption']=result.caption
        post_data['date']=result.date
        post_data['image']=result.image
        post_data['namep']=result.namep
        output.append(post_data)
    return jsonify(output)

@app.route('/post',methods=['POST'])
@jwt_required()
def post():
    id=None
    title=request.form.get("title")
    caption=request.form.get("caption")
    userp_id=request.form.get("userp_id")
    date=request.form.get("date")
    namep=request.form.get("namep")
    result=PostModel(id=id,title=title,caption=caption,userp_id=userp_id,date=date,image='no',namep=namep)
    db.session.add(result)
    db.session.commit()

    post_data={}
    post_data['id']=result.id
    post_data['userp_id']=result.userp_id
    post_data['title']=result.title
    post_data['caption']=result.caption
    post_data['date']=result.date
    post_data['image']=result.image
    post_data['namep']=result.namep
    return jsonify(post_data)


@app.route('/post/u/<int:post_id>',methods=['PUT'])
@jwt_required()
def put_post(post_id):
    image=request.form.get("image")
    title=request.form.get("title")
    caption=request.form.get("caption")
    date=request.form.get("date")
    result = PostModel.query.filter_by(id=post_id).first()
    if not result:
        abort(404, message="post doesn't exist, cannot update")
    
    if title is not None:
        result.title=title
    if caption is not None:
        result.caption=caption
    if date is not None:
        result.date=date
    if image is not None:
        result.image=image
    db.session.commit()

    post_data={}
    post_data['id']=result.id
    post_data['userp_id']=result.userp_id
    post_data['title']=result.title
    post_data['caption']=result.caption
    post_data['date']=result.date
    post_data['image']=result.image
    post_data['namep']=result.namep
    return jsonify(post_data)

@app.route('/post/u/<int:post_id>',methods=['DELETE'])
@jwt_required()
def delete(post_id):
    data = PostModel.query.get(post_id)
    db.session.delete(data)
    db.session.commit()
    return 'deleted'

@app.route('/file-upload',methods=["POST"])
@jwt_required()
def postf():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('../Frontend/fsecond/src/assets', filename))
            return {'message' : 'success'},201



@app.route('/user/internal/<string:usernamee>',methods=['GET'])
@jwt_required()
def get_one_user_i(usernamee):
    user=UserModel.query.filter_by(username=usernamee).first()
    if not user:
        return jsonify({'message':'No user found'})
    user_data={}
    user_data['id']=user.id
    # user_data['public_id']=user.public_id
    user_data['username']=user.username
    # user_data['password']=user.password
    user_data['name']=user.name
    user_data['following']=user.following
    user_data['follower']=user.follower
    user_data['email']=user.email


    return jsonify(user_data)


@celery.task
def pdf():
    result=UserModel.query.all()
    output=[]
    for user in result:
        output.append([user.id,user.email])
    for i in output:
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        posts = PostModel.query.filter_by(userp_id=i[0]).filter(PostModel.date >= one_month_ago.strftime("%Y-%m-%d")).all()
        outputPosts=[]
        for post in posts:
            post_data={}
            post_data['title']=post.title
            post_data['caption']=post.caption
            post_data['date']=post.date
            outputPosts.append(post_data)
        emaill=i[1]
        create_pdf_report(outputPosts,emaill)
    return "done"

def create_pdf_report(data,emaill):
    message=format_report("pdf.html",data=data)
    html=HTML(string=message)
    file_name=str(uuid.uuid4())+".pdf"
    print(file_name)
    pdf_path = os.path.join(app.root_path, "pdfs", file_name)
    html.write_pdf(target=pdf_path)

    with app.open_resource(pdf_path) as fp:
        pdf_data = fp.read()

    msg = Message("Bloglite", sender='deyroh777@gmail.com', recipients=[emaill])
    msg.body = 'Hey there! We have attached your montly engangement pdf'
    msg.attach(file_name, "application/pdf", pdf_data)
    mail.send(msg)

    print('sent')

    os.remove(pdf_path)
    return "mail sent"



def format_report(template_file,data={}):
    with open(template_file) as file:
        template=Template(file.read())
        return template.render(data=data)



if __name__=="__main__":
    app.run(debug=True)

#follower and folowing list