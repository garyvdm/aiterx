from asyncio import ensure_future, shield, wait_for, TimeoutError
from typing import AsyncGenerator, AsyncIterable, TypeVar

__all__ = [
    "debounce",
]


T = TypeVar("T")


async def debounce(iterable: AsyncIterable[T], duetime: float) -> AsyncGenerator[T, None]:
    iterator = aiter(iterable)
    next_item = None
    try:
        item = await anext(iterator)
    except StopAsyncIteration:
        return
    get_next = ensure_future(anext(iterator))

    while True:
        try:
            next_item = await wait_for(shield(get_next), timeout=duetime)
        except TimeoutError:
            yield item
        except StopAsyncIteration:
            # This might be early, but that's ok, cause we know there is nothing more comming.
            yield item
            return
        else:
            item = next_item
            get_next = ensure_future(anext(iterator))
