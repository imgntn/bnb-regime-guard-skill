from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


ELIGIBLE_TOKENS = {
    "ETH", "USDT", "USDC", "XRP", "TRX", "DOGE", "ZEC", "ADA", "LINK", "BCH",
    "DAI", "TON", "USD1", "USDE", "M", "LTC", "AVAX", "SHIB", "XAUT", "WLFI",
    "H", "DOT", "UNI", "ASTER", "DEXE", "USDD", "ETC", "AAVE", "ATOM", "U",
    "STABLE", "FIL", "INJ", "币安人生", "NIGHT", "FET", "TUSD", "BONK", "PENGU",
    "CAKE", "SIREN", "LUNC", "ZRO", "KITE", "FDUSD", "BEAT", "PIEVERSE", "BTT",
    "NFT", "EDGE", "FLOKI", "LDO", "B", "FF", "PENDLE", "NEX", "STG", "AXS",
    "TWT", "HOME", "RAY", "COMP", "GWEI", "XCN", "GENIUS", "XPL", "BAT",
    "SKYAI", "APE", "IP", "SFP", "TAG", "NXPC", "AB", "SAHARA", "1INCH",
    "CHEEMS", "BANANAS31", "RIVER", "MYX", "RAVE", "SNX", "FORM", "LAB", "HTX",
    "USDF", "CTM", "BDX", "SLX", "UB", "DUCKY", "FRAX", "BILL", "WFI", "KOGE",
    "ALE", "FRXUSD", "GOMINING", "VCNT", "GUA", "DUSD", "SMILEK", "0G", "BEAM",
    "MY", "SOON", "REAL", "Q", "AIOZ", "ZIG", "YFI", "TAC", "LISUSD", "CYS",
    "ZAMA", "TRIA", "HUMA", "PLUME", "ZIL", "XPR", "ZETA", "BABYDOGE", "NILA",
    "ROSE", "VELO", "UAI", "BRETT", "OPEN", "BSB", "TOSHI", "BAS", "ACH", "AXL",
    "LUR", "ELF", "KAVA", "APR", "IRYS", "EURI", "XUSD", "BARD", "DUSK", "SUSHI",
    "PEAQ", "COAI", "BDCA", "XAUM",
}


@dataclass(frozen=True)
class Signal:
    symbol: str
    action: str
    confidence: int
    target_weight_pct: float
    score: float
    risk_score: float
    reasons: list[str]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def market_regime(snapshot: dict[str, Any]) -> dict[str, Any]:
    market = snapshot.get("market", {})
    fear_greed = float(market.get("fear_greed", 50))
    btc_24h = float(market.get("btc_24h_change_pct", 0))
    global_24h = float(market.get("global_market_cap_24h_change_pct", 0))
    stable_dominance = float(market.get("stablecoin_dominance_change_pct", 0))

    score = 0.0
    score += clamp((fear_greed - 50) / 2.0, -20, 20)
    score += clamp(btc_24h * 3, -18, 18)
    score += clamp(global_24h * 3, -18, 18)
    score -= clamp(stable_dominance * 4, -12, 12)

    if score >= 18:
        label = "risk_on"
    elif score <= -18:
        label = "risk_off"
    else:
        label = "mixed"

    return {
        "label": label,
        "score": round(score, 2),
        "fear_greed": int(fear_greed),
        "inputs": {
            "btc_24h_change_pct": btc_24h,
            "global_market_cap_24h_change_pct": global_24h,
            "stablecoin_dominance_change_pct": stable_dominance,
        },
    }


