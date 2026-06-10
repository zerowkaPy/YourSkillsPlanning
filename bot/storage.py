from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.base import StorageKey, StateType

from asyncpg import Record, create_pool

import json
from typing import Mapping, Any


class PostgreStorage(BaseStorage):

    @classmethod
    async def set_pool(cls, db_url):
        cls.pool = await create_pool(db_url)
        
    @classmethod
    async def close_pool(cls):
        await cls.pool.close()

    async def execute(self, query:str, *args):
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def query(self, query:str, *args) -> tuple[dict[str,Any], ...]:
        async with self.pool.acquire() as conn:
            records:list[Record] = await conn.fetch(query, *args)
            if not records:
                    return ()
            return tuple(dict(r) for r in records)
        
    async def insert_user_id(self, user_id):
        await self.execute("INSERT INTO states (user_id) VALUES($1) ON CONFLICT (user_id) DO NOTHING", user_id)
    


#####################################################################################

    async def set_state(self, key:StorageKey, state:StateType = None):
        user_id = key.user_id
        key = str(key) 
        state = str(state)
        await self.insert_user_id(user_id)
        await self.execute("UPDATE states SET state = $1, key = $2 WHERE user_id = $3", state, key, user_id)  

    async def get_state(self, key:StorageKey) -> str|None: 
        data = await self.query("SELECT state FROM states WHERE user_id = $1", key.user_id)
        if not data:
             return None
        return data[0]["state"]

    async def set_data(self, key: StorageKey, data: Mapping[str, Any]):
            userdata = json.dumps(data)
            await self.execute("UPDATE states SET userdata = $1 WHERE user_id = $2", userdata, key.user_id)

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
            data = await self.query("SELECT userdata FROM states WHERE user_id = $1", key.user_id)
            if not data:
                return {}
            return json.loads(data[0]["userdata"])
    
    async def close(self):
         pass