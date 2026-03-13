---
name: coingecko
description: >
  Use this skill for any request involving cryptocurrency market data, coin prices,
  trading volume, market cap, OHLC charts, historical data, exchanges, derivatives,
  NFTs, DeFi, on-chain token data, liquidity pools, DEX data, or anything powered
  by CoinGecko or GeckoTerminal APIs. Trigger this skill whenever the user asks
  about crypto prices, token data, market trends, or wants to call any CoinGecko
  or GeckoTerminal endpoint — even if they don't explicitly say "CoinGecko". Also
  trigger when the user asks about API keys, rate limits, or authentication for
  these APIs.
---

# CoinGecko Skill

You have access to the CoinGecko API (aggregated data) and the GeckoTerminal API
(on-chain DEX data). Together they cover virtually all crypto market data needs.

## Before anything else

Always read `references/core.md` first. It contains the methodology for choosing between
CoinGecko and GeckoTerminal, authentication setup, and rate limit guidance — all of which
affect how every request should be made.

## Reference index

Load the relevant reference file based on what the user is asking for. You only need to
load the file(s) that match the current request.

### CoinGecko (aggregated)

| File | When to load |
|---|---|
| `references/core.md` | **Always** — auth, methodology, rate limits |
| `references/coins.md` | Coin prices, market data, metadata, tickers, gainers/losers |
| `references/coin-history.md` | Historical charts, OHLC, time-range queries by coin ID |
| `references/coin-supply.md` | Circulating/total supply charts |
| `references/contract.md` | Coin data or charts looked up by token contract address |
| `references/asset-platforms.md` | Blockchain platform IDs, token lists |
| `references/categories.md` | Coin categories and sector market data |
| `references/exchanges.md` | Spot and DEX exchange data, tickers, volume charts, volume chart by date range |
| `references/derivatives.md` | Derivatives exchanges and tickers |
| `references/treasury.md` | Public company/institution crypto treasury holdings |
| `references/nfts.md` | NFT collection data, market data, charts, tickers (per-marketplace floor prices), contract address lookups |
| `references/global.md` | Global market stats and DeFi data |
| `references/utils.md` | API status, API key usage, supported currencies, search, trending coins/NFTs/categories, exchange rates |

### GeckoTerminal (on-chain)

| File | When to load |
|---|---|
| `references/onchain-networks.md` | Supported networks and DEXes (ID resolution) |
| `references/onchain-pools.md` | Pool discovery, trending/new pools, megafilter |
| `references/onchain-tokens.md` | Token data, holders, traders, price by contract address |
| `references/onchain-ohlcv-trades.md` | OHLCV candles and trade history for pools/tokens |
| `references/onchain-categories.md` | On-chain pool categories (GeckoTerminal-specific) |

## General guidance

- Prefer CoinGecko endpoints over GeckoTerminal when both could answer the question —
  aggregated data across CEX + DEX is more reliable than DEX-only on-chain data.
- Use GeckoTerminal when the user is asking about a specific pool, DEX-native token,
  or on-chain activity that CoinGecko doesn't cover.
- If a request spans multiple domains (e.g. coin price + exchange data), load multiple
  reference files.
- When uncertain which file to load, check the index above before answering.