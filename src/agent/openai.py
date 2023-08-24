"""
Agents generate responses and use tools in response to natural language instructions

This file contains the configuration for the OpenAI agents
"""
from vocode.streaming.agent.base_agent import RespondAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import AgentConfig, ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage

from src.agent.prompt import agenda


def cnf(*args, **kwargs) -> AgentConfig:
    return ChatGPTAgentConfig(
        initial_message=BaseMessage(text=agenda.initial),
        prompt_preamble=agenda.preamble,
        *args,
        **kwargs,
    )


def agent(cnf: AgentConfig, *args, **kwargs) -> RespondAgent:
    return ChatGPTAgent(
        agent_config=cnf,
        *args,
        **kwargs,
    )
