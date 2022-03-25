from asyncio import sleep

from asyncstdlib.builtins import list as alist
from asyncstdlib.builtins import iter as aiter

import aiterx.transform as transform


async def test_bufer():
    async def source():
        yield 1
        await sleep(0.2)
        yield 2
        yield 3
        await sleep(0.2)
        yield 4
        yield 5
        await sleep(0.2)
        yield 6
        yield 7

    async def boundaries():
        await sleep(0.1)
        yield
        await sleep(0.2)
        yield
        await sleep(0.2)
        yield

    result = await alist(transform.buffer(source(), boundaries()))
    assert result == [
        [1],
        [2, 3],
        [4, 5],
    ]


async def test_bufer_with_count():
    source = aiter(range(7))
    result = await alist(transform.buffer_with_count(source, 3))
    assert result == [[0, 1, 2], [3, 4, 5], [6]]


async def test_buffer_with_time():
    async def source():
        for i in range(5):
            yield i
            await sleep(0.1)

    result = await alist(transform.buffer_with_time(source(), 0.3))
    assert result == [
        [0, 1, 2],
        [3, 4],
    ]
