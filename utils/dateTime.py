from datetime import datetime, date, timezone, UTC
from dateutil.parser import parse
from dateparser import parse
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_date_range_from_natural_language(timeframe: str = None):
    now = datetime.now(UTC)
    if not timeframe or not isinstance(timeframe, str) or timeframe.lower() == 'none':
        timeframe = '6 months ago'
    parsed_date = parse(date_string=timeframe, settings={
        'PREFER_DATES_FROM': 'past',
        'PREFER_DAY_OF_MONTH': 'first',
        'PREFER_MONTH_OF_YEAR': 'first',
        'TIMEZONE': 'UTC',
        'RELATIVE_BASE': now,
    })
    if not parsed_date:
        raise ValueError(f"Unable to determine date range for : {timeframe}")

    start_date = int(parsed_date.timestamp())
    end_date = int(now.timestamp())
    return start_date, end_date

def to_iso_format_if_date(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value

def get_iso_and_timestamp_date(date_str):
    if pd.isna(date_str) or pd.isnull(date_str):
        raise ValueError(f"Missing or invalid review date")
    try:
        sanitized_date_str = to_iso_format_if_date(date_str)
        dt = parse(sanitized_date_str)
        date_iso_str = dt.astimezone(timezone.utc).replace(tzinfo=None).isoformat()
        timestamp = parse(date_iso_str).timestamp()
        date_timestamp = int(timestamp)
        return date_iso_str, date_timestamp
    except Exception as e:
        raise ValueError(f"Failed to parse {date_str}: {e}")