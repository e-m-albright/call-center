"""
Telephony server for the app.
"""
import logging
import os

from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.server.base import (
    TwilioInboundCallConfig,
    TelephonyServer,
)

from src import eventsmanager
from src.agent import openai
from src.agent import AppAgentFactory
from src.agent.action.texting import TwilioSendTextActionConfig
from src.synthesizer import elevenlabs
from src.transcriber import deepgram


def server(base_url: str, config_manager: RedisConfigManager, logger: logging.Logger):
    logger.info("Starting telephony server")
    return TelephonyServer(
        base_url=base_url,
        config_manager=config_manager,
        inbound_call_configs=[
            TwilioInboundCallConfig(
                url="/inbound_call",
                twilio_config=TwilioConfig(
                    account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                    auth_token=os.environ["TWILIO_AUTH_TOKEN"],
                ),
                agent_config=openai.cnf(
                    generate_responses=True,
                    end_conversation_on_goodbye=True,
                    # TODO see the texting action for note on specifying inbound number
                    actions=[TwilioSendTextActionConfig()],
                ),
                transcriber_config=deepgram.cnf_for_telephone(),
                synthesizer_config=elevenlabs.cnf_for_telephone(),
            )
        ],
        agent_factory=AppAgentFactory(),
        events_manager=eventsmanager.EventsManager(),
        logger=logger,
    )
