import flet as ft

from app import app


def main(page: ft.Page):
    page.title = 'VDSApp'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.render(app)


if __name__ == "__main__":
    ft.run(main)
