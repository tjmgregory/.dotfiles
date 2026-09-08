#!/usr/bin/env python3
"""Collect, normalize, and route coding-agent benchmark evidence."""

import argparse
import hashlib
import json
import os
import re
import tempfile
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path

HEADERS = ["Agent", "Model", "Index", "DeepSWE", "Terminal-Bench v2.1",
           "SWE-Atlas-QnA", "Cost / Task", "Time / Task", "Tokens / Task"]
HARNESS = {"Claude Code": "claude-code", "Codex": "codex"}
METRIC_COLUMN = {"deepswe": 3, "terminal": 4, "qna": 5}


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.table, self.cell = [], None, None
        self.visible, self.hidden = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if tag == "table":
            self.table = []
        elif self.table is not None and tag == "tr":
            self.table.append([])
        elif self.table is not None and tag in ("th", "td"):
            self.cell = []

    def handle_data(self, data):
        if not self.hidden:
            self.visible.append(data)
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden -= 1
        if self.table is not None and tag in ("th", "td"):
            self.table[-1].append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def stable_json(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()


def canonical_hash(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def decimal(text, field, minimum=None, maximum=None):
    try:
        value = Decimal(text)
    except (InvalidOperation, TypeError):
        raise ValueError(f"invalid {field}: {text!r}")
    if not value.is_finite() or (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise ValueError(f"invalid {field}: {text!r}")
    return value


def normalized_decimal(value):
    value = value.normalize()
    return format(value, "f")


def parse_html(policy, raw, retrieved_at):
    expected_version = policy["source"]["index_version"]
    decoded = raw.decode("utf-8")
    parser = Tables()
    parser.feed(decoded)
    visible = " ".join(" ".join(parser.visible).split())
    versions = re.findall(r"Artificial Analysis Coding Agent Index v([^ ]+) · Higher is better", visible)
    if versions != [expected_version]:
        raise ValueError(f"expected visible Coding Agent Index v{expected_version}; found {versions}")
    matches = [table for table in parser.tables if table and table[0] == HEADERS]
    if len(matches) != 1:
        raise ValueError("expected exactly one Model Variants table with known headers")
    table = matches[0]
    models = {(m["harness"], m["source_name"]): m for m in policy["models"]}
    found, records, seen = set(), [], set()
    name_pattern = re.compile(r"^(.*?) \(([^()]*)\)(?: \(with fallback\))?$")
    for row in table[1:]:
        if len(row) != len(HEADERS):
            if row and any(row[1].startswith(name) for _, name in models if len(row) > 1):
                raise ValueError(f"malformed mapped row: {row!r}")
            continue
        harness = HARNESS.get(row[0])
        mapped = next((entry for (known_harness, name), entry in models.items()
                       if known_harness == harness and (row[1] == name or row[1].startswith(name + " "))), None)
        match = name_pattern.fullmatch(row[1])
        if harness is None or mapped is None:
            continue
        if match is None or match.group(1) != mapped["source_name"]:
            raise ValueError(f"malformed mapped model label: {row[1]!r}")
        key = (harness, match.group(1))
        model = models[key]
        found.add(key)
        effort = match.group(2)
        fallback = row[1].endswith(" (with fallback)")
        if effort not in model["efforts"]:
            raise ValueError(f"unexpected effort for {row[1]}")
        if fallback and not model["allow_fallback"]:
            raise ValueError(f"unexpected fallback for {row[1]}")
        config_id = f'{harness}:{model["id"]}:{effort}' + (":fallback" if fallback else "")
        if config_id in seen:
            raise ValueError(f"duplicate configuration: {config_id}")
        seen.add(config_id)
        decimal(row[2], "index", Decimal(0), Decimal(100))
        scores = {}
        for metric, column in METRIC_COLUMN.items():
            text = row[column]
            if not text.endswith("%"):
                raise ValueError(f"missing percentage in {config_id} {metric}")
            scores[metric] = normalized_decimal(decimal(text[:-1], metric, Decimal(0), Decimal(100)))
        if row[6] not in ("", "-") and not row[6].startswith("$"):
            raise ValueError(f"invalid cost in {config_id}")
        cost = None if row[6] in ("", "-") else normalized_decimal(decimal(row[6][1:], "cost", Decimal(0)))
        time = None
        if row[7] not in ("", "-"):
            if not row[7].endswith("m"):
                raise ValueError(f"invalid time in {config_id}")
            time = normalized_decimal(decimal(row[7][:-1], "time", Decimal(0)) * 60)
        if row[8] not in ("", "-"):
            token_match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([KM])", row[8])
            if token_match is None:
                raise ValueError(f"invalid tokens in {config_id}")
            decimal(token_match.group(1), "tokens", Decimal(0))
        records.append({"id": config_id, "harness": harness, "model": model["id"],
                        "effort": effort, "fallback": fallback, "scores": scores,
                        "cost_usd": cost, "time_seconds": time,
                        "comparison_group": f'{policy["source"]["comparison_group"]}:{harness}',
                        "provisional": True})
    gaps = [{"harness": h, "model": models[(h, name)]["id"], "reason": "mapped model absent from source table"}
            for (h, name) in sorted(set(models) - found)]
    records.sort(key=lambda record: record["id"])
    return {"schema_version": 1,
            "source": {"url": policy["source"]["url"], "raw_sha256": hashlib.sha256(raw).hexdigest(),
                       "retrieved_at": retrieved_at, "index_version": expected_version,
                       "comparison_group": policy["source"]["comparison_group"]},
            "records": records, "gaps": gaps}


def config_label(record, model):
    label = f'{model["display_name"]} ({record["effort"]})'
    return label + (" (with fallback)" if record["fallback"] else "")


def select(route, mode_name, mode, records, model_map, base_group):
    incumbent_id = mode.get("incumbent")
    result = {"harness": route["harness"], "route": route["task_id"], "mode": mode_name, "selected_id": incumbent_id,
              "label": mode["label"], "reason": "", "eligible": [], "rejected": []}
    if mode.get("pinned_reason"):
        result["reason"] = "pinned: " + mode["pinned_reason"]
        return result
    by_id = {r["id"]: r for r in records}
    incumbent = by_id.get(incumbent_id)
    if incumbent is None:
        result["reason"] = "saved route retained: incumbent evidence missing"
        return result
    expected_group = f'{base_group}:{route["harness"]}'
    if incumbent["comparison_group"] != expected_group:
        result["reason"] = "saved route retained: comparison group mismatch"
        return result
    allowed = set(route["allowed_models"])
    qualifiers = []
    for candidate in records:
        reasons = []
        if candidate["harness"] != route["harness"] or candidate["model"] not in allowed:
            continue
        if candidate["comparison_group"] != expected_group:
            reasons.append("comparison group mismatch")
        for metric in route["metrics"]:
            score = candidate["scores"].get(metric)
            floor = mode["floors"].get(metric)
            if score is None or floor is None:
                reasons.append(f"missing {metric}")
            elif Decimal(score) < Decimal(floor) - Decimal(mode.get("allowed_loss", {}).get(metric, "0")):
                reasons.append(f"{metric} below floor")
        if reasons:
            result["rejected"].append({"id": candidate["id"], "reasons": reasons})
        else:
            qualifiers.append(candidate)
            result["eligible"].append({"id": candidate["id"], "reasons": ["meets all floors"]})
    if not qualifiers:
        result["reason"] = "saved route retained: no qualifying candidate"
        return result
    if mode_name == "conserve":
        if incumbent["cost_usd"] is None:
            result["reason"] = "saved route retained: incumbent cost missing"
            return result
        usable = [r for r in qualifiers if r["cost_usd"] is not None]
        if not usable:
            result["reason"] = "saved route retained: no candidate has comparable cost"
            return result
        selected = tie_select(usable, [("cost_usd", False)], incumbent_id)
    elif mode_name == "balanced":
        improving = []
        if incumbent["cost_usd"] is not None:
            for candidate in qualifiers:
                if candidate["cost_usd"] is None:
                    continue
                scores = [Decimal(candidate["scores"][m]) >= Decimal(incumbent["scores"][m]) for m in route["metrics"]]
                improved = any(Decimal(candidate["scores"][m]) > Decimal(incumbent["scores"][m]) for m in route["metrics"])
                cheaper = Decimal(candidate["cost_usd"]) < Decimal(incumbent["cost_usd"])
                if all(scores) and (cheaper or (improved and Decimal(candidate["cost_usd"]) <= Decimal(incumbent["cost_usd"]))):
                    improving.append(candidate)
        if not improving:
            selected = incumbent
            result["reason"] = "incumbent retained: no candidate dominates"
        else:
            selected = tie_select(improving, [("cost_usd", False)] + [("scores." + m, True) for m in route["metrics"]], incumbent_id)
    else:
        selected = tie_select(qualifiers, [("scores." + m, True) for m in route["metrics"]] +
                              [("time_seconds", False), ("cost_usd", False)], incumbent_id)
    result["selected_id"] = selected["id"]
    result["label"] = config_label(selected, model_map[(selected["harness"], selected["model"])])
    if not result["reason"]:
        result["reason"] = f"{mode_name} selection"
    return result


def field(record, name):
    value = record
    for part in name.split("."):
        value = value.get(part) if isinstance(value, dict) else None
    return None if value is None else Decimal(value)


def tie_select(candidates, rules, incumbent_id):
    tied = list(candidates)
    for name, descending in rules:
        if len(tied) < 2:
            break
        values = [field(candidate, name) for candidate in tied]
        if any(value is None for value in values):
            continue
        target = max(values) if descending else min(values)
        tied = [candidate for candidate, value in zip(tied, values) if value == target]
    incumbent = next((candidate for candidate in tied if candidate["id"] == incumbent_id), None)
    return incumbent or min(tied, key=lambda candidate: candidate["id"])


def validate_snapshot(policy, snapshot):
    if snapshot.get("schema_version") != 1:
        raise ValueError("snapshot schema_version must be 1")
    source = snapshot.get("source")
    required_source = {"url", "raw_sha256", "retrieved_at", "index_version", "comparison_group"}
    if not isinstance(source, dict) or not required_source.issubset(source):
        raise ValueError("snapshot source fields are missing")
    if source["url"] != policy["source"]["url"]:
        raise ValueError("snapshot source URL differs from configured URL")
    if not isinstance(source["raw_sha256"], str) or re.fullmatch(r"[0-9a-fA-F]{64}", source["raw_sha256"]) is None:
        raise ValueError("snapshot raw_sha256 is invalid")
    try:
        retrieved_at = datetime.fromisoformat(source["retrieved_at"])
    except (TypeError, ValueError):
        raise ValueError("snapshot retrieved_at is not ISO 8601")
    if retrieved_at.tzinfo is None or retrieved_at.utcoffset() is None:
        raise ValueError("snapshot retrieved_at must include a timezone")
    for name in ("index_version", "comparison_group"):
        if not isinstance(source[name], str) or not source[name].strip():
            raise ValueError(f"snapshot {name} must be nonempty")
    if not isinstance(snapshot.get("records"), list) or not isinstance(snapshot.get("gaps"), list):
        raise ValueError("snapshot records and gaps must be lists")
    model_map = {(m["harness"], m["id"]): m for m in policy["models"]}
    source_group = source["comparison_group"]
    seen = set()
    for record in snapshot.get("records", []):
        model = model_map.get((record.get("harness"), record.get("model")))
        if model is None:
            raise ValueError(f'unknown snapshot model: {record.get("model")!r}')
        effort, fallback = record.get("effort"), record.get("fallback")
        if effort not in model["efforts"] or not isinstance(fallback, bool) or (fallback and not model["allow_fallback"]):
            raise ValueError(f'invalid snapshot configuration for {record.get("id")!r}')
        expected = f'{record["harness"]}:{record["model"]}:{effort}' + (":fallback" if fallback else "")
        if record.get("id") != expected or expected in seen:
            raise ValueError(f'invalid or duplicate snapshot id: {record.get("id")!r}')
        seen.add(expected)
        if record.get("comparison_group") != f'{source_group}:{record["harness"]}':
            raise ValueError(f"invalid comparison group for {expected}")
        if record.get("provisional") is not True:
            raise ValueError(f"record must remain provisional: {expected}")
        if set(record.get("scores", {})) != set(METRIC_COLUMN):
            raise ValueError(f"invalid scores for {expected}")
        for metric, score in record["scores"].items():
            decimal(score, metric, Decimal(0), Decimal(100))
        if record.get("cost_usd") is not None:
            decimal(record["cost_usd"], "cost", Decimal(0))
        if record.get("time_seconds") is not None:
            decimal(record["time_seconds"], "time", Decimal(0))


def generate(policy, snapshot, output_dir):
    validate_snapshot(policy, snapshot)
    floor_origin = policy.get("floor_origin")
    if floor_origin and (floor_origin.get("comparison_group") != policy["source"]["comparison_group"] or
                         floor_origin.get("index_version") != policy["source"]["index_version"]):
        raise ValueError("floor origin version/group differs from policy source; review floors")
    if (snapshot["source"]["comparison_group"] != policy["source"]["comparison_group"] or
            snapshot["source"]["index_version"] != policy["source"]["index_version"]):
        source_matches = False
    else:
        source_matches = True
    model_map = {(m["harness"], m["id"]): m for m in policy["models"]}
    decisions, harness_rows = [], {"claude-code": [], "codex": []}
    records = snapshot["records"] if source_matches else []
    for route in policy["routes"]:
        cells = []
        for mode_name in ("conserve", "balanced", "burn"):
            decision = select(route, mode_name, route["modes"][mode_name], records, model_map,
                              policy["source"]["comparison_group"])
            if not source_matches:
                decision["reason"] = "saved route retained: comparison group mismatch"
            decisions.append(decision)
            prefix = "P " if (route["modes"][mode_name].get("pinned_reason") or "retained" in decision["reason"]) else ""
            cells.append(prefix + decision["label"])
        harness_rows[route["harness"]].append([route["task_label"], *cells, route["escalation"]])
    source = snapshot["source"]
    intro = (f'Source: [Artificial Analysis]({source["url"]}), Coding Agent Index v{source["index_version"]}. '
             "Public benchmark results are provisional routing evidence, not completion estimates.\n\n")
    for harness in ("claude-code", "codex"):
        lines = [f"# {harness} routes", "", intro.rstrip(), "", "| Task | Conserve | Balanced | Burn | Escalation |",
                 "|---|---|---|---|---|"]
        for row in harness_rows[harness]:
            lines.append("| " + " | ".join(row) + " |")
        atomic_write(Path(output_dir) / f"{harness}-routes.md", ("\n".join(lines) + "\n").encode())
    score_lines = ["# Model scores", "", intro.rstrip(), "",
                   "| Harness | Model | Effort | DeepSWE | Terminal | QnA | Cost | Time |",
                   "|---|---|---:|---:|---:|---:|---:|---:|"]
    for record in snapshot["records"]:
        model = model_map.get((record["harness"], record["model"]))
        name = model["display_name"] if model else record["model"]
        effort = record["effort"] + (" + fallback" if record["fallback"] else "")
        scores = record["scores"]
        cost = "unknown" if record["cost_usd"] is None else "$" + record["cost_usd"]
        time = "unknown" if record["time_seconds"] is None else record["time_seconds"] + "s"
        score_lines.append(f'| {record["harness"]} | {name} | {effort} | {scores["deepswe"]} | '
                           f'{scores["terminal"]} | {scores["qna"]} | {cost} | {time} |')
    if snapshot["gaps"]:
        score_lines.extend(["", "Gaps:"] +
                           [f'- {gap["harness"]}:{gap["model"]}: {gap["reason"]}' for gap in snapshot["gaps"]])
    atomic_write(Path(output_dir) / "model-scores.md", ("\n".join(score_lines) + "\n").encode())
    atomic_write(Path(output_dir) / "decisions.json", stable_json({"schema_version": 1,
                 "policy_sha256": canonical_hash(policy), "snapshot_sha256": canonical_hash(snapshot),
                 "decisions": decisions}))


def main(argv=None):
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("collect", "parse"):
        command = commands.add_parser(name)
        command.add_argument("--policy", required=True)
        command.add_argument("--output", required=True)
        if name == "collect":
            command.add_argument("--raw-dir", required=True)
        else:
            command.add_argument("--html", required=True)
            command.add_argument("--retrieved-at", required=True)
    command = commands.add_parser("generate")
    command.add_argument("--policy", required=True)
    command.add_argument("--snapshot", required=True)
    command.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    policy = load(args.policy)
    if args.command == "generate":
        generate(policy, load(args.snapshot), args.output_dir)
    elif args.command == "parse":
        raw = Path(args.html).read_bytes()
        atomic_write(args.output, stable_json(parse_html(policy, raw, args.retrieved_at)))
    else:
        request = urllib.request.Request(policy["source"]["url"], headers={"User-Agent": "model-guidance/1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
        digest = hashlib.sha256(raw).hexdigest()
        raw_path = Path(args.raw_dir) / f"{digest}.html"
        atomic_write(raw_path, raw)
        snapshot = parse_html(policy, raw, datetime.now(timezone.utc).isoformat())
        atomic_write(args.output, stable_json(snapshot))


if __name__ == "__main__":
    main()
