import flet as ft

from app.services.account_service import AccountService
from app.state.app_state import AppState


def AccountView(state: AppState, page: ft.Page, service: AccountService) -> ft.Control:
    page.title = 'Данные аккаунта'

    if state.account.info is None and not state.account.loading and not state.account.error:
        page.run_task(service.load_account, state)

    if state.account.loading:
        return ft.Column(
            [ft.ProgressRing()],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    if state.account.error:
        return ft.Text(f"Ошибка: {state.account.error}", color="red")
    if not state.account.info:
        return ft.Text("Аккаунт не загружен")

    info = state.account.info

    def get(key, default=''):
        return info.get(key, default)

    full_name = ' '.join(filter(None, [get('name'), get('middlename'), get('surname')]))
    if not full_name:
        full_name = 'Не указано'

    face_id = get('face_id')
    client_type = {
        '1': 'Физическое лицо (резидент)',
        '2': 'Юридическое лицо',
        '3': 'Физическое лицо (нерезидент)'
    }.get(face_id, 'Не указано') if face_id else 'Не указано'

    state_status = 'Активен' if get('state') == '1' else 'Неактивен'

    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.BLUE_400),
                ft.Column(
                    [
                        ft.Text(full_name, size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Статус: {state_status}", size=14,
                                color=ft.Colors.GREEN if state_status == 'Активен' else ft.Colors.RED),
                    ],
                    spacing=5,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=10,
        margin=ft.Margin.only(bottom=20),
        border_radius=10,
    )

    info_rows = [
        ft.ListTile(
            leading=ft.Icon(ft.Icons.EMAIL),
            title=ft.Text("Email"),
            subtitle=ft.Text(get('email', 'Не указан')),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.CALENDAR_MONTH),
            title=ft.Text("Дата активации"),
            subtitle=ft.Text(get('actdate', 'Не указана')),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.PHONE),
            title=ft.Text("Мобильный телефон"),
            subtitle=ft.Text(get('mobile', 'Не указан')),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.PUBLIC),
            title=ft.Text("Страна"),
            subtitle=ft.Text(get('country', 'Не указана')),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.BUSINESS),
            title=ft.Text("Тип клиента"),
            subtitle=ft.Text(client_type),
        ),
    ]

    content = ft.Column(
        [
            header,
            ft.Card(
                content=ft.Container(
                    content=ft.Column(info_rows, spacing=0),
                    padding=0,
                ),
                elevation=2,
                margin=ft.Margin.only(bottom=10),
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.Container(content=content, padding=20, expand=True)
