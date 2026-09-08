import copy
import json
import random
import tempfile
import unittest
from pathlib import Path

import model_guidance as mg


HEAD = """<html><body><div>Artificial Analysis Coding Agent Index v1.4 · Higher is better</div><table><tr>{}</tr>""".format(
    "".join(f"<th>{h}</th>" for h in mg.HEADERS))
TAIL = "</table></body></html>"


def row(agent, model, d="60%", t="80%", q="50%", cost="$2.00", time="2.0m"):
    values = [agent, model, "64", d, t, q, cost, time, "2M"]
    return "<tr>" + "".join(f"<td>{v}</td>" for v in values) + "</tr>"


def policy():
    mode = {"incumbent": "codex:sol:high", "label": "Sol high", "floors": {"deepswe": "60", "terminal": "80"},
            "allowed_loss": {"deepswe": "0", "terminal": "0"}, "pinned_reason": None}
    return {"schema_version": 1, "source": {"adapter": "aa-agent-comparison-v1", "url": "https://example.test",
            "index_version": "1.4", "comparison_group": "g"},
            "models": [{"harness": "codex", "id": "sol", "source_name": "Sol", "display_name": "Sol",
                        "efforts": ["low", "high"], "allow_fallback": True}],
            "routes": [{"harness": "codex", "task_id": "build", "task_label": "Build", "metrics": ["deepswe", "terminal"],
                        "allowed_models": ["sol"], "escalation": "high", "modes": {name: copy.deepcopy(mode) for name in ("conserve", "balanced", "burn")}}]}


def parse(p=None, rows=None, version="1.4"):
    p = p or policy()
    html = (HEAD + "".join(rows or [row("Codex", "Sol (high)")]) + TAIL).replace("v1.4", "v" + version)
    return mg.parse_html(p, html.encode(), "2026-01-01T00:00:00Z")


class ParserTests(unittest.TestCase):
    def test_real_fixture_shape_and_fallback(self):
        actual_policy = json.loads((Path(__file__).parent.parent / "data/policy.json").read_text())
        raw = Path("/Users/theo/tse/agent-logs/explore-deterministic-model-routing/aa.html").read_bytes()
        snapshot = mg.parse_html(actual_policy, raw, "2026-09-08T00:00:00Z")
        self.assertGreater(len(snapshot["records"]), 20)
        fallback = next(r for r in snapshot["records"] if r["fallback"])
        self.assertTrue(fallback["id"].endswith(":fallback"))
        self.assertEqual(fallback["comparison_group"], "aa-cai-1.4:claude-code")

    def test_header_and_version_drift_fail(self):
        with self.assertRaisesRegex(ValueError, "known headers"):
            mg.parse_html(policy(), (HEAD.replace("DeepSWE", "Deep SWE") + row("Codex", "Sol (high)") + TAIL).encode(), "x")
        with self.assertRaisesRegex(ValueError, "v1.4"):
            parse(version="1.5")

    def test_duplicate_missing_numeric_and_unknown_effort_fail(self):
        cases = [
            [row("Codex", "Sol (high)"), row("Codex", "Sol (high)")],
            [row("Codex", "Sol (high)", d="-")],
            [row("Codex", "Sol (medium)")],
        ]
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                parse(rows=rows)

    def test_null_cost_and_absent_mapped_model_gap(self):
        p = policy()
        p["models"].append({"harness": "codex", "id": "other", "source_name": "Other", "display_name": "Other",
                            "efforts": ["high"], "allow_fallback": False})
        snapshot = parse(p, [row("Codex", "Sol (high)", cost="-")])
        self.assertIsNone(snapshot["records"][0]["cost_usd"])
        self.assertEqual(snapshot["gaps"][0]["model"], "other")

    def test_malformed_mapped_label_fails(self):
        with self.assertRaisesRegex(ValueError, "malformed mapped"):
            parse(rows=[row("Codex", "Sol high")])

    def test_visible_version_wins_over_script_history(self):
        html = (HEAD.replace("v1.4", "v1.5") + row("Codex", "Sol (high)") + TAIL +
                "<script>Artificial Analysis Coding Agent Index v1.4 · Higher is better</script>")
        with self.assertRaisesRegex(ValueError, "found.*1.5"):
            mg.parse_html(policy(), html.encode(), "x")

    def test_source_order_does_not_change_records(self):
        rows = [row("Codex", "Sol (high)"), row("Codex", "Sol (low)", cost="$1")]
        self.assertEqual(parse(rows=rows)["records"], parse(rows=list(reversed(rows)))["records"])


