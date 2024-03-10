from Data.db import MongoDB
import asyncio


# This class is for CRU operations with MongoDB
class UsersService:

    def __init__(self):
        db = MongoDB.get_instance()
        self.users = db['users']

    async def get_user(self, chat_id):
        return await self.users.find_one({"chat_id": chat_id})

    async def post_user(self, chat_id, username):
        user_to_post = {
            "chat_id": chat_id,
            "username": username,
            "credits": 15,
            "state": "",
            "chat_history": [],
        }

        print(user_to_post)
        res = await self.users.insert_one(user_to_post)
        print(res)

        if res.acknowledged:
            inserted_user = await self.users.find_one({"_id": res.inserted_id})
            return inserted_user
        return None

    async def create_chat_history(self, chat_id, role, message):
        res = await self.users.update_one({"chat_id": chat_id},
                                          {
                                              "$push": {
                                                  "chat_history": {
                                                      "$each": [{"role": role, "content": message}],
                                                      "$slice": -5
                                                      # Ограничиваем размер массива до последних 5 элементов
                                                  }
                                              }
                                          })
        return res.acknowledged

    async def get_chat_history(self, chat_id):
        user = await self.get_user(chat_id)
        return user['chat_history']

    async def update_credits(self, chat_id, credits_amount):
        res = await self.users.update_one({"chat_id": chat_id},
                                          {
                                              "$set": {
                                                  "credits": credits_amount
                                              }
                                          })
        return res.acknowledged

    async def update_state(self, chat_id, state: str):
        res = await self.users.update_one({'chat_id': chat_id},
                                          {
                                              "$set": {
                                                  "state": state
                                              }
                                          })
        if res.acknowledged:
            updated_user = await self.get_user(chat_id)
            return updated_user['state']

    async def remove_state(self, chat_id):
        res = await self.users.update_one({'chat_id': chat_id},
                                          {
                                              "$unset": {
                                                  "state": ""
                                              }
                                          })
        return res.acknowledged

    async def get_current_state(self, chat_id):
        user = await self.get_user(chat_id)
        return user['state']
