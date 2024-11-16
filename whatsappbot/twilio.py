import os
from twilio.rest import Client

client = Client(os.environ["SID"], os.environ["TOKEN"])  # client request


def send(number):

    from_whatsapp_number = "whatsapp:+14155238886"
    to_whatsapp_number = "whatsapp:" + number

    message = client.messages.create(
        body="Hello world!",
        from_=from_whatsapp_number,
        to=to_whatsapp_number,
    )

    return message.body
