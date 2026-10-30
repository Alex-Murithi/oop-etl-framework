from etl.extractors import (
    CSVExtractor,
    APIExtractor,
)
from etl.transformer import DataTransformer
from etl.loader import DataLoader
from etl.pipeline import Pipeline


CONFIG = [
    {
        "name": "Orders CSV",
        "extractor": CSVExtractor(
            "data/orders.csv"
        ),
        "required_fields": [
            "order_id",
            "customer_email",
            "product_sku",
            "quantity",
            "unit_price_kes",
        ],
        "destination": "output/orders_clean.csv",
    },
    {
        "name": "Users API",
        "extractor": APIExtractor(
            "https://jsonplaceholder.typicode.com/users"
        ),
        "required_fields": [
            "id",
            "name",
            "email",
        ],
        "destination": "output/users.json",
    },
]


def print_summary(results):

    print("\n=== ETL Execution Summary ===\n")

    successes = 0
    failures = 0

    for result in results:

        print(result.report())
        print()

        if result.status == "FAILED":
            failures += 1
        else:
            successes += 1

    print(
        f"Total pipelines: {len(results)} | "
        f"Succeeded: {successes} | "
        f"Failed: {failures}"
    )


def main():

    results = []

    for cfg in CONFIG:

        transformer = DataTransformer(
            cfg["required_fields"]
        )

        loader = DataLoader(
            cfg["destination"]
        )

        pipeline = Pipeline(
            name=cfg["name"],
            extractor=cfg["extractor"],
            transformer=transformer,
            loader=loader,
        )

        results.append(
            pipeline.run()
        )

    print_summary(results)


if __name__ == "__main__":
    main()