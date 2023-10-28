import os
from dotenv import load_dotenv
import motor.motor_asyncio as motorio


class MongoDB:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDB._instance is None:
            MongoDB()
        return MongoDB._instance.get_database("chat_bot_test")

    def __init__(self):
        if MongoDB._instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            load_dotenv()
            MONGO_STRING = os.environ.get("MONGO_STRING")
            MongoDB._instance = motorio.AsyncIOMotorClient(MONGO_STRING)
