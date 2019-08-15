import os

import requests
from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client


# Variables from https://www.twilio.com/console
SID = os.environ['TWILIO_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

# This URL calls a service which extract text from an image or a PDF file.
# The endpoint `inpsect` receives a POST request with form data and a single
# parameter 'url' which contains the URL to the media file.
EXTRACTOR_URL = 'http://0.0.0.0:5042/inspect'


client = Client(SID, AUTH_TOKEN)
app = Flask(__name__)


def media_content(url):
    """ Calls a service which extracts text from images and PDF files.

    :param String url: URL to Image/PDF file.
    """
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'url': url}
    response = requests.post(EXTRACTOR_URL, headers=headers, data=data)
    return response.content


@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    # Whatsapp number message comes frome
    _from = request.form['From']
    # Twilio sandbox number
    _to = request.form['To']
    # Number of media files. As far as I know, it's always 1 or 0.
    # If more than one file is sent, this endpoint will receive two or more
    # requests.
    num_media = int(request.form['NumMedia'])
    message = None
    if num_media > 0:
        # Process media (Image or PDF)
        url = request.form['MediaUrl0']
        message = media_content(url)
    else:
        # Reply with generic message
        message = 'Holi, crayoli!'

    return str(client.messages.create(
        to=_from,
        from_=_to,
        body=message
    ))


if __name__ == '__main__':
    app.run()
