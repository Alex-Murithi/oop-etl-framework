import csv

from abc import ABC, abstractmethod
from typing import Any

import requests

from etl.errors import ExtractionError


class DataExtractor(ABC):
    """
    Abstract base extractor.
    """

    def __init__(self, source: str, name: str | None = None):
        self.source = source
        self.name = name or self.__class__.__name__

    @abstractmethod
    def extract(self) -> list[dict[str, Any]]:
        pass

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(source='{self.source}')"
        )


class CSVExtractor(DataExtractor):
    """
    Extract records from CSV.
    """

    def extract(self) -> list[dict[str, Any]]:
        try:
            records = []

            with open(
                self.source,
                "r",
                encoding="utf-8"
            ) as file:
                reader = csv.DictReader(file)

                for row in reader:
                    records.append(dict(row))

            return records

        except Exception as e:
            raise ExtractionError(
                f"CSV extraction failed: {e}"
            )


class APIExtractor(DataExtractor):
    """
    Extract records from API.
    """

    def __init__(
        self,
        source: str,
        name: str | None = None,
        timeout: float = 10.0
    ):
        super().__init__(source, name)
        self.timeout = timeout

    def extract(self) -> list[dict[str, Any]]:
        try:

            response = requests.get(
                self.source,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                raise ExtractionError(
                    "API response is not a list."
                )

            return data

        except requests.RequestException as e:
            raise ExtractionError(
                f"API extraction failed: {e}"
            )

    def __repr__(self):

        return (
            f"APIExtractor("
            f"source='{self.source}', "
            f"timeout={self.timeout})"
        )