import logging
import os


if len(logging.getLogger().handlers) > 0:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO if os.getenv("LOG_LEVEL", None) is None else logging.DEBUG,
                        format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        )
LOGGER = logging.getLogger(__name__)