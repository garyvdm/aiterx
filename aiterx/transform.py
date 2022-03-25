from asyncio import sleep
from typing import AsyncGenerator, AsyncIterable, List, TypeVar

from aiterx.util import task_context


__all__ = [
    "buffer",
    "buffer_with_count",
    "buffer_with_time",
]

T = TypeVar("T")


async def buffer(
    iterable: AsyncIterable[T], boundaries: AsyncIterable
) -> AsyncGenerator[List[T], None]:
    buffer = []

    async def add_to_buffer():
        nonlocal buffer, iterable
        async for item in iterable:
            buffer.append(item)

    async with task_context(add_to_buffer()) as buffer_task:
        async for _ in boundaries:
            yield buffer
            buffer = []

        await buffer_task


async def buffer_with_count(
    iterable: AsyncIterable[T], count: int
) -> AsyncGenerator[List[T], None]:
    buffer = []
    buf_len = 0
    async for item in iterable:
        buffer.append(item)
        buf_len += 1
        if buf_len >= count:
            yield buffer
            buffer = []
            buf_len = 0
    if buffer:
        yield buffer


async def buffer_with_time(
    iterable: AsyncIterable[T], timespan: float
) -> AsyncGenerator[List[T], None]:
    buffer = []
    done = False

    async def add_to_buffer():
        nonlocal buffer, iterable, done
        try:
            async for item in iterable:
                buffer.append(item)
        finally:
            done = True

    async with task_context(add_to_buffer()) as buffer_task:
        while not done:
            await sleep(timespan)
            yield buffer
            buffer = []

        await buffer_task
