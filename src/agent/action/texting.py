from typing import Optional, Type, cast, Any
from pydantic import BaseModel, Field
import os
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
    ActionType,
)
from vocode.streaming.action.factory import ActionFactory
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import ActionConfig
from vocode.streaming.telephony.config_manager.base_config_manager import (
    BaseConfigManager,
)
from twilio.rest import Client

from src.loggers import stream_logger


logger = stream_logger(__file__)


# TODO reinitialized redis config manager used globally here cannot be the right way to do this
# should ask the community or keep poking around to see how to pass in the right info to the action config
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)

config_manager = RedisConfigManager()


class TextingActionFactory(ActionFactory):
    def create_action(self, action_config: ActionConfig) -> BaseAction:
        if isinstance(action_config, TwilioSendTextActionConfig):
            return TwilioSendText(action_config, should_respond=True)
        else:
            raise Exception("Invalid action type")


class TwilioSendTextActionConfig(ActionConfig, type="action_twilio_send_text"):
    # config_manager: Optional[Any] = None  # TODO: getting tired, optional[any] is bad
    pass


class TwilioSendTextParameters(BaseModel):
    # TODO adding a number here might allow the agent to pick the number to send to from the transcription
    message: str = Field(..., description="The message to send.")


class TwilioSendTextResponse(BaseModel):
    success: bool


class TwilioSendText(
    BaseAction[
        TwilioSendTextActionConfig, TwilioSendTextParameters, TwilioSendTextResponse
    ]
):
    description: str = "Sends a text message to the patient."
    parameters_type: Type[TwilioSendTextParameters] = TwilioSendTextParameters
    response_type: Type[TwilioSendTextResponse] = TwilioSendTextResponse

    async def run(
        self, action_input: ActionInput[TwilioSendTextParameters]
    ) -> ActionOutput[TwilioSendTextResponse]:
        logger.info(
            f"Text message action triggered in conversation {action_input.conversation_id}"
        )

        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)

        logger.info("Text action getting phone numbers")
        # action_config = cast(TwilioSendTextActionConfig, self.action_config)
        if config_manager is not None:
            logger.info("Config manager found, using config manager")
            call_config = await config_manager.get_config(
                conversation_id=action_input.conversation_id
            )
            logger.info(f"Call config: {call_config}")
            # Note the swap - this should be an inbound call, hence "from" is the text target, and "to" is the service's number
            from_phone = call_config.to_phone
            to_phone = call_config.from_phone
        else:
            # Should just be in testing
            logger.info("No config manager found, using dotenv vars")
            # b/c it's not an inbound call, we likely mean the opposite of the above
            from_phone = os.getenv("FROM_PHONE")
            to_phone = os.getenv("TO_PHONE")

        logger.info(f"Sending text message from {from_phone} to {to_phone}...")
        message = client.messages.create(
            body=action_input.params.message,
            to=to_phone,
        )
        logger.info(f"Sent text message from {from_phone} to {to_phone}: {message.sid}")
        logger.debug(f"Message body: {action_input.params.message}")

        return ActionOutput(
            action_type=self.action_config.type,
            response=TwilioSendTextResponse(success=True),
        )
