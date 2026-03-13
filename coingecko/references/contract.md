# CoinGecko API — Contract Address Reference

Covers endpoints that identify coins and fetch data by asset platform + token contract
address rather than CoinGecko coin ID. Load this file when the user has a contract
address (e.g. `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`) instead of a coin ID, or
when they ask for token price, coin data, or historical charts by contract address.

Asset platform IDs can be resolved via `references/asset-platforms.md` →
`GET /asset_platforms`. Supported currencies via `references/utils.md` →
`GET /simple/supported_vs_currencies`.

---

## `GET /simple/token_price/{id}` — Coin Price by Token Addresses

| Field | Value |
|---|---|
| Description | Query current price(s) for one or more tokens by contract address |
| Path | `GET /simple/token_price/{id}` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | Asset platform ID. Refer to `references/asset-platforms.md` → `GET /asset_platforms` |
| `contract_addresses` | string | Yes | One or more token contract addresses, comma-separated |
| `vs_currencies` | string | Yes | One or more target currencies, comma-separated. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `include_market_cap` | boolean | No | Include market cap. Default: `false` |
| `include_24hr_vol` | boolean | No | Include 24hr volume. Default: `false` |
| `include_24hr_change` | boolean | No | Include 24hr price change. Default: `false` |
| `include_last_updated_at` | boolean | No | Include last updated UNIX timestamp. Default: `false` |
| `precision` | string | No | Decimal places: `full` or `0`–`18` |

### Notes
- Returns the global average price aggregated across all active exchanges on CoinGecko.
- Cache / Update Frequency: every 20 seconds (Basic, Analyst, Lite, Pro, Enterprise).

### Example Response
```json
{
  "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": {
    "usd": 67187.34,
    "usd_market_cap": 1317802988326.25,
    "usd_24h_vol": 31260929299.52,
    "usd_24h_change": 3.64,
    "last_updated_at": 1711356300
  }
}
```

### Response Fields

| Field | Description |
|---|---|
| `{contract_address}` | Top-level key is the queried contract address |
| `{vs_currency}` | Price in the requested currency |
| `{vs_currency}_market_cap` | Market cap in the requested currency. Present when `include_market_cap=true` |
| `{vs_currency}_24h_vol` | 24hr volume in the requested currency. Present when `include_24hr_vol=true` |
| `{vs_currency}_24h_change` | 24hr price change in the requested currency. Present when `include_24hr_change=true` |
| `last_updated_at` | Last updated UNIX timestamp. Present when `include_last_updated_at=true` |

---

## `GET /coins/{id}/contract/{contract_address}` — Coin Data by Token Address

| Field | Value |
|---|---|
| Description | Query full coin metadata and market data using an asset platform and contract address |
| Path | `GET /coins/{id}/contract/{contract_address}` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | Asset platform ID. Refer to `references/asset-platforms.md` → `GET /asset_platforms` |
| `contract_address` | string | Yes (path) | Token contract address |

### Notes
- Returns the same data structure as `GET /coins/{id}` in `references/coins.md`. Refer there for the full response field reference.
- `twitter_followers` is no longer supported as of May 15, 2025.
- Coin descriptions may contain `\r\n` escape sequences.
- Cache / Update Frequency: every 60 seconds for all plans.

### Example Response
```json
{
  "id": "usd-coin",
  "symbol": "usdc",
  "name": "USDC",
  "asset_platform_id": "ethereum",
  "platforms": {
    "ethereum": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "solana": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
  },
  "detail_platforms": {
    "ethereum": {
      "decimal_place": 6,
      "contract_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    }
  }
}
```

### Response Fields

See `references/coins.md` → `GET /coins/{id}` for the complete field reference. Additional contract-specific fields:

| Field | Description |
|---|---|
| `asset_platform_id` | The asset platform this coin is primarily associated with |
| `platforms` | Map of platform ID → contract address for all chains this token is deployed on |
| `detail_platforms` | Map of platform ID → `{decimal_place, contract_address}` with token decimal precision |

---

## `GET /coins/{id}/contract/{contract_address}/market_chart` — Coin Historical Chart Data by Token Address

| Field | Value |
|---|---|
| Description | Query historical price, market cap, and 24hr volume time-series by contract address up to N days ago |
| Path | `GET /coins/{id}/contract/{contract_address}/market_chart` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | Asset platform ID. Refer to `references/asset-platforms.md` → `GET /asset_platforms` |
| `contract_address` | string | Yes (path) | Token contract address |
| `vs_currency` | string | Yes | Target currency. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `days` | string | Yes | Number of days ago — any integer or `max` |
| `interval` | string | No | Explicit granularity override — omit for auto (recommended). Options: `daily` (all plans), `5m` (**Enterprise only** — max 10 days back), `hourly` (**Enterprise only** — max 100 days back). Without this param, auto-granularity applies: 1 day → 5-minutely, 2–90 days → hourly, 90+ days → daily |
| `precision` | string | No | Decimal places: `full` or `0`–`18` |

### Notes
- Non-Enterprise subscribers wanting hourly data should leave `interval` empty and use `days` within 2–90.
- Cache / Update Frequency: every 5 minutes for all plans.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "prices": [
    [1711843200000, 69702.31],
    [1711929600000, 71246.95]
  ],
  "market_caps": [
    [1711843200000, 1370247487960.09],
    [1711929600000, 1401370211582.37]
  ],
  "total_volumes": [
    [1711843200000, 16408802301.84],
    [1711929600000, 19723005998.22]
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `prices` | Array of `[UNIX timestamp (ms), price]` pairs |
| `market_caps` | Array of `[UNIX timestamp (ms), market cap]` pairs |
| `total_volumes` | Array of `[UNIX timestamp (ms), 24hr volume]` pairs |

---

## `GET /coins/{id}/contract/{contract_address}/market_chart/range` — Coin Historical Chart Data within Time Range by Token Address

| Field | Value |
|---|---|
| Description | Query historical price, market cap, and 24hr volume within a specific date range by contract address |
| Path | `GET /coins/{id}/contract/{contract_address}/market_chart/range` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | Asset platform ID. Refer to `references/asset-platforms.md` → `GET /asset_platforms` |
| `contract_address` | string | Yes (path) | Token contract address |
| `vs_currency` | string | Yes | Target currency. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `from` | string | Yes | Start date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `to` | string | Yes | End date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `interval` | string | No | Explicit granularity override — omit for auto (recommended). Options: `daily` (all plans), `5m` (**Enterprise only** — max 10-day range), `hourly` (**Enterprise only** — max 100-day range). Without this param, auto-granularity applies: 1 day → 5-minutely, 2–90 days → hourly, 90+ days → daily |
| `precision` | string | No | Decimal places: `full` or `0`–`18` |

### Notes
- Use ISO date strings (`YYYY-MM-DD`) for best compatibility over UNIX timestamps.
- Non-Enterprise subscribers wanting hourly data should leave `interval` empty and use a range within 2–90 days.
- Cache varies by range: 1 day → 30s, 2–90 days → 30 min, above 90 days → 12 hours.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "prices": [
    [1704067241331, 42261.04],
    [1704070847420, 42493.28]
  ],
  "market_caps": [
    [1704067241331, 827596236151.20],
    [1704070847420, 831531023621.41]
  ],
  "total_volumes": [
    [1704067241331, 14305769170.95],
    [1704070847420, 14130205376.17]
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `prices` | Array of `[UNIX timestamp (ms), price]` pairs |
| `market_caps` | Array of `[UNIX timestamp (ms), market cap]` pairs |
| `total_volumes` | Array of `[UNIX timestamp (ms), 24hr volume]` pairs |