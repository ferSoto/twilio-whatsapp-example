import os

import requests
from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client


# Variables from https://www.twilio.com/console
SID = os.environ['TWILIO_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']


client = Client(SID, AUTH_TOKEN)
app = Flask(__name__)


@app.route('/whatsapp', methods=['POST'])
def whatsapp_entry():
    # Whatsapp number message comes frome
    _from = request.form['From']
    # Twilio sandbox number
    _to = request.form['To']
    message = 'Holi, crayoli!'

    return str(client.messages.create(
        to=_from,
        from_=_to,
        body=message
    ))


if __name__ == '__main__':
    app.run()
