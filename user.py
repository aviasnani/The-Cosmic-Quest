from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo


app = Flask(__name__) #instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'timelineismalleable'
app.config['MONGO_URI'] = "mongodb://localhost:27017/chapter_quizzes"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"



@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin): #table 
  id = db.Column(db.Integer, primary_key = True)
  fname = db.Column(db.String(20), nullable = False)
  lname = db.Column(db.String(20), nullable = False)
  email = db.Column(db.String(40), nullable = False, unique=True)
  phone = db.Column(db.String(20), nullable = False, unique=True)
  username = db.Column(db.String(20), nullable = False, unique = True)
  password = db.Column(db.String(100), nullable = False)

class Score(db.Model):  
  score_id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  score = db.Column(db.Integer, nullable=False)





class SignupForm(FlaskForm):
  fname = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "First Name"})
  lname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name"})
  email = EmailField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Email id"})
  phone = StringField(validators=[InputRequired(), Length(min=10, max=20)], render_kw={"placeholder": "Phone number"})
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
  password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Signup")
  error = ""
  def validate_username(self, username):
    existing_username = User.query.filter_by(username=username.data).first()
    if existing_username:
      raise ValidationError("This username already exists.")
  def validate_email(self, email):
    existing_email = User.query.filter_by(email=email.data).first()
    if existing_email:
      raise ValidationError("This email id already exists.")
  def validate_phone(self, phone):
    existing_phone = User.query.filter_by(phone=phone.data).first()
    if existing_phone:
      raise ValidationError("This phone number already exists")
    
   
  
class LoginForm(FlaskForm):
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
  password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Login")



@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signup', methods = ["GET", "POST"])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data)
      new_user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, phone=form.phone.data, username=form.username.data, password=hashed_password)
      db.session.add(new_user) #adding new user to the database
      db.session.commit() #saving changes
      initial_score = Score(user_id=new_user.id, score=0) #setting an initial score of 0 for every new user
      db.session.add(initial_score) # adding that initial score to the score table in the database
      db.session.commit() #saving changes
      return redirect(url_for('login')) #redirecting to login after the new user is created

  return render_template('signup.html',form=form)

@app.route('/login', methods = ["GET", "POST"])
def login():
  error = None
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      if bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user) 
        session.pop('score', None)  # clearning the score session variable
        session.pop('message', None) # clearing the message session variable
        return redirect(url_for('dashboard'))
      else:
       error = "Incorrect Password!"
    else: 
      error = "Username not found!"
  return render_template('login.html',form=form, error=error)



@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
  first_name = current_user.fname
  return render_template('dashboard.html', first_name=first_name)

@app.route('/stats', methods=["GET", "POST"])
def stats():
  total_score = 125
  user_id = current_user.id
  user_score = Score.query.filter_by(user_id=user_id).order_by(Score.score_id.desc()).first()
  score = user_score.score if user_score else 0
  return render_template('stats.html', score=score, total_score=total_score)

@app.route('/profile', methods=["GET","POST"])
@login_required
def profile():
  first_name = current_user.fname
  last_name = current_user.lname
  email = current_user.email
  phone = current_user.phone
  username = current_user.username
  return render_template('profile.html', first_name = first_name, last_name = last_name, email = email, phone = phone, username=username)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/chapters', methods=['GET', 'POST'])
def chapters():
  return render_template('chapters.html')

@app.route('/chapter1')
def chapter1():
  return render_template('chapter1.html')

@app.route('/chapter2')
def chapter2():
  return render_template('chapter2.html')

@app.route('/chapter3')
def chapter3():
  return render_template('chapter3.html')

@app.route('/chapter4')
def chapter4():
  return render_template('chapter4.html')

@app.route('/chapter5')
def chapter5():
  return render_template('chapter5.html')

@app.route('/chapter6')
def chapter6():
  return render_template('chapter6.html')

@app.route('/c1q1', methods=["GET","POST"])
def c1q1():
   if 'score' not in session:
        session['score'] = 0 
   quiz = mongo.db.chapter1.find_one() # chapter 1 quiz 1
   if request.method == "POST":
        selected_answer = request.form.get('planet')
        correct_answer = quiz["correct answer"] #correct answer of quiz one
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        if message == "That was correct!":
           user_score = Score.query.filter_by(user_id=user_id).order_by(Score.score_id.desc()).first()
           current_score = user_score.score if user_score else 0
           new_score_value = current_score + 5
           if user_score:
              user_score.score = new_score_value
           else:
              new_score = Score(user_id=user_id, score=new_score_value)
              db.session.add(new_score)
        db.session.commit()
    
   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c1q1.html', quiz=quiz, message=message, score=score)

@app.route('/c1q2', methods=["GET","POST"])
def c1q2():
   quiz_cursor = mongo.db.chapter1.find().skip(1).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('planet')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        
    
   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c1q2.html', quiz=quiz, message=message, score=score)

@app.route('/c1q3', methods=["GET","POST"])
def c1q3():
   quiz_cursor = mongo.db.chapter1.find().skip(2).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('planet')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()
  
   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c1q3.html', quiz=quiz, message=message, score=score)

@app.route('/c1q4', methods=["GET","POST"])
def c1q4():
   quiz_cursor = mongo.db.chapter1.find().skip(3).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('planet')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()
    
   
   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c1q4.html', quiz=quiz, message=message, score=score)

@app.route('/c1q5', methods=["GET","POST"])
def c1q5():
   quiz_cursor = mongo.db.chapter1.find().skip(4).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('planet')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()

   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c1q5.html', quiz=quiz, message=message, score=score)

@app.route('/c2q1', methods=["GET","POST"])
def c2q1():
   quiz = mongo.db.chapter2.find_one()
   if request.method == "POST":
        selected_answer = request.form.get('galaxy')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()

   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c2q1.html', quiz=quiz, message=message, score=score)

@app.route('/c2q2', methods=["GET","POST"])
def c2q2():
   quiz_cursor = mongo.db.chapter2.find().skip(1).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('galaxy')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()

   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c2q2.html', quiz=quiz, message=message, score=score)

@app.route('/c2q3', methods=["GET","POST"])
def c2q3():
   quiz_cursor = mongo.db.chapter2.find().skip(2).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('galaxy')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()

   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c2q3.html', quiz=quiz, message=message, score=score)

@app.route('/c2q4', methods=["GET","POST"])
def c2q4():
   quiz_cursor = mongo.db.chapter2.find().skip(3).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('galaxy')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()

   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c2q4.html', quiz=quiz, message=message, score=score)

@app.route('/c2q5', methods=["GET","POST"])
def c2q5():
   quiz_cursor = mongo.db.chapter2.find().skip(4).limit(1)
   quiz = next(quiz_cursor, None)
   if request.method == "POST":
        selected_answer = request.form.get('galaxy')
        correct_answer = quiz["correct answer"]
        message = 'That was correct!' if selected_answer == correct_answer else f'Sorry, the answer was {correct_answer}'
        session['message'] = message
        session['score'] = session.get('score', 0) + 5 if message == 'That was correct!' else session.get('score', 0)
        user_id = current_user.id
        new_score = Score(user_id=user_id, score=session['score'])
        db.session.add(new_score)
        db.session.commit()

   message = session.pop('message', None)
   score = session.get('score', 0)
   return render_template('c2q5.html', quiz=quiz, message=message, score=score)

    
@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('login'))
 


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)