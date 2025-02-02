from __future__ import annotations

from langchain.chains.conversational_retrieval.base import (
    BaseConversationalRetrievalChain,
)
from langchain.chains.conversational_retrieval.base import (
    ConversationalRetrievalChain,
)  # noqa: E501
from langchain.memory import ConversationSummaryMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

from src.project_chat.config import Config


def retrieve(db: Chroma, config: Config) -> BaseConversationalRetrievalChain:
    """
    Retrieves a conversational retrieval chain using a specified database and
    configuration settings.
    :param config: Configuration settings for the language model.
    :param db: The database instance used for retrieval.
    :return: A conversational retrieval chain instance.
    """
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8},
    )
    llm = ChatOpenAI(
        model=config.model,
        temperature=0,
    )
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    return ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, memory=memory
    )
