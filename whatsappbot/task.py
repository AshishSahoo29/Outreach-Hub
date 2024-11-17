import os
from django.http import HttpResponse
from django.core.cache import cache
from celery import shared_task
from twilio.rest import Client
from .query import Gen

client = Client(os.environ["SID"], os.environ["TOKEN"])


@shared_task
def process_campign_user_request(client_message: str, client_number: str):
    bot = Gen()
    bot_response = bot.query(client_message)
    print("BOT", bot_response)
    cache.set(client_message, bot_response, 300)
    from_whatsapp_number = "whatsapp:+14155238886"
    to_whatsapp_number = client_number

    message = client.messages.create(
        body=str(bot_response),
        from_=from_whatsapp_number,
        to=to_whatsapp_number,
    )
    return message.body