def score_asset(asset: dict[str, Any], regime: str) -> Signal:
    symbol = str(asset["symbol"]).upper()
    reasons: list[str] = []

    if not asset.get("eligible", symbol in ELIGIBLE_TOKENS):
        return Signal(symbol, "AVOID", 0, 0.0, -100.0, 100.0, ["not in contest eligible token set"])

    score = 0.0
    risk = 0.0

    ema20 = float(asset.get("ema_20", asset.get("price", 0)))
    ema50 = float(asset.get("ema_50", asset.get("price", 0)))
    if ema20 > ema50:
        score += 20
        reasons.append("EMA20 above EMA50")
    else:
        score -= 18
        reasons.append("EMA20 below EMA50")

    change_7d = float(asset.get("change_7d_pct", 0))
    score += clamp(change_7d * 2.0, -20, 20)
    if abs(change_7d) >= 3:
        reasons.append(f"7d momentum {change_7d:+.1f}%")

    rsi = float(asset.get("rsi_14", 50))
    if 45 <= rsi <= 68:
        score += 14
        reasons.append("RSI in constructive trend band")
    elif rsi > 78:
        score -= 22
        risk += 12
        reasons.append("RSI overheated")
    elif rsi < 32:
        score -= 8
        risk += 8
        reasons.append("RSI weak/oversold")

    macd = float(asset.get("macd_histogram", 0))
    if macd > 0:
        score += 14
        reasons.append("MACD histogram positive")
    elif macd < 0:
        score -= 14
        reasons.append("MACD histogram negative")

    funding = float(asset.get("funding_rate_pct", 0))
    if abs(funding) <= 0.03:
        score += 5
        reasons.append("funding not crowded")
    elif funding > 0.08:
        score -= 12
        risk += 10
        reasons.append("long funding crowded")
    elif funding < -0.08:
        score -= 4
        risk += 6
        reasons.append("short funding stressed")

    oi_change = float(asset.get("open_interest_change_pct", 0))
    if oi_change > 8 and change_7d > 0:
        score += 7
        reasons.append("open interest confirms trend")
    elif oi_change > 15 and change_7d < 0:
        risk += 12
        reasons.append("open interest rising into weakness")

    sentiment = float(asset.get("news_sentiment", 0))
    social = float(asset.get("social_dominance_change_pct", 0))
    score += clamp(sentiment * 12, -12, 12)
    score += clamp(social * 1.5, -8, 8)
    if sentiment > 0.25:
        reasons.append("positive news/social tone")
    elif sentiment < -0.25:
        reasons.append("negative news/social tone")

    atr = float(asset.get("atr_pct", 0))
    volume = float(asset.get("volume_24h", 0))
    market_cap = float(asset.get("market_cap", 1))
    liquidity = float(asset.get("bnb_chain_liquidity_score", 50))
    volume_ratio = volume / market_cap if market_cap else 0

    risk += clamp((atr - 6) * 3, 0, 30)
    if volume_ratio < 0.015:
        risk += 20
        reasons.append("thin volume versus market cap")
    if liquidity < 50:
        risk += 20
        reasons.append("weak BNB Chain liquidity score")
    elif liquidity >= 75:
        score += 8
        reasons.append("strong BNB Chain liquidity score")

    if regime == "risk_off":
        score -= 18
        reasons.append("market regime risk_off")
    elif regime == "risk_on":
        score += 10
        reasons.append("market regime risk_on")

    net = score - risk
    if net >= 42:
        action = "ROTATE_IN"
    elif net >= 18:
        action = "HOLD"
    elif net >= -5:
        action = "REDUCE"
    else:
        action = "AVOID"

    confidence = int(clamp(50 + abs(net) * 0.8 - risk * 0.25, 5, 95))
    target_weight = 0.0
    if action == "ROTATE_IN":
        target_weight = clamp(net / 4.0, 8, 25)
    elif action == "HOLD":
        target_weight = clamp(net / 5.0, 3, 10)

    return Signal(
        symbol=symbol,
        action=action,
        confidence=confidence,
        target_weight_pct=round(target_weight, 2),
        score=round(net, 2),
        risk_score=round(risk, 2),
        reasons=reasons[:6],
    )


def normalize_weights(signals: list[Signal], max_gross_pct: float = 80.0) -> list[Signal]:
    active = [s for s in signals if s.target_weight_pct > 0]
    gross = sum(s.target_weight_pct for s in active)
    if gross <= max_gross_pct:
        return signals
    scale = max_gross_pct / gross
    out = []
    for s in signals:
        if s.target_weight_pct > 0:
            out.append(Signal(**{**asdict(s), "target_weight_pct": round(s.target_weight_pct * scale, 2)}))
        else:
            out.append(s)
    return out


def analyze_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    regime = market_regime(snapshot)
    signals = [score_asset(asset, regime["label"]) for asset in snapshot.get("assets", [])]
    signals.sort(key=lambda s: (s.target_weight_pct, s.score, s.confidence), reverse=True)
    signals = normalize_weights(signals)

    invested = round(sum(s.target_weight_pct for s in signals), 2)
    stable = round(max(0.0, 100.0 - invested), 2)
    max_drawdown_stop = 12 if regime["label"] == "risk_on" else 8

    return {
        "strategy": "Regime Guard CMC Strategy",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_snapshot_at": snapshot.get("generated_at"),
        "regime": regime,
        "portfolio": {
            "target_gross_exposure_pct": invested,
            "stable_reserve_pct": stable,
            "max_single_position_pct": 25,
            "daily_loss_stop_pct": 4,
            "weekly_drawdown_stop_pct": max_drawdown_stop,
            "rebalance_frequency": "daily; intraday only when risk stop or regime flip triggers",
        },
        "signals": [asdict(s) for s in signals],
        "execution_policy": {
            "track": "Track 2 strategy specification; no live execution required",
            "eligible_universe": "BNB Hack eligible BEP-20 tokens available through CoinMarketCap data",
            "order_style": "spot rotation strategy specification; no orders are generated by this Track 2 repo",
            "slippage_cap_pct": 0.75,
            "min_liquidity_score": 50,
        },
    }
