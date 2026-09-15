from collections import defaultdict
import datetime
from typing import List, Mapping

from src.models.billing import BillingOperation, BillingUsage


def group_operations_by_year_month_sync(
    billing_operations: list[BillingOperation],
) -> dict[int, dict[int, list[BillingOperation]]]:
    grouped: dict[
        int,
        dict[int, list[BillingOperation]],
    ] = defaultdict(lambda: defaultdict(list))

    for operation in billing_operations:
        grouped[operation.created.year][operation.created.month].append(operation)

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


def format_operation_price(operation: BillingOperation, sign="+") -> str:
    price = int(operation.price)

    return sign + format_money(price)


def format_money(value: int) -> str:
    rubles = value / 100

    return f"{rubles:,.2f}".replace(",", " ").replace(".", ",") + " ₽"


def get_resource_word(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        return "ресурс"

    if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return "ресурса"

    return "ресурсов"


def get_operation_word(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        return "операция"

    if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return "операции"

    return "операций"


def get_years_list_for_consumption_period(
    start_date: datetime.date,
) -> List[int]:
    current_date = datetime.date.today()

    years_list_for_payments_period = []

    start_year = start_date.year
    end_year = current_date.year

    for year in range(end_year, start_year - 1, -1):
        years_list_for_payments_period.append(year)

    return years_list_for_payments_period


def parse_billing_usage(
    response: Mapping[str, dict],
) -> List[BillingUsage]:
    result: List[BillingUsage] = []

    for timestamp, resources in response.items():
        period = datetime.datetime.fromtimestamp(int(timestamp))

        for resource_id, resource_data in resources.items():
            for plan, usage in resource_data.items():
                if plan == "summ":
                    continue

                result.append(
                    BillingUsage(
                        period=period,
                        resource_id=str(resource_id),
                        plan=plan,
                        count=int(usage["count"]),
                        summ=int(usage["summ"]),
                    )
                )

    return sorted(
        result,
        key=lambda item: (
            item.period,
            item.resource_id,
        ),
        reverse=True,
    )


def group_usage_by_period(
    operations: list[BillingUsage],
) -> dict[int, dict[int, list[BillingUsage]]]:
    grouped = defaultdict(lambda: defaultdict(list))

    for operation in operations:
        grouped[operation.period.year][operation.period.month].append(operation)

    return {
        year: {
            month: sorted(
                items,
                key=lambda item: (
                    item.resource_id,
                    item.plan,
                ),
            )
            for month, items in sorted(
                months.items(),
                reverse=True,
            )
        }
        for year, months in sorted(
            grouped.items(),
            reverse=True,
        )
    }


def get_resource_name(usage: BillingUsage) -> str:
    return f"Ресурс {usage.resource_id} · " f"{usage.plan}"
