import asyncio
from Database import DatabaseManager
from functools import partial


class EndPointBase(object):
    def __init__(self):
        self.db = DatabaseManager.DatabaseManager()

    @classmethod
    async def run_executor(cls, function_ptr, *args):
        return await asyncio.get_event_loop().run_in_executor(None, partial(function_ptr, *args))