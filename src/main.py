import logging

import flet as ft

from app import app
from core.logging_config import setup_logging

setup_logging(log_level="INFO", log_file=None)

logger = logging.getLogger(__name__)


def main(page: ft.Page):
    logger.info("Settings page properties")

    page.title = 'VDSApp'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    logger.info("Render main app component")

    page.render(app)


if __name__ == "__main__":
    logger.info("Starting app")
    ft.run(main)
