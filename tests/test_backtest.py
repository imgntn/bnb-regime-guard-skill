import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from regime_guard.backtest import run_backtest


class BacktestTest(unittest.TestCase):
    def test_backtest_outputs_core_metrics(self):
        series = json.loads((ROOT / "data" / "sample_backtest_series.json").read_text())
        report = run_backtest(series, 1000)
        self.assertIn("total_return_pct", report)
        self.assertIn("max_drawdown_pct", report)
        self.assertEqual(len(report["equity_curve"]), len(series))
        self.assertGreaterEqual(report["rebalance_events"], 1)


if __name__ == "__main__":
    unittest.main()

