import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation, Donor, User
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
#app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        donor_switch = 0
        for donor in Donor.select().where(Donor.name == request.form['name']):
            donor_switch = donor.name
        if not donor_switch:
            return render_template('create.jinja2', error="Name entered does not exist in database.")
        if not request.form['number']:
            return render_template('create.jinja2', error="Donation amount cannot be 0.")

        donor_id = Donor.select().where(Donor.name == request.form['name']).get()
        donation = Donation(donor=donor_id, value=request.form['number'])
        donation.save()
        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.select().where(User.name == request.form['name']).get()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('create'))

        return render_template('login.jinja2', error="Incorrect username or password.")

    else:
        return render_template('login.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