class SelectionTests(unittest.TestCase):
    def records(self):
        return parse(rows=[row("Codex", "Sol (high)", d="60%", t="80%", cost="$2", time="2m"),
                           row("Codex", "Sol (low)", d="61%", t="80%", cost="$1", time="-")])["records"]

    def test_threshold_equality_and_allowed_loss(self):
        p = policy(); route = p["routes"][0]; mode = route["modes"]["conserve"]
        result = mg.select(route, "conserve", mode, self.records(), {("codex", "sol"): p["models"][0]}, "g")
        self.assertEqual(result["selected_id"], "codex:sol:low")
        mode["floors"]["deepswe"] = "62"; mode["allowed_loss"]["deepswe"] = "1"
        self.assertEqual(mg.select(route, "conserve", mode, self.records(), {("codex", "sol"): p["models"][0]}, "g")["selected_id"], "codex:sol:low")

    def test_balanced_requires_domination(self):
        p = policy(); route = p["routes"][0]; records = self.records()
        low = next(r for r in records if r["effort"] == "low")
        low["scores"]["terminal"] = "79"
        result = mg.select(route, "balanced", route["modes"]["balanced"], records, {("codex", "sol"): p["models"][0]}, "g")
        self.assertEqual(result["selected_id"], "codex:sol:high")

    def test_burn_missing_time_skips_tie_break_for_whole_set(self):
        p = policy(); route = p["routes"][0]; records = self.records()
        for record in records:
            record["scores"] = {"deepswe": "60", "terminal": "80", "qna": "50"}
        result = mg.select(route, "burn", route["modes"]["burn"], records, {("codex", "sol"): p["models"][0]}, "g")
        self.assertEqual(result["selected_id"], "codex:sol:low")  # cost applies after time is skipped

    def test_pinned_missing_incumbent_and_group_mismatch_retain(self):
        p = policy(); route = p["routes"][0]; mode = route["modes"]["burn"]
        mode["pinned_reason"] = "seed"
        self.assertIn("pinned", mg.select(route, "burn", mode, [], {}, "g")["reason"])
        mode["pinned_reason"] = None
        self.assertIn("missing", mg.select(route, "burn", mode, [], {}, "g")["reason"])
        records = self.records(); records[0]["comparison_group"] = "other"
        self.assertIn("mismatch", mg.select(route, "burn", mode, records, {("codex", "sol"): p["models"][0]}, "g")["reason"])

    def test_fallback_policy(self):
        snapshot = parse(rows=[row("Codex", "Sol (high) (with fallback)")])
        self.assertEqual(snapshot["records"][0]["id"], "codex:sol:high:fallback")
        p = policy(); p["models"][0]["allow_fallback"] = False
        with self.assertRaisesRegex(ValueError, "fallback"):
            parse(p, [row("Codex", "Sol (high) (with fallback)")])

    def test_generate_is_byte_identical(self):
        p = policy(); snapshot = parse(rows=[row("Codex", "Sol (high)"), row("Codex", "Sol (low)")])
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            mg.generate(p, snapshot, a); mg.generate(p, snapshot, b)
            self.assertEqual({x.name: x.read_bytes() for x in Path(a).iterdir()},
                             {x.name: x.read_bytes() for x in Path(b).iterdir()})
            decisions = json.loads((Path(a) / "decisions.json").read_text())
            self.assertEqual(len(decisions["policy_sha256"]), 64)
            self.assertEqual(decisions["decisions"][0]["harness"], "codex")

    def test_generate_rejects_bad_imported_snapshot(self):
        p = policy(); snapshot = parse()
        bad_cases = []
        for change in ({"id": "wrong"}, {"effort": "medium"}, {"fallback": "yes"}, {"cost_usd": "NaN"},
                       {"comparison_group": "wrong"}, {"provisional": False}):
            bad = copy.deepcopy(snapshot); bad["records"][0].update(change); bad_cases.append(bad)
        duplicate = copy.deepcopy(snapshot); duplicate["records"].append(copy.deepcopy(duplicate["records"][0])); bad_cases.append(duplicate)
        for bad in bad_cases:
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as target, self.assertRaises(ValueError):
                mg.generate(p, bad, target)

    def test_generate_rejects_bad_snapshot_provenance(self):
        p = policy(); snapshot = parse()
        changes = [
            ("schema_version", 999),
            ("source.url", "https://fake.test"),
            ("source.raw_sha256", "not-a-hash"),
            ("source.retrieved_at", "not-a-date"),
            ("source.retrieved_at", "2026-01-01T00:00:00"),
            ("source.index_version", ""),
            ("source.comparison_group", ""),
        ]
        for path, value in changes:
            bad = copy.deepcopy(snapshot)
            if path.startswith("source."):
                bad["source"][path.split(".")[1]] = value
            else:
                bad[path] = value
            with self.subTest(path=path), tempfile.TemporaryDirectory() as target, self.assertRaises(ValueError):
                mg.generate(p, bad, target)
        for missing in ("url", "raw_sha256", "retrieved_at", "index_version", "comparison_group"):
            bad = copy.deepcopy(snapshot); del bad["source"][missing]
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as target, self.assertRaises(ValueError):
                mg.generate(p, bad, target)

    def test_valid_source_version_or_group_mismatch_retains_routes(self):
        p = policy(); snapshot = parse()
        for field, value in (("index_version", "1.5"), ("comparison_group", "g-next")):
            changed = copy.deepcopy(snapshot); changed["source"][field] = value
            if field == "comparison_group":
                for record in changed["records"]:
                    record["comparison_group"] = value + ":" + record["harness"]
            with self.subTest(field=field), tempfile.TemporaryDirectory() as target:
                mg.generate(p, changed, target)
                decisions = json.loads((Path(target) / "decisions.json").read_text())["decisions"]
                self.assertTrue(all("retained" in decision["reason"] for decision in decisions))
                self.assertIn("P Sol high", (Path(target) / "codex-routes.md").read_text())


if __name__ == "__main__":
    unittest.main()
