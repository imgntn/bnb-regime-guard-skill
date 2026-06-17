from __future__ import annotations

"""Integration notes for replacing sample data with live CoinMarketCap data.

This module deliberately avoids hard-coding paid endpoint behavior. For the hackathon entry,
the Skill describes the exact CMC fields it expects and the sample files make the strategy
reproducible without credentials. In production, populate the same snapshot shape from:

- CMC MCP: quotes, technical analysis, derivatives, sentiment/news, global metrics.
- CMC CLI: stable JSON output redirected into this schema.
- CMC REST: pro-api.coinmarketcap.com with X-CMC_PRO_API_KEY.
- CMC x402: pay-per-request data access for agents without API-key management.
"""

REQUIRED_ASSET_FIELDS = [
    "symbol",
    "price",
    "volume_24h",
    "market_cap",
    "rsi_14",
    "macd_histogram",
    "ema_20",
    "ema_50",
    "atr_pct",
    "change_7d_pct",
    "funding_rate_pct",
    "open_interest_change_pct",
    "news_sentiment",
    "social_dominance_change_pct",
    "bnb_chain_liquidity_score",
]


def validate_snapshot(snapshot: dict) -> list[str]:
    errors: list[str] = []
    if "market" not in snapshot:
        errors.append("missing market object")
    for idx, asset in enumerate(snapshot.get("assets", [])):
        for field in REQUIRED_ASSET_FIELDS:
            if field not in asset:
                errors.append(f"asset[{idx}] {asset.get('symbol', '?')} missing {field}")
    return errors

