from dataclasses import replace

import flet as ft
from dotenv import load_dotenv

from src.services.app_services import AppServices
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
    services = None

    async def set_token(new_token: str):
        nonlocal services, state
        new_state = replace(state, token=new_token)
        state = new_state

        services = AppServices.create(new_token, set_state)

        await set_state(new_state)

    async def set_state(new_state):
        nonlocal state
        state = new_state
        await render_page()

    async def render_page():
        page.clean()

        if state.token is not None and services is not None:
            page.add(
                AppLayout(
                    state=state,
                    page=page,
                    services=services,
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
        page.go(f"/{Screen.SERVERS}")
    else:
        await render_page()


ft.run(main, view=ft.AppView.WEB_BROWSER, host='0.0.0.0', port=8080)
