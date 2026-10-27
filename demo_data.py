"""Deterministic, synthetic demo records shared by Flask and Tableau CSV export."""

from __future__ import annotations

import csv
from io import StringIO


FIELDS = (
    "demo_record_id", "age", "bmi", "systolic_bp", "cholesterol", "glucose",
    "smoker", "alcohol_use", "exercise_level", "fatigue", "chest_pain", "dizziness",
    "heart_disease", "diabetes", "stroke",
)


def generate_records(count: int = 320) -> list[dict[str, object]]:
    seed = 360

    def random() -> float:
        nonlocal seed
        seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
        return seed / 4294967296

    def js_round(value: float) -> int:
        return int(value + 0.5)

    records = []
    for index in range(count):
        age = 18 + int(random() * 72)
        bmi = float(f"{17 + random() * 24:.1f}")
        smoker = random() < 0.22
        alcohol = random() < 0.31
        inactive = random() < 0.36
        systolic = js_round(92 + random() * 78 + (8 if age > 55 else 0) + (6 if bmi > 30 else 0))
        cholesterol = js_round(135 + random() * 145 + (12 if age > 55 else 0))
        glucose = js_round(68 + random() * 96 + (12 if bmi > 30 else 0))
        age_risk = max(0, age - 35) / 55
        heart = random() < min(0.58, 0.035 + age_risk * 0.22 + (0.10 if bmi > 30 else 0) + (0.09 if smoker else 0) + (0.10 if systolic > 140 else 0))
        diabetes = random() < min(0.54, 0.025 + age_risk * 0.14 + (0.20 if bmi > 30 else 0) + (0.22 if glucose > 125 else 0) + (0.05 if inactive else 0))
        stroke = random() < min(0.34, 0.012 + age_risk * 0.105 + (0.10 if systolic > 140 else 0) + (0.035 if heart else 0))
        fatigue = random() < 0.23 + (0.08 if inactive else 0)
        chest_pain = random() < 0.08 + (0.30 if heart else 0)
        dizziness = random() < 0.10 + (0.10 if systolic > 150 else 0)
        records.append({
            "demo_record_id": f"H{index + 1:04d}", "age": age, "bmi": bmi,
            "systolic_bp": systolic, "cholesterol": cholesterol, "glucose": glucose,
            "smoker": smoker, "alcohol_use": alcohol,
            "exercise_level": "Low" if inactive else "Regular",
            "fatigue": fatigue, "chest_pain": chest_pain, "dizziness": dizziness,
            "heart_disease": heart, "diabetes": diabetes, "stroke": stroke,
        })
    return records


def csv_text() -> str:
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(generate_records())
    return output.getvalue()
