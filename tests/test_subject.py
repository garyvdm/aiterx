from asyncio import ensure_future, wait
from aiterx import Subject

from asyncstdlib import list as alist
from asyncstdlib import iter as aiter


async def test_subject_consume():
    subject: Subject[int] = Subject()

    observe_task1 = ensure_future(alist(subject.observe()))
    observe_task2 = ensure_future(alist(subject.observe()))

    source = [0, 1, 2]
    await subject.consume(aiter(source))
    await wait((observe_task1, observe_task2))

    assert observe_task1.result() == source
    assert observe_task2.result() == source
