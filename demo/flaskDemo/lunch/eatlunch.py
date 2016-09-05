from flask import Flask
 
# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
import flask_sqlalchemy as sqlalchemy
 
app = Flask(__name__)
# We'll just use SQLite here so we don't need an external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
 
db = sqlalchemy.SQLAlchemy(app)

class Lunch(db.Model):
    """A single lunch"""
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(63))
    food = db.Column(db.String(255))

from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
 
app.config['SECRET_KEY'] = 'please, tell nobody'
 
class LunchForm(Form):
    submitter = StringField(u'Hi, my name is')
    food = StringField(u'and I ate')
    # submit button will read "share my lunch!"
    submit = SubmitField(u'share my lunch!')

from flask import render_template
 
@app.route("/")
def root():
    lunches = Lunch.query.all()
    form = LunchForm()
    return render_template('index.html', form=form, lunches=lunches)

from flask import url_for, redirect
 
@app.route(u'/new', methods=[u'POST'])
def newlunch():
    form = LunchForm()
    if form.validate_on_submit():
        lunch = Lunch()
        form.populate_obj(lunch)
        db.session.add(lunch)
        db.session.commit()
    return redirect(url_for('root'))

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run()