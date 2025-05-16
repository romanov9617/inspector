import asyncio  # noqa: I001
import logging
import signal

from faststream import FastStream

from server import broker

# without handle upload import broker can't subscribe it

async def shutdown(loop):
    logging.info("Shutting down gracefully…")
    await broker.stop()
    tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():

    logging.info("Start server...")
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(loop)))
    app = FastStream(broker)
    await app.run()



if __name__ == "__main__":
    asyncio.run(main())
