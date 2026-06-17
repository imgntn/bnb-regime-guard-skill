# Final Submission Checklist

## Required For DoraHacks

- [x] Publish this folder to GitHub, GitLab, or Bitbucket.
- [x] Add the public repo URL to `submission/DORAHACKS_BUIDL.md`.
- [ ] Submit under Track 2: Strategy Skills.
- [ ] Optional: upload or link a short demo video.
- [ ] Use `submission/DORAHACKS_BUIDL.md` as the project description.
- [ ] Reference `submission/STRATEGY_SPEC.md` as the backtestable strategy spec.

## Suggested BUIDL Fields

Project name:

```text
Regime Guard CMC Strategy
```

Tagline:

```text
A CoinMarketCap Strategy Skill that turns market regime, technicals, derivatives, sentiment, and BNB Chain liquidity into backtestable portfolio signals.
```

Track:

```text
Track 2 - Strategy Skills
```

Demo instructions:

```text
Run the CLI commands in README.md or open docs/index.html. The repo includes sample CMC-style data, so the strategy and backtest are reproducible without API credentials.
```

What to emphasize:

- CoinMarketCap Agent Hub data is the center of the strategy.
- The Skill is reusable by any LLM agent.
- The output is deterministic and backtestable.
- The repo includes tests and sample reports.
- TWAK execution is documented as a future Track 1 extension, not claimed as complete.

## Local Verification

```powershell
$env:PYTHONPATH='src'
python -m regime_guard.cli analyze --input data/sample_market_snapshot.json --output docs/sample_signal.json
python -m regime_guard.cli backtest --input data/sample_backtest_series.json --output docs/backtest_report.json
python -m unittest discover -s tests
```

Expected result:

```text
Ran 5 tests
OK
```
