from typing import Annotated
from typing_extensions import TypedDict
import os
## tools
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
##langgraph
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
#llm
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition


wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=5) # type: ignore
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper) 

# wiki_tool.invoke('who is Brad Pitt')
tools = [wiki_tool]

#langgraph application
class State(TypedDict):
    messages: Annotated[list[str], add_messages]

graph_builder = StateGraph(State)
llm = ChatOpenAI(model="gpt-4o",temperature=0)

llm_with_wikitool = llm.bind_tools(tools=tools)

def chatbot(state: State)->object:
    return {'messages': [llm_with_wikitool.invoke(state['messages'])]}


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

graph=graph_builder.compile()

user_input = "who is Angelina Jolie"
events = graph.stream(
    {"messages":[("user", user_input)]}, stream_mode="values"
)

for event in events:
    event["messages"][-1].pretty_print()
    