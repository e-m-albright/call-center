import os

from dotenv import load_dotenv
from langchain.agents import tool
from twilio.rest import Client

from src.loggers import stream_logger


load_dotenv()

logger = stream_logger(__file__)


@tool("text caller appointment details")
def text_caller_appointment_details(message: str) -> str:
    """texts the calling phone number the appointment details."""

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=os.getenv("FROM_PHONE"),
        body=message,
        to=os.getenv("TO_PHONE"),
    )

    logger.info("Texted caller: %s", message.sid)
    # get_transcript(call.conversation_id) ?
    return
