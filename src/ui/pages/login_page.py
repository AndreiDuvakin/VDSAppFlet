import flet as ft

from core.contexts import AuthContext


@ft.component
def login_page():
    auth = ft.use_context(AuthContext)
    token_ref = ft.use_ref(None)

    text_field = ft.TextField(label='Токен API', password=True, can_reveal_password=True, ref=token_ref),

    async def lets_auth():
        token_str = token_ref.current.value.strip()

        if not token_str.strip():
            return

        text_field.read_only = True
        auth.set_token()

        try:
            account = await auth.account_service.get_account()
            print(account)
        except Exception as e:
            pass

        finally:
            text_field.read_only = False

    return ft.Column(
        [
            ft.Text('VDSApp', size=25, weight=ft.FontWeight.BOLD),
            ft.Text('Вставьте токен API от вашего аккаунта VDS Selectel', text_align=ft.TextAlign.CENTER),
            text_field,
            ft.FilledButton('Войти', on_click=login_page),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
