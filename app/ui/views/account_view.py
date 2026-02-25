import flet as ft


@ft.component
def AccountView(state: dict, service: "AccountService", page: ft.Page) -> ft.Control:
    print(f"AccountView РЕНДЕР | loading={state['account']['loading']} | "
          f"info={bool(state['account']['info'])} | error={bool(state['account']['error'])}")

    acc = state["account"]

    def start_loading():          # ← обычная функция
        if acc["info"] is None and not acc["loading"]:
            print("use_effect: запускаем асинхронную загрузку")
            page.run_task(service.load_account)   # ← вот магия!

    ft.use_effect(start_loading, [])

    print(acc["loading"])
    print(acc["info"])

    if acc["loading"]:
        return ft.ProgressRing(width=50, height=50)

    if acc["error"]:
        return ft.Text(f"Ошибка: {acc['error']}", color="red")

    if not acc["info"]:
        return ft.Text("Аккаунт не загружен")

    info = acc["info"]
    return ft.Column(
        [
            ft.Text("✅ Аккаунт загружен", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Имя: {info.get('name')} {info.get('surname')}", size=18),
            ft.Text(f"Email: {info.get('email')}"),
            ft.Text(f"Статус: {'Активен' if info.get('state') == '1' else 'Неактивен'}"),
            ft.Text(f"Дата активации: {info.get('actdate')}"),
        ],
        spacing=15,
    )