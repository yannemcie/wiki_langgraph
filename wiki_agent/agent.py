from typing import Annotated
from typing_extensions import TypedDict
import os
## tools
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_core.runnables.config import RunnableConfig
##langgraph
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

#llm
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition


wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=1000) # type: ignore
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
memory = MemorySaver()


# wiki_tool.invoke('who is Brad Pitt')
tools = [wiki_tool]

#langgraph application
class State(TypedDict):
    messages: Annotated[list[str], add_messages]
    prompt:str

graph_builder = StateGraph(State)
llm = ChatOpenAI(model="gpt-4o",temperature=0)

llm_with_wikitool = llm.bind_tools(tools=tools)

def chatbot(state: State)->object:
    conversation = [state['prompt']] + state['messages']
    return {'messages': [llm_with_wikitool.invoke(conversation)]}


# building our graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")

tool_node=ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph_builder.add_edge("tools",  "chatbot")
graph_builder.add_edge("chatbot", END)

graph=graph_builder.compile(checkpointer=memory)

user_prompt = """
Start by introducing your self as Peter Finkeld. You're going to represent the idea of selling you the subject i'll ask about.
Make sure that your goal is to sell the product im asking about and see how it fits my business needs.

Ask a maximum of 5 questions, no more than that.
Make it conversational questions and relate it to the subject.
Don't paste questions as bullet points. Remember you're talking to a client and you want to be as conversational as possible.
Don't elaborate too much, just be streight to the point. Don't ask long questions.
If you have enough information asking less questions than you can ask less.
Do not ask multiple questions at once.
Don't ask Yes or No questions continue the discussion until i give you either my phone or email.

Don't ask personal information to which you have no interraction with.
If you can't technically send an email to the client, then don't propose that you're send an email even if the client asks.
Don't schedule anything if you don't have the tools to do so.
If you can't generate a link of some kind like Zoom or Google meet, don't propose it.
The idea is to lead the user to ask if he could leave you an email or phone to talk over.
"""

config  = RunnableConfig({"configurable": {"thread_id": "2"}})

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [("user", user_input)], "prompt": user_prompt}, config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)