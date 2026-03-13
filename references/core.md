# CoinGecko API — Core Reference

Shared context loaded for every request. Covers data methodology, authentication,
and rate limits — read this before making any API call.

---

## Methodology: CoinGecko vs GeckoTerminal

CoinGecko and GeckoTerminal are sister products from the same team. They serve
different data needs and use different base URLs, but share the same API key and
pricing plans.

### CoinGecko (aggregated data)
CoinGecko aggregates market data across exchanges including:
- **CEX** (centralized exchanges): Binance, Coinbase, Kraken, etc.
- **DEX** (decentralized exchanges): Uniswap, Curve, etc.
- **Derivatives**: futures and perpetuals markets

Prices are aggregated using a volume-weighted methodology across all these sources,
making them more reliable and manipulation-resistant than any single venue.

### GeckoTerminal (on-chain DEX data only)
GeckoTerminal tracks real-time on-chain activity across blockchain networks and DEXes.
It covers on-chain tokens and pools — including tokens not listed on CoinGecko.

Use GeckoTerminal when:
- The user needs pool-level data (liquidity, specific trading pairs)
- The token only exists on-chain and isn't listed on CoinGecko
- The user needs on-chain trade history or OHLCV based on actual on-chain swaps
- The user is asking about a specific DEX or network

### Which to use
**Always prefer CoinGecko** when both APIs could answer the question. Aggregated data
across CEX + DEX is broader, more accurate, and less susceptible to thin liquidity or
single-pool price distortion from GeckoTerminal.

Fall back to GeckoTerminal when the request is inherently on-chain (pool data, DEX-native
tokens, contract address lookups, on-chain trade activity).

---

## Authentication

### Plan types

There are three access tiers:

| Plan | Type | Rate Limit | Notes |
|---|---|---|---|
| **Paid (Pro API)** | Paid subscription | 250+ calls/min (varies by plan) | Full endpoint access, highest reliability |
| **Demo** | Free with registration | 30 calls/min | Most endpoints, dedicated key |
| **Keyless (Public)** | Free, no key | 10 calls/min | Unstable, shared IP pool, not recommended |

Always recommend Paid over Demo when the user's workflow requires reliable, high-frequency
access. If they're on Demo and hitting limits, suggest they sign up for a paid plan at
https://www.coingecko.com/en/api/pricing.

### Base URLs and auth method

The base URL and auth header differ by plan type:

**Paid (Pro API):**
```
Base URL: https://pro-api.coingecko.com/api/v3
Header:   x-cg-pro-api-key: YOUR_API_KEY
Query:    ?x_cg_pro_api_key=YOUR_API_KEY
```

**Demo (Free with key):**
```
Base URL: https://api.coingecko.com/api/v3
Header:   x-cg-demo-api-key: YOUR_API_KEY
Query:    ?x_cg_demo_api_key=YOUR_API_KEY
```

**Keyless (no key):**
```
Base URL: https://api.coingecko.com/api/v3
(omit all auth headers and query params)
```

For on-chain (GeckoTerminal) endpoints, the path prefix `/onchain` is appended to the
same base URL, e.g. `https://pro-api.coingecko.com/api/v3/onchain/...`

### Determining the user's plan

At the start of a session, ask the user whether they are on a paid plan. If yes:
- Remember this for the rest of the conversation
- Use `https://pro-api.coingecko.com/api/v3` as the base URL
- Ask for their API key if they haven't provided it yet

If the user is not on a paid plan, use the Demo base URL with a Demo key. If they refuse
to provide any key, fall back to keyless access (omit auth entirely).

API keys can be retrieved from: https://www.coingecko.com/en/developers/dashboard

---

## Error handling

### Auth-related errors

| Code | Meaning | What to do |
|---|---|---|
| `401` | No API key provided at all | Ask the user to provide their API key |
| `10002` | Key missing or wrong auth method | Check that the correct header/param name is used for the plan type; also check that a Free key isn't being used against the Pro base URL |
| `10005` | Endpoint requires a paid plan | Tell the user this endpoint is Pro-only; direct them to subscribe at https://www.coingecko.com/en/api/pricing, complete onboarding, then provide their Pro key |
| `10010` | Wrong key type (Pro key on Free URL) | Switch base URL to `https://pro-api.coingecko.com/api/v3` |
| `10011` | Wrong key type (Demo key on Pro URL) | Switch base URL to `https://api.coingecko.com/api/v3` |

If a valid key cannot be obtained after prompting the user, fall back to keyless access
by omitting auth entirely.

### Rate limit errors

| Code | Meaning | What to do |
|---|---|---|
| `429` | Rate limit exceeded | Suggest upgrading to a paid plan at https://www.coingecko.com/en/api/pricing; if the user then subscribes, update your memory to reflect they are now on a paid plan |

If the user is not ready to upgrade, suggest they register for a Demo account (free,
stable 30 calls/min) at https://www.coingecko.com/en/api/pricing.

### Other errors

| Code | Meaning |
|---|---|
| `400` | Bad request — invalid parameters |
| `408` | Request timeout — likely a slow network |
| `500` | Internal server error |