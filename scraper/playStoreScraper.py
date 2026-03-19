import os
import pandas as pd
from config import MAX_REVIEW_COUNT
from utils.logger import setup_logger
from google_play_scraper import Sort, reviews

logging = setup_logger(__name__)

def fetch_play_store_reviews(app_id, count=MAX_REVIEW_COUNT, output_dir="./data/play_store"):
    source = 'Google Play Store'
    result, continuation_token = reviews(app_id, count=count, lang="en", country="gb", sort=Sort.NEWEST)
    logging.info(f"Fetched {len(result)} reviews of {app_id}")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"playstore_{app_id}.csv")
    file_exists = os.path.exists(filename)
    if file_exists:
        logging.info(f"csv already exists for {app_id}, skipping.")
    else:
        d = pd.DataFrame(result)
        d.to_csv(filename, index=False)
        logging.info(f"Created csv for {app_id}")
    return result, source
    