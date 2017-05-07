import logging
import json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

# from twilio.rest import Client

# this is gitignored, so add your credentials here
# from env import * 

# Setup twilio info
# account_sid = TWILIO_ACCOUNT_SID
# auth_token = TWILIO_AUTH_TOKEN
# client = Client(account_sid, auth_token)


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
@ask.intent("AddContactInitIntent")
def prompt_new_contact_name():
    msg = render_template('prompt_for_name')
    return question(msg)

"""
"""
@ask.intent("AddContactNameIntent", convert={'name': str})
def prompt_new_contact_number(name):
    session.attributes['name'] = name
    msg = render_template('prompt_for_number', name=name)
    return question(msg)

"""
"""
@ask.intent("AddContactNumberIntent", convert={'number': int})
def add_to_contact_book_confirm(number):
    name = session.attributes['name']

    contacts = []

    # load the contacts
    with open('contacts.json', 'r') as f:
        contacts = json.loads(f.read())
    
    contacts.append({
        'name': name,
        'number': number
    })

    with open('contacts.json', 'w') as f:
            json.dump(contacts, f)
    
    msg = render_template('add_contact_confirm', name=name)

    return statement(msg)

"""
"""
@ask.intent("SendToContactIntent", convert={'name':str, 'query':str})
def send_to_contact(name, query):
    try:
        contacts = []
        with open('contacts.json', 'r') as f:
            contacts = json.loads(f.read())
        
        number = None
        for contact in contacts:
            if contact['name'] == name:
                number = contact['number']

        if number == None:
            msg = render_template('send_to_contact_missing', name=name)
            return statement(msg)

        # message = client.messages.create(to='+1{number}'.format(number=str(number)),
        #                                  from_=TWILIO_NUMBER,
        #                                  body="Her look there's a {query}!!!".format(query=query))
        
        print("Enable twilio to send text");

        msg = render_template('send_to_contact_confirm')

        return statement(msg)

    except Exception as e:
        print(e)

        msg = render_template('send_to_contact_error')
        return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)