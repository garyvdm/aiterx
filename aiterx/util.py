from asyncio import CancelledError, Future, ensure_future
from contextlib import asynccontextmanager
from typing import Coroutine, Union


@asynccontextmanager
async def task_context(coro_or_future: Union[Coroutine, Future]):
    task = ensure_future(coro_or_future)
    try:
        yield task
    finally:
        if not task.done():
            task.cancel()
            try:
                await task
            except CancelledError:
                pass
