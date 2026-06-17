# Regime Guard CMC Strategy

Track 2 entry for **BNB Hack: AI Trading Agent Edition - CoinMarketCap x Trust Wallet**.

Regime Guard is a CoinMarketCap Strategy Skill that turns CMC market, technical, derivatives, sentiment, and liquidity data into a backtestable BNB Chain spot-rotation strategy. It does not custody funds or execute trades. It produces transparent strategy reports that can later be routed into Trust Wallet Agent Kit for Track 1 execution.

## Why This Fits Track 2

- **CMC-native data model:** designed around CMC Agent Hub fields: quotes, technicals, derivatives, sentiment/news, global metrics, and token/liquidity context.
- **Backtestable spec:** deterministic rules, target weights, drawdown stops, and sample backtest runner.
- **Agent Skill deliverable:** `skills/regime-guard-cmc-strategy/SKILL.md` is the reusable LLM Skill.
- **Demo without credentials:** sample CMC-style data and a local CLI show the full flow.

## Repository Layout

```text
skills/regime-guard-cmc-strategy/SKILL.md  # Skill instructions for an agent
src/regime_guard/engine.py                 # deterministic signal and allocation logic
src/regime_guard/backtest.py               # simple close-to-close backtest
src/regime_guard/cmc_adapter.py            # CMC integration schema and validation notes
data/sample_market_snapshot.json           # reproducible sample input
data/sample_backtest_series.json           # reproducible sample backtest data
submission/DORAHACKS_BUIDL.md              # copy/paste BUIDL submission draft
submission/STRATEGY_SPEC.md                # formal strategy spec
docs/index.html                            # static demo page
tests/                                     # unittest coverage
```

## Quickstart

```bash
cd bnb-regime-guard-skill
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python -m regime_guard.cli analyze --input data/sample_market_snapshot.json --output docs/sample_signal.json
python -m regime_guard.cli backtest --input data/sample_backtest_series.json --output docs/backtest_report.json
python -m unittest discover -s tests
```

PowerShell without installation:

```powershell
$env:PYTHONPATH='src'
python -m regime_guard.cli analyze --input data/sample_market_snapshot.json
python -m regime_guard.cli backtest --input data/sample_backtest_series.json
python -m unittest discover -s tests
```

## Strategy Summary

Regime Guard has two layers:

1. **Market regime filter:** Fear & Greed, BTC trend, global market trend, and stablecoin dominance classify the market as `risk_on`, `mixed`, or `risk_off`.
2. **Asset score:** each eligible token is scored from trend, RSI, MACD, derivatives crowding, news/social tone, liquidity, and volatility.

Actions:

- `ROTATE_IN`: allocate capital, capped at 25% per asset.
- `HOLD`: keep a smaller allocation.
- `REDUCE`: exit or shrink exposure.
- `AVOID`: no allocation.

Portfolio guardrails:

- Max gross exposure: 80%.
- Stable reserve: at least 20%.
- Daily loss stop: 4%.
- Weekly drawdown stop: 8% to 12%, depending on regime.
- Spot-only strategy for Track 2; no leverage assumed.

## CMC Integration

The sample files use the same shape expected from live CMC data. Replace them with data from:

- CoinMarketCap MCP at `https://mcp.coinmarketcap.com/mcp`.
- CMC CLI JSON output.
- CMC REST API at `https://pro-api.coinmarketcap.com`.
- CMC x402 pay-per-request access.

The integration contract is documented in `src/regime_guard/cmc_adapter.py`.

## Track 1 Extension

For Track 1, wire the generated decisions into Trust Wallet Agent Kit:

1. Query CMC data and generate a strategy report.
2. Convert `ROTATE_IN` and `REDUCE` deltas into quote-only TWAK swap previews.
3. Reject any trade violating allowlist, slippage, per-trade notional, daily loss, or drawdown limits.
4. Execute through TWAK autonomous agent wallet only after all rules pass.
5. Register the agent wallet with `twak compete register`.

This repo intentionally keeps Track 2 non-executing so the submitted Skill is safe, reproducible, and judgeable.

## Disclaimer

This is hackathon software and a strategy research artifact, not financial advice. Live trading can lose money.

