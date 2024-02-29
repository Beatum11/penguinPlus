import os
from dotenv import load_dotenv
import motor.motor_asyncio as motorio
from loguru import logger


class MongoDB:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDB._instance is None:
            MongoDB()
        return MongoDB._instance.get_database("gpt_4_bot")

    def __init__(self):
        if MongoDB._instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            try:
                load_dotenv()
                MONGO_STRING: str = os.environ.get("MONGO_STRING")
                MongoDB._instance = motorio.AsyncIOMotorClient(MONGO_STRING)
            except Exception as e:
                logger.error(f'Some error with the database: {e}')
