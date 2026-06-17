from __future__ import annotations

from collections import defaultdict
from typing import Any

from .engine import analyze_snapshot


def run_backtest(series: list[dict[str, Any]], starting_equity: float = 1000.0) -> dict[str, Any]:
    """Run a simple close-to-close allocation backtest over CMC-style snapshots.

    Each snapshot must include asset prices. The strategy uses the signal generated at day N
    and marks the portfolio at day N+1 prices.
    """
    if len(series) < 2:
        raise ValueError("backtest requires at least two snapshots")

    equity = starting_equity
    equity_curve = [{"date": series[0].get("generated_at"), "equity": round(equity, 2)}]
    positions: dict[str, float] = {}
    daily_returns: list[float] = []
    trades = 0

    for idx in range(len(series) - 1):
        today = series[idx]
        tomorrow = series[idx + 1]
        report = analyze_snapshot(today)
        price_now = {a["symbol"].upper(): float(a["price"]) for a in today.get("assets", [])}
        price_next = {a["symbol"].upper(): float(a["price"]) for a in tomorrow.get("assets", [])}

        target_weights = {
            s["symbol"]: s["target_weight_pct"] / 100.0
            for s in report["signals"]
            if s["target_weight_pct"] > 0 and s["symbol"] in price_now and s["symbol"] in price_next
        }
        if target_weights != positions:
            trades += max(1, len(set(target_weights) ^ set(positions)))
        positions = target_weights

        period_return = 0.0
        for symbol, weight in positions.items():
            if price_now[symbol] <= 0:
                continue
            period_return += weight * ((price_next[symbol] / price_now[symbol]) - 1.0)

        equity *= 1.0 + period_return
        daily_returns.append(period_return)
        equity_curve.append({"date": tomorrow.get("generated_at"), "equity": round(equity, 2)})

    total_return = (equity / starting_equity) - 1.0
    max_dd = _max_drawdown([p["equity"] for p in equity_curve])
    win_rate = sum(1 for r in daily_returns if r > 0) / len(daily_returns)

    return {
        "starting_equity": starting_equity,
        "ending_equity": round(equity, 2),
        "total_return_pct": round(total_return * 100, 2),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "daily_win_rate_pct": round(win_rate * 100, 2),
        "rebalance_events": trades,
        "equity_curve": equity_curve,
        "notes": [
            "Backtest is intentionally simple and reproducible: daily close-to-close, no leverage.",
            "Live Track 1 execution should add gas, DEX price impact, and TWAK quote slippage checks.",
        ],
    }


def _max_drawdown(values: list[float]) -> float:
    peak = values[0]
    worst = 0.0
    for value in values:
        peak = max(peak, value)
        if peak:
            worst = max(worst, (peak - value) / peak)
    return worst

