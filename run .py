from flask import Flask, render_template,json,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

with open('cofigure.json','r') as c:
    params=json.load(c) ["params"]

app.secret_key="super-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/hotel"
# initialize the app with the extension
db= SQLAlchemy(app)



    

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/login',methods=["GET","POST"])
def login():
     if request.method == "POST":
        uname = request.form["name"]
        passw = request.form["passw"]
        login =  Account.query.filter_by(name=uname, password=passw).first()
        
     if login is not None:
            return render_template("room2.html")
     else:
        userprofile = Account.query.filter_by(name=uname, password=passw).first()
        return render_template("userprofile.html",userprofile=userprofile)
     return render_template("login_page.html")

class Account(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(20))
    password = db.Column(db.String(80))
    confirm = db.Column(db.String(120))
    date = db.Column(db.String(12))


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password  = request.form.get('passw')
        confirm  = request.form.get('re-passw')

        register = Account(name = name, email = email, password = password, confirm = confirm,date=datetime.now())
        db.session.add(register)
        db.session.commit()
        return render_template("login_page.html")
    return render_template("register_page.html")


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(20))
    whatsup_no = db.Column(db.Integer)
    subject = db.Column(db.String(20))
    date = db.Column(db.String(120))

@app.route('/contact',methods=["GET","POST"])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        whatsup_no=request.form.get('Whatsup_no')
        subject=request.form.get('subject')
        entry = Contact(name=name,whatsup_no=whatsup_no,date=datetime.now(),email=email,subject=subject)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html")

@app.route('/room')
def room():
    return render_template("room.html")

@app.route('/room2')
def room2():
    return render_template("room2.html")

@app.route('/luxuary')
def luxuary():
    return render_template("luxuary.html")


@app.route('/dulex')
def dulex():
    return render_template("dulex.html")

@app.route('/single')
def single():
    return render_template("single.html")

@app.route('/double')
def double():
    return render_template("double.html")

@app.route('/triple')
def triple():
    return render_template("triple.html")

@app.route('/guest')
def guest():
    return render_template("guest.html")


@app.route('/booknow')
def booknow():
    return render_template("booknow.html")

@app.route('/userprofile')
def userprofile():
    account = Account.query.all()
    return render_template("userprofile.html",account=account)

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    if request.method=="POST":
        username=request.form.get('uname')
        userpass=request.form.get('passw')
        if (username == params['admin_user'] and  userpass == params['admin_pass']):
            session['user'] = username
            contact = Contact.query.all()
            account = Account.query.all()
            payment = Payment.query.all()
        return render_template("dashboard.html",params=params,contact=contact,account=account,payment=payment)
    return render_template("admin.html",params=params)



class Payment(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(20))
    city = db.Column(db.String(20))
    check_in = db.Column(db.String(20))
    check_out = db.Column(db.String(20))
    room_type = db.Column(db.String(20))
    name_on_card = db.Column(db.Integer)
    credit_no = db.Column(db.String(20))
    exp_month = db.Column(db.String(20))
    exp_year = db.Column(db.String(20))
    cvv = db.Column(db.String(20))
    date = db.Column(db.String(120))


@app.route('/payment',methods=["GET","POST"])
def payment():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        check_in=request.form.get('check_in')
        check_out=request.form.get('check_out')
        city=request.form.get('city')
        room_type=request.form.get('room_type')
        name_on_card=request.form.get('name_on_card')
        credit_no=request.form.get('credit_no')
        exp_month=request.form.get('exp_month')
        exp_year=request.form.get('exp_year')
        cvv=request.form.get('cvv')
        
        payment = Payment(name=name,exp_month=exp_month,city=city,exp_year=exp_year,cvv=cvv,credit_no=credit_no,date=datetime.now(),name_on_card=name_on_card,email=email,check_in=check_in,check_out = check_out , room_type = room_type)
        
        db.session.add(payment)
        db.session.commit()
        
        return render_template("id.html")
    
    return render_template("payment.html")

@app.route('/logout')
def logout():
    session.clear
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/index2')
def index2():
    return render_template("index2.html")


class Id(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    id = db.Column(db.String(20))
    date = db.Column(db.String(20))


@app.route('/id',methods=["GET","POST"])
def id():
    if(request.method=='POST'):
        name=request.form.get('name')

    detai = Payment.query.filter_by(name=name).first()
    if detai:
        return str(detai.sno)
    else:
        return "no recird"

if __name__ == '__main__':
    app.run(debug=True)