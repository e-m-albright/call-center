
TODO not sure if this would be useful yet

```python

from src.agent.tool.contacts import get_all_contacts
from src.agent.tool.vocode import call_phone_number
from src.agent.tool.word_of_the_day import word_of_the_day
from langchain.memory import ConversationBufferMemory

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType


if __name__ == "__main__":
    OBJECTIVE = (
        input("Objective: ")
        or "Find a random person in my contacts and tell them a joke"
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")  # type: ignore
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # Logging of LLMChains
    agent = initialize_agent(
        tools=[get_all_contacts, call_phone_number, word_of_the_day],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )
    agent.run(OBJECTIVE)

```

Some scratch code while we work out how tool use / texting should operate

```python


# TODO readd to agent getter or it's not going to do anything
class TextingChatGPTAgent(ChatGPTAgent):
    def get_functions(self):
        self.logger.info("Getting functions")
        actions = super().get_functions()
        self.logger.info("Got: " + str(actions))
        return actions
        # assert self.agent_config.actions
        # if not self.action_factory:
        #     return None
        # return [
        #     self.action_factory.create_action(action_config).get_openai_function()
        #     for action_config in self.agent_config.actions
        # ]

    # async def respond(
    #     self,
    #     human_input,
    #     conversation_id: str,
    #     is_interrupt: bool = False,
    # ) -> Tuple[str, bool]:
    #     assert self.transcript is not None
    #     if is_interrupt and self.agent_config.cut_off_response:
    #         cut_off_response = self.get_cut_off_response()
    #         return cut_off_response, False
    #     self.logger.debug("LLM responding to human input")
    #     if self.is_first_response and self.first_response:
    #         self.logger.debug("First response is cached")
    #         self.is_first_response = False
    #         text = self.first_response
    #     else:
    #         chat_parameters = self.get_chat_parameters()
    #         chat_completion = await openai.ChatCompletion.acreate(**chat_parameters)
    #         text = chat_completion.choices[0].message.content
    #     self.logger.debug(f"LLM response: {text}")
    #     return text, False

    # async def generate_response(
    #     self,
    #     human_input: str,
    #     conversation_id: str,
    #     is_interrupt: bool = False,
    # ) -> AsyncGenerator[Union[str, FunctionCall], None]:
    #     if is_interrupt and self.agent_config.cut_off_response:
    #         cut_off_response = self.get_cut_off_response()
    #         yield cut_off_response
    #         return
    #     assert self.transcript is not None

    #     if self.agent_config.vector_db_config:
    #         docs_with_scores = await self.vector_db.similarity_search_with_score(
    #             self.transcript.get_last_user_message()[1]
    #         )
    #         docs_with_scores_str = "\n\n".join(
    #             [
    #                 "Document: "
    #                 + doc[0].metadata["source"]
    #                 + f" (Confidence: {doc[1]})\n"
    #                 + doc[0].lc_kwargs["page_content"].replace(r"\n", "\n")
    #                 for doc in docs_with_scores
    #             ]
    #         )
    #         vector_db_result = f"Found {len(docs_with_scores)} similar documents:\n{docs_with_scores_str}"
    #         messages = format_openai_chat_messages_from_transcript(
    #             self.transcript, self.agent_config.prompt_preamble
    #         )
    #         messages.insert(
    #             -1, vector_db_result_to_openai_chat_message(vector_db_result)
    #         )
    #         chat_parameters = self.get_chat_parameters(messages)
    #     else:
    #         chat_parameters = self.get_chat_parameters()
    #     chat_parameters["stream"] = True
    #     stream = await openai.ChatCompletion.acreate(**chat_parameters)
    #     async for message in collate_response_async(
    #         openai_get_tokens(stream), get_functions=True
    #     ):
    #         yield message


# class SpellerAgent(BaseAgent):
#     def __init__(self, agent_config: SpellerAgentConfig):
#         super().__init__(agent_config=agent_config)
#         self.config_manager = RedisConfigManager()

#     async def respond(
#         self,
#         human_input,
#         conversation_id: str,
#         is_interrupt: bool = False,
#     ) -> Tuple[Optional[str], bool]:
#         call_config = self.config_manager.get_config(conversation_id)
#         if call_config is not None:
#             from_phone = call_config.twilio_from
#             to_phone = call_config.twilio_to
#         return "".join(c + " " for c in human_input), False

#     # is_interrupt is True when the human has just interrupted the bot's last response
#     def respond(
#         self, human_input, is_interrupt: bool = False
#     ) -> tuple[Optional[str], bool]:
#         return self.agent_config.message

#     def generate_response(
#         self, human_input, is_interrupt: bool = False
#     ) -> Generator[str, None, None]:
#         """Returns a generator that yields the agent's response one sentence at a time."""
#         yield self.agent_config.message


# from vocode.streaming.user_implemented_agent.restful_agent import RESTfulAgent
# from vocode.streaming.models.agent import (
#     RESTfulAgentOutput,
#     RESTfulAgentText,
#     RESTfulAgentEnd,
# )


# class YourAgent(RESTfulAgent):
#     # input: the transcript from the Conversation that the agent must respond to
#     async def respond(self, input: str, conversation_id: str) -> RESTfulAgentOutput:
#         if "bye" in input:
#             return RESTfulAgentEnd()  ## ends the conversation
#         else:
#             return RESTfulAgentText(response=input)  ## responds with the input received

# TODO - goodbye detection for triggering text?
# AgentResponseStop

# nah... try tools


```