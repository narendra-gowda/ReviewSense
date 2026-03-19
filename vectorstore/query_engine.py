from vectorstore.retriever_factory import get_cached_retriever_with_filters
from vectorstore.filters import get_filter_params
from langchain_core.documents import Document
from utils.constants import Platform

def app_store_retriever(filter_data) -> list[Document]:
    filter_params, query = get_filter_params(filter_data, platform=Platform.IOS)
    print("--APP STORE--", filter_params, query)
    retriever = get_cached_retriever_with_filters(platform=Platform.IOS, filter_params=filter_params)
    return retriever.invoke(query)

def play_store_retriever(filter_data) -> list[Document]:
    filter_params, query = get_filter_params(filter_data, platform=Platform.ANDROID)
    print("--PLAY STORE--", filter_params, query)
    retriever = get_cached_retriever_with_filters(platform=Platform.ANDROID, filter_params=filter_params)
    return retriever.invoke(query)

def in_store_retriever(filter_data) -> list[Document]:
    filter_params, query = get_filter_params(filter_data, platform=Platform.INSTORE)
    print("--IN STORE--", filter_params, query)
    retriever = get_cached_retriever_with_filters(platform=Platform.INSTORE, filter_params=filter_params)
    return retriever.invoke(query)