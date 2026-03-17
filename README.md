# Cross-Venue BTC Options Relative Value — A Practitioner's Framework

A systematic research framework for identifying and sizing mispricings across BTC 
options venues — ETF options, CME futures options, and Deribit — built on rigorous 
forward price construction and fee-adjusted volatility surface modeling.

**Author:** Mike Hyland | Former Global Head of OTC Derivatives, BNY Mellon | 
SIG-trained market maker  
**LinkedIn:** [linkedin.com/in/hylandmike](https://linkedin.com/in/hylandmike)

---

## The Core Problem

Most BTC options pricing frameworks skip a step that would be unacceptable in any 
traditional derivatives market: they never correctly compute the forward price.

Without the right forward, you cannot build a correct volatility surface. Without a 
correct surface, cross-venue comparisons are noise. This repo builds the framework 
from the ground up — forward construction first, then surface building, then 
cross-venue relative value.

---

## Section 1 — Computing the BTC Forward Price

BTC presents a forward pricing problem with no clean analog in traditional markets. 
There is no single authoritative spot price, no dividend, funding rates vary across 
venues, and the instruments referencing BTC span regulated and unregulated markets 
simultaneously. Six methods exist for observing the BTC forward, each with distinct 
characteristics.

### Method 1: CME Futures

The most institutionally credible anchor. CME BTC futures settle to the Bitcoin 
Reference Rate (BRR), a once-daily calculation based on a volume-weighted composite 
of constituent exchange prices during the 3–4pm London window. This means CME futures 
do not settle to any single spot price — they settle to a specific index at a specific 
time.

Key BTC-specific adjustments:
- **ETF NAV vs. market price:** When using ETF options alongside CME futures, ETF 
  share prices trade at small premiums or discounts to NAV intraday. The economically 
  correct reference is NAV, not market price.
- **Cash and carry basis:** The futures-spot basis in BTC is driven by funding demand, 
  not interest rate carry alone. It fluctuates with market sentiment and leverage demand.
- **Quanto adjustment for inverse perpetuals:** Crypto-native inverse perpetual 
  contracts are denominated in BTC but pay P&L in BTC. This introduces a quanto 
  effect — the payoff currency is the same as the underlying, creating a correlation 
  exposure between BTC price and the USD value of the P&L. Standard quanto adjustments 
  apply in principle; in practice the correlation is unstable.

**Contrast with Eurodollar futures:** Eurodollar futures required two adjustments that 
BTC futures do not. The *convexity adjustment* arose from the nonlinear relationship 
between bond prices and yields — as rates change, the delta of a futures position 
requires continuous rebalancing, and the cost of that rebalancing is not zero. The 
*futures-forward price difference* arose from daily mark-to-market creating a 
correlation between futures P&L and short-term interest rates. BTC futures require 
neither adjustment: BTC spot has no inherent convexity (the delta of a BTC futures 
contract with respect to BTC spot is fixed at one), and BTC's correlation with 
short-term interest rates is too unstable to apply a meaningful systematic correction.

### Method 2: Crypto Exchange Futures Curves

Offshore venues — Deribit, Bybit, OKX, Binance — publish their own futures curves. 
These provide real-time forward price observations but introduce venue-specific 
counterparty and basis risk. Differences between offshore futures curves and CME 
futures represent a combination of genuine arbitrage opportunity, structural access 
barriers, and regulatory risk premium.

### Method 3: ETF Share/BTC Ratios

BTC ETFs pay management fees by periodically reducing the Bitcoin backing per share. 
The shares-per-BTC ratio therefore increases over time at a deterministic rate driven 
by the fee structure.

This creates a compounding divergence between ETFs. Two ETFs that both track BTC 
deliver slightly different BTC exposure every day, and the divergence is permanent and 
predictable. The ETF with the lower fee is the better BTC replication vehicle on a 
forward basis; the ETF with the higher fee is a worse one — predictably, not randomly.

For IBIT (0.25% fee) and GBTC (1.50% fee), the annualized divergence in BTC exposure 
is approximately 1.25% per year, compounding continuously.

### Method 4: ETF Option Combos — Put-Call Parity

Long call / short put at the same strike and expiry implies the forward directly:
```
F = K + e^(rT) × (C − P)
```

This method is self-consistent within the ETF options market — fee drag and ETF 
mechanics are already embedded in the option prices. Differences between the 
put-call-parity-implied forward and the CME futures forward are themselves potential 
mispricing signals.

### Method 5: Spot Plus Funding Implied Forwards

Perpetual swap funding rates provide a continuous, real-time market signal for the 
BTC forward. If the funding rate is r_f per period, the implied forward can be 
bootstrapped from spot:
```
F(T) = S × ∏ (1 + r_f,i)
```

This method is granular and real-time but noisy. Funding rates spike around market 
dislocations, liquidation cascades, and sentiment shifts. The implied forward from 
funding is most useful as a real-time signal rather than a structural anchor.

### Method 6: Synthetic Forwards

A synthetic forward is constructed directly from options via put-call parity. Unlike 
Method 4, which derives the forward from market prices, a synthetic forward can be 
used to *create* forward exposure where listed futures are unavailable or illiquid.

### Triangulation

No single method is unambiguously correct. The analytical framework treats all six 
as simultaneous estimates of the same underlying quantity and looks for convergence 
and divergence:

- Where multiple methods agree: the forward is well-anchored and the market is 
  functioning efficiently at that point on the curve.
- Where methods disagree: the divergence is either a genuine relative value 
  opportunity or reflects a structural barrier to convergence (regulatory, collateral, 
  counterparty) that must be understood before trading.

---

## Section 2 — ETF Mechanics and Fee Drag

Management fees in BTC ETFs are not paid in cash — they are paid by reducing BTC 
holdings per share. The shares-per-BTC ratio (or equivalently, BTC per share) drifts 
continuously and deterministically.

For an ETF with annual fee rate *f*, the BTC per share at time T is:
```
BTC_per_share(T) = BTC_per_share(0) × e^(−fT)
```

In forward pricing terms, the management fee behaves exactly like a negative 
dividend yield. The correct forward price formula is:
```
F = S × e^((r − f)T)
```

**Impact by ETF (3-month forward, r = 5.3%):**

| ETF  | Fee  | Forward Adjustment | Basis Point Error if Ignored |
|------|------|--------------------|------------------------------|
| IBIT | 0.25%| −0.25% × T         | ~5 bps                       |
| FBTC | 0.25%| −0.25% × T         | ~5 bps                       |
| GBTC | 1.50%| −1.50% × T         | ~38 bps                       |

Getting the forward wrong by 38 basis points before the volatility surface is even 
built means any implied vol derived from GBTC options is systematically incorrect 
before any other error is introduced.

---

## Section 3 — BTC-Equivalent Strike Conversion

ETF options are struck on ETF share price, not on BTC price. Before building a 
volatility surface or comparing across venues, ETF option strikes must be converted 
to BTC-equivalent strikes using the projected shares-per-BTC ratio at each expiry.

For an option expiring at time T, the BTC-equivalent strike is:
```
K_BTC = K_ETF / BTC_per_share(T)
```

Where BTC_per_share(T) uses the fee-adjusted projection from Section 2.

This conversion is deterministic — no estimation is required, only the known fee rate 
and current BTC-per-share ratio. It is also the step most BTC options pricing 
frameworks skip entirely, which means their cross-venue strike comparisons are 
economically wrong by construction.

---

## Section 4 — Volatility Surface Construction

With fee-adjusted forwards and BTC-equivalent strikes in hand, the vol surface is 
built in the standard way:

1. **Anchor on liquid instruments** — near-the-money options at front expiries. 
   These are the most reliably priced points on the surface.
2. **Project shares-per-BTC forward** for each expiry using known fee rates.
3. **Convert all ETF strikes to BTC-equivalent strikes** using the projection.
4. **Fit a parametric model** across the resulting (strike, expiry, implied vol) 
   surface. Candidate frameworks include SABR, SVI, and proprietary forward-vol 
   decomposition approaches developed in institutional market-making contexts.
5. **Identify thick vs. thin areas** — where the surface is well-anchored by liquid 
   options vs. where it requires interpolation or extrapolation.

The result is a BTC volatility surface that is directly comparable across ETF 
options, CME futures options, and Deribit — because all three have been expressed 
in the same units against the same correctly computed forward.

---

## Section 5 — Cross-Venue Comparison

With a common surface, systematic comparison becomes tractable. The three major 
venues for BTC options are:

**BTC ETF Options (IBIT, FBTC, GBTC, etc.)**
- Regulated, US exchange-listed
- Settled in USD, physically vs. cash depending on ETF type
- Subject to ETF mechanics and fee drag
- Accessible to all US institutional and retail participants

**CME Futures Options**
- Regulated, US exchange-listed
- Options on CME BTC futures contracts
- Margined through CME clearing
- Preferred venue for institutional hedgers

**Deribit**
- Offshore, unregulated from US perspective
- Options on BTC spot and perpetuals
- Historically the deepest liquidity in BTC options
- BTC-margined (creates quanto effects)
- Accessible to non-US institutions and offshore accounts

Systematic differences between venues arise from: differences in settlement 
mechanics, collateral requirements, regulatory access, and liquidity. The goal 
is to distinguish *structural* differences (which are permanent and must be modeled) 
from *temporary dislocations* (which may be tradeable).

---

## Section 6 — Identifying and Sizing Mispricings

Cross-venue relative value trades require that the mispricing exceed the cost of 
carry, bid-offer, margin, and execution friction before they are worth pursuing. 
The framework identifies five categories of structural inefficiency:

1. **ETF fee drag mispricings** — Options priced as if all ETFs have identical 
   forward prices. Correcting for fee drag reveals mispricing in relative vol levels 
   across ETFs.
2. **ETF-CME basis** — Differences between put-call-parity-implied forwards from 
   ETF options and the CME futures price. Should be close to zero for liquid strikes; 
   persistent divergences indicate either a structural barrier or a genuine 
   opportunity.
3. **Cross-venue vol surface differences** — The same BTC-equivalent strike at the 
   same expiry should imply the same volatility across venues, modulo structural 
   adjustments. Systematic differences in skew, term structure, or ATM vol levels 
   across venues are the primary target of this research.
4. **Funding rate dislocations** — Periods where spot-plus-funding-implied forwards 
   diverge sharply from CME or ETF-derived forwards. Often short-lived but can be 
   large.
5. **Forward vol structure** — Implied forward volatilities derived from the term 
   structure may be inconsistent across venues. Calendar spread mispricings are 
   the direct expression of this.

---

## Research Status

| Component | Status |
|-----------|--------|
| ETF fee drag and forward pricing | ✅ Complete |
| BTC-equivalent strike conversion | ✅ Complete |
| CME futures forward methodology | 🔄 In progress |
| ETF option surface construction | 🔄 In progress |
| Cross-venue vol surface comparison | 📋 Planned |
| Mispricing identification and sizing | 📋 Planned |

---

## Related Research

**[systematic-trading-strategies](https://github.com/mikehyland-quant/systematic-trading-strategies)**  
Systematic crypto strategies with documented track records. COVID ETF strategy 
(Sharpe 3.4), CME crypto calendar spreads (Sharpe 4.0). Demonstrates the 
quantitative infrastructure underlying this relative value research.

---

## Background

This framework draws on experience as Global Head of OTC Derivatives at BNY Mellon 
and market-making training at Susquehanna International Group (SIG). The volatility 
surface methodology reflects institutional practice in options market-making — 
building from forward construction through surface parameterization to relative 
value identification — applied to the structural inefficiencies specific to the 
fragmented BTC options market.

---

*For questions or collaboration inquiries: 
[linkedin.com/in/hylandmike](https://linkedin.com/in/hylandmike)*
