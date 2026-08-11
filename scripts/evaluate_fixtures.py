"""Deterministic fixture evaluator for the Skill validation layer."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

CLASSES = {"PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "FALSE_POSITIVE"}


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def evaluate_fixture(case):
    expected = case.get("expected", {})
    if case.get("class") not in CLASSES:
        return False, "invalid class"
    expected_status = expected.get("status")
    if expected_status is None:
        expected_status = {
            "PASS": "pass",
            "FAIL": "fail",
            "INSUFFICIENT_EVIDENCE": "insufficient_evidence",
            "FALSE_POSITIVE": "no_finding",
        }[case["class"]]
    # Fixture contract validation is deterministic. Runtime execution is a separate adapter.
    if case["class"] == "INSUFFICIENT_EVIDENCE" and expected_status != "insufficient_evidence":
        return False, "evidence-gating contract mismatch"
    if case["class"] == "FALSE_POSITIVE" and expected_status != "no_finding":
        return False, "false-positive contract mismatch"
    return True, expected_status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", default="evals/fixtures")
    args = parser.parse_args()
    root = Path(args.fixtures)
    files = sorted(root.glob("*.yaml"))
    total = passed = 0
    for path in files:
        data = load(path)
        if path.name == "core-skills.yaml":
            for skill, cases in data.get("skills", {}).items():
                for klass, case in cases.items():
                    total += 1
                    ok, detail = evaluate_fixture({"class": klass, **case})
                    passed += ok
                    print(f"{'PASS' if ok else 'FAIL'} {skill}:{klass} — {detail}")
        elif path.name != "README.md":
            for case in data.get("cases", []):
                total += 1
                ok, detail = evaluate_fixture(case)
                passed += ok
                print(f"{'PASS' if ok else 'FAIL'} {data.get('skill')}:{case.get('id')} — {detail}")
    print(f"\nFixture contract: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
