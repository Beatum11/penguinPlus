from Data.db import MongoDB
import asyncio


class UsersService:

    def __init__(self):
        db = MongoDB.get_instance()
        self.users = db['users']

    # GET
    async def get_user(self, chat_id):
        return await self.users.find_one({"chat_id": chat_id})

    # POST
    async def post_user(self, chat_id, username):
        user_to_post = {
            "chat_id": chat_id,
            "username": username,
            "credits": 1000
        }

        res = await self.users.insert_one(user_to_post)

        if res.acknowledged:
            inserted_user = await self.users.find_one({"_id": res.inserted_id})
            return inserted_user
        return None

        # UPDATE
    async def update_credits(self, chat_id, credits_amount):
        res = await self.users.update_one({"chat_id": chat_id},
                                          {
                                              "$set": {
                                                  "credits": credits_amount
                                              }
                                          })
        return res.acknowledged
