"""Describe the frozen corpus in read-only mode; does not select or exclude papers."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/corpus_clean_v1/corpus.parquet"
AUDIT = ROOT / "research/cleaning_2026-09-15"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(name, rows):
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(name):
    with (AUDIT / name).open() as handle:
        return list(csv.DictReader(handle))


def main():
    columns = ["field_id", "field_display_name", "period_start", "publication_year",
               "cohort", "language_ambiguous", "abstract_50_79"]
    rows = pq.read_table(SOURCE, columns=columns).to_pylist()
    cohorts, cells, annual = Counter(), Counter(), Counter()
    ambiguous, short, union = Counter(), Counter(), Counter()
    names = {}
    for row in rows:
        fid, period, cohort = row["field_id"], row["period_start"], row["cohort"]
        assert cohort in ("base", "extra")
        assert 2000 <= row["publication_year"] <= 2024
        assert period == 2000 + ((row["publication_year"] - 2000) // 5) * 5
        names[fid] = row["field_display_name"]
        cohorts[cohort] += 1
        cells[fid, period, cohort] += 1
        annual[fid, row["publication_year"]] += 1
        ambiguous[fid, period] += int(row["language_ambiguous"])
        short[fid, period] += int(row["abstract_50_79"])
        union[fid, period] += int(row["language_ambiguous"] or row["abstract_50_79"])
    assert len(rows) == 500_000 and cohorts == {"base": 400_000, "extra": 100_000}
    assert len(names) == 26 and len(annual) == 650
    fields, periods, cell_rows = [], [], []
    for fid in sorted(names):
        base = sum(cells[fid, p, "base"] for p in range(2000, 2025, 5))
        extra = sum(cells[fid, p, "extra"] for p in range(2000, 2025, 5))
        fields.append(dict(field_id=fid, field_name=names[fid], base=base, extra=extra,
                           total=base + extra, base_pct=base / 4000,
                           final_pct=(base + extra) / 5000))
        for period in range(2000, 2025, 5):
            b, e = cells[fid, period, "base"], cells[fid, period, "extra"]
            n = b + e
            assert n > 0
            cell_rows.append(dict(field_id=fid, field_name=names[fid], period_start=period,
                                  base=b, extra=e, total=n,
                                  language_ambiguous=ambiguous[fid, period],
                                  abstract_50_79=short[fid, period],
                                  union_flagged=union[fid, period],
                                  hypothetical_remaining=n - union[fid, period],
                                  ambiguous_pct=100 * ambiguous[fid, period] / n))
    for period in range(2000, 2025, 5):
        b = sum(cells[f, period, "base"] for f in names)
        e = sum(cells[f, period, "extra"] for f in names)
        periods.append(dict(period_start=period, period_end=period + 4, base=b, extra=e,
                            total=b + e, base_pct=b / 4000, final_pct=(b + e) / 5000))
    # Compare fresh Parquet counts with the prior cleaning audit, independently of its code.
    stored_fields = {int(r["field_id"]): r for r in read_csv("field_summary.csv")}
    stored_cells = {(int(r["field_id"]), int(r["period_start"])): r
                    for r in read_csv("field_period_counts.csv")}
    for row in fields:
        assert all(row[k] == int(stored_fields[row["field_id"]][k])
                   for k in ("base", "extra", "total"))
    for row in cell_rows:
        old = stored_cells[row["field_id"], row["period_start"]]
        assert all(row[k] == int(old[k]) for k in ("base", "extra", "total"))
    assert len(cell_rows) == 130
    assert sum(r["total"] for r in fields) == sum(r["total"] for r in periods) == 500_000
    assert abs(sum(r["base_pct"] for r in fields) - 100) < 1e-9
    assert abs(sum(r["final_pct"] for r in fields) - 100) < 1e-9
    minimum = min(r["total"] for r in cell_rows)
    weakest = [r for r in cell_rows if r["total"] == minimum]
    write_csv("field_proportions.csv", fields)
    write_csv("period_proportions.csv", periods)
    write_csv("field_period_diagnostics.csv", cell_rows)
    write_csv("smallest_cells.csv", weakest)
    summary = dict(
        checked_at=datetime.now(timezone.utc).isoformat(),
        source=str(SOURCE.relative_to(ROOT)), source_sha256=sha256(SOURCE),
        script_sha256=sha256(Path(__file__)),
        audit_counts_match=True, rows=len(rows), cohorts=dict(cohorts),
        fields=len(names), field_periods=len(cell_rows), field_years=len(annual),
        minimum_period_n=minimum, cells_at_minimum=len(weakest),
        cells_at_2165_or_2166=sum(r["total"] in (2165, 2166) for r in cell_rows),
        minimum_year_n=min(annual.values()),
        weakest_years=[dict(field_id=f, field_name=names[f], year=y, n=n)
                       for (f, y), n in annual.items() if n == min(annual.values())],
        language_ambiguous=sum(ambiguous.values()), short_abstracts=sum(short.values()),
        hypothetical_remaining=len(rows) - sum(union.values()),
        hypothetical_smallest=sorted(cell_rows, key=lambda r: r["hypothetical_remaining"])[:5],
        highest_ambiguous_rates=sorted(cell_rows, key=lambda r: r["ambiguous_pct"], reverse=True)[:5],
        limitations=["Descriptive counts, not precision or model stability estimates.",
                     "Hypothetical flag exclusion is a diagnostic, not a new cleaning rule.",
                     "Base percentages describe the cleaned random sample, not exact OpenAlex shares."])
    (OUT / "balance_verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("rows", "audit_counts_match", "minimum_period_n",
                                             "cells_at_minimum", "cells_at_2165_or_2166",
                                             "minimum_year_n", "hypothetical_remaining")}, indent=2))
    for r in fields:
        print(f'{r["field_name"]}|{r["total"]:,}|{r["base_pct"]:.2f}|{r["final_pct"]:.2f}')


if __name__ == "__main__":
    main()
