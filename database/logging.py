from loguru import logger

logger.add("info.log", format="{time} | {level} | {message}", level="DEBUG", rotation="5 MB")
