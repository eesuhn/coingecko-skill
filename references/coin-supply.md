# CoinGecko API — Coin Supply Charts Reference

Covers historical circulating and total supply time-series by coin ID. Load this file
when the user asks about supply charts, circulating supply history, total supply history,
or token emission schedules. All four endpoints are **Enterprise only**.

For current circulating/total supply figures (not charts), see `references/coins.md` →
`GET /coins/{id}`. Coin IDs can be resolved via `GET /search` in `references/utils.md`
if the target is known, or `GET /coins/list` in `references/coins.md` for the full ID map.

---

## `GET /coins/{id}/circulating_supply_chart` — Circulating Supply Chart by ID

| Field | Value |
|---|---|
| Description | Query historical circulating supply of a coin up to N days ago |
| Path | `GET /coins/{id}/circulating_supply_chart` |
| Plan | **Enterprise only** |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `days` | string | Yes | Number of days ago — any integer or `max` |
| `interval` | string | No | Data granularity: `5m`, `hourly`, or `daily`. Leave empty for auto granularity |

### Notes
- Leave `interval` empty for automatic granularity based on the `days` value:
  - 1 day from now → 5-minutely
  - 2–90 days from now → hourly
  - 91 days and above from now → daily (00:00 UTC)
- Data available from 22 June 2019 onwards.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "circulating_supply": [
    [1712448000000, "19675268.0"],
    [1712534400000, "19675268.0"],
    [1712586776000, "19675268.0"]
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `circulating_supply` | Array of `[UNIX timestamp (ms), circulating supply]` pairs. Supply value is a string |

---

## `GET /coins/{id}/circulating_supply_chart/range` — Circulating Supply Chart within Time Range by ID

| Field | Value |
|---|---|
| Description | Query historical circulating supply of a coin within a specific date range |
| Path | `GET /coins/{id}/circulating_supply_chart/range` |
| Plan | **Enterprise only** |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `from` | string | Yes | Start date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `to` | string | Yes | End date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |

### Notes
- Use ISO date strings (`YYYY-MM-DD`) for best compatibility over UNIX timestamps.
- Auto granularity applies based on the date range:
  - 1 day from now → 5-minutely
  - 2–90 days from now → hourly
  - 91 days and above from now → daily (00:00 UTC)
- Data available from 22 June 2019 onwards.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "circulating_supply": [
    [1712448000000, "19675268.0"],
    [1712534400000, "19675268.0"],
    [1712586776000, "19675268.0"]
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `circulating_supply` | Array of `[UNIX timestamp (ms), circulating supply]` pairs. Supply value is a string |

---

## `GET /coins/{id}/total_supply_chart` — Total Supply Chart by ID

| Field | Value |
|---|---|
| Description | Query historical total supply of a coin up to N days ago |
| Path | `GET /coins/{id}/total_supply_chart` |
| Plan | **Enterprise only** |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `days` | string | Yes | Number of days ago — any integer or `max` |
| `interval` | string | No | Only `daily` is supported. Leave empty for auto granularity |

### Notes
- Leave `interval` empty for auto granularity:
  - 1 day from now → 5-minutely
  - 2–90 days from now → hourly
  - 91 days and above from now → daily (00:00 UTC)
- Data available from 22 June 2019 onwards.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "total_supply": [
    [1712448000000, "21000000.0"],
    [1712534400000, "21000000.0"],
    [1712586776000, "21000000.0"]
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `total_supply` | Array of `[UNIX timestamp (ms), total supply]` pairs. Supply value is a string |

---

## `GET /coins/{id}/total_supply_chart/range` — Total Supply Chart within Time Range by ID

| Field | Value |
|---|---|
| Description | Query historical total supply of a coin within a specific date range |
| Path | `GET /coins/{id}/total_supply_chart/range` |
| Plan | **Enterprise only** |

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes (path) | CoinGecko coin ID |
| `from` | string | Yes | Start date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |
| `to` | string | Yes | End date as ISO string (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, recommended) or UNIX timestamp |

### Notes
- Unlike the circulating supply range endpoint, there is no `interval` param — data is always returned at **daily intervals (00:00 UTC)**.
- Use ISO date strings (`YYYY-MM-DD`) for best compatibility over UNIX timestamps.
- Data available from 22 June 2019 onwards.
- The last completed UTC day is available 35 minutes after midnight (00:35 UTC).

### Example Response
```json
{
  "total_supply": [
    [1712448000000, "21000000.0"],
    [1712534400000, "21000000.0"],
    [1712586776000, "21000000.0"]
  ]
}
```

### Response Fields

| Field | Description |
|---|---|
| `total_supply` | Array of `[UNIX timestamp (ms), total supply]` pairs. Supply value is a string |