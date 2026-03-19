import logging

from utils.dateTime import get_date_range_from_natural_language
from typing import List, Tuple, Dict
from utils.constants import Platform
import ast


def get_source(platform: Platform):
    if platform == Platform.IOS:
        return 'App Store'
    elif platform == Platform.ANDROID:
        return 'Google Play Store'
    else:
        return 'In Store'

def get_platform(platform: Platform):
    if platform == Platform.INSTORE:
        return 'android, iOS'
    else:
        return platform.value

def store_filter(store_number):
    if isinstance(store_number, List):
        stores = list(map(int, store_number))
        return {"store_number": {"$in": stores}}
    else:
        return {"store_number": {"$eq": int(store_number)}}

def get_app_name_filter(app_name):
    if isinstance(app_name, List):
        return {"app_name": {"$in": app_name}}
    else:
        return {"app_name": {"$eq": app_name}}

def get_filter_params(data, platform: Platform) -> Tuple[Dict, str]:
    input_data = ast.literal_eval(data)
    sentiment = input_data.get("sentiment") or None
    app_name = input_data.get("app_name") or None
    query = input_data.get("query", '')
    is_competitor = input_data.get("is_competitor") or None
    app_version = input_data.get("app_version") or None
    timeframe = input_data.get("timeframe") or None
    rating = input_data.get("rating") or None
    store_number = input_data.get("store_number") or None

    start_date, end_date = get_date_range_from_natural_language(timeframe)
    logging.log(start_date, end_date)
    filter_params = {"$and": [
        {"date_timestamp": {"$gte": start_date}},
        {"date_timestamp": {"$lte": end_date}},
    ]}
    if isinstance(sentiment, str):
        filter_params["$and"].append({"sentiment": {"$eq": sentiment.lower()}})
    if isinstance(is_competitor, bool):
        filter_params["$and"].append({"is_competitor": {"$eq": str(is_competitor).lower()}})
    if app_name:
        filter_params["$and"].append(get_app_name_filter(app_name))
    if isinstance(app_version, str):
        filter_params["$and"].append({"app_version": {"$eq": app_version}})
    if isinstance(rating, int) and not isinstance(rating, bool):
        filter_params["$and"].append({"rating": {"$eq": rating}})
    if platform == Platform.INSTORE and not app_name:
        filter_params["$and"].append({"app_name": {"$eq": 'Asda Scan & Go'}})
    if platform == Platform.INSTORE and store_number:
        filter_params["$and"].append(store_filter(store_number))

    return filter_params, query