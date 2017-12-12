from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from functools import wraps
from twilio.request_validator import RequestValidator
from flask import render_template

TWILIO_ACCOUNT_SID = "AC4a4419d0b3aeb6023b49c188e5457f7e"
TWILIO_AUTH_TOKEN = '1d6bde4be1288abb42aa4178e0d631e1'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           configuration_error=None)

@app.route('/', methods=['GET', 'POST'])
def getUserInput():
    response = VoiceResponse()
    new_url = request.url + 'gather'

    getInput = Gather(action=new_url, method='POST', num_digits=5, finishOnKey='#')
    getInput.say("We are going to play Fizz Buzz. Please enter a number and press pound.")

    response.append(getInput)

    return str(response)

@app.route('/gather', methods=['GET', 'POST'])
def fizzbuzzTWIML():
    response = VoiceResponse()

    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    request_valid = validator.validate(
        request.url,
        request.form,
        request.headers.get('X-TWILIO-SIGNATURE', ''))

    if not request_valid:
        response.say("Not a Twilio account")

    response.say("Starting now")

    number = int(request.form.get('Digits', ''))

    for i in range(1, number + 1):
        if i % 3 == 0 and i % 5 == 0:
            response.say("fizzbuzz.")
        elif i % 3 == 0:
            response.say("fizz.")
        elif i % 5 == 0:
            response.say("buzz.")
        else:
            string = str(i) + "."
            response.say(string)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
