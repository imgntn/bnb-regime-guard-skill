# Strategy Spec: Regime Guard CMC Strategy

## Objective

Generate a daily, backtestable BNB Chain rotation strategy from CoinMarketCap data. The strategy favors liquid, eligible BNB Hack assets only when top-down market regime and asset-specific signals agree.

## Universe

The strategy uses the BNB Hack eligible token list, narrowed to assets with:

- CoinMarketCap identity resolution available.
- Sufficient 24h volume and market cap.
- Usable CMC technical, derivatives, sentiment, and liquidity fields.
- BNB Chain liquidity score above the configured threshold.

## Data Inputs

Market-level:

- Fear & Greed.
- BTC 24h percent change.
- Global market cap 24h percent change.
- Stablecoin dominance change.

Asset-level:

- Price.
- Volume 24h.
- Market cap.
- RSI 14.
- MACD histogram.
- EMA 20 and EMA 50.
- ATR percent.
- 7d percent change.
- Funding rate.
- Open interest change.
- News sentiment.
- Social dominance change.
- BNB Chain liquidity score.

## Regime Model

The top-down regime score combines Fear & Greed, BTC trend, global market trend, and stablecoin dominance.

- `risk_on`: score >= 18.
- `mixed`: -18 < score < 18.
- `risk_off`: score <= -18.

Risk-on regimes add a modest score bonus to strong assets. Risk-off regimes subtract from all assets and force a lower weekly drawdown stop.

## Asset Scoring

Positive factors:

- EMA20 above EMA50.
- Positive 7d momentum, capped to avoid chasing.
- RSI between 45 and 68.
- Positive MACD histogram.
- Funding rate near neutral.
- Open interest confirming positive price trend.
- Positive news/social tone.
- Strong BNB Chain liquidity score.

Negative factors:

- EMA20 below EMA50.
- Negative 7d momentum.
- RSI above 78 or below 32.
- Negative MACD histogram.
- Crowded long funding.
- Open interest rising into price weakness.
- Thin volume versus market cap.
- Weak BNB Chain liquidity.
- High ATR percent.

## Actions

- `ROTATE_IN`: net score >= 42.
- `HOLD`: 18 <= net score < 42.
- `REDUCE`: -5 <= net score < 18.
- `AVOID`: net score < -5 or not eligible.

## Portfolio Construction

- Max gross exposure: 80%.
- Minimum stable reserve: 20%.
- Max single asset: 25%.
- Position weight for `ROTATE_IN`: net score / 4, capped to 8%-25%.
- Position weight for `HOLD`: net score / 5, capped to 3%-10%.
- If total desired gross exposure exceeds 80%, weights are scaled down proportionally.

## Risk Controls

- Daily loss stop: 4%.
- Weekly drawdown stop: 12% in risk-on, 8% otherwise.
- Suggested slippage cap for any downstream execution system: 0.75%.
- No leverage in Track 2.
- Assets outside the eligible list are always avoided.

## Rebalance Cadence

- Evaluate daily.
- Rebalance daily only when target weight changes exceed practical thresholds.
- Intraday action is reserved for risk-stop or regime-flip events.

## Backtest Method

The included backtest is daily close-to-close:

1. Generate signals from day N snapshot.
2. Apply target weights for day N to day N+1 price movement.
3. Mark portfolio equity.
4. Repeat for the sample series.

The backtest is intentionally simple and reproducible. A production execution system should add DEX quote impact, gas, slippage checks, and actual BSC liquidity routing.
