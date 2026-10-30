import csv
import json

from pathlib import Path


class DataLoader:

    def __init__(self, destination):

        self.destination = Path(
            destination
        )

        if (
            self.destination.suffix
            not in [".csv", ".json"]
        ):
            raise ValueError(
                "Only CSV and JSON outputs are supported."
            )

    def load(self, records):

        self.destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not records:
            return 0

        if (
            self.destination.suffix
            == ".csv"
        ):

            with open(
                self.destination,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=records[
                        0
                    ].keys()
                )

                writer.writeheader()
                writer.writerows(records)

        else:

            with open(
                self.destination,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    records,
                    file,
                    indent=4
                )

        return len(records)