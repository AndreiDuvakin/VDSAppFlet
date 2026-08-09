import logging
import logging.handlers
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str | None = "app.log"):
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            Path(log_file),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
