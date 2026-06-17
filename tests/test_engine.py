import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from regime_guard.engine import ELIGIBLE_TOKENS, analyze_snapshot, market_regime, score_asset


class EngineTest(unittest.TestCase):
    def test_market_regime_risk_on(self):
        snapshot = {
            "market": {
                "fear_greed": 72,
                "btc_24h_change_pct": 2.4,
                "global_market_cap_24h_change_pct": 1.8,
                "stablecoin_dominance_change_pct": -0.8,
            }
        }
        self.assertEqual(market_regime(snapshot)["label"], "risk_on")

    def test_ineligible_token_is_avoided(self):
        signal = score_asset({"symbol": "NOTREAL", "eligible": False}, "risk_on")
        self.assertEqual(signal.action, "AVOID")
        self.assertEqual(signal.target_weight_pct, 0)

    def test_official_hackathon_universe_includes_long_tail_tokens(self):
        self.assertIn("USD1", ELIGIBLE_TOKENS)
        self.assertIn("ZAMA", ELIGIBLE_TOKENS)
        self.assertIn("币安人生", ELIGIBLE_TOKENS)

    def test_sample_snapshot_generates_allocations_and_stable_reserve(self):
        sample = json.loads((ROOT / "data" / "sample_market_snapshot.json").read_text())
        report = analyze_snapshot(sample)
        self.assertIn(report["regime"]["label"], {"risk_on", "risk_off", "mixed"})
        self.assertLessEqual(report["portfolio"]["target_gross_exposure_pct"], 80)
        self.assertGreaterEqual(report["portfolio"]["stable_reserve_pct"], 20)
        self.assertTrue(any(s["action"] == "ROTATE_IN" for s in report["signals"]))


if __name__ == "__main__":
    unittest.main()
