from asyncio import sleep

from asyncstdlib import list as list_a
from asyncstdlib import iter as a_iter

import aiterx.filter as filter


async def test_debounce():
    async def source():
        yield 1
        await sleep(0.2)
        yield 2
        await sleep(0.1)
        yield 3
        await sleep(0.1)
        yield 4
        await sleep(0.2)
        yield 5

    # Do we need an assert on the timeing of the output? I don't think so.
    assert await list_a(filter.debounce(source(), 0.15)) == [1, 4, 5]


async def test_debounce_empty():
    assert await list_a(filter.debounce(a_iter([]), 0.15)) == []
