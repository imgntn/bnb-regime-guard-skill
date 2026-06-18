---
name: regime-guard-cmc-strategy
description: Generate a backtestable, regime-aware BNB Chain trading strategy from CoinMarketCap market, technical, derivatives, sentiment, and liquidity data.
---

# Regime Guard CMC Strategy

Use this skill when a user asks for a crypto trading strategy, a BNB Hack Track 2 strategy spec, a CMC-backed signal workflow, or a backtestable market regime model for eligible BNB Chain assets.

This is a strategy-generation skill, not a live trading executor. It produces transparent `ROTATE_IN`, `HOLD`, `REDUCE`, and `AVOID` decisions plus target weights and risk controls.

## Required Data

Prefer CoinMarketCap Agent Hub data through MCP, CMC CLI JSON, CMC REST, or x402. The strategy expects:

- Market context: Fear & Greed, BTC 24h change, global market cap 24h change, stablecoin dominance change.
- Per asset: price, volume 24h, market cap, RSI 14, MACD histogram, EMA 20, EMA 50, ATR percent, 7d change, funding rate, open interest change, news sentiment, social dominance change, and BNB Chain liquidity score.
- Universe: only assets eligible for the BNB Hack competition token set, or a user-supplied allowlist.

If live data is unavailable, use `data/sample_market_snapshot.json` to demonstrate the workflow.

## Workflow

1. Resolve assets to stable CoinMarketCap IDs. Do not rely on ambiguous symbols when CMC IDs are available.
2. Build a CMC-style snapshot with the fields listed above.
3. Classify the market regime:
   - `risk_on`: positive breadth, Fear & Greed above neutral, BTC/global market trend supportive.
   - `risk_off`: negative breadth, stablecoin dominance rising, BTC/global market trend weak.
   - `mixed`: no strong top-down confirmation.
4. Score each eligible asset:
   - Trend: EMA20 versus EMA50, 7d momentum, MACD histogram.
   - Entry quality: RSI trend band and overheat checks.
   - Derivatives: funding crowding and open-interest confirmation.
   - Sentiment: CMC news/social tone.
   - Liquidity/risk: volume-to-market-cap, BNB Chain liquidity score, ATR percent.
5. Produce portfolio weights:
   - Max gross exposure: 80%.
   - Max single position: 25%.
   - Stable reserve: at least 20%.
   - Daily loss stop: 4%.
   - Weekly drawdown stop: 8% in mixed/risk-off, 12% in risk-on.
6. Return a strategy report with:
   - Market regime.
   - Ranked signals.
   - Target weights.
   - Reasons for every decision.
   - Execution policy and risk constraints.

## Local Commands

From the repository root:

```bash
python -m regime_guard.cli analyze --input data/sample_market_snapshot.json --output docs/sample_signal.json
python -m regime_guard.cli backtest --input data/sample_backtest_series.json --output docs/backtest_report.json
python -m unittest discover -s tests
```

If the package is not installed, run with `PYTHONPATH=src` on Unix-like shells or `$env:PYTHONPATH='src'` in PowerShell.

## Output Contract

The strategy report must include:

```json
{
  "strategy": "Regime Guard CMC Strategy",
  "regime": {"label": "risk_on|mixed|risk_off", "score": 0},
  "portfolio": {
    "target_gross_exposure_pct": 0,
    "stable_reserve_pct": 100,
    "max_single_position_pct": 25,
    "daily_loss_stop_pct": 4,
    "weekly_drawdown_stop_pct": 8
  },
  "signals": [
    {
      "symbol": "BNB",
      "action": "ROTATE_IN|HOLD|REDUCE|AVOID",
      "confidence": 0,
      "target_weight_pct": 0,
      "score": 0,
      "risk_score": 0,
      "reasons": ["transparent rationale"]
    }
  ]
}
```

## Safety Rules

- Do not present this strategy as financial advice.
- Do not generate live orders inside Track 2.
- Do not recommend assets outside the contest-eligible or user-approved universe.
- Reduce exposure when risk controls conflict with signal strength.
- If data fields are missing, explicitly state which fields are missing and run a reduced-confidence analysis only when the user accepts that limitation.
