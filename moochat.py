import logging
import json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

from twilio.rest import Client

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


"""
"""
@ask.launch
def prompt_welcome():
    msg = render_template('prompt_welcome')
    return question(msg)

"""
"""
@ask.intent("SayHelloIntent", convert={'name':str})
def prompt_say_hello(name):
    msg = render_template('prompt_say_hellp', name=name)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)