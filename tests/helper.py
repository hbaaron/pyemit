import asyncio
import functools


def async_test(func):
    async def run_with_setup_teardown(self, *args, **kwargs):
        await self.asyncSetUp()
        await func(self, *args, **kwargs)
        await self.asyncTearDown()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(run_with_setup_teardown(*args, **kwargs))

    return wrapper
