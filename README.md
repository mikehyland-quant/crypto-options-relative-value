# crypto-options-relative-value

**Author:** Mike Hyland | [LinkedIn](https://www.linkedin.com/in/mikehyland) | Former Global Head of OTC Multi-Asset Derivatives Trading, BNY Mellon | SIG-trained market maker

---

## Overview

This repository contains research infrastructure and analytical tools for identifying relative value opportunities across the Bitcoin derivatives ecosystem — spanning ETFs, spot, futures, perpetuals, and options across multiple venues.

The work is grounded in institutional derivatives practice: forward curve construction, volatility surface modeling, cross-venue basis analysis, and systematic arb detection. The goal is a unified framework that ingests prices from every major BTC instrument and surfaces mispricings in real time.

---

## Architecture

### Market Data Infrastructure (`Class_FI/`)

A modular, asyncio-based market data system built for multi-venue real-time streaming:

- **`MktData`** — base class managing WebSocket feed registration, connection lifecycle, and shared state
- **`FinancialInstrument`** — abstract instrument layer with expiry/settlement logic (`FI_Dates` mixin)
- **`Spot` / `Equity`** — spot and ETF instrument handlers
- **`Future` / `FutureSpread`** — futures and calendar spread objects with forward pricing
- **`Option`** — options layer with Greeks, vol surface hooks, and expiry logic

Data sources: Deribit, Bitfinex, OKX, KuCoin, Gemini, CME (via IBKR/`ib_insync`)

### BTC Forward Curve Construction

Six methods for deriving the BTC forward price at each tenor:
1. CME futures prices
2. Crypto exchange futures curves (Deribit, OKX, Bybit)
3. ETF share/BTC ratios (IBIT, FBTC, BITB, ARKB, HODL)
4. ETF option synthetic forwards (put-call parity)
5. Spot + funding rate implied forwards
6. Synthetic forwards via options combos

The term structure is assembled using the tightest available market at each node, with flat-forward interpolation between nodes.

### BTC Futures Tightest-Market Optimizer

A dual-path Bellman-Ford optimizer that finds the best executable bid and ask for any BTC futures spread across all venues simultaneously:

- Spreads stored as upper-triangle matrix (far − near convention)
- Bids positive / asks negative for automatic directional arithmetic
- Independent bid/ask path optimization with visited-node cycle prevention
- Arb detection when `bestBid[j] > −bestAsk[j]` with decomposed execution legs and shared-leg netting

### Volatility Surface

- SABR and SVI vol surface fitting across Deribit options term structure
- Forward vol decomposition between tenors
- Cross-venue vol comparison (ETF options vs. spot BTC options vs. futures options)

---

## Daily Deribit Option Snapshots (`Daily_Deribit_Option_Snapshot/`)

End-of-day snapshots of the full Deribit BTC options surface, including strikes, expiries, bid/ask IVs, and mark prices. Used as the foundation for term structure research and historical vol analysis.

---

## Relative Value Opportunity Set

| Category | Description |
|---|---|
| ETF-to-spot basis | Pricing dislocations across IBIT, FBTC, BITB vs. spot BTC |
| Inter-ETF spreads | Fee-adjusted ETF cross ratios |
| Futures basis | CME vs. crypto exchange calendar spread mispricings |
| Forward curve arb | Inconsistencies across the six forward construction methods |
| Options arb | Put-call parity violations, cross-venue IV gaps |
| Forward vol spreads | Term structure shape mispricings |
| 0DTE opportunities | Near-expiry vol dislocations |

---

## Live Track Record

| Strategy | Sharpe Ratio | Max Drawdown |
|---|---|---|
| Fixed Income ETF Pairs (COVID era) | 3.4 | -1.8% |
| CME Crypto Calendar Spreads | 4.0 | -0.7% |

---

## Background

Built by a practitioner with 25+ years in institutional derivatives — SIG probabilistic pricing framework, Global Head of OTC Multi-Asset Derivatives at BNY Mellon, crypto options via LedgerX from 2021. This repo reflects the same analytical rigor applied to crypto markets that was previously applied to equity, fixed income, FX, and commodity derivatives at scale.

---

## Status

Active development. Research series published on LinkedIn — covering forward curve construction,
