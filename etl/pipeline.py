import time

from dataclasses import (
    dataclass,
    field,
)

from collections import Counter

from etl.errors import ExtractionError


@dataclass
class RunSummary:

    name: str
    extractor_name: str
    destination: str

    extracted: int = 0
    valid: int = 0
    rejected: int = 0
    loaded: int = 0

    duration: float = 0

    status: str = "SUCCESS"

    rejection_reasons: dict = field(
        default_factory=dict
    )

    errors: list[str] = field(
        default_factory=list
    )

    def report(self):

        lines = []

        lines.append(
            f"Pipeline: {self.name} "
            f"({self.extractor_name}"
            f" -> {self.destination})"
        )

        lines.append(
            f"  Extracted : {self.extracted}"
        )

        lines.append(
            f"  Valid     : {self.valid}"
        )

        lines.append(
            f"  Rejected  : {self.rejected}"
        )

        for (
            reason,
            count,
        ) in self.rejection_reasons.items():

            lines.append(
                f"    - {reason}: {count}"
            )

        lines.append(
            f"  Loaded    : {self.loaded}"
        )

        lines.append(
            f"  Duration  : "
            f"{self.duration:.2f}s"
        )

        lines.append(
            f"  Status    : {self.status}"
        )

        return "\n".join(lines)


class Pipeline:

    def __init__(
        self,
        name,
        extractor,
        transformer,
        loader,
    ):
        self.name = name
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):

        start = time.time()

        summary = RunSummary(
            name=self.name,
            extractor_name=
            self.extractor.__class__.__name__,
            destination=str(
                self.loader.destination
            ),
        )

        try:

            records = (
                self.extractor.extract()
            )

            summary.extracted = len(
                records
            )

            valid_records = (
                self.transformer.transform(
                    records
                )
            )

            summary.valid = len(
                valid_records
            )

            summary.rejected = len(
                self.transformer.rejected_records
            )

            summary.loaded = (
                self.loader.load(
                    valid_records
                )
            )

            summary.rejection_reasons = (
                dict(
                    self.transformer.rejection_reasons
                )
            )

            if summary.rejected > 0:
                summary.status = (
                    "PARTIAL"
                )

        except ExtractionError as e:

            summary.status = "FAILED"

            summary.errors.append(
                str(e)
            )

        summary.duration = (
            time.time() - start
        )

        return summary