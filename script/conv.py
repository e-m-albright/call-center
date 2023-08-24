"""
Streaming local conversation employing an Agent

Use headphones or push-to-talk on the microphone to avoid the Agent talking & interrupting itself

This script tests conversation functionality locally (no telephone involved)
We don't have any local components set up so it's still all using API's / keys for Agent/Transcriber/Synthesizer

We can get them locally following this
https://docs.vocode.dev/open-source/local-conversation

Built from
https://docs.vocode.dev/open-source/python-quickstart
"""
import asyncio
import signal
from dotenv import load_dotenv

from vocode.streaming.streaming_conversation import StreamingConversation
from vocode.helpers import (
    create_streaming_microphone_input_and_speaker_output as create_io,
)

from src.loggers import stream_logger
from src.agent import openai
from src.agent.prompt import agenda
from src.transcriber import deepgram
from src.synthesizer import elevenlabs
from src.eventsmanager import EventsManager
from src.agent.action.texting import TextingActionFactory, TwilioSendTextActionConfig

load_dotenv()

logger = stream_logger(__file__)


async def main():
    microphone_input, speaker_output = create_io(use_default_devices=True)

    conversation = StreamingConversation(
        output_device=speaker_output,
        agent=openai.agent(
            openai.cnf(
                generate_responses=True,
                end_conversation_on_goodbye=True,
                prompt_preamble=agenda.test_preamble,
                actions=[TwilioSendTextActionConfig()],
            ),
            action_factory=TextingActionFactory(),
            logger=logger,
        ),
        # TODO log the transcriber/synthesizer?
        transcriber=deepgram.transcriber(deepgram.cnf_for_device(microphone_input)),
        synthesizer=elevenlabs.synthesizer(elevenlabs.cnf_for_device(speaker_output)),
        events_manager=EventsManager(),
        logger=logger,
    )

    # The intro is super choppy, I would expect this to fix that - but I don't think it's implemented on the ElevenLabs client
    # Maybe a "cold" synthesizer isn't the reason the start is rushed?
    conversation.warmup_synthesizer()

    await conversation.start()
    print("Conversation started, press Ctrl+C to end")
    signal.signal(
        signal.SIGINT, lambda _0, _1: asyncio.create_task(conversation.terminate())
    )

    while conversation.is_active():
        chunk = await microphone_input.get_audio()
        conversation.receive_audio(chunk)


if __name__ == "__main__":
    asyncio.run(main())
