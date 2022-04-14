from asyncio import (
    FIRST_COMPLETED,
    CancelledError,
    Queue,
    Event,
    ensure_future,
    sleep,
    wait,
)
from typing import AsyncGenerator, AsyncIterable, Generic, List, TypeVar

T = TypeVar("T")


class Subject(Generic[T]):
    def __init__(self):
        self._observer_queues: List[Queue] = []
        self._complete = Event()

    async def consume(self, aiter: AsyncIterable[T]):
        await sleep(0)  # Yield to event loop so that observer tasks can start.
        try:
            async for item in aiter:
                await self.next(item)
        finally:
            self.completed()

    async def next(self, item: T):
        for queue in self._observer_queues:
            await queue.put(item)

    def completed(self):
        self._complete.set()

    async def observe(self, queue_maxsize: int = 0) -> AsyncGenerator[T, None]:
        queue: Queue[T] = Queue(queue_maxsize)
        self._observer_queues.append(queue)
        try:
            get_next = ensure_future(queue.get())
            complete = ensure_future(self._complete.wait())
            while True:
                await wait((get_next, complete), return_when=FIRST_COMPLETED)
                if get_next.done():
                    yield get_next.result()
                    get_next = ensure_future(queue.get())
                if complete.done():
                    get_next.cancel()
                    try:
                        # This will most likely fail due to the cancel,
                        # but incase it succeeds, yield the value.
                        yield await get_next
                    except CancelledError:
                        pass
                    break

            # Subject is complete, but there may still be items
            while not queue.empty():
                yield await queue.get()
        finally:
            self._observer_queues.remove(queue)
