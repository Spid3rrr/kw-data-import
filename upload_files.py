from supa import insert_csv

PROPERTIES_FILE = "./data/kw-skipper_properties.csv"
SALES_FILE = "./data/kw-sales.csv"
SKIPPER_STATS_SALES_FILE = "./data/kw-skipper-stats-sales.csv"

def upload_properties():
    return insert_csv(PROPERTIES_FILE)

def upload_sales():
    return insert_csv(SALES_FILE)

def upload_skipper_stats_sales():
    return insert_csv(SKIPPER_STATS_SALES_FILE)
