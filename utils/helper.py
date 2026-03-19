from typing import Tuple
import pandas as pd
import re
from utils.constants import Platform

def is_low_information(content):
    return len(content) < 7

def is_content_available(content):
    return not (pd.isna(content) or pd.isnull(content) or str(content).strip() == '')

def sanitise_content(content):
    content = str(content) if is_content_available(content) else ''
    content = re.sub(r'(\n|\\n)+', ' ', content)
    return re.sub(r'\s+', ' ', content).strip()

def get_noise_filtered_content(content):
    sanitised_content = sanitise_content(content)

    if is_low_information(sanitised_content):
        return "No meaningful content"
    else:
        return sanitised_content

def get_platform_specific_content(review, platform):
    raw_content = review.get('content', '')
    sanitised_content = get_noise_filtered_content(raw_content)

    if platform == Platform.IOS:
        title = review.get('title', '').strip()
        title = sanitise_content(title)
        if title:
            if sanitised_content.lower() != 'no meaningful content':
                return f"{title} - {sanitised_content}"
            else:
                return title
    return sanitised_content

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def identify_platform_from_device_name(name):
    if not name or pd.isna(name):
        return None

    name = name.lower()
    ios_keywords = ['iphone, ipad', 'ipod']
    if any(keyword in name for keyword in ios_keywords):
        return Platform.IOS.value
    return Platform.ANDROID.value

def extract_details_from_filename(filename) -> Tuple[str, str, str]:
    parts = filename.split('_')
    company_name = parts[0]
    app_name = f"{company_name} {parts[1]}"
    device = parts[2]
    return company_name, app_name, device