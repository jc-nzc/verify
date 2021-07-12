import os
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, render_template, redirect, session, url_for
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()
app = Flask(__name__)
app.secret_key = 'secretkeyfordungeon'
app.config.from_object('settings')

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID= os.environ.get('VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

KNOWN_PARTICIPANTS = app.config['KNOWN_PARTICIPANTS']


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        if username in KNOWN_PARTICIPANTS:
            session['username'] = username
            send_verification(username)
            return redirect(url_for('verify_passcode_input'))
        error = "User not found. Please try again."
        return render_template('index.html', error = error)
    return render_template('index.html')
