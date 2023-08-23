
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