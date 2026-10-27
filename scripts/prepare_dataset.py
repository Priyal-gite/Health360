"""Whitelist, normalize, and quality-check an approved CSV dataset."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path


FIELDS = (
    "age", "bmi", "systolic_bp", "cholesterol", "glucose", "smoker", "alcohol_use",
    "exercise_level", "fatigue", "chest_pain", "dizziness", "heart_disease", "diabetes",
    "stroke", "observation_date",
)
NUMERIC_FIELDS = {"age", "bmi", "systolic_bp", "cholesterol", "glucose"}
INTEGER_FIELDS = {"age", "systolic_bp", "cholesterol", "glucose"}
BOOLEAN_FIELDS = {"smoker", "alcohol_use", "fatigue", "chest_pain", "dizziness", "heart_disease", "diabetes", "stroke"}
TRUE_VALUES = {"1", "true", "t", "yes", "y"}
FALSE_VALUES = {"0", "false", "f", "no", "n"}
REQUIRED_OUTCOMES = {"heart_disease", "diabetes", "stroke"}


def normalize(field: str, value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if field in BOOLEAN_FIELDS:
        lowered = value.lower()
        if lowered in TRUE_VALUES:
            return "true"
        if lowered in FALSE_VALUES:
            return "false"
        raise ValueError(f"unrecognized boolean value for {field}")
    if field in NUMERIC_FIELDS:
        number = float(value)
        if not (number == number and abs(number) != float("inf")):
            raise ValueError(f"non-finite numeric value for {field}")
        if field in INTEGER_FIELDS:
            if not number.is_integer():
                raise ValueError(f"non-integer value for {field}")
            return str(int(number))
        return f"{number:g}"
    if field == "observation_date":
        try:
            return date.fromisoformat(value[:10]).isoformat()
        except ValueError as error:
            raise ValueError("date must begin with ISO format YYYY-MM-DD") from error
    return " ".join(value.split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Approved source CSV")
    parser.add_argument("--mapping", required=True, type=Path, help="JSON mapping from canonical field names to source headers")
    parser.add_argument("--output", required=True, type=Path, help="Restricted destination for prepared CSV")
    parser.add_argument("--report", type=Path, help="Quality report JSON (defaults to OUTPUT.quality.json)")
    args = parser.parse_args()

    with args.mapping.open(encoding="utf-8") as mapping_file:
        mapping_data = json.load(mapping_file)
    mapping = mapping_data.get("columns", {})
    unknown = set(mapping) - set(FIELDS)
    if unknown:
        parser.error(f"Mapping includes unsupported fields: {', '.join(sorted(unknown))}")
    if not REQUIRED_OUTCOMES.issubset(mapping):
        parser.error("Map heart_disease, diabetes, and stroke, or revise the analysis scope before preparation.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    report_path = args.report or args.output.with_suffix(args.output.suffix + ".quality.json")
    mapped_headers = list(mapping.values())
    if len(set(mapped_headers)) != len(mapped_headers):
        parser.error("Each canonical field must map to a distinct source column.")

    row_count = 0
    missing_counts = {field: 0 for field in FIELDS}
    invalid_counts = {field: 0 for field in FIELDS}
    duplicate_rows = 0
    seen_rows: set[tuple[str, ...]] = set()
    invalid_examples: list[dict[str, object]] = []
    temp_name: str | None = None
    try:
        with args.input.open(newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            headers = reader.fieldnames or []
            missing_headers = set(mapped_headers) - set(headers)
            if missing_headers:
                parser.error(f"Mapped source headers not found: {', '.join(sorted(missing_headers))}")
            if not mapped_headers:
                parser.error("The columns mapping is empty.")
            with tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8", dir=args.output.parent, delete=False) as prepared:
                temp_name = prepared.name
                writer = csv.DictWriter(prepared, fieldnames=FIELDS)
                writer.writeheader()
                for row_number, row in enumerate(reader, start=2):
                    row_count += 1
                    normalized: dict[str, str] = {}
                    for field in FIELDS:
                        source_header = mapping.get(field)
                        raw = row.get(source_header, "") if source_header else ""
                        raw = "" if raw is None else raw
                        if not raw.strip():
                            missing_counts[field] += 1
                            normalized[field] = ""
                            continue
                        try:
                            normalized[field] = normalize(field, raw)
                        except (ValueError, OverflowError):
                            invalid_counts[field] += 1
                            normalized[field] = ""
                            if len(invalid_examples) < 20:
                                invalid_examples.append({"row": row_number, "field": field})
                    signature = tuple(normalized[field] for field in FIELDS)
                    if signature in seen_rows:
                        duplicate_rows += 1
                    else:
                        seen_rows.add(signature)
                    writer.writerow(normalized)
        report = {
            "rows_read": row_count,
            "exact_duplicate_rows_after_field_mapping": duplicate_rows,
            "missing_values_by_field": missing_counts,
            "invalid_values_by_field": invalid_counts,
            "invalid_row_field_examples": invalid_examples,
            "mapped_fields": sorted(mapping),
            "excluded_source_field_count": len(set(headers) - set(mapped_headers)),
            "status": "ready for review" if not any(invalid_counts.values()) else "blocked: invalid values need mapping or source correction",
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        if any(invalid_counts.values()):
            print(f"Found invalid values. Review {report_path}; no prepared file was published.", file=sys.stderr)
            return 2
        if args.output.exists():
            print(f"Refusing to overwrite existing prepared dataset: {args.output}", file=sys.stderr)
            return 2
        os.replace(temp_name, args.output)
        temp_name = None
        print(f"Prepared {row_count:,} rows. Review the quality report at {report_path} before analysis.")
        return 0
    finally:
        if temp_name and Path(temp_name).exists():
            Path(temp_name).unlink()


if __name__ == "__main__":
    raise SystemExit(main())
