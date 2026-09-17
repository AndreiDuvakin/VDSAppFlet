import flet as ft

from src.core.contexts import AppContext
from src.state.load_state import LoadState


@ft.component
def price_widget(
        plan: str,
) -> ft.Control:
    app_state = ft.use_context(AppContext)

    if app_state.price_loading_status.value == LoadState.LOADING.value:
        return ft.ProgressRing()

    if app_state.price_loading_status.value == LoadState.IDLE.value:
        return ft.Text('Цена не загружена')

    price = app_state.price.get_month_price_beautiful(plan)

    if price is None:
        return ft.Icon(ft.Icons.MONEY_OFF)

    return ft.Text(price, size=15)
