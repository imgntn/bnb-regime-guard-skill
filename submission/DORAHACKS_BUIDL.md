# DoraHacks BUIDL Submission Draft

## Project Name

Regime Guard CMC Strategy

## Track

Track 2: Strategy Skills

## Short Description

Regime Guard is a CoinMarketCap Strategy Skill that turns CMC market, technical, derivatives, sentiment, and liquidity data into a transparent, backtestable BNB Chain rotation strategy.

## Long Description

Regime Guard helps an AI agent decide when to rotate into, hold, reduce, or avoid BNB Chain assets using CoinMarketCap-native data. It first classifies the broader market as risk-on, mixed, or risk-off from Fear & Greed, BTC trend, global market trend, and stablecoin dominance. It then scores each eligible token using trend, RSI, MACD, funding, open interest, news/social tone, volatility, and BNB Chain liquidity.

The output is a reproducible strategy report with target weights, confidence, reasons, and risk controls. The repo includes a complete Skill file, deterministic Python strategy engine, sample CMC-style data, a close-to-close backtest runner, tests, and a static demo page. It is intentionally non-custodial and non-executing for Track 2.

## Problem

Most trading agents mix market reading, reasoning, and execution into an opaque loop. That makes them hard to backtest and hard to trust. Regime Guard separates the strategy layer from execution and produces an auditable signal contract that a live agent can consume later.

## What It Does

- Reads CMC-style market snapshots.
- Classifies market regime.
- Scores eligible BNB Hack assets.
- Emits `ROTATE_IN`, `HOLD`, `REDUCE`, and `AVOID` decisions.
- Builds capped target portfolio weights.
- Applies drawdown, loss, liquidity, and slippage guardrails.
- Runs a reproducible sample backtest.

## CoinMarketCap Usage

Regime Guard is designed for CoinMarketCap Agent Hub data:

- MCP for live quotes, technicals, derivatives, sentiment/news, and global metrics.
- CMC CLI for scriptable JSON snapshots.
- CMC REST for direct app integration.
- Optional x402 for pay-per-request data access.

The sample data mirrors the expected CMC snapshot schema so judges can run the strategy without credentials.

## Technical Stack

- Python 3.10+.
- Agent Skill in `skills/regime-guard-cmc-strategy/SKILL.md`.
- Deterministic strategy engine in `src/regime_guard/engine.py`.
- Backtest runner in `src/regime_guard/backtest.py`.
- Static demo in `docs/index.html`.
- No live private keys required for Track 2.

## How To Run

```bash
cd bnb-regime-guard-skill
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

## Demo

Open `docs/index.html` for the static demo. Generate fresh local reports with the commands above.

## Related Project

The separate Track 1 autonomous agent implementation is at `https://github.com/imgntn/bnb-regime-guard-agent`.

## Repository Link

https://github.com/imgntn/bnb-regime-guard-skill

## Video Link

Not included. The repository includes a static demo page at `docs/index.html` and reproducible CLI commands for generating the strategy report and backtest.

## Submission Checklist

- Public repo link: https://github.com/imgntn/bnb-regime-guard-skill
- Skill file included: yes.
- Strategy spec included: `submission/STRATEGY_SPEC.md`.
- Reproducible setup instructions: yes.
- Demo page: `docs/index.html`.
- Tests: `python -m unittest discover -s tests`.
- Track 1 on-chain proof: not applicable for Track 2.
