import asyncpg
import asyncio

class Database:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
              host='ep-restless-thunder-068432.us-east-2.aws.neon.tech',
              port='5432',
              database='neondb',
              user='rimmyraa',
              password='uvQA3gf4rNDR'
            )
        )

    async def register_user(self, first_name, last_name, username, telegram_id):
        sql = f"""
        INSERT INTO telegram_users (first_name, last_name, username, telegram_id) 
        VALUES ('{first_name}', '{last_name}', '{username}', '{telegram_id}')
        """
        await self.pool.execute(sql)

    async def check_user(self, telegram_id):
        sql = f"""
        SELECT * FROM books WHERE telegram_id = '{telegram_id}'
        """
        result = await self.pool.fetchrow(sql)
        return result
    
    async def insert_search_query(self, telegram_id, search_query):
        sql = f"""
        UPDATE books
        SET search_query ='{search_query}' 
        WHERE telegram_id = '{telegram_id}'
        """
        await self.pool.execute(sql)
        
    async def get_uers(self):
        sql = f"""
        SELECT * 
        FROM books
        WHERE search_query is NOT NULL
        """
        
        result = await self.pool.fetch(sql)
        return result 
        