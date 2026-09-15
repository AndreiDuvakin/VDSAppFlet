import flet as ft

from src.core.constants import MARKDOWN_README


@ft.component
def info_page():
    page = ft.context.page

    async def open_url(e):
        await page.launch_url(e.data)

    return ft.Column(
        [
            ft.Container(
                margin=10,
                padding=10,
                content=ft.Markdown(
                    MARKDOWN_README,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=open_url,
                    expand=True,
                ),
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
