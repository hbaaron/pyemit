
# Usage

To use py-emit in a project

## step 1. Import pyemit
```python
from pyemit import emit
```
## step 2. Register events
pyemit provides both annotation based registering and direct registering. Annotation can be used if the handler is
 not a class method.

Be noticed that the handler MUST be a coroutine function.
```python
from pyemit import emit
@emit.on('event_name')
async def handler(msg):
    pass
```
or, if it's a class method, use `emit.register` instead:
```python
from pyemit import emit
class Foo:
    async def bar(self, msg):
        pass

foo = Foo()
emit.register('event_name', foo.bar)
```

To know what causes the difference, please refer to $todo

## step 3. Start the message pumping
you can start a local message pump by:
```python
from pyemit import emit
async def init():
    await emit.start()
```
Or, if you're prefer a remote message server, use this:
```python
from pyemit import emit
# aioredis is required. You can install it by running `pip install aioredis>=1.3.1
async def init(dsn):
    await emit.start(emit.Engine.REDIS, dsn=dsn)
```
## step 4. Fire and consume events
Now you can fire and consume events. To emit a message, running:
```python
from pyemit import emit
async def foo():
    # construct msg
    msg = {}
    await emit.emit('event_name', msg)
```
You can fire an event without providing any message. By doing so, be sure provide no parameter to the handler. The
 msg must be and dict and is json serializable.

# Troubeshooting
You can enable heartbeat when using REDIS engine:
```python
from pyemit import emit
async def init(dsn):
    await emit.start(emit.Engine.REDIS, dsn=dsn, heart_beat=1)
```
and set logging level to DEBUG, this should print a heart beat msg every 1 second. If not seen, then check your
 configurations and Redis setup.

# Advanced topic
## RPC call
```python
from pyemit import emit as e
from pyemit.remote import Remote

class Sum(Remote):
    def __init__(self, to_be_sum):
        super().__init__()
        self.to_be_sum = to_be_sum

    async def server_impl(self, *args, **kwargs):
        result = sum(self.to_be_sum)
        await super().respond(result)

async def test_rpc():
    await e.start(e.Engine.REDIS, dsn="redis://localhost")
    foo = Sum([0, 1, 2])
    response = await foo()
    assert response == 3
```

**step 1.** Subclass from `Remote`, and implement `Remote.server_impl` method. This one is supposed to be executed on
 the server side. When calculation is done, then call `super().respond()` to send the result back to client

 **step 2.** At client side, create instance of the subclass you defined (i.e., `foo` in the example), then by calling
  `await foo()` you will get what you want.

 ## stop the message pump
 call `emit.stop` to stop the whole machine. call `emit.unsubscribe` to remove a handler.
