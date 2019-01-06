# all code in this file was obtained from Twilio.com python quickstart tutorial, unless otherwise notated

# Download the helper library from https://www.twilio.com/docs/python/install

from twilio.rest import Client
# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'your twilio api sid goes here'
auth_token = 'your twilio auth token goes here'
client = Client(account_sid, auth_token)
# message template  # this came from twilio
# message = client.messages.create(body="Join Earth's mightiest heroes. Like Kevin Bacon.",from_='+18645010610',to='+18645094713')  # this came from twilio

def get_txt_client():  # Code by Christopher Torok
	return client
