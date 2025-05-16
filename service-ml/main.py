import asyncio
import logging
import signal

from faststream import FastStream

from server import broker

# without handle upload import broker can't subscribe it
from src.adapter.delivery.kafka.subscriber import handle_upload  # noqa: F401


async def shutdown(loop):
    logging.info("Shutting down gracefully…")
    await broker.stop()
    tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(loop)))
    await app.run()


app = FastStream(broker)

if __name__ == "__main__":
    asyncio.run(main())
