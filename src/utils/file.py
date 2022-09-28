import logging

logger = logging.getLogger(__name__)


def read_file(file_name: str) -> list[int]:
    try:
        with open(file_name, encoding="utf-8") as f:
            return [int(line) for line in f.readlines()]
    except Exception as e:
        logger.exception(e)
        raise


def save_channel_id(file_name: str, channel_id: int) -> None:
    try:
        with open(file_name, "a+t", encoding="utf-8") as f:
            f.write(str(channel_id) + "\n")
            logger.debug("Saved channel id %s to %s", channel_id, file_name)
    except Exception as e:
        logger.exception(e)
        raise
