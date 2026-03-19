from utils.helper import safe_int, extract_details_from_filename, identify_platform_from_device_name
from utils.dateTime import get_iso_and_timestamp_date
from utils.sentiment import sentiment_analyzer
from utils.constants import Platform
from typing import Optional

def get_metadata(
        platform: Platform,
        review,
        content: str,
        app: Optional[dict[str, int | str | list[str]]] = None,
        source: Optional[str]  = None,
        csv_filename: Optional[str] = None):
    if platform == Platform.INSTORE:
        date_str = review.get('event_date', '')
    else:
        date_str = review.get('at', '')

    date_iso_str, date_timestamp = get_iso_and_timestamp_date(date_str)

    if platform == Platform.INSTORE:
        if not csv_filename:
            raise ValueError("csv_filename must be specified")
        company_name, app_name, device = extract_details_from_filename(csv_filename)
        device_model = review.get('mobile_phone_model') or None
        device_platform = identify_platform_from_device_name(device_model)
        return {
            "rating": safe_int(review.get('rating')),
            "sentiment": sentiment_analyzer(content),
            "app_name": app_name,
            "platform": device_platform,
            "company_name": company_name,
            "source": "In Store",
            "category": "Scan & Go",
            "is_competitor": 'false',
            "device": device,
            "date": date_iso_str,
            "date_timestamp": date_timestamp,
            "store_number": safe_int(review.get('store_number')),
            "app_version": review.get('app_version') or None,
            "device_model": device_model,
            "device_os_version": review.get('mobile_os_version') or None,
        }
    else:
        return {
            "rating": safe_int(review.get('score')),
            "user_name": review.get('userName') or None,
            "date": date_iso_str,
            "date_timestamp": date_timestamp,
            "sentiment": sentiment_analyzer(content),
            "app_version": review.get('appVersion') or None,
            "app_name": app.get('app_name') or None,
            "categories": ", ".join(app.get('categories', [])),
            "is_competitor": app.get('is_competitor', 'false'),
            "company_name": app.get('company_name') or None,
            "app_id": app.get('ios_appid') if platform == Platform.IOS else app.get('android_appid'),
            "source": source,
            "platform": platform.value,
        }