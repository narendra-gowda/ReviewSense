MAX_REVIEW_COUNT = 1000
BATCH_SIZE = 1000
LLM = "mistral-small3.2"
EMBEDDING_MODEL = "mxbai-embed-large"
BASE_DB_LOCATION = "./chroma_db/"
COLLECTION_NAME = "app_reviews"
APPSTORE_CHROMA_DB_LOCATION = "app_store_reviews"
PLAYSTORE_CHROMA_DB_LOCATION = "play_store_reviews"
IN_STORE_CHROMA_DB_LOCATION = "in_store_reviews"

APPS_TO_FETCH_FOR_REVIEWS = [
    # Asda Rewards
    {
        'ios_appid': 1578902078,
        'android_appid': 'com.asda.rewards',
        'app_name': 'Asda Rewards',
        'categories': ['Loyalty'],
        'is_competitor': 'false',
        'company_name': 'Asda'
    },
    # # Asda Scan & Go
    # {
    #     'ios_appid': 1413258515,
    #     'android_appid': 'com.asda.ScanandGoMobile',
    #     'app_name': 'Asda Scan & Go',
    #     'categories': ['Scan & Go'],
    #     'is_competitor': 'false',
    #     'company_name': 'Asda'
    # },
    # # George at Asda
    # {
    #     'ios_appid': 1507115261,
    #     'android_appid': 'com.georgeatasda',
    #     'app_name': 'George',
    #     'categories': ['Fashion', 'Home'],
    #     'is_competitor': 'false',
    #     'company_name': 'Asda'
    # },
    # Asda Groceries
    {
        'ios_appid': 396089960,
        'android_appid': 'com.asda.android',
        'app_name': 'Asda Groceries',
        'categories': ['Groceries'],
        'is_competitor': 'false',
        'company_name': 'Asda'
    },
    # M&S Sparks
    {
        'ios_appid': 538410698,
        'android_appid': 'com.marksandspencer.app',
        'app_name': 'M&S',
        'categories': ['Loyalty', 'Groceries', 'Fashion', 'Home'],
        'is_competitor': 'true',
        'company_name': 'M&S'
    },
    # Morrisons More
    {
        'ios_appid': 919226668,
        'android_appid': 'com.morrisons.matchandmore.app',
        'app_name': 'Morrisons More',
        'categories': ['Loyalty'],
        'is_competitor': 'true',
        'company_name': 'Morrisons'
    },
    # Tesco Grocery & Club card
    {
        'ios_appid': 389581236,
        'android_appid': 'com.tesco.grocery.view',
        'app_name': 'Tesco Grocery & Clubcard',
        'categories': ['Loyalty', 'Groceries'],
        'is_competitor': 'true',
        'company_name': 'Tesco'
    },
    # Sainsbury's Groceries
    {
        'ios_appid': 1086056964,
        'android_appid': 'com.sainsburys.gol',
        'app_name': "Sainsbury's Groceries",
        'categories': ['Groceries'],
        'is_competitor': 'true',
        'company_name': "Sainsbury's"
    },
]
