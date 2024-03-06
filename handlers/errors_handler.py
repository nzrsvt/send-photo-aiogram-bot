from loguru import logger

async def errors_handler(update, exception):
    logger.error(f"Caught an exception in update {update}:\n{exception}")