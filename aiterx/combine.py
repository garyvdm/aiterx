from asyncio import FIRST_COMPLETED, Future, ensure_future, wait
from typing import AsyncGenerator, Sequence


__all__ = [
    "combine_latest",
]


async def combine_latest(*iterables) -> AsyncGenerator[Sequence, None]:
    current_values = [None] * len(iterables)
    iterators = tuple(aiter(iterable) for iterable in iterables)
    next_tasks = set(ensure_future(anext(iterator)) for iterator in iterators)
    for i, next_task in enumerate(next_tasks):
        next_task.i = i  # type: ignore
    still_running = len(iterables)
    still_waiting_from = set(range(len(iterables)))

    while still_running > 0:
        done_tasks, next_tasks = await wait(next_tasks, return_when=FIRST_COMPLETED)
        for done_task in done_tasks:
            i = done_task.i  # type: ignore
            try:
                current_values[i] = done_task.result()
            except StopAsyncIteration:
                still_running -= 1
            else:
                still_waiting_from.discard(i)
                if not still_waiting_from:
                    yield tuple(current_values)
                next_task = ensure_future(anext(iterators[i]))
                next_task.i = i  # type: ignore
                next_tasks.add(next_task)
