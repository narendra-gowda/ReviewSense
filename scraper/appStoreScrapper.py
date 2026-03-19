from utils.logger import setup_logger
import os
import pandas as pd
import requests
import time

logging = setup_logger(__name__)

def safe_get(review, attributes):
   keys = attributes.split(".")
   for key in keys:
       if isinstance(review, dict):
           review = review.get(key, {})
       else :
           return {}
   return  review.get("label", "")

def fetch_with_retires(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response
            elif response.status_code == 400:
                logging.error(f"{response.status_code} Bad request for - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed: {e}, retrying in {delay} seconds")
            time.sleep(delay)
    return None

def fetch_app_store_reviews_paginated(appid, page_number):
    url = f"https://itunes.apple.com/gb/rss/customerreviews/page={page_number}/id={appid}/sortBy=mostRecent/json"
    response = fetch_with_retires(url)
    if not response:
        return []

    data = response.json()
    entries = data.get("feed", {}).get("entry", [])
    parsed_reviews = []
    for entry in entries:
        parsed_reviews.append({
            "userName": safe_get(entry, "author.name"),
            "at": safe_get(entry, "updated"),
            "score": safe_get(entry, "im:rating"),
            "appVersion": safe_get(entry, "im:version"),
            "reviewId": safe_get(entry, "id"),
            "title": safe_get(entry, "title"),
            "content": safe_get(entry, "content"),
        })
    return parsed_reviews

def fetch_app_store_reviews(appid, app_name, output_dir="./data/app_store"):
    page_count = 10 #ToDo - add to config
    source = "App Store"
    os.makedirs(output_dir, exist_ok=True)
    file = os.path.join(output_dir, f"appStore_{app_name}.csv")
    file_exit = os.path.exists(file)
    total_reviews = []
    for page_number in range(1, page_count + 1):
        review_per_page = fetch_app_store_reviews_paginated(appid, page_number)
        total_reviews.extend(review_per_page)
    logging.info(f"Fetched {len(total_reviews)} reviews for {app_name} app")
    if file_exit:
        logging.info(f"csv already exists for {app_name} app")
    else: #TODO - add option to config
        d = pd.DataFrame(total_reviews)
        d.to_csv(file, index=False)
        logging.info(f"Created csv for {app_name} app")
    return total_reviews, source