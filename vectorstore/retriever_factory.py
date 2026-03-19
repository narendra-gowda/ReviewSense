from config import EMBEDDING_MODEL, BASE_DB_LOCATION, COLLECTION_NAME
from vectorstore.document_creator import create_documents_from_reviews
from vectorstore.retriever_config import get_retriever_args
from utils.vector_store_utils import batch_insert
from langchain_ollama import OllamaEmbeddings
from utils.logger import setup_logger
from utils.constants import Platform
from langchain_chroma import Chroma
from typing import Optional
import os

logger = setup_logger(__name__)

INITIALISED_RETRIEVERS = {}

def get_retriever(
        platform: Platform,
        db_name: str,
        collection: str,
        csv_filename: Optional[str] = None,
        force_insert: Optional[bool] = False) -> Chroma:

    if not isinstance(platform, Platform):
        raise ValueError(f'Platform must be an instance of Platform, received {platform}')

    collection_name = f"{platform.value}_{collection}"
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db_location = BASE_DB_LOCATION+db_name
    add_documents = force_insert or not os.path.exists(db_location)

    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=db_location,
        embedding_function=embeddings,
    )

    if add_documents:
        if force_insert:
            logger.info(f"Re-vectorizing {platform.value} app reviews, this might take a while...")
        else:
            logger.info(f"\n⚠️ Oops looks like {platform.value} app reviews are not available in Vector Store, this might take a while...\n")
        documents, ids = create_documents_from_reviews(platform, csv_filename)
        batch_insert(vector_store, documents, ids)

    return vector_store

def create_retriever(platform: Platform) -> Chroma:
    args = get_retriever_args(platform)
    return get_retriever(
        platform=platform,
        db_name=args.get("db_name"),
        collection=COLLECTION_NAME,
        csv_filename=args.get("csv_filename", ''))

def setup_and_initialise_vector_db():
    for platform in Platform:
        INITIALISED_RETRIEVERS[platform] = create_retriever(platform)

def get_cached_vector_store(platform: Platform):
    return INITIALISED_RETRIEVERS.get(platform) or create_retriever(platform)

def get_cached_retriever_with_filters(platform: Platform, filter_params):
    vector_store = get_cached_vector_store(platform)
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 25, "filter": filter_params}
    )
    return retriever