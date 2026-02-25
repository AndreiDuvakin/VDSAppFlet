import flet as ft

from app.api.account_client import AccountClient


class AccountService:
    def __init__(self, client: AccountClient, state: dict, set_state, page: ft.Page):
        self.client = client
        self.state = state
        self.set_state = set_state
        self.page = page

    async def load_account(self) -> None:
        print("=== ЗАПУСК АСИНХРОННОЙ ЗАГРУЗКИ ===")

        # Показываем ProgressRing сразу
        new_state = {"account": {"info": None, "loading": True, "error": None}}
        self.set_state(new_state)
        self.page.update()

        try:
            print("Запрос к API...")
            raw = await self.client.get()
            print("Данные получены:", raw)

            new_state = {"account": {"info": raw, "loading": False, "error": None}}
        except Exception as e:
            print("Ошибка:", e)
            new_state = {"account": {"info": None, "loading": False, "error": str(e)}}

        # Показываем результат
        self.set_state(new_state)
        self.page.update()
        print("=== ЗАГРУЗКА ЗАВЕРШЕНА ===")