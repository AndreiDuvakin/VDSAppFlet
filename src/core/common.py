import asyncio
from collections import defaultdict

from models.billing import BillingOperation


def group_operations_by_year_month_sync(
        billing_operations: list[BillingOperation],
) -> dict[int, dict[int, list[BillingOperation]]]:
    grouped: dict[
        int,
        dict[int, list[BillingOperation]],
    ] = defaultdict(lambda: defaultdict(list))

    for operation in billing_operations:
        grouped[
            operation.created.year
        ][
            operation.created.month
        ].append(operation)

    for months in grouped.values():
        for operations in months.values():
            operations.sort(
                key=lambda operation: operation.created,
                reverse=True,
            )

    return {
        year: {
            month: operations
            for month, operations in sorted(
                months.items(),
                reverse=True,
            )
        }
        for year, months in sorted(
            grouped.items(),
            reverse=True,
        )
    }


async def group_operations_by_year_month(
        billing_operations: list[BillingOperation],
) -> dict[int, dict[int, list[BillingOperation]]]:
    return await asyncio.to_thread(
        group_operations_by_year_month_sync,
        billing_operations,
    )


def format_operation_price(operation: BillingOperation) -> str:
    price = operation.price / 100

    if price <= 0:
        return f'-{price:,.2f} ₽'.replace(',', ' ')

    return f'+{abs(price):,.2f} ₽'.replace(',', ' ')


def get_operation_word(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        return 'операция'

    if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return 'операции'

    return 'операций'
