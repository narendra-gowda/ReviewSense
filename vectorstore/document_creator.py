from utils.helper import get_platform_specific_content
from scraper.appStoreScrapper import fetch_app_store_reviews
from scraper.playStoreScraper import fetch_play_store_reviews
from vectorstore.metadata import get_metadata
from langchain_core.documents import Document
from config import APPS_TO_FETCH_FOR_REVIEWS
from utils.logger import setup_logger
from utils.constants import Platform
from typing import Tuple, List
from tqdm import tqdm
import pandas as pd
import os

logger = setup_logger(__name__)

def create_documents_from_reviews(platform: Platform, csv_filename: str) -> Tuple[List[Document], List[str]]:
    documents = []
    ids = []

    if platform == Platform.INSTORE:
        in_store_csv_path = f"./data/in_store/{csv_filename}.csv"

        if not os.path.exists(in_store_csv_path):
            raise FileNotFoundError(f"In store review csv file not found at {in_store_csv_path}")

        logger.info(f"Reading csv file from {in_store_csv_path}")
        df = pd.read_csv(in_store_csv_path)

        for i, row in tqdm(df.iterrows(), total=len(df), desc="Processing reviews"):
            try:
                review_id = f"{csv_filename}-{i}"
                content = get_platform_specific_content(row, platform)
                document = Document(
                    page_content=content,
                    metadata=get_metadata(platform=platform, review=row, content=content, csv_filename=csv_filename),
                    id=review_id,
                )
                documents.append(document)
                ids.append(review_id)
            except Exception as e:
                tqdm.write(f"Skipping review {i + 2}: {e}")
                continue
    else:
        for app in APPS_TO_FETCH_FOR_REVIEWS:
            if platform == Platform.ANDROID:
                reviews, source = fetch_play_store_reviews(app.get('android_appid'))
            elif platform == Platform.IOS:
                reviews, source = fetch_app_store_reviews(app.get('ios_appid'), app.get('app_name'))
            else:
                continue

            for i, review in tqdm(enumerate(reviews), total=len(reviews), desc=f"Processing reviews of {app.get('app_name', '')}"):
                try:
                    review_id = str(review.get('reviewId', f"missing-{i}")) + str(i)
                    content = get_platform_specific_content(review, platform)
                    document = Document(
                        page_content=content,
                        metadata=get_metadata(platform=platform, review=review, content=content, app=app, source=source),
                        id=review_id,
                    )
                    documents.append(document)
                    ids.append(review_id)
                except Exception as e:
                    tqdm.write(f"Skipping review {review_id} of {app['app_name']}: {e}")
                    continue
    return documents, ids