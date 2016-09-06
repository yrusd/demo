from flask import Flask
 
# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
import flask_sqlalchemy as sqlalchemy
 
app = Flask(__name__)
# We'll just use SQLite here so we don't need an external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
 
db = sqlalchemy.SQLAlchemy(app)

class BankContacts(db.Model):
    """Bank Contacts"""
    id = db.Column(db.Integer, primary_key=True)
    bankname = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    other = db.Column(db.String(255))

from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
 
app.config['SECRET_KEY'] = 'please, tell nobody'
 
class BankContactsForm(Form):
    bankname = StringField(u'The Bank Name is')
    phone = StringField(u'Phone')
    other = StringField(u'Other')
    # submit button will read "share my lunch!"
    submit = SubmitField(u'commit!')

from flask import render_template
 
@app.route("/")
def root():
    banks = BankContacts.query.all()
    form = BankContactsForm()
    return render_template('index.html', form=form, banks=banks)

from flask import url_for, redirect
 
@app.route(u'/new', methods=[u'POST'])
def newlunch():
    form = BankContactsForm()
    if form.validate_on_submit():
        bankContacts = BankContacts()
        form.populate_obj(bankContacts)
        db.session.add(bankContacts)
        db.session.commit()
    return redirect(url_for('root'))

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run()