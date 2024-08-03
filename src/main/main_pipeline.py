import os
from dotenv import load_dotenv
from src.stages.extract.extract_api import ExtractFromAPI
from src.stages.transform.transform_raw_data import TransformRawData
from src.stages.load.load_data import LoadData
from src.drivers.api_requester import ApiRequester
from src.drivers.api_collector import ApiCollector
from src.infra.database_connector import DatabaseConnection
from src.infra.database_repository import DatabaseRepository

class MainPipeline:
    def __init__(self) -> None:
        load_dotenv()

        self.api_key = os.getenv('API_KEY')

        if not self.api_key:
            raise ValueError("API key is not set in environment variables.")

        self.__extract_api = ExtractFromAPI(ApiRequester(self.api_key), ApiCollector())
        self.__transform_raw_data = TransformRawData()
        self.__load_data = LoadData(DatabaseRepository())

    def run_pipeline(self) -> None:
        try:
            print("Connecting to the database...")
            DatabaseConnection.connect()
            print("Database connected.")

            print("Starting extraction...")
            extract_contract = self.__extract_api.extract()
            print("Extraction complete.")

            print("Starting transformation...")
            transformed_data_contract = self.__transform_raw_data.transform(extract_contract)
            print("Transformation complete.")

            print("Starting loading...")
            self.__load_data.load(transformed_data_contract)
            print("Loading complete.")
        except Exception as e:
            print(f"Error running the pipeline: {e}")

if __name__ == "__main__":
    pipeline = MainPipeline()
    pipeline.run_pipeline()
