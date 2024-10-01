# # main.py
# from langchain.utilities import WikipediaAPIWrapper
# from langchain.tools.wikipedia.tool import WikipediaQueryRun
# from langgraph.graph import StateGraph, START, END
# from wiki_agent.state import WikiState

# # Initialize the Wikipedia client provided by langchain_community
# wikipedia_client = WikipediaAPIWrapper

# # Initialize the Wikipedia API wrapper with the correct wiki_client
# wikipedia_api = WikipediaAPIWrapper(wiki_client=wikipedia_client)

# # Initialize the WikipediaQueryRun tool with the API wrapper
# wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_api)

# # Define the function for fetching Wikipedia content using LangChain's Wikipedia tool
# def fetch_wikipedia_content(state: WikiState) -> WikiState:
#     result = wikipedia_tool.run({"query": state["query"]})  # Use the Wikipedia tool to fetch content
#     state["content"] = result[:500]  # Truncate to the first 500 characters
#     return state

# # Define the function to display the content
# def display_content(state: WikiState) -> WikiState:
#     print(f"Topic: {state['query']}")
#     print(f"Summary: {state['content']}")
#     return state

# # Create and configure the StateGraph
# graph = StateGraph(WikiState)
# graph.add_node("fetch_content", fetch_wikipedia_content)
# graph.add_node("display_content", display_content)

# # Define edges between the nodes
# graph.add_edge(START, "fetch_content")
# graph.add_edge("fetch_content", "display_content")
# graph.add_edge("display_content", END)

# # Compile the graph
# compiled_graph = graph.compile()

# def main() -> None:
#     topic: str = input("Enter a Wikipedia topic: ")
#     initial_state: WikiState = {"query": topic, "content": ""}
#     compiled_graph.invoke(initial_state)

# if __name__ == "__main__":
#     main()
