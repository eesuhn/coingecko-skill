# CoinGecko API — Coin Historical Data Reference

Covers historical price, market cap, volume, and OHLC data by coin ID. Load this file
when the user is asking about historical charts, time-series prices, OHLC candlesticks,
or data over a specific date range. For current market data, see `references/coins.md`.
For supply charts, see `references/coin-supply.md`.

Coin IDs can be resolved via `GET /search` in `references/utils.md` if the target is
known, or `GET /coins/list` in `references/coins.md` for the full ID map.

---

## `GET /coins/{id}/history` — Coin Historical Data by ID

| Field | Value |
|---|---|
| Description | Query historical price, market cap, and 24hr volume for a coin at a specific date |
| Path | `GET /coins/{id}/history` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `date` | string | Yes | Date snapshot in `DD-MM-YYYY` format |
| `localization` | boolean | No | Include localized coin names. Default: `true` |

### Notes
- Data is returned at `00:00:00 UTC` for the given date.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "id": "bitcoin",
  "symbol": "btc",
  "name": "Bitcoin",
  "image": {
    "thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png",
    "small": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png"
  },
  "market_data": {
    "current_price": { "usd": 42074.71 },
    "market_cap": { "usd": 822933961870.54 },
    "total_volume": { "usd": 24832397519.05 }
  }
}
```

### Response Fields

| Field | Description |
|---|---|
| `id` | Coin ID |
| `symbol` | Coin symbol |
| `name` | Coin name |
| `localization` | Coin name in all languages. Present when `localization=true` |
| `image.thumb` | Thumbnail image URL |
| `image.small` | Small image URL |
| `market_data.current_price` | Price in all supported currencies at the given date |
| `market_data.market_cap` | Market cap in all supported currencies |
| `market_data.total_volume` | 24hr volume in all supported currencies |
| `community_data` | Community stats (Facebook likes, Reddit metrics) |
| `developer_data` | GitHub repo stats (forks, stars, commits, issues) |
| `public_interest_stats` | Alexa rank and Bing matches |

---

## `GET /coins/{id}/market_chart` — Coin Historical Chart Data by ID

| Field | Value |
|---|---|
| Description | Query historical price, market cap, and 24hr volume time-series up to N days ago |
| Path | `GET /coins/{id}/market_chart` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `vs_currency` | string | Yes | Target currency. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `days` | string | Yes | Number of days ago (`1`, `7`, `14`, `30`, `90`, `180`, `365`, or `max`) |
| `interval` | string | No | Explicit granularity override — omit for auto (recommended). Options: `daily` (all plans), `5m` (**Enterprise only** — max 10 days back), `hourly` (**Enterprise only** — max 100 days back). Without this param, auto-granularity applies: 1 day → 5-minutely, 2–90 days → hourly, 90+ days → daily |
| `precision` | string | No | Decimal places: `full` or `0`–`18` |

### Notes
- Leave `interval` empty for automatic granularity based on the `days` value:
  - 1 day from now → 5-minutely
  - 2–90 days from now → hourly
  - Above 90 days from now → daily (00:00 UTC)
- `interval=5m` and `interval=hourly` (explicit) are **Enterprise only** and bypass auto-granularity.
- Non-Enterprise subscribers wanting hourly data should leave `interval` empty and use a range of 2–90 days.

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

## `GET /coins/{id}/market_chart/range` — Coin Historical Chart Data within Time Range by ID

| Field | Value |
|---|---|
| Description | Query historical price, market cap, and 24hr volume within a specific date range |
| Path | `GET /coins/{id}/market_chart/range` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `vs_currency` | string | Yes | Target currency. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `from` | string | Yes | Start date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `to` | string | Yes | End date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `interval` | string | No | Explicit granularity override — omit for auto (recommended). Options: `daily` (all plans), `5m` (**Enterprise only** — max 10-day range), `hourly` (**Enterprise only** — max 100-day range). Without this param, auto-granularity applies: 1 day → 5-minutely, 2–90 days → hourly, 90+ days → daily |
| `precision` | string | No | Decimal places: `full` or `0`–`18` |

### Notes
- Use ISO date strings (`YYYY-MM-DD`) for best compatibility over UNIX timestamps.
- Leave `interval` empty for automatic granularity based on the date range:
  - 1 day → 5-minutely
  - 1 day (not current) or 2–90 days → hourly
  - Above 90 days → daily (00:00 UTC)
- `interval=5m` and `interval=hourly` (explicit) are **Enterprise only**.
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

---

## `GET /coins/{id}/ohlc` — Coin OHLC Chart by ID

| Field | Value |
|---|---|
| Description | Query OHLC candlestick data for a coin up to N days ago |
| Path | `GET /coins/{id}/ohlc` |
| Plan | Free + Paid |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `vs_currency` | string | Yes | Target currency. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `days` | string | Yes | Number of days ago: `1`, `7`, `14`, `30`, `90`, `180`, `365`, or `max` |
| `interval` | string | No | Candle interval: `daily` (paid — valid for `1/7/14/30/90/180` days only) or `hourly` (paid — valid for `1/7/14/30/90` days only). Leave empty for auto granularity (free + paid) |
| `precision` | string | No | Decimal places: `full` or `0`–`18` |

### Notes
- `interval=daily` and `interval=hourly` are available to **all paid plan subscribers** (Analyst, Lite, Pro, Enterprise).
- Leaving `interval` empty uses auto granularity available to all plans:
  - 1–2 days → 30-minute candles
  - 3–30 days → 4-hour candles
  - 31 days and above → 4-day candles
- Timestamp in the response indicates the **close** time of each candle.

### Example Response
```json
[
  [1709395200000, 61942, 62211, 61721, 61845],
  [1709409600000, 61828, 62139, 61726, 62139],
  [1709424000000, 62171, 62210, 61821, 62068]
]
```

### Response Fields

| Field | Description |
|---|---|
| `[0]` | UNIX timestamp in milliseconds (close time of the candle) |
| `[1]` | Open price |
| `[2]` | High price |
| `[3]` | Low price |
| `[4]` | Close price |

---

## `GET /coins/{id}/ohlc/range` — Coin OHLC Chart within Time Range by ID

| Field | Value |
|---|---|
| Description | Query OHLC candlestick data for a coin within a specific date range |
| Path | `GET /coins/{id}/ohlc/range` |
| Plan | **Paid only** (Analyst, Lite, Pro, Enterprise) |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `vs_currency` | string | Yes | Target currency. Refer to `references/utils.md` → `GET /simple/supported_vs_currencies` |
| `from` | string | Yes | Start date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `to` | string | Yes | End date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `interval` | string | Yes | Candle interval: `daily` (max 180 days / 180 candles per request) or `hourly` (max 31 days / 744 candles per request) |

### Notes
- Use ISO date strings (`YYYY-MM-DD`) for best compatibility over UNIX timestamps.
- Timestamp in the response indicates the **close** time of each candle.
- Data available from 9 February 2018 onwards.

### Example Response
```json
[
  [1709395200000, 61942, 62211, 61721, 61845],
  [1709409600000, 61828, 62139, 61726, 62139],
  [1709424000000, 62171, 62210, 61821, 62068]
]
```

### Response Fields

| Field | Description |
|---|---|
| `[0]` | UNIX timestamp in milliseconds (close time of the candle) |
| `[1]` | Open price |
| `[2]` | High price |
| `[3]` | Low price |
| `[4]` | Close price |