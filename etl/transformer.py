import re

from datetime import datetime
from collections import Counter


class DataTransformer:

    def __init__(self, required_fields: list[str]):
        self.required_fields = required_fields
        self.rejected_records = []
        self.rejection_reasons = Counter()

    def validate(self, record):
        reasons = []

        for field in self.required_fields:

            value = str(
                record.get(field, "")
            ).strip()

            if not value:
                reasons.append(
                    f"Missing {field}"
                )

        email = record.get(
            "customer_email"
        )

        if email:

            pattern = (
                r"^[A-Za-z0-9._%+-]+"
                r"@[A-Za-z0-9.-]+"
                r"\.[A-Za-z]{2,}$"
            )

            if not re.match(pattern, email):
                reasons.append(
                    "Invalid email"
                )

        quantity = record.get(
            "quantity"
        )

        if quantity:

            try:
                quantity = int(quantity)

                if quantity <= 0:
                    reasons.append(
                        "Non-positive quantity"
                    )

            except ValueError:
                reasons.append(
                    "Invalid quantity"
                )

        price = record.get(
            "unit_price_kes"
        )

        if price:

            try:
                price = float(
                    str(price).replace(
                        ",",
                        ""
                    )
                )

                if price <= 0:
                    reasons.append(
                        "Non-positive price"
                    )

            except ValueError:
                reasons.append(
                    "Invalid price"
                )

        return reasons

    def clean(self, record):

        cleaned = record.copy()

        city = cleaned.get("city")

        if city:
            cleaned["city"] = (
                city.strip().title()
            )

        status = cleaned.get(
            "status"
        )

        if status:
            cleaned["status"] = (
                status.strip().upper()
            )

        order_date = cleaned.get(
            "order_date"
        )

        if order_date:
            try:

                cleaned["order_date"] = (
                    datetime.strptime(
                        order_date,
                        "%m/%d/%Y"
                    ).strftime(
                        "%Y-%m-%d"
                    )
                )

            except ValueError:
                pass

        if "quantity" in cleaned:
            cleaned["quantity"] = int(
                cleaned["quantity"]
            )

        if "unit_price_kes" in cleaned:
            cleaned["unit_price_kes"] = int(
                float(
                    str(
                        cleaned[
                            "unit_price_kes"
                        ]
                    ).replace(
                        ",",
                        ""
                    )
                )
            )

        if (
            "quantity" in cleaned
            and "unit_price_kes"
            in cleaned
        ):
            cleaned[
                "line_total_kes"
            ] = (
                cleaned["quantity"]
                * cleaned["unit_price_kes"]
            )

        return cleaned

    def transform(self, records):

        valid_records = []

        seen_orders = set()

        for record in records:

            reasons = self.validate(
                record
            )

            order_id = record.get(
                "order_id"
            )

            if order_id:

                if order_id in seen_orders:
                    reasons.append(
                        "Duplicate order_id"
                    )
                else:
                    seen_orders.add(
                        order_id
                    )

            if reasons:

                for reason in reasons:
                    self.rejection_reasons[
                        reason
                    ] += 1

                self.rejected_records.append(
                    {
                        "order_id": record.get(
                            "order_id",
                            ""
                        ),
                        "reasons": "; ".join(
                            reasons
                        ),
                        **record
                    }
                )

            else:

                valid_records.append(
                    self.clean(record)
                )

        return valid_records