from typing import Optional, Type
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
from twilio.rest import Client

from src.loggers import stream_logger


logger = stream_logger(__file__)


class TextingActionFactory(ActionFactory):
    def create_action(self, action_config: ActionConfig) -> BaseAction:
        if isinstance(action_config, TwilioSendTextActionConfig):
            return TwilioSendText(action_config, should_respond=True)
        else:
            raise Exception("Invalid action type")


class TwilioSendTextActionConfig(ActionConfig, type="action_twilio_send_text"):
    pass


class TwilioSendTextParameters(BaseModel):
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
        logger.info("Text message action triggered")

        logger.info(f"Message body: {action_input}")
        logger.info(f"ac: {action_input.action_config}")
        logger.info(f"ci: {action_input.conversation_id}")
        logger.info(f"p: {action_input.params}")
        logger.info(f"umt: {action_input.user_message_tracker}")

        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)

        # TODO this is hardcoded to the dotenv vars
        # use action_input.conversation_id to phone number lookup? force the agent to provide the transcription number?
        # RedisConfigManager has a action_input.conversation_id lookup - could that help store the number?
        message = client.messages.create(
            from_=os.getenv("FROM_PHONE"),
            body=action_input.params.message,
            to=os.getenv("TO_PHONE"),
        )
        logger.info(f"Sent text message: {message.sid}")
        logger.debug(f"Message body: {action_input.params.message}")

        return ActionOutput(
            action_type=self.action_config.type,
            response=TwilioSendTextResponse(success=True),
        )
