from __future__ import annotations

import argparse
import json
from pathlib import Path

from .backtest import run_backtest
from .engine import analyze_snapshot


def _read_json(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str, data: object) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def cmd_analyze(args: argparse.Namespace) -> int:
    report = analyze_snapshot(_read_json(args.input))
    if args.output:
        _write_json(args.output, report)
    print(json.dumps(report, indent=2))
    return 0


def cmd_backtest(args: argparse.Namespace) -> int:
    data = _read_json(args.input)
    if not isinstance(data, list):
        raise SystemExit("backtest input must be a JSON list of snapshots")
    report = run_backtest(data, args.starting_equity)
    if args.output:
        _write_json(args.output, report)
    print(json.dumps(report, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regime Guard CMC Strategy Skill")
    sub = parser.add_subparsers(dest="cmd", required=True)

    analyze = sub.add_parser("analyze", help="generate strategy report from a CMC-style snapshot")
    analyze.add_argument("--input", default="data/sample_market_snapshot.json")
    analyze.add_argument("--output")
    analyze.set_defaults(fn=cmd_analyze)

    backtest = sub.add_parser("backtest", help="run deterministic daily backtest")
    backtest.add_argument("--input", default="data/sample_backtest_series.json")
    backtest.add_argument("--starting-equity", type=float, default=1000.0)
    backtest.add_argument("--output")
    backtest.set_defaults(fn=cmd_backtest)

    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())

