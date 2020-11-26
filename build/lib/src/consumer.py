import os
from abc import ABC, abstractmethod

from kinesis.consumer import KinesisConsumer
from kinesis.state import DynamoDB

from src.logger import LoggerFactory
from src.db import MySql


class Consumer(ABC):
    def __init__(self):
        self._app_name = os.environ.get("APP_NAME")
        self._kinesis_source_stream_name = os.environ.get("KINESIS_SOURCE_STREAM_NAME")
        self._kcl_state_manager_table_name = os.environ.get("KCL_STATE_MANAGER_TABLE_NAME")
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        self._logger = LoggerFactory.get_logger(name=__name__, log_level=log_level)
        self._mysql_host_url = os.environ.get("MYSQL_HOST_URL")
        self._mysql_database_name = os.environ.get("MYSQL_DATABASE_NAME")
        self._endpoint_url = os.environ.get("ENDPOINT_URL")
        db_host = os.environ.get("MYSQL_HOST_URL")
        db_name = os.environ.get("MYSQL_DATABASE_NAME")
        db_username = os.environ.get("MYSQL_DB_USERNAME")
        db_password = os.environ.get("MYSQL_DB_PASSWORD")
        self._mysql = MySql(host=db_host, db=db_name, user=db_username, password=db_password)

        self.process_messages()

    def process_messages(self):
        self._logger.info(f"Starting processing for app: {self._app_name}")
        try:
            state = DynamoDB(table_name=self._kcl_state_manager_table_name, endpoint_url=self._endpoint_url)
            consumer = KinesisConsumer(stream_name=self._kinesis_source_stream_name, state=state, endpoint_url=self._endpoint_url)
            for message in consumer:
                self._logger.debug(message)
                self.process(message["Data"].decode("utf-8"))

        except Exception as e:
            self._logger.error(f"Core error: {str(e)}")

    @abstractmethod
    def process(self, message):
        pass
