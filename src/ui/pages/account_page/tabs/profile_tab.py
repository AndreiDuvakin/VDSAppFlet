import flet as ft

from core.contexts import AppContext


@ft.component
def profile_tab():
    app_state = ft.use_context(AppContext)

    account = app_state.account.info

    full_name = account.full_name
    state_status = "Активен" if account.is_active else "Неактивен"
    status_color = ft.Colors.GREEN if account.is_active else ft.Colors.RED
    client_type = account.client_type

    header = ft.Container(
        content=ft.Row(
            [
                ft.CircleAvatar(
                    content=ft.Text(full_name[0].upper() if full_name != "Не указано" else "?"),
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_400,
                    radius=35,
                ),
                ft.Column(
                    [
                        ft.Text(full_name, size=24, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.CIRCLE,
                                    size=12,
                                    color=status_color,
                                ),
                                ft.Text(state_status, size=14, color=status_color),
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=5,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        border_radius=ft.BorderRadius.all(12),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_400),
        expand=True,
    )

    info_rows = ft.Column(
        [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Основная информация", size=18, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.EMAIL, color=ft.Colors.BLUE_400),
                                title=ft.Text("Email", weight=ft.FontWeight.W_500),
                                subtitle=ft.Text(account.email or "Не указан"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.PHONE, color=ft.Colors.BLUE_400),
                                title=ft.Text("Телефон", weight=ft.FontWeight.W_500),
                                subtitle=ft.Text(account.mobile or "Не указан"),
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.Padding.all(15),
                ),
                elevation=2,
            ),

            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Информация об аккаунте", size=18, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_400),
                                title=ft.Text("Дата активации", weight=ft.FontWeight.W_500),
                                subtitle=ft.Text(account.str_actdate or "Не указана"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.BLUE_400),
                                title=ft.Text("Тип клиента", weight=ft.FontWeight.W_500),
                                subtitle=ft.Text(client_type),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.BLUE_400),
                                title=ft.Text("Страна", weight=ft.FontWeight.W_500),
                                subtitle=ft.Text(account.country or "Не указана"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.LANGUAGE, color=ft.Colors.BLUE_400),
                                title=ft.Text("Локаль", weight=ft.FontWeight.W_500),
                                subtitle=ft.Text(account.locale or "Не указана"),
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.Padding.all(15),
                ),
                elevation=2,
            ),
        ],
        spacing=15,
    )

    content = ft.Column(
        [
            header,
            info_rows
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return content
