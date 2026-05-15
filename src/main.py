from dataclasses import replace

import flet as ft
from dotenv import load_dotenv

from src.core.screens import Screen
from src.state.app_state import AppState
from src.ui.app_layout import AppLayout
from src.ui.pages.login_page import LoginPage


async def main(page: ft.Page):
    load_dotenv()
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = AppState()

    async def set_token(new_token: str):
        new_state = replace(state, token=new_token)
        await set_state(new_state)

    async def set_state(new_state):
        nonlocal state
        state = new_state
        await render_page()

    async def render_page():
        page.clean()

        if state.token is not None:
            page.add(
                AppLayout(
                    state=state,
                    page=page,
                    set_state=set_state,
                )
            )

        else:
            page.add(
                await LoginPage(
                    page=page,
                    state=state,
                    set_state=set_state,
                    set_token=set_token,
                )
            )

    async def on_route_change(e: ft.RouteChangeEvent):
        await render_page()

    page.on_route_change = on_route_change
    if not page.route:
        page.go(f"/{Screen.ACCOUNT}")
    else:
        await render_page()


ft.run(main) #, view=ft.AppView.WEB_BROWSER, host='0.0.0.0')
