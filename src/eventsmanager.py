import os
import typing
from typing import Optional

from fastapi import FastAPI
from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import TranscriptCompleteEvent, TranscriptEvent
from vocode.streaming.utils import events_manager

from src import ROOT_DIR
from src.loggers import stream_logger


logger = stream_logger(__file__)

CALL_TRANSCRIPTS_DIR = ROOT_DIR / "out" / "transcripts"
os.makedirs(CALL_TRANSCRIPTS_DIR, exist_ok=True)


def add_transcript(conversation_id: str, transcript: str) -> None:
    transcript_path = os.path.join(
        CALL_TRANSCRIPTS_DIR, "{}.txt".format(conversation_id)
    )
    with open(transcript_path, "a") as f:
        f.write(transcript)


def get_transcript(conversation_id: str) -> Optional[str]:
    transcript_path = os.path.join(
        CALL_TRANSCRIPTS_DIR, "{}.txt".format(conversation_id)
    )
    if os.path.exists(transcript_path):
        with open(transcript_path, "r") as f:
            return f.read()
    return None


def delete_transcript(conversation_id: str) -> bool:
    transcript_path = os.path.join(
        CALL_TRANSCRIPTS_DIR, "{}.txt".format(conversation_id)
    )
    if os.path.exists(transcript_path):
        os.remove(transcript_path)
        return True
    return False


class EventsManager(events_manager.EventsManager):
    def __init__(self):
        super().__init__(subscriptions=[EventType.TRANSCRIPT_COMPLETE])

    async def handle_event(self, event: Event):
        if event.type == EventType.TRANSCRIPT:
            transcript_event = typing.cast(TranscriptEvent, event)
            logger.info("transcript: {}".format(transcript_event.text))
        elif event.type == EventType.TRANSCRIPT_COMPLETE:
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            add_transcript(
                transcript_complete_event.conversation_id,
                transcript_complete_event.transcript.to_string(),
            )
        elif event.type == EventType.PHONE_CALL_CONNECTED:
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            logger.info("Phone call started!")
        elif event.type == EventType.PHONE_CALL_ENDED:
            transcript_complete_event = typing.cast(TranscriptCompleteEvent, event)
            logger.info("Phone call ended")
        elif event.type == EventType.RECORDING:
            logger.info("Recording")
        elif event.type == EventType.ACTION:
            logger.info("Action")
