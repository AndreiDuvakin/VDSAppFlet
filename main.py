import logging

import flet as ft

from src.run_app import main

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting app")
    ft.run(main)
