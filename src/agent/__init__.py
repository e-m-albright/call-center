import logging
from typing import Optional, Tuple
import typing
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import AgentConfig, AgentType, ChatGPTAgentConfig
from vocode.streaming.agent.base_agent import BaseAgent, RespondAgent
from vocode.streaming.agent.factory import AgentFactory

from src.agent import openai
from src.agent.action.texting import TextingActionFactory


class AppAgentFactory(AgentFactory):
    def create_agent(
        self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None
    ) -> BaseAgent:
        if agent_config.type == AgentType.CHAT_GPT:
            return openai.agent(
                agent_config,
                logger=logger,
                # Action Factory selection is specified via configuration actions
                # include a list of configurations that map to the desired actions
                action_factory=TextingActionFactory(),
            )
        raise Exception("Invalid agent config")
