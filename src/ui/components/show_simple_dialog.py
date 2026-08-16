import flet as ft


def show_simple_dialog(
    title: str,
    content: ft.Control,
    page: ft.Page,
) -> None:
    def handle_action_click(e):
        page.pop_dialog()

    actions = [ft.TextButton("Закрыть", on_click=handle_action_click)]
    dialog = ft.AlertDialog(
        title=title,
        content=content,
        actions=actions,
    )
    page.show_dialog(dialog)
