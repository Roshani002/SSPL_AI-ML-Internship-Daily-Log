from load_data import DatabaseConnect
from fetch_transform_data import fetch_data_api, transform_data
from news_table import News

loader = DatabaseConnect()

def etl_pipeline():
    extracted_data = fetch_data_api()
    transformed_data = transform_data(extracted_data)
    loader.load_data(transformed_data)

etl_pipeline()