from typing import Dict
from config import IN_STORE_CHROMA_DB_LOCATION, APPSTORE_CHROMA_DB_LOCATION, PLAYSTORE_CHROMA_DB_LOCATION
from utils.constants import Platform


def get_retriever_args(platform: Platform) -> Dict[str, str]:
    args = {
        Platform.INSTORE: {
            'db_name': IN_STORE_CHROMA_DB_LOCATION,
            'csv_filename': "Asda_Scan & Go_mobile"
        },
        Platform.IOS: {
            'db_name': APPSTORE_CHROMA_DB_LOCATION,
        },
        Platform.ANDROID: {
            'db_name': PLAYSTORE_CHROMA_DB_LOCATION,
        }
    }
    return args.get(platform, {})