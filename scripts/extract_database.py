"""Export an explicitly approved, read-only SQL query to CSV."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import tempfile
from pathlib import Path

from sqlalchemy import create_engine, text


def validate_select(query: str) -> str:
    query = query.strip()
    if not query:
        raise ValueError("SOURCE_QUERY is empty.")
    # Allow one terminal semicolon, but never accept a second statement.
    query = query[:-1].rstrip() if query.endswith(";") else query
    if ";" in query:
        raise ValueError("SOURCE_QUERY must contain exactly one SQL statement.")
    if not re.match(r"^(select|with)\b", query, flags=re.IGNORECASE):
        raise ValueError("Only SELECT or read-only CTE queries are allowed.")
    if re.search(r"\b(insert|update|delete|merge|drop|alter|create|truncate|grant|revoke|execute|call)\b", query, flags=re.IGNORECASE):
        raise ValueError("SOURCE_QUERY contains a write or execution keyword.")
    return query


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Restricted destination for the approved extract CSV")
    args = parser.parse_args()

    if os.environ.get("EXTRACTION_APPROVED", "false").lower() != "true":
        parser.error("Set EXTRACTION_APPROVED=true only after source-owner and privacy approval.")
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if not database_url:
        parser.error("DATABASE_URL is not set.")
    try:
        query = validate_select(os.environ.get("SOURCE_QUERY", ""))
    except ValueError as error:
        parser.error(str(error))

    # Use a database account that is read-only and approved for this dataset.
    # A query prefix check is not a substitute for server-side permissions.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        print(f"Refusing to overwrite existing extract: {args.output}", file=sys.stderr)
        return 2
    engine = create_engine(database_url, pool_pre_ping=True)
    row_count = 0
    temp_name: str | None = None
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            with tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8-sig", dir=args.output.parent, delete=False) as output:
                temp_name = output.name
                writer = csv.writer(output)
                writer.writerow(result.keys())
                while batch := result.fetchmany(1000):
                    writer.writerows(batch)
                    row_count += len(batch)
        os.replace(temp_name, args.output)
        temp_name = None
    finally:
        engine.dispose()
        if temp_name and Path(temp_name).exists():
            Path(temp_name).unlink()

    print(f"Extract completed: {row_count:,} rows written to {args.output}")
    print("Keep the extract in restricted storage; review its columns and privacy classification before use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
