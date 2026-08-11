#!/usr/bin/env python3
"""Validate Core Skills, Rule dependencies, and Rule -> Knowledge provenance."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

REQUIRED = [
    "# ", "## Purpose", "## Use When", "## Do Not Use When",
    "## Required Inputs", "## Preconditions", "## Knowledge Dependencies",
    "## Rule Dependencies", "## Workflow", "## Output Contract",
    "## Confidence", "## Safety", "## Related Skills", "## Examples"
]


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def as_list(value) -> list:
    return value if isinstance(value, list) else []


def normalize_conditional(items) -> list[dict]:
    normalized = []
    for item in as_list(items):
        if not isinstance(item, dict):
            normalized.append(item)
            continue
        normalized.append({
            "when": item.get("when"),
            "rules": as_list(item.get("rules")),
        })
    return normalized


def normalize_paths(value) -> list[str]:
    return [str(x) for x in as_list(value)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", default="skills", type=Path)
    parser.add_argument("--registry", default="skills/registry.yaml", type=Path)
    parser.add_argument("--rule-registry", default="rules/registry.yaml", type=Path)
    args = parser.parse_args()

    registry = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    rule_registry = yaml.safe_load(args.rule_registry.read_text(encoding="utf-8"))
    entries = registry.get("skills", [])
    rule_entries = rule_registry.get("rules", [])
    errors: list[str] = []

    if registry.get("version") != "2.1.0":
        errors.append("registry: expected version 2.1.0")
    if registry.get("schema") != "skill-dependency-graph/v1":
        errors.append("registry: expected schema skill-dependency-graph/v1")
    if registry.get("dependency_policy", {}).get("no_inference") is not True:
        errors.append("registry: dependency_policy.no_inference must be true")
    if registry.get("rule_provenance_registry") != "rules/registry.yaml":
        errors.append("registry: rule_provenance_registry must point to rules/registry.yaml")

    if rule_registry.get("version") != "1.0.0":
        errors.append("rule registry: expected version 1.0.0")
    if rule_registry.get("schema") != "rule-knowledge-provenance/v1":
        errors.append("rule registry: expected schema rule-knowledge-provenance/v1")
    if rule_registry.get("dependency_policy", {}).get("no_inference") is not True:
        errors.append("rule registry: dependency_policy.no_inference must be true")

    rule_map: dict[str, dict] = {}
    for entry in rule_entries:
        path = str(entry.get("path", ""))
        rule_id = str(entry.get("id", ""))
        if not rule_id or not path:
            errors.append("rule registry: every entry needs id and path")
            continue
        if path in rule_map:
            errors.append(f"rule registry: duplicate path {path}")
        rule_map[path] = entry

        rule_path = Path(path)
        if not rule_path.exists():
            errors.append(f"rule registry: missing rule path {path}")
            continue
        try:
            rule = yaml.safe_load(rule_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"rule registry: invalid YAML {path}: {exc}")
            continue

        if rule.get("id") != rule_id:
            errors.append(f"{path}: rule id != rule registry id")
        rule_knowledge = normalize_paths(rule.get("knowledge_dependencies"))
        registry_knowledge = normalize_paths(entry.get("knowledge"))
        if rule_knowledge != registry_knowledge:
            errors.append(f"{path}: knowledge_dependencies != rule registry")
        if not rule_knowledge:
            errors.append(f"{path}: missing knowledge_dependencies")
        for dep in rule_knowledge:
            if not Path(dep).exists():
                errors.append(f"{path}: missing Knowledge dependency {dep}")

    for entry in entries:
        name = entry["name"]
        expected_path = args.skills / name / "SKILL.md"
        declared_path = Path(entry.get("path", ""))

        if declared_path.as_posix() != expected_path.as_posix():
            errors.append(f"{name}: registry path mismatch")
        if not expected_path.exists():
            errors.append(f"{name}: missing SKILL.md")
            continue

        text = expected_path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        if not meta.get("version"):
            errors.append(f"{name}: missing version")

        for marker in REQUIRED:
            if marker not in text:
                errors.append(f"{name}: missing section {marker}")
        if "Rule Engine Contract" not in text:
            errors.append(f"{name}: missing Rule Engine Contract")
        if "human approval" not in text.lower() and "approval" not in text.lower():
            errors.append(f"{name}: safety/approval behavior not explicit")

        registry_knowledge = normalize_paths(entry.get("knowledge"))
        registry_rules = normalize_paths(entry.get("rules"))
        frontmatter_knowledge = normalize_paths(meta.get("knowledge_dependencies"))
        frontmatter_rules = normalize_paths(meta.get("rule_dependencies"))

        if frontmatter_knowledge != registry_knowledge:
            errors.append(f"{name}: frontmatter knowledge_dependencies != registry knowledge")
        if frontmatter_rules != registry_rules:
            errors.append(f"{name}: frontmatter rule_dependencies != registry rules")

        registry_conditional = normalize_conditional(entry.get("conditional_rules"))
        frontmatter_conditional = normalize_conditional(meta.get("conditional_rule_dependencies"))
        if frontmatter_conditional != registry_conditional:
            errors.append(f"{name}: conditional Rule dependencies != registry conditional_rules")

        for dep in registry_knowledge + registry_rules:
            if not Path(dep).exists():
                errors.append(f"{name}: missing dependency path {dep}")
        for group in registry_conditional:
            for dep in group.get("rules", []):
                if not Path(dep).exists():
                    errors.append(f"{name}: missing conditional dependency path {dep}")

        all_rule_paths = registry_rules + [
            dep for group in registry_conditional for dep in group.get("rules", [])
        ]
        for rule_path in all_rule_paths:
            if rule_path not in rule_map:
                errors.append(f"{name}: Rule missing from rule provenance registry: {rule_path}")

    if errors:
        print("SKILL VALIDATION FAILED")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(
        f"SKILL VALIDATION PASSED: {len(entries)} Core Skills; "
        f"{len(rule_entries)} Rules; Rule -> Knowledge provenance consistent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
