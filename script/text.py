"""
Send a text message using Twilio.
"""
import os

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

FROM_PHONE = os.environ["FROM_PHONE"]
TO_PHONE = os.environ["TO_PHONE"]

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


if __name__ == "__main__":
    message = client.messages.create(
        from_=FROM_PHONE,
        body="Hello, testing testing, 1-2-3",
        to=TO_PHONE,
    )

    print(message.sid)
