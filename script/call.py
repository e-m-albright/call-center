"""
Execute an outbound call with an Agent
"""
import os

from dotenv import load_dotenv
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.telephony.config_manager.in_memory_config_manager import (
    InMemoryConfigManager,
)

from src.agent import openai
from src.loggers import stream_logger
from src.synthesizer import elevenlabs
from src.transcriber import deepgram


load_dotenv()
logger = stream_logger(__name__)

BASE_URL = os.environ["BASE_URL"]
FROM_PHONE = os.environ["FROM_PHONE"]
TO_PHONE = os.environ["TO_PHONE"]

# Little annoyed by the redis rename in the docker compose when running outside, just use in-mem for this test script
# os.environ["REDISHOST"] = "redis"


async def main():
    config_manager = InMemoryConfigManager()

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        from_phone=FROM_PHONE,
        to_phone=TO_PHONE,
        config_manager=config_manager,
        agent_config=openai.cnf(
            generate_responses=True, end_conversation_on_goodbye=True
        ),
        synthesizer_config=elevenlabs.cnf_for_telephone(),
        transcriber_config=deepgram.cnf_for_telephone(),
        logger=logger,
    )

    input("Press enter to start call...")
    await outbound_call.start()

    # TODO: this isn't seemingly working. The call doesn't stream back and forth. Needs the telephony server?


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
