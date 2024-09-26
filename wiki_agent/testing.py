from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import WikipediaRetriever
from typing import Any

retriever = WikipediaRetriever() # type: ignore
docs = retriever.invoke("TOKYO GHOUL")

prompt = ChatPromptTemplate.from_template(
    """Answer the question very rudely based only on the context provided.

Context: {context}

Question: {question}"""
)

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

def format_docs(docs: Any) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

chain:Any= (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke(
    "Who is the main character in `Tokyo Ghoul` and does he transform into a ghoul?"
))