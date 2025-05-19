# import asyncio  # noqa: I001
# import logging
# import signal

# from faststream import FastStream

# from server import broker

# # without handle upload import broker can't subscribe it
# from src.usecases.image_upload import subscriber  # noqa: F401

# async def shutdown(loop):
#     logging.info("Shutting down gracefully…")
#     await broker.stop()
#     tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
#     [task.cancel() for task in tasks]
#     await asyncio.gather(*tasks, return_exceptions=True)
#     loop.stop()

# async def main():

#     logging.info("Start server...")
#     loop = asyncio.get_event_loop()
#     for sig in (signal.SIGINT, signal.SIGTERM):
#         loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(loop)))
#     app = FastStream(broker)
#     await app.run()



# if __name__ == "__main__":
#     asyncio.run(main())




# titles = save_image_tiles(image_path=Path("0-250-ls-r1-1-23nv.png"), out_dir=Path("./out"))
# results = model("./out/images/0-250-ls-r1-1-23nv", save=True, project="./results")
# stitch_tiles_to_ribbon(Path("./results/predict"), Path("0-250-ls-r1-1-23nv_out.png"))
