import random

TEST_SEARCH_QUERIES = ["iphone", "led tv sony", "toy", "baby cloth"]
_RANDOM_SEARCH_QUERY = TEST_SEARCH_QUERIES[
    random.randint(0, len(TEST_SEARCH_QUERIES) - 1)
]

TEST_PRODUCT_URLS = [
    "https://www.flipkart.com/google-pixel-7a-coral-128-gb/p/itmb4d7b100b1a4d?pid=MOBGT5F26QJYZUZS",
    "https://www.flipkart.com/boat-stone-350-10-w-bluetooth-speaker/p/itmba477fc3ec7ae?pid=ACCFVWMHBGUNFG97",
    "https://www.flipkart.com/skechers-walking-shoes-women/p/itm188d2075e9fdd?pid=SHOG5MEYY6E8FHTK",
    "https://www.flipkart.com/fossil-kerrigan-analog-watch-women/p/itm072de2231f6d8?pid=WATG3MWAHRQSXFTQ",
]
_RANDOM_PRODUCT_URL = TEST_PRODUCT_URLS[random.randint(0, len(TEST_PRODUCT_URLS) - 1)]
