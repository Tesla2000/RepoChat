from __future__ import annotations

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.project_chat.config import Config


def vectorize(config: Config) -> Chroma:
    loader = GenericLoader.from_filesystem(
        path=config.repo_path,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
    )
    documents = loader.load()
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    return Chroma.from_documents(
        texts,
        OpenAIEmbeddings(disallowed_special=()),
        persist_directory=str(config.persistence.absolute()),
    )
