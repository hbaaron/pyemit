
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
## kind-of RPC call
```python
from pyemit import emit as e

async def rpc_handler(msg):
    if msg['command'] == 'add':
        msg["result"] = msg["count"] + 1
        msg.pop('count')

        await e.rpc_respond(msg)

async def test_redis_rpc_call():
    e.rpc_register_handler(rpc_handler)
    await e.start(e.Engine.REDIS, dsn="redis://localhost")
    response = await e.rpc_send({"command": "add", "count": 0})
    assert response['result'] == 1
```

At first you provide a server rpc call handler, and register it with `emit.rpc_register_handler`. Then you send your
 call to the server with `emit.rpc_send`. At server side, in your rpc call handler function, got client's message, do
  the calculation, and finally respond to the client with `emit.rpc_respond`

You can also implement your own server message handling mech, especially if your choose languange other than python
. In such case, you should listen to channel '__emit_rpc_server_channel__' and respond with
 '__emit_rpc_client_channel__'.

 ## stop the message pump
 call `emit.stop` to stop the whole machine. call `emit.unsubscribe` to remove a handler.
