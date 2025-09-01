import random
from django.conf import settings

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def send_otp_via_sms(phone, otp):
    # DEV: print to console (fallback)
    print(f"DEBUG OTP for {phone}: {otp}")

    # PRODUCTION (Twilio example) - uncomment + configure env vars
    # from twilio.rest import Client
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=f"Your OTP is {otp}",
    #     from_=settings.TWILIO_FROM_NUMBER,
    #     to=phone
    # )
    # return message.sid
