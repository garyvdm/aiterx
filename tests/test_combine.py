from asyncio import sleep

from asyncstdlib import list as list_a

import aiterx.combine as combine


async def test_combine_latest():
    async def source1():
        await sleep(0.1)
        yield "a"
        await sleep(0.2)
        yield "b"
        await sleep(0.1)
        yield "c"

    async def source2():
        yield "1"
        await sleep(0.2)
        yield "2"
        await sleep(0.3)
        yield "3"

    result = await list_a(combine.combine_latest(source1(), source2()))
    assert result == [
        ("a", "1"),
        ("a", "2"),
        ("b", "2"),
        ("c", "2"),
        ("c", "3"),
    ]
